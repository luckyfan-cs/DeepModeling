#!/usr/bin/env python3
"""
批量转换 ScienceAgent-bench 任务到 MLE-Bench 格式

使用方法:
    python convert_scienceagent_to_mlebench.py --instance-ids 1 2 3
    python convert_scienceagent_to_mlebench.py --all
    python convert_scienceagent_to_mlebench.py --list
"""

import argparse
import json
import re
import subprocess
import textwrap
from string import Template
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd


# 路径配置
SCIENCEAGENT_DIR = Path('/home/aiops/liufan/projects/ScienceAgent-bench/benchmark')
SCIENCEBENCH_REGISTRY_DIR = Path('/home/aiops/liufan/projects/DeepModeling/benchmarks/sciencebench/competitions')
SCIENCEBENCH_DATA_DIR = Path('/home/aiops/liufan/projects/ScienceAgent-bench/competitions')
GOLD_RESULTS_DIR = SCIENCEAGENT_DIR / 'eval_programs' / 'gold_results'

IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.tif', '.tiff'}
METADATA_CSV = SCIENCEAGENT_DIR / 'ScienceAgentBench.csv'


def load_scienceagent_metadata() -> pd.DataFrame:
    """加载 ScienceAgent-bench 的元数据"""
    df = pd.read_csv(METADATA_CSV)
    print(f"📊 Loaded {len(df)} tasks from ScienceAgentBench.csv")
    return df


def clean_task_instruction(task_inst: str) -> str:
    """清理任务说明，移除路径以及具体模型要求"""
    if pd.isna(task_inst) or not str(task_inst).strip():
        return "Generate the requested output based on the provided scientific data."

    text = str(task_inst)

    # 标准化空白和换行
    text = re.sub(r"\s+", " ", text.strip())

    # 替换 pred_results 相关的路径引用
    text = re.sub(r'"[^"\n]*pred_results[^"\n]*"', '"output file"', text, flags=re.IGNORECASE)
    text = re.sub(r'`[^`\n]*pred_results[^`\n]*`', '`output file`', text, flags=re.IGNORECASE)

    sentences = re.split(r'(?<=[.!?])\s+', text)
    cleaned_sentences: List[str] = []
    for sentence in sentences:
        lowered = sentence.lower()

        # 移除保存路径相关内容
        if any(keyword in lowered for keyword in ['pred_results', ' save ', 'saving to', 'stored in', '/tmp/', './']):
            continue

        # 移除强制使用特定模型或库的句子
        if 'use ' in lowered and (' model' in lowered or '`' in sentence):
            continue

        cleaned_sentences.append(sentence.strip())

    if not cleaned_sentences:
        return "Generate the requested output based on the provided scientific data."

    cleaned = ' '.join(cleaned_sentences)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def is_image_output(output_fname: Optional[str]) -> bool:
    if not output_fname or pd.isna(output_fname):
        return False
    return Path(str(output_fname)).suffix.lower() in IMAGE_EXTENSIONS


def generate_candidate_tokens(task_data: Dict[str, Any]) -> List[str]:
    tokens: List[str] = []

    output_fname = task_data.get('output_fname')
    if isinstance(output_fname, str) and output_fname:
        stem = Path(output_fname).stem.lower()
        tokens.append(stem)
        tokens.append(stem.replace('pred_', '').replace('_pred', '').replace('-pred', ''))

    for key in ['gold_program_name', 'eval_script_name']:
        value = task_data.get(key)
        if isinstance(value, str) and value:
            stem = Path(value).stem.lower()
            tokens.append(stem)
            tokens.append(stem.replace('_eval', ''))

    dataset_tree = task_data.get('dataset_folder_tree')
    if isinstance(dataset_tree, str):
        match = re.search(r'\|--\s*([^/\n]+)', dataset_tree)
        if match:
            tokens.append(match.group(1).strip().lower())

    return [token for token in {t for t in tokens if t}]


def find_gold_result_path(task_data: Dict[str, Any]) -> Optional[Path]:
    """根据任务信息猜测 gold_results 文件路径"""
    if not GOLD_RESULTS_DIR.exists():
        return None

    candidates = generate_candidate_tokens(task_data)
    if not candidates:
        return None

    best_match: Optional[Path] = None
    best_score = 0
    expected_suffix = None

    output_fname = task_data.get('output_fname')
    if isinstance(output_fname, str) and output_fname:
        expected_suffix = Path(output_fname).suffix.lower()

    for gold_file in GOLD_RESULTS_DIR.iterdir():
        if not gold_file.is_file():
            continue

        stem = gold_file.stem.lower()
        score = 0

        for token in candidates:
            if token in stem or stem in token:
                score = max(score, len(token))

        if expected_suffix and gold_file.suffix.lower() == expected_suffix:
            score += 5

        if score > best_score:
            best_match = gold_file
            best_score = score

    return best_match


def create_competition_id(instance_id: int, gold_program_name: str) -> str:
    """生成比赛 ID"""
    # 从 gold_program_name 提取基本名称
    if pd.isna(gold_program_name):
        name_part = f"task-{instance_id}"
    else:
        # 移除 .py 后缀
        name_part = gold_program_name.replace('.py', '')
        # 转换为小写，用连字符分隔
        name_part = re.sub(r'[_\s]+', '-', name_part.lower())
        # 移除特殊字符
        name_part = re.sub(r'[^a-z0-9-]', '', name_part)

    return f"sciencebench-{instance_id:03d}-{name_part}"


def extract_dataset_name(dataset_folder_tree: str) -> str:
    """从数据集文件夹树中提取数据集名称"""
    if pd.isna(dataset_folder_tree):
        return "unknown"

    # 提取第一个顶层目录名
    # 例如 "|-- clintox/\n|---- ..." -> "clintox"
    match = re.search(r'\|--\s*([^/\n]+)', dataset_folder_tree)
    if match:
        return match.group(1).strip()
    return "unknown"


def infer_metric_from_task(task_inst: str, output_fname: str, subtask_categories: str) -> str:
    """根据任务类型推断评估指标"""
    task_lower = (task_inst or "").lower()
    output_lower = (output_fname or "").lower()
    subtask_lower = (subtask_categories or "").lower()

    # 可视化任务
    if any(keyword in task_lower for keyword in ['visualize', 'plot', 'figure', 'chart']):
        return 'visual_similarity'
    if any(keyword in output_lower for keyword in ['.png', '.jpg', '.jpeg', '.pdf']):
        return 'visual_similarity'

    # 深度学习/机器学习任务
    if 'deep learning' in subtask_lower or 'machine learning' in subtask_lower:
        if 'classification' in task_lower or 'predict' in task_lower:
            return 'accuracy'
        elif 'regression' in task_lower:
            return 'rmse'

    # 回归任务
    if any(keyword in task_lower for keyword in ['regression', 'predict.*values']):
        return 'rmse'

    # 分类任务
    if any(keyword in task_lower for keyword in ['classification', 'classify', 'toxicity']):
        return 'accuracy'

    # 特征选择/工程
    if 'feature' in subtask_lower:
        return 'exact_match'

    # 默认使用 RMSE（适用于大多数数值预测）
    return 'rmse'


def create_image_prepare_py(task_data: Dict, dataset_name: str, gold_path: Optional[Path]) -> str:
    """生成图像任务的 prepare.py"""
    output_fname = task_data.get('output_fname', 'output.png') or 'output.png'
    expected_filename = Path(output_fname).name
    gold_literal = gold_path.as_posix() if gold_path else ''

    template = '''"""
Data preparation for ScienceBench task {instance_id}
Dataset: {dataset_name}
"""

import base64
from pathlib import Path
import shutil
import pandas as pd


EXPECTED_FILENAME = "{expected_filename}"
GOLD_IMAGE_PATH = Path("{gold_literal}") if "{gold_literal}" else None
SOURCE_DATASET = "{dataset_name}"


def prepare(raw: Path, public: Path, private: Path):
    """Prepare data for image-based ScienceBench task."""
    print("=" * 60)
    print("Preparing ScienceBench Task {instance_id}")
    print("Dataset:", SOURCE_DATASET)
    print("=" * 60)
    print("Raw directory:", raw)
    print("Public directory:", public)
    print("Private directory:", private)

    if not raw.exists():
        print("\\n⚠ Warning: Raw data directory not found:", raw)
        public.mkdir(parents=True, exist_ok=True)
        private.mkdir(parents=True, exist_ok=True)
        placeholder = pd.DataFrame([
            {{"file_name": EXPECTED_FILENAME, "image_base64": ""}}
        ])
        placeholder.to_csv(public / "sample_submission.csv", index=False)
        placeholder.to_csv(private / "answer.csv", index=False)
        return

    file_count = 0
    for file in raw.rglob('*'):
        if file.is_file() and not file.name.startswith('.'):
            rel_path = file.relative_to(raw)
            target = public / rel_path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file, target)
            file_count += 1
            if file_count <= 10:
                print("  ✓ Copied:", rel_path)

    if file_count > 10:
        print("  ... and", file_count - 10, "more files")
    print("  Total files copied:", file_count)

    public.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)

    gold_base64 = ""
    if GOLD_IMAGE_PATH and GOLD_IMAGE_PATH.exists():
        gold_bytes = GOLD_IMAGE_PATH.read_bytes()
        (private / EXPECTED_FILENAME).write_bytes(gold_bytes)
        gold_base64 = base64.b64encode(gold_bytes).decode("utf-8")
        print("✓ Embedded gold image from", GOLD_IMAGE_PATH)
    else:
        print("⚠ Gold image not found; creating empty placeholder.")

    sample_df = pd.DataFrame([
        {{"file_name": EXPECTED_FILENAME, "image_base64": ""}}
    ])
    sample_df.to_csv(public / "sample_submission.csv", index=False)
    print("✓ Created sample_submission.csv")

    answer_df = pd.DataFrame([
        {{"file_name": EXPECTED_FILENAME, "image_base64": gold_base64}}
    ])
    answer_df.to_csv(private / "answer.csv", index=False)
    print("✓ Created answer.csv with encoded gold image")

    print("\\nData preparation completed!")
'''

    return template.format(
        instance_id=task_data['instance_id'],
        dataset_name=dataset_name,
        expected_filename=expected_filename,
        gold_literal=gold_literal,
    )


def create_image_grade_py(task_data: Dict) -> str:
    """生成图像任务的 grade.py"""
    expected_filename = Path(task_data.get('output_fname', 'output.png') or 'output.png').name

    template = '''"""
Grading function for ScienceBench task {instance_id}

Image similarity is approximated via pixel-level comparison after decoding
base64 encoded submissions.
"""

import base64
import io
import numpy as np
import pandas as pd
from PIL import Image


EXPECTED_FILENAME = "{expected_filename}"


def _decode_image(data: str) -> Image.Image:
    if not isinstance(data, str) or not data.strip():
        raise ValueError("Empty image_base64 value")
    buffer = io.BytesIO(base64.b64decode(data))
    return Image.open(buffer).convert("RGB")


def _similarity_score(gold_img: Image.Image, pred_img: Image.Image) -> float:
    pred_resized = pred_img.resize(gold_img.size)
    gold_arr = np.asarray(gold_img, dtype=np.float32) / 255.0
    pred_arr = np.asarray(pred_resized, dtype=np.float32) / 255.0

    mse = float(np.mean((gold_arr - pred_arr) ** 2))
    return max(0.0, 1.0 - mse)


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    required_columns = {{"file_name", "image_base64"}}
    if not required_columns.issubset(submission.columns):
        raise ValueError(f"Submission must contain columns: {{required_columns}}")

    if not required_columns.issubset(answers.columns):
        raise ValueError(f"Answers must contain columns: {{required_columns}}")

    merged = pd.merge(
        answers.rename(columns={{"image_base64": "image_base64_gold"}}),
        submission.rename(columns={{"image_base64": "image_base64_pred"}}),
        on="file_name",
        how="inner",
    )

    if merged.empty:
        return 0.0

    scores = []
    for _, row in merged.iterrows():
        try:
            gold_img = _decode_image(row["image_base64_gold"])
            pred_img = _decode_image(row["image_base64_pred"])
        except ValueError:
            scores.append(0.0)
            continue

        scores.append(_similarity_score(gold_img, pred_img))

    return float(np.mean(scores)) if scores else 0.0
'''

    return template.format(
        instance_id=task_data['instance_id'],
        expected_filename=expected_filename,
    )


def create_config_yaml(comp_id: str, task_name: str, metric: str) -> str:
    """生成 config.yaml 内容"""
    return f"""id: {comp_id}
name: "ScienceBench - {task_name}"
competition_type: code
awards_medals: false
prizes: null
description: benchmarks/sciencebench/competitions/{comp_id}/description.md

dataset:
  answers: {comp_id}/prepared/private/answer.csv
  sample_submission: {comp_id}/prepared/public/sample_submission.csv

grader:
  name: {metric}
  grade_fn: benchmarks.sciencebench.competitions.{comp_id}.grade:grade

preparer: benchmarks.sciencebench.competitions.{comp_id}.prepare:prepare
"""


def create_description_md(task_data: Dict, task_type: str, metric: str) -> str:
    """生成 description.md 内容"""
    instance_id = task_data['instance_id']
    domain = task_data.get('domain', 'Unknown')
    subtask = task_data.get('subtask_categories', 'Unknown')
    github = task_data.get('github_name', '')
    task_inst = clean_task_instruction(task_data.get('task_inst', ''))
    dataset_preview = task_data.get('dataset_preview', '')
    expected_output = Path(task_data.get('output_fname', 'output')).name

    overview_lines = [
        f"- Domain: {domain}",
        f"- Subtask Categories: {subtask}",
        f"- Source: {github if github else 'N/A'}",
        f"- Expected Output: {expected_output}",
        f"- Output Type: {task_type.replace('_', ' ').title()}",
    ]

    dataset_section = dataset_preview if dataset_preview and not pd.isna(dataset_preview) else 'N/A'

    if task_type == 'image':
        submission_text = (
            "Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. "
            "Encode your final image as base64 (UTF-8 string) and associate it with the expected file name."
        )
        evaluation_text = (
            "The grader decodes your base64 image, rescales it to the reference size, "
            "and computes a similarity score between 0 and 1."
        )
    else:
        submission_text = (
            "Submit `sample_submission.csv` with the same header and column order as the template. "
            "Ensure numeric columns retain their dtype and identifiers remain aligned."
        )

        metric_descriptions = {
            'roc_auc': 'Receiver Operating Characteristic AUC (higher is better).',
            'accuracy': 'Classification accuracy (higher is better).',
            'rmse': 'Negative root mean squared error (closer to zero is better).',
            'mae': 'Negative mean absolute error (closer to zero is better).',
            'exact_match': 'Element-wise equality between your submission and the reference.',
            'visual_similarity': 'Similarity score computed between generated visual artifacts.',
        }
        evaluation_text = metric_descriptions.get(metric, 'Comparison with the reference answer file.')

    description = f"""# ScienceBench Task {instance_id}

## Overview

{chr(10).join(overview_lines)}

## Task

{task_inst}

## Dataset

{dataset_section}

## Submission Format

{submission_text}

## Evaluation

{evaluation_text}
"""

    return description





def create_prepare_py(task_data: Dict, dataset_name: str, gold_path: Optional[Path]) -> str:
    """生成 prepare.py 内容，使用真实 gold 结果"""
    dataset_literal = dataset_name or 'unknown'
    gold_literal = gold_path.as_posix() if gold_path else ''
    task_id = task_data['instance_id']

    template = Template(
        """
"""
Data preparation for ScienceBench task $TASK_ID
Dataset: $DATASET
"""

import json
import shutil
from pathlib import Path

import numpy as np
import pandas as pd


SOURCE_DATASET = "$DATASET"
GOLD_PATH = Path("$GOLD_PATH") if "$GOLD_PATH" else None
ANSWER_FILENAME = "answer.csv"
SAMPLE_FILENAME = "sample_submission.csv"


def load_gold_dataframe(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()

    if suffix == ".csv":
        return pd.read_csv(path)

    if suffix in {".json", ".jsonl"}:
        if suffix == ".jsonl":
            records = []
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        records.append(json.loads(line))
        else:
            with open(path, "r", encoding="utf-8") as f:
                payload = json.load(f)
            if isinstance(payload, list):
                records = payload
            elif isinstance(payload, dict):
                records = [payload]
            else:
                records = [{"value": payload}]

        return pd.json_normalize(records)

    if suffix in {".pkl", ".pickle"}:
        obj = pd.read_pickle(path)
        if isinstance(obj, pd.DataFrame):
            return obj.reset_index(drop=True)
        if isinstance(obj, dict):
            return pd.json_normalize(obj)
        if isinstance(obj, list):
            return pd.json_normalize(obj)
        return pd.DataFrame({"value": [obj]})

    if suffix in {".npy", ".npz"}:
        arr = np.load(path, allow_pickle=True)
        if isinstance(arr, np.ndarray):
            if arr.dtype.names is not None:
                return pd.DataFrame(arr.tolist())
            if arr.ndim == 1:
                return pd.DataFrame({"value": arr.tolist()})
            reshaped = arr.reshape(arr.shape[0], -1) if arr.ndim > 2 else arr
            return pd.DataFrame(reshaped)
        if isinstance(arr, dict):
            return pd.DataFrame(arr)
        return pd.DataFrame({"value": [arr]})

    if suffix in {".txt", ".tsv"}:
        if suffix == ".tsv":
            return pd.read_csv(path, sep="	")
        text = path.read_text(encoding="utf-8").splitlines()
        return pd.DataFrame({"value": text})

    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)

    raise ValueError(f"Unsupported gold result format: {suffix}")


def create_sample_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    sample = df.copy()
    for column in sample.columns:
        if pd.api.types.is_numeric_dtype(sample[column]):
            sample[column] = 0
        else:
            sample[column] = ""
    return sample.fillna("")


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def create_placeholder_files(public: Path, private: Path) -> None:
    ensure_directory(public)
    ensure_directory(private)

    pd.DataFrame({"info": ["Data not available"]}).to_csv(
        public / SAMPLE_FILENAME, index=False
    )

    pd.DataFrame({"info": ["Answer not available"]}).to_csv(
        private / ANSWER_FILENAME, index=False
    )

    print("Placeholder files created")


def prepare(raw: Path, public: Path, private: Path):
    """Prepare the ScienceAgent task data."""
    print("=" * 60)
    print("Preparing ScienceBench Task $TASK_ID")
    print("Dataset:", SOURCE_DATASET)
    print("=" * 60)
    print("Raw directory:", raw)
    print("Public directory:", public)
    print("Private directory:", private)

    ensure_directory(public)
    ensure_directory(private)

    if raw.exists():
        print("\nCopying data files to public directory...")
        file_count = 0
        for file in raw.rglob('*'):
            if file.is_file() and not file.name.startswith('.'):
                rel_path = file.relative_to(raw)
                target = public / rel_path
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file, target)
                file_count += 1
                if file_count <= 10:
                    print("  ✓ Copied:", rel_path)
        if file_count > 10:
            print("  ... and", file_count - 10, "more files")
        print("  Total files copied:", file_count)
    else:
        print("\n⚠ Warning: Raw data directory not found:", raw)

    if GOLD_PATH and GOLD_PATH.exists():
        try:
            gold_df = load_gold_dataframe(GOLD_PATH)
            sample_df = create_sample_dataframe(gold_df)

            answer_path = private / ANSWER_FILENAME
            sample_path = public / SAMPLE_FILENAME

            gold_df.to_csv(answer_path, index=False)
            sample_df.to_csv(sample_path, index=False)

            print("✓ Created answer file:", answer_path)
            print("✓ Created sample submission:", sample_path)

            gold_copy = private / GOLD_PATH.name
            if GOLD_PATH != gold_copy:
                shutil.copy2(GOLD_PATH, gold_copy)
                print("✓ Copied original gold file:", gold_copy)

        except Exception as exc:
            print("⚠ Failed to process gold results:", exc)
            print("   Falling back to placeholder files")
            create_placeholder_files(public, private)
    else:
        print("⚠ Gold results not found; creating placeholder files")
        create_placeholder_files(public, private)

    print("\nData preparation completed!")
    public_list = [p.name for p in public.iterdir() if p.is_file()]
    private_list = [p.name for p in private.iterdir() if p.is_file()]
    print("  Public files:", public_list)
    print("  Private files:", private_list)
"""
    )

    script = template.substitute(
        TASK_ID=task_id,
        DATASET=dataset_literal,
        GOLD_PATH=gold_literal,
    )

    return textwrap.dedent(script)
def create_grade_py(task_data: Dict, metric: str) -> str:
    """生成 grade.py 内容"""
    output_fname = task_data.get('output_fname', 'output.csv')
    is_image = output_fname.endswith(('.png', '.jpg', '.jpeg', '.pdf'))

    code = f'''"""
Grading function for ScienceBench task {task_data['instance_id']}
"""

import pandas as pd
import numpy as np
from pathlib import Path
'''

    if metric == 'accuracy':
        code += '''from sklearn.metrics import accuracy_score


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    """
    Grade submission using accuracy metric.

    Args:
        submission: DataFrame with predictions
        answers: DataFrame with ground truth

    Returns:
        Accuracy score (0-1)
    """
    # 对齐数据
    if 'id' in submission.columns and 'id' in answers.columns:
        merged = pd.merge(answers, submission, on='id', suffixes=('_true', '_pred'))

        # 找到预测列
        pred_col = [c for c in merged.columns if c.endswith('_pred')][0]
        true_col = pred_col.replace('_pred', '_true')

        return accuracy_score(merged[true_col], merged[pred_col])
    else:
        # 简单比较
        return float(np.mean(submission.values == answers.values))
'''

    elif metric == 'rmse':
        code += '''from sklearn.metrics import mean_squared_error


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    """
    Grade submission using RMSE metric (lower is better).

    Args:
        submission: DataFrame with predictions
        answers: DataFrame with ground truth

    Returns:
        Negative RMSE (higher is better for consistency)
    """
    # 对齐数据
    if 'id' in submission.columns and 'id' in answers.columns:
        merged = pd.merge(answers, submission, on='id', suffixes=('_true', '_pred'))

        # 找到预测列
        pred_col = [c for c in merged.columns if c.endswith('_pred')][0]
        true_col = pred_col.replace('_pred', '_true')

        rmse = mean_squared_error(merged[true_col], merged[pred_col], squared=False)
        return -rmse  # 负数，因为更高的分数更好
    else:
        # 简单 RMSE
        rmse = np.sqrt(np.mean((submission.values - answers.values) ** 2))
        return -rmse
'''

    elif metric == 'visual_similarity':
        code += '''from PIL import Image
import imagehash


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    """
    Grade submission by comparing images.

    Args:
        submission: DataFrame or path info about submitted image
        answers: DataFrame or path info about reference image

    Returns:
        Similarity score (0-1)
    """
    # This is a placeholder implementation
    # Actual image comparison would require the image files

    # 如果提交的是文件路径或元数据，比较它们
    try:
        # 尝试计算图像哈希距离
        # 实际实现需要访问图像文件
        return 0.5  # Placeholder
    except Exception as e:
        print(f"Error in visual comparison: {e}")
        return 0.0
'''

    else:  # exact_match
        code += '''

def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    """
    Grade submission using exact match.

    Args:
        submission: DataFrame with predictions
        answers: DataFrame with ground truth

    Returns:
        Match ratio (0-1)
    """
    # 逐元素比较
    if submission.shape != answers.shape:
        print(f"Shape mismatch: submission {submission.shape} vs answers {answers.shape}")
        return 0.0

    # 计算匹配比例
    matches = (submission.values == answers.values).sum()
    total = submission.size

    return matches / total if total > 0 else 0.0
'''

    return code


def create_leaderboard_csv() -> str:
    """生成 leaderboard.csv 内容"""
    return """submission_id,score,username,date
random_baseline,0.0,random,2024-01-01
"""


def create_checksums_yaml() -> str:
    """生成 checksums.yaml 内容"""
    return """# Checksums for data integrity verification
# Will be populated after data preparation

public: {}
private: {}
"""


def convert_task(instance_id: int, task_data: Dict, dry_run: bool = False) -> bool:
    """
    转换单个任务

    Args:
        instance_id: 任务 ID
        task_data: 任务数据字典
        dry_run: 是否只预览不实际创建

    Returns:
        是否成功
    """
    try:
        # 生成 competition ID
        comp_id = create_competition_id(instance_id, task_data.get('gold_program_name'))

        print(f"\n{'='*60}")
        print(f"Converting Task {instance_id} -> {comp_id}")
        print(f"{'='*60}")
        print(f"Domain: {task_data.get('domain', 'Unknown')}")
        print(f"Subtask: {task_data.get('subtask_categories', 'Unknown')}")

        if dry_run:
            print("🔍 DRY RUN - No files will be created")
            return True

        # 创建注册目录（registry - 存放 config, description, grade, prepare 文件）
        comp_dir = SCIENCEBENCH_REGISTRY_DIR / comp_id
        comp_dir.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created registry directory: {comp_dir}")

        # 创建数据目录（data-dir - 存放 prepared/public 和 prepared/private）
        data_dir = SCIENCEBENCH_DATA_DIR / comp_id
        data_dir.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created data directory: {data_dir}")

        # 提取数据集名称
        dataset_name = extract_dataset_name(task_data.get('dataset_folder_tree'))

        output_fname = task_data.get('output_fname', '')
        task_type = 'image' if is_image_output(output_fname) else 'tabular'
        gold_path = find_gold_result_path(task_data)

        if gold_path:
            print(f"✓ Located gold reference: {gold_path.name}")
        else:
            print("⚠ Gold reference not found in gold_results directory")

        # 推断评估指标
        metric = infer_metric_from_task(
            task_data.get('task_inst'),
            output_fname,
            task_data.get('subtask_categories')
        )

        if task_type == 'image':
            metric = 'image_similarity'

        print(f"✓ Inferred metric: {metric}")

        description_content = create_description_md(task_data, task_type, metric)

        if task_type == 'image':
            prepare_code = create_image_prepare_py(task_data, dataset_name, gold_path)
            grade_code = create_image_grade_py(task_data)
        else:
            prepare_code = create_prepare_py(task_data, dataset_name, gold_path)
            grade_code = create_grade_py(task_data, metric)

        # 生成所有文件
        files_to_create = {
            'config.yaml': create_config_yaml(
                comp_id,
                task_data.get('gold_program_name', f'Task {instance_id}'),
                metric
            ),
            'description.md': description_content,
            'prepare.py': prepare_code,
            'grade.py': grade_code,
            'leaderboard.csv': create_leaderboard_csv(),
            'checksums.yaml': create_checksums_yaml()
        }

        for filename, content in files_to_create.items():
            file_path = comp_dir / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Created {filename}")

        print(f"✅ Task {instance_id} converted successfully!")
        return True

    except Exception as e:
        print(f"❌ Error converting task {instance_id}: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_auto_prepare(comp_id: str, dataset_name: str, timeout: int = 120) -> bool:
    """
    自动运行 prepare.py

    Args:
        comp_id: Competition ID
        dataset_name: Dataset name (for raw data path)
        timeout: 超时时间（秒）

    Returns:
        是否成功
    """
    comp_dir = SCIENCEBENCH_REGISTRY_DIR / comp_id
    prepare_script = comp_dir / "prepare.py"

    if not prepare_script.exists():
        print(f"⚠ Prepare script not found: {prepare_script}")
        return False

    print(f"\n📦 Auto-preparing data for {comp_id}...")

    try:
        # 路径配置
        raw_dir = SCIENCEAGENT_DIR / 'datasets' / dataset_name
        data_dir = SCIENCEBENCH_DATA_DIR / comp_id / 'prepared'
        public_dir = data_dir / 'public'
        private_dir = data_dir / 'private'

        print(f"  Raw: {raw_dir}")
        print(f"  Public: {public_dir}")
        print(f"  Private: {private_dir}")

        # 创建数据目录
        public_dir.mkdir(parents=True, exist_ok=True)
        private_dir.mkdir(parents=True, exist_ok=True)

        # 运行 prepare 函数
        import sys
        sys.path.insert(0, str(comp_dir))

        try:
            from prepare import prepare
            prepare(raw_dir, public_dir, private_dir)
            print(f"✅ Data prepared successfully!")
            return True
        except Exception as e:
            print(f"❌ Prepare failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            # 清理导入
            if str(comp_dir) in sys.path:
                sys.path.remove(str(comp_dir))
            # 移除已导入的 prepare 模块
            if 'prepare' in sys.modules:
                del sys.modules['prepare']

    except Exception as e:
        print(f"❌ Error running prepare: {e}")
        import traceback
        traceback.print_exc()
        return False


def list_tasks(df: pd.DataFrame, category: Optional[str] = None):
    """列出所有任务"""
    if category:
        df = df[df['domain'].str.contains(category, case=False, na=False)]

    print(f"\n{'='*80}")
    print(f"ScienceAgent-bench Tasks ({len(df)} total)")
    print(f"{'='*80}\n")

    # 按领域分组
    for domain in df['domain'].unique():
        domain_tasks = df[df['domain'] == domain]
        print(f"\n## {domain} ({len(domain_tasks)} tasks)")
        print("-" * 80)

        for _, task in domain_tasks.head(10).iterrows():  # 每个领域最多显示10个
            comp_id = create_competition_id(task['instance_id'], task['gold_program_name'])
            print(f"  [{task['instance_id']:3d}] {comp_id}")
            print(f"       {task.get('subtask_categories', 'N/A')}")

        if len(domain_tasks) > 10:
            print(f"       ... and {len(domain_tasks) - 10} more tasks")

    print(f"\n{'='*80}\n")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Convert ScienceAgent-bench tasks to MLE-Bench format'
    )
    parser.add_argument(
        '--instance-ids',
        type=int,
        nargs='+',
        help='Specific instance IDs to convert'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Convert all tasks'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all available tasks'
    )
    parser.add_argument(
        '--category',
        type=str,
        help='Filter by domain category'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview conversion without creating files'
    )
    parser.add_argument(
        '--auto-prepare',
        action='store_true',
        help='Automatically run prepare.py after conversion'
    )
    parser.add_argument(
        '--limit',
        type=int,
        help='Limit number of tasks to convert (for testing)'
    )

    args = parser.parse_args()

    # 加载元数据
    df = load_scienceagent_metadata()

    # 列出任务
    if args.list:
        list_tasks(df, args.category)
        return

    # 确定要转换的任务
    if args.instance_ids:
        tasks_to_convert = df[df['instance_id'].isin(args.instance_ids)]
    elif args.all:
        tasks_to_convert = df
        if args.category:
            tasks_to_convert = tasks_to_convert[
                tasks_to_convert['domain'].str.contains(args.category, case=False, na=False)
            ]
    else:
        print("❌ Error: Please specify --instance-ids, --all, or --list")
        parser.print_help()
        return

    # 限制数量（用于测试）
    if args.limit:
        tasks_to_convert = tasks_to_convert.head(args.limit)

    print(f"\n🚀 Converting {len(tasks_to_convert)} task(s)...")
    if args.auto_prepare:
        print("⚡ Auto-prepare mode enabled\n")
    if args.dry_run:
        print("🔍 DRY RUN mode - no files will be created\n")

    # 创建目标目录
    if not args.dry_run:
        SCIENCEBENCH_REGISTRY_DIR.mkdir(parents=True, exist_ok=True)
        SCIENCEBENCH_DATA_DIR.mkdir(parents=True, exist_ok=True)
        print(f"📁 Registry directory: {SCIENCEBENCH_REGISTRY_DIR}")
        print(f"📁 Data directory: {SCIENCEBENCH_DATA_DIR}\n")

    # 转换任务
    success_count = 0
    failed_tasks = []

    for _, task_data in tasks_to_convert.iterrows():
        task_dict = task_data.to_dict()
        instance_id = task_dict['instance_id']

        success = convert_task(instance_id, task_dict, args.dry_run)

        if success:
            success_count += 1

            # Auto-prepare
            if args.auto_prepare and not args.dry_run:
                comp_id = create_competition_id(instance_id, task_dict.get('gold_program_name'))
                dataset_name = extract_dataset_name(task_dict.get('dataset_folder_tree'))
                run_auto_prepare(comp_id, dataset_name)
        else:
            failed_tasks.append(instance_id)

    # 总结
    print(f"\n{'='*60}")
    print(f"Conversion Summary")
    print(f"{'='*60}")
    print(f"✅ Success: {success_count}/{len(tasks_to_convert)}")
    if failed_tasks:
        print(f"❌ Failed: {len(failed_tasks)} tasks")
        print(f"   Task IDs: {failed_tasks}")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()

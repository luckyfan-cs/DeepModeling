#!/usr/bin/env python3
"""
改进版：批量转换 ScienceAgent-bench 任务到 MLE-Bench 格式

关键改进：
1. 正确使用 eval_programs 和 gold_results
2. 根据 eval 脚本生成正确的评估逻辑
3. 从 gold_results 获取真实答案
"""

import pandas as pd
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional


# 路径配置
SCIENCEAGENT_DIR = Path('/home/aiops/liufan/projects/ScienceAgent-bench/benchmark')
SCIENCEBENCH_COMPETITIONS_DIR = Path('/home/aiops/liufan/projects/DeepModeling/benchmarks/sciencebench/competitions')
METADATA_CSV = SCIENCEAGENT_DIR / 'ScienceAgentBench.csv'


def load_scienceagent_metadata() -> pd.DataFrame:
    """加载 ScienceAgent-bench 的元数据"""
    df = pd.read_csv(METADATA_CSV)
    print(f"📊 Loaded {len(df)} tasks from ScienceAgentBench.csv")
    return df


def infer_gold_results_path(eval_script_name: str, output_fname: str) -> Optional[Path]:
    """
    推断 gold_results 文件路径

    例如:
    - eval_script_name: clintox_nn_eval.py
    - 可能的 gold: clintox_gold.csv
    """
    if pd.isna(eval_script_name):
        return None

    # 移除 _eval.py 后缀
    base_name = eval_script_name.replace('_eval.py', '').replace('.py', '')

    # 可能的 gold 文件名
    possible_names = [
        f"{base_name}_gold.csv",
        f"{base_name}_gold.json",
        f"{base_name}_gold.png",
        f"{base_name}.csv",
    ]

    gold_results_dir = SCIENCEAGENT_DIR / 'eval_programs' / 'gold_results'

    for name in possible_names:
        gold_path = gold_results_dir / name
        if gold_path.exists():
            return gold_path

    return None


def analyze_eval_script(eval_script_name: str) -> Dict[str, Any]:
    """
    分析 eval 脚本，提取评估逻辑

    返回:
    {
        'metric': 'roc_auc' | 'rmse' | 'visual_similarity' | 'exact_match',
        'threshold': float or None,
        'columns': list of column names
    }
    """
    if pd.isna(eval_script_name):
        return {'metric': 'exact_match', 'threshold': None, 'columns': []}

    eval_path = SCIENCEAGENT_DIR / 'eval_programs' / eval_script_name

    if not eval_path.exists():
        return {'metric': 'exact_match', 'threshold': None, 'columns': []}

    try:
        with open(eval_path, 'r') as f:
            content = f.read()

        # 检测指标类型
        if 'roc_auc_score' in content:
            metric = 'roc_auc'
        elif 'mean_squared_error' in content or 'rmse' in content.lower():
            metric = 'rmse'
        elif 'ssim' in content.lower() or 'image' in content.lower():
            metric = 'visual_similarity'
        else:
            metric = 'exact_match'

        # 提取阈值
        threshold_match = re.search(r'threshold\s*=\s*([\d.]+)', content)
        threshold = float(threshold_match.group(1)) if threshold_match else None

        # 提取列名
        columns = []
        col_matches = re.findall(r'\[[\'\"]([^\'\"]+)[\'\"]\]', content)
        columns = list(set(col_matches))

        return {'metric': metric, 'threshold': threshold, 'columns': columns}

    except Exception as e:
        print(f"⚠ Warning: Could not analyze {eval_script_name}: {e}")
        return {'metric': 'exact_match', 'threshold': None, 'columns': []}


def create_prepare_py_v2(task_data: Dict, dataset_name: str, gold_path: Optional[Path]) -> str:
    """
    生成改进版 prepare.py

    关键改进：使用 gold_results 作为答案
    """
    output_fname = task_data.get('output_fname', '')
    is_csv = output_fname.endswith('.csv')
    is_image = output_fname.endswith(('.png', '.jpg', '.jpeg'))

    code = f'''"""
Data preparation for ScienceBench task {task_data['instance_id']}

改进版：使用 gold_results 作为答案
"""

import pandas as pd
import numpy as np
from pathlib import Path
import shutil
import json


def prepare(raw: Path, public: Path, private: Path):
    """
    Prepare the ScienceAgent task data.

    改进：从 gold_results 获取真实答案

    Args:
        raw: Path to ScienceAgent-bench/benchmark/datasets/{dataset_name}
        public: Path to public directory (visible to participants)
        private: Path to private directory (used for grading)
    """
    print(f"Preparing ScienceBench task {task_data['instance_id']}...")

    # Gold results 路径
    gold_path = Path("{gold_path if gold_path else 'N/A'}")
'''

    if gold_path and is_csv:
        # CSV 格式：有 gold_results
        code += f'''

    if not gold_path.exists():
        print(f"⚠ Warning: Gold results not found: {{gold_path}}")
        print("Creating placeholder files...")
        create_placeholder_files(public, private, raw)
        return

    # 1. 读取 gold results（测试集答案）
    gold = pd.read_csv(gold_path)
    print(f"Loaded gold results: {{gold_path}}")
    print(f"Gold shape: {{gold.shape}}")
    print(f"Gold columns: {{gold.columns.tolist()}}")

    # 2. 复制训练数据（如果存在）
    train_files = list(raw.glob('*train*.csv'))
    if train_files:
        train = pd.read_csv(train_files[0])
        train.to_csv(public / train_files[0].name, index=False)
        print(f"Copied training data: {{train_files[0].name}}")

    # 3. 创建测试集（仅特征，移除标签列）
    # 通常第一列是 ID 或特征，其他列是标签
    if len(gold.columns) > 1:
        feature_cols = [gold.columns[0]]  # 通常是 ID 或主要特征
        test_public = gold[feature_cols].copy()
    else:
        test_public = gold.copy()

    test_public.to_csv(public / "test_features.csv", index=False)
    print(f"Created test features ({{len(feature_cols)}} columns)")

    # 4. 保存完整的 gold 到 private
    gold.to_csv(private / gold_path.name, index=False)
    print(f"Saved gold results to private/{{gold_path.name}}")

    # 5. 创建 sample_submission（与 gold 格式相同，但填充零）
    sample = gold.copy()
    for col in sample.columns:
        if col not in feature_cols:
            # 标签列填充默认值
            if sample[col].dtype in ['int64', 'float64']:
                sample[col] = 0
            else:
                sample[col] = ''

    sample.to_csv(public / "sample_submission.csv", index=False)
    print(f"Created sample_submission.csv")
'''

    elif is_image:
        # 图像任务
        code += f'''

    # 图像任务：gold 是参考图像
    gold_path_obj = Path("{gold_path if gold_path else 'N/A'}")

    if gold_path_obj.exists():
        # 复制参考图像到 private
        shutil.copy2(gold_path_obj, private / gold_path_obj.name)
        print(f"Copied reference image to private/{{gold_path_obj.name}}")

    # 复制数据文件到 public
    for file in raw.rglob('*'):
        if file.is_file() and not file.name.startswith('.'):
            rel_path = file.relative_to(raw)
            target = public / rel_path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file, target)
            print(f"  Copied: {{rel_path}}")

    # 创建提交说明
    with open(public / "README.txt", "w") as f:
        f.write(f"Task: Generate image {{gold_path_obj.name}}\\n")
        f.write(f"Expected output: {{gold_path_obj.name}}\\n")
'''

    else:
        # 其他格式
        code += f'''

    # 复制所有数据到 public
    for file in raw.rglob('*'):
        if file.is_file() and not file.name.startswith('.'):
            rel_path = file.relative_to(raw)
            target = public / rel_path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file, target)
            print(f"  Copied: {{rel_path}}")

    # 创建默认的提交文件
    with open(public / "sample_submission.txt", "w") as f:
        f.write("Your submission should match the format specified in the task description.\\n")
'''

    code += '''

    print(f"\\nData preparation completed!")
    print(f"  Public files: {list(public.glob('*'))}")
    print(f"  Private files: {list(private.glob('*'))}")


def create_placeholder_files(public: Path, private: Path, raw: Path):
    """创建占位符文件（当 gold 不存在时）"""
    # 尝试复制原始数据
    for file in raw.rglob('*.csv'):
        if file.is_file():
            shutil.copy2(file, public / file.name)

    # 创建默认文件
    pd.DataFrame({"info": ["Data not available"]}).to_csv(
        public / "sample_submission.csv", index=False
    )
    pd.DataFrame({"info": ["Answer not available"]}).to_csv(
        private / "answer.csv", index=False
    )
'''

    return code


def create_grade_py_v2(task_data: Dict, eval_info: Dict) -> str:
    """
    生成改进版 grade.py

    根据 eval_info 生成相应的评分逻辑
    """
    metric = eval_info['metric']
    threshold = eval_info['threshold']

    code = f'''"""
Grading function for ScienceBench task {task_data['instance_id']}

Metric: {metric}
Threshold: {threshold if threshold else 'N/A'}
"""

import pandas as pd
import numpy as np
from pathlib import Path
'''

    if metric == 'roc_auc':
        code += '''from sklearn.metrics import roc_auc_score


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    """
    Grade using ROC-AUC score (multi-label)

    Similar to ScienceAgent-bench eval logic
    """
    try:
        # 检查是否有相同的 ID 列（如 smiles）
        id_col = submission.columns[0]  # 通常第一列是 ID

        # 检查 ID 匹配
        if id_col in answers.columns:
            if not (list(submission[id_col]) == list(answers[id_col])):
                print("⚠ Warning: ID columns do not match")
                return 0.0

        # 获取标签列（除了第一列）
        label_cols = [col for col in answers.columns if col != id_col]

        if not label_cols:
            print("⚠ Warning: No label columns found")
            return 0.0

        # 计算 ROC-AUC
        metric = roc_auc_score(
            answers[label_cols],
            submission[label_cols]
        )

        print(f"ROC-AUC Score: {metric:.4f}")
'''

        if threshold:
            code += f'''
        # 应用阈值
        threshold = {threshold}
        if metric >= threshold:
            return metric
        else:
            print(f"Score {{metric:.4f}} below threshold {{threshold}}")
            return 0.0
'''
        else:
            code += '''
        return metric
'''

    elif metric == 'rmse':
        code += '''from sklearn.metrics import mean_squared_error


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    """
    Grade using RMSE (lower is better, return negative for consistency)
    """
    try:
        # 对齐数据
        id_col = submission.columns[0]
        label_cols = [col for col in answers.columns if col != id_col]

        # 计算 RMSE
        rmse = np.sqrt(mean_squared_error(
            answers[label_cols],
            submission[label_cols]
        ))

        print(f"RMSE: {rmse:.4f}")

        # 返回负值（更高的分数更好）
        return -rmse
'''

    elif metric == 'visual_similarity':
        code += '''from PIL import Image
import imagehash


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    """
    Grade by comparing images

    Note: This is a placeholder. Actual implementation
    would need access to the image files.
    """
    # 图像评分需要访问实际的图像文件
    # 这里返回占位符分数
    print("⚠ Warning: Image grading not fully implemented")
    return 0.5
'''

    else:  # exact_match
        code += '''

def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    """
    Grade using exact match
    """
    # 检查形状
    if submission.shape != answers.shape:
        print(f"Shape mismatch: {submission.shape} vs {answers.shape}")
        return 0.0

    # 计算匹配比例
    matches = (submission.values == answers.values).sum()
    total = submission.size

    return matches / total if total > 0 else 0.0
'''

    code += '''

    except Exception as e:
        print(f"Error in grading: {e}")
        import traceback
        traceback.print_exc()
        return 0.0
'''

    return code


# ... (其他函数保持不变，但使用新的 create_prepare_py_v2 和 create_grade_py_v2)

# 此处省略其他辅助函数，它们与 v1 版本相同
# 只需要在 convert_task 函数中调用新的生成函数

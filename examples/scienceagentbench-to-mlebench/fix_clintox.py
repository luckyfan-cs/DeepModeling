#!/usr/bin/env python3
"""
修正 sciencebench-001-clintox-nn 任务

正确使用 gold_results 和 eval_programs 的逻辑
"""

from pathlib import Path


# 修正后的 prepare.py
PREPARE_PY_FIXED = '''"""
Data preparation for ScienceBench task 1 (Clintox)

正确版本：使用 gold_results 作为答案
"""

import pandas as pd
from pathlib import Path


def prepare(raw: Path, public: Path, private: Path):
    """
    Prepare the Clintox dataset.

    改进：
    1. 从 gold_results 获取测试集答案
    2. 测试集只提供 smiles（移除标签）
    3. 答案保存到 private/

    Args:
        raw: Path to datasets/clintox/
        public: Path to public directory
        private: Path to private directory
    """
    print("Preparing Clintox dataset (FIXED VERSION)...")

    # 1. 读取训练数据（完整的）
    train = pd.read_csv(raw / "clintox_train.csv")
    print(f"Loaded training data: {train.shape}")
    print(f"Training columns: {train.columns.tolist()}")

    # 2. 读取 gold results（测试集真实答案）
    gold_path = Path("/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/eval_programs/gold_results/clintox_gold.csv")

    if not gold_path.exists():
        raise FileNotFoundError(f"Gold results not found: {gold_path}")

    gold = pd.read_csv(gold_path)
    print(f"Loaded gold results: {gold.shape}")
    print(f"Gold columns: {gold.columns.tolist()}")

    # 3. 保存训练数据到 public（完整的）
    train.to_csv(public / "clintox_train.csv", index=False)
    print(f"✓ Saved training data to public/")

    # 4. 创建测试集（仅 smiles，无标签）
    test_public = gold[['smiles']].copy()
    test_public.to_csv(public / "clintox_test.csv", index=False)
    print(f"✓ Saved test data (features only) to public/")

    # 5. 保存 gold 到 private（完整的答案）
    gold.to_csv(private / "clintox_gold.csv", index=False)
    print(f"✓ Saved gold results to private/")

    # 6. 创建 sample_submission（与 gold 格式相同，但标签填零）
    sample = gold.copy()
    sample['FDA_APPROVED'] = 0
    sample['CT_TOX'] = 0
    sample.to_csv(public / "sample_submission.csv", index=False)
    print(f"✓ Created sample_submission.csv")

    print(f"\\nData preparation completed!")
    print(f"  Public files: {list(public.glob('*'))}")
    print(f"  Private files: {list(private.glob('*'))}")
'''


# 修正后的 grade.py
GRADE_PY_FIXED = '''"""
Grading function for ScienceBench task 1 (Clintox)

正确版本：使用 ROC-AUC 评分，与 clintox_nn_eval.py 一致
"""

import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    """
    Grade using ROC-AUC score for multi-label classification.

    与 ScienceAgent-bench 的 clintox_nn_eval.py 逻辑一致:
    1. 检查 smiles 列是否匹配 (data_correctness)
    2. 计算 ROC-AUC 分数 (func_correctness)
    3. 阈值 0.77

    Args:
        submission: DataFrame with columns [smiles, FDA_APPROVED, CT_TOX]
        answers: DataFrame with columns [smiles, FDA_APPROVED, CT_TOX]

    Returns:
        float: ROC-AUC score if >= 0.77, else 0.0
    """
    try:
        print(f"Grading Clintox submission...")
        print(f"  Submission shape: {submission.shape}")
        print(f"  Answers shape: {answers.shape}")

        # 1. 检查 smiles 列是否匹配
        if 'smiles' not in submission.columns or 'smiles' not in answers.columns:
            print("❌ Missing 'smiles' column")
            return 0.0

        data_correctness = (list(submission["smiles"]) == list(answers["smiles"]))

        if not data_correctness:
            print("❌ Data correctness failed: smiles columns do not match")
            return 0.0

        print("✓ Data correctness passed")

        # 2. 检查标签列
        required_cols = ['FDA_APPROVED', 'CT_TOX']
        for col in required_cols:
            if col not in submission.columns:
                print(f"❌ Missing column: {col}")
                return 0.0

        # 3. 计算 ROC-AUC（多标签）
        try:
            metric = roc_auc_score(
                answers[required_cols],
                submission[required_cols]
            )
        except ValueError as e:
            print(f"❌ ROC-AUC calculation failed: {e}")
            # 可能是概率值问题，尝试转换
            try:
                # 如果提交的是 0/1 标签，转换为概率
                metric = roc_auc_score(
                    answers[required_cols],
                    submission[required_cols].astype(float)
                )
            except:
                print("❌ Could not calculate ROC-AUC")
                return 0.0

        print(f"  ROC-AUC Score: {metric:.4f}")

        # 4. 应用阈值
        threshold = 0.77

        if metric >= threshold:
            print(f"✅ Func correctness passed (score >= {threshold})")
            return metric
        else:
            print(f"❌ Func correctness failed (score {metric:.4f} < {threshold})")
            return 0.0

    except Exception as e:
        print(f"❌ Error in grading: {e}")
        import traceback
        traceback.print_exc()
        return 0.0
'''


# 修正后的 config.yaml
CONFIG_YAML_FIXED = '''id: sciencebench-001-clintox-nn
name: "ScienceBench - clintox_nn.py"
competition_type: code
awards_medals: false
prizes: null
description: mlebench.benchmarks.sciencebench.competitions.sciencebench-001-clintox-nn.description:DESCRIPTION

dataset:
  answers: sciencebench-001-clintox-nn/prepared/private/clintox_gold.csv
  sample_submission: sciencebench-001-clintox-nn/prepared/public/sample_submission.csv

grader:
  name: roc_auc
  grade_fn: mlebench.benchmarks.sciencebench.competitions.sciencebench-001-clintox-nn.grade:grade

preparer: mlebench.benchmarks.sciencebench.competitions.sciencebench-001-clintox-nn.prepare:prepare
'''


def main():
    """修正 clintox 任务"""
    comp_dir = Path("/home/aiops/liufan/projects/DeepModeling/benchmarks/sciencebench/competitions/sciencebench-001-clintox-nn")

    print("🔧 Fixing sciencebench-001-clintox-nn...")

    # 1. 更新 prepare.py
    print("\n1. Updating prepare.py...")
    with open(comp_dir / "prepare.py", "w") as f:
        f.write(PREPARE_PY_FIXED)
    print("   ✓ prepare.py updated")

    # 2. 更新 grade.py
    print("\n2. Updating grade.py...")
    with open(comp_dir / "grade.py", "w") as f:
        f.write(GRADE_PY_FIXED)
    print("   ✓ grade.py updated")

    # 3. 更新 config.yaml
    print("\n3. Updating config.yaml...")
    with open(comp_dir / "config.yaml", "w") as f:
        f.write(CONFIG_YAML_FIXED)
    print("   ✓ config.yaml updated")

    print("\n✅ Fix completed!")
    print("\nNext steps:")
    print("1. Re-run data preparation:")
    print("   python prepare_data.py --competitions sciencebench-001-clintox-nn")
    print("\n2. Verify data structure:")
    print("   ls data/competitions/sciencebench-001-clintox-nn/prepared/private/")
    print("   # Should see: clintox_gold.csv")


if __name__ == '__main__':
    main()

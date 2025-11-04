#!/usr/bin/env python3
"""
再次修正 clintox 任务

修正内容：
1. test.csv 和 sample_submission.csv 格式一致（都包含所有列，但标签为空/零）
2. 完整的测试数据（带真实标签）放在 private/
"""

from pathlib import Path


PREPARE_PY_V2 = '''"""
Data preparation for ScienceBench task 1 (Clintox) - V2

修正：test 和 sample_submission 格式一致
"""

import pandas as pd
from pathlib import Path


def prepare(raw: Path, public: Path, private: Path):
    """
    Prepare the Clintox dataset (V2).

    修正：
    1. public/test.csv 和 sample_submission.csv 格式相同（都有所有列）
    2. private/ 保存完整的 gold results

    Args:
        raw: Path to datasets/clintox/
        public: Path to public directory
        private: Path to private directory
    """
    print("Preparing Clintox dataset (V2 - FORMAT FIXED)...")

    # 1. 读取训练数据
    train = pd.read_csv(raw / "clintox_train.csv")
    print(f"Loaded training data: {train.shape}")

    # 2. 读取 gold results（测试集真实答案）
    gold_path = Path("/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/eval_programs/gold_results/clintox_gold.csv")

    if not gold_path.exists():
        raise FileNotFoundError(f"Gold results not found: {gold_path}")

    gold = pd.read_csv(gold_path)
    print(f"Loaded gold results: {gold.shape}")
    print(f"Gold columns: {gold.columns.tolist()}")

    # 3. 保存训练数据到 public
    train.to_csv(public / "train.csv", index=False)
    print(f"✓ Saved training data to public/train.csv")

    # 4. 创建测试集（包含所有列，但标签为空）
    # 这样格式和 sample_submission 一致
    test_public = gold.copy()
    # 将标签列设为空字符串或 NaN（让 agent 知道需要预测这些列）
    test_public['FDA_APPROVED'] = ''
    test_public['CT_TOX'] = ''
    test_public.to_csv(public / "test.csv", index=False)
    print(f"✓ Saved test data (with empty labels) to public/test.csv")

    # 5. 创建 sample_submission（格式与 test.csv 完全一致）
    sample = gold.copy()
    sample['FDA_APPROVED'] = 0
    sample['CT_TOX'] = 0
    sample.to_csv(public / "sample_submission.csv", index=False)
    print(f"✓ Created sample_submission.csv (format matches test.csv)")

    # 6. 保存完整的 gold 到 private/（带真实标签）
    gold.to_csv(private / "test.csv", index=False)
    print(f"✓ Saved gold results (with true labels) to private/test.csv")

    print(f"\\nData preparation completed!")
    print(f"  Public files: {list(public.glob('*'))}")
    print(f"  Private files: {list(private.glob('*'))}")

    # 验证格式一致性
    test_cols = test_public.columns.tolist()
    sample_cols = sample.columns.tolist()
    print(f"\\n✓ Format check:")
    print(f"  test.csv columns: {test_cols}")
    print(f"  sample_submission.csv columns: {sample_cols}")
    print(f"  Format match: {test_cols == sample_cols}")
'''


CONFIG_YAML_V2 = '''id: sciencebench-001-clintox-nn
name: "ScienceBench - clintox_nn.py"
competition_type: code
awards_medals: false
prizes: null
description: mlebench.benchmarks.sciencebench.competitions.sciencebench-001-clintox-nn.description:DESCRIPTION

dataset:
  answers: sciencebench-001-clintox-nn/prepared/private/test.csv
  sample_submission: sciencebench-001-clintox-nn/prepared/public/sample_submission.csv

grader:
  name: roc_auc
  grade_fn: mlebench.benchmarks.sciencebench.competitions.sciencebench-001-clintox-nn.grade:grade

preparer: mlebench.benchmarks.sciencebench.competitions.sciencebench-001-clintox-nn.prepare:prepare
'''


def main():
    """修正 clintox 任务 V2"""
    comp_dir = Path("/home/aiops/liufan/projects/DeepModeling/benchmarks/sciencebench/competitions/sciencebench-001-clintox-nn")

    print("🔧 Fixing sciencebench-001-clintox-nn (V2 - Format Fix)...")

    # 1. 更新 prepare.py
    print("\n1. Updating prepare.py...")
    with open(comp_dir / "prepare.py", "w") as f:
        f.write(PREPARE_PY_V2)
    print("   ✓ prepare.py updated (V2)")

    # 2. 更新 config.yaml
    print("\n2. Updating config.yaml...")
    with open(comp_dir / "config.yaml", "w") as f:
        f.write(CONFIG_YAML_V2)
    print("   ✓ config.yaml updated (answers -> private/test.csv)")

    print("\n✅ Fix V2 completed!")
    print("\n修改内容:")
    print("  1. public/test.csv 和 sample_submission.csv 格式一致（都包含所有列）")
    print("  2. private/test.csv 包含真实标签")
    print("\nNext steps:")
    print("  python prepare_data.py --competitions sciencebench-001-clintox-nn")


if __name__ == '__main__':
    main()

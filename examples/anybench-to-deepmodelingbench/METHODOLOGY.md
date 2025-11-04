# 任意 Benchmark 转换到 DeepModeling/MLE-Bench 格式的方法论

## 📋 概述

本文档提供了一套通用的方法论，用于将任意数据集/基准测试转换为 DeepModeling/MLE-Bench 格式。此方法论基于 DABench 到 MLE-Bench 的成功转换经验。

## 🎯 核心理念

**关键目标**: 将任何数据科学任务转换为标准化的比赛格式，使其可以被自动化评估系统运行和评分。

### 三个核心目录
- **Benchmark 注册目录**: 存放比赛定义和评估逻辑
- **数据源目录**: 存放原始数据（保持不变）
- **转换脚本目录**: 存放批量转换工具

## 📂 标准目录结构

```
/home/aiops/liufan/projects/
├── DeepModeling/
│   ├── benchmarks/
│   │   └── <benchmark-name>/           # 比赛注册目录
│   │       └── competitions/
│   │           └── <task-id>/
│   │               ├── config.yaml      # 比赛配置 ⭐
│   │               ├── description.md   # 任务描述
│   │               ├── grade.py         # 评分函数 ⭐
│   │               ├── prepare.py       # 数据准备函数 ⭐
│   │               ├── leaderboard.csv  # 排行榜（可选）
│   │               └── checksums.yaml   # 数据校验（可选）
│   └── examples/
│       ├── anybench-to-deepmodelingbench/  # 方法论文档（本文档）
│       └── <source>-to-mlebench/           # 具体转换脚本
│           ├── README.md
│           ├── convert_<source>_to_mlebench.py
│           └── ... (其他辅助脚本)
└── <SourceBenchmark>/                  # 原始数据源目录
    └── benchmark/
        └── <task-id>/
            ├── public/                  # 公开数据
            ├── private/                 # 私有数据（答案）
            └── ... (其他原始文件)
```

## 🔑 六个核心文件

### 1. config.yaml - 比赛配置文件

**作用**: 定义比赛的元数据和路径

**模板**:
```yaml
id: <competition-id>
name: "<Competition Name>"
competition_type: code  # 或 notebook
awards_medals: false
prizes: null
description: mlebench/competitions/<competition-id>/description.md

dataset:
  answers: <competition-id>/prepared/private/answer.csv
  sample_submission: <competition-id>/prepared/public/sample_submission.csv

grader:
  name: <metric-name>  # accuracy, rmse, exact_match 等
  grade_fn: mlebench.competitions.<competition-id>.grade:grade

preparer: mlebench.competitions.<competition-id>.prepare:prepare
```

**关键决策点**:
- **competition_type**: code 还是 notebook
- **grader.name**: 选择合适的评估指标
- **dataset paths**: 确保路径与数据准备函数一致

### 2. description.md - 任务描述

**作用**: 提供任务的详细描述，供 Agent 理解任务

**结构**:
```markdown
# <Task Name>

## Task Description
<详细描述任务目标>

## Dataset Description
- **Training Data**: <描述训练数据>
- **Test Data**: <描述测试数据>
- **Target**: <描述预测目标>

## Evaluation Metric
<描述评估方式>

## Data Fields
- `field1`: <描述>
- `field2`: <描述>

## Submission Format
<描述提交文件格式>
```

### 3. prepare.py - 数据准备函数

**作用**: 将原始数据转换为标准格式

**核心函数签名**:
```python
from pathlib import Path

def prepare(raw: Path, public: Path, private: Path):
    """
    准备数据集

    Args:
        raw: 原始数据目录
        public: 公开数据目录（参赛者可见）
        private: 私有数据目录（仅用于评分）
    """
    # 1. 从 raw 读取原始数据
    # 2. 处理并分割数据
    # 3. 保存到 public 和 private
    pass
```

**标准输出**:
- **public/**:
  - `train.csv` 或 `train_data.npy`: 训练数据
  - `sample_submission.csv`: 提交样本
- **private/**:
  - `answer.csv` 或 `test_labels.csv`: 测试集答案

**最佳实践**:
1. ✅ 添加详细的数据加载日志
2. ✅ 包含数据验证检查
3. ✅ 处理异常情况（try-except）
4. ✅ 使用 assert 验证输出文件存在

### 4. grade.py - 评分函数

**作用**: 比较提交结果和正确答案，计算得分

**核心函数签名**:
```python
import pandas as pd

def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    """
    评分函数

    Args:
        submission: 参赛者提交的预测结果
        answers: 正确答案

    Returns:
        float: 得分（通常在 0-1 之间）
    """
    # 1. 数据对齐（merge on id）
    # 2. 计算评估指标
    # 3. 返回得分
    pass
```

**常见评估指标**:
- **准确率**: `sklearn.metrics.accuracy_score`
- **RMSE**: `sklearn.metrics.mean_squared_error(squared=False)`
- **精确匹配**: 自定义字符串匹配逻辑
- **F1 分数**: `sklearn.metrics.f1_score`

### 5. leaderboard.csv - 排行榜（可选）

**作用**: 记录基准分数

**格式**:
```csv
submission_id,score,username,date
baseline,0.75,random_baseline,2024-01-01
human,0.90,human_expert,2024-01-01
```

### 6. checksums.yaml - 数据校验（可选）

**作用**: 验证数据完整性

**格式**:
```yaml
public:
  train.csv: <md5-hash>
  sample_submission.csv: <md5-hash>
private:
  answer.csv: <md5-hash>
```

## 🔄 转换流程 (7步法)

### Step 1: 分析源数据集结构

**任务清单**:
- [ ] 确定有多少个任务/题目
- [ ] 找到数据文件位置
- [ ] 了解数据格式（CSV, JSON, NPY 等）
- [ ] 确定评估方式和答案格式

**输出**: 源数据集的结构文档

### Step 2: 设计 competition_id 命名规则

**命名规范**:
```
<source>-<task-id>-<keywords>
```

**示例**:
- DABench: `dabench-0-mean-fare`
- ScienceAgent: `sciencebench-01-glacier-plot`
- MathModeling: `mathmodel-a-population-growth`

**最佳实践**:
- 使用小写字母和连字符
- 包含数字 ID 以保证唯一性
- 添加 2-3 个描述性关键词

### Step 3: 创建数据映射逻辑

**关键问题**:
1. **训练/测试分割**: 如何划分？是否已经划分？
2. **答案提取**: 答案存储在哪里？格式是什么？
3. **文件格式**: CSV, JSON, NPY, 还是其他？

**数据流图**:
```
源数据 → prepare.py → public/  (train.csv, sample_submission.csv)
                   → private/ (answer.csv)
```

### Step 4: 编写转换脚本

**核心脚本结构**:
```python
# convert_<source>_to_mlebench.py

import argparse
from pathlib import Path

# 1. 配置路径
SOURCE_DIR = Path('/path/to/source')
COMPETITIONS_DIR = Path('/path/to/DeepModeling/benchmarks/<name>/competitions')

# 2. 加载源数据
def load_source_data():
    pass

# 3. 生成六个核心文件
def create_config_yaml(task_id):
    pass

def create_description_md(task_data):
    pass

def create_prepare_py(task_data):
    pass

def create_grade_py(task_data):
    pass

# 4. 批量转换函数
def convert_task(task_id):
    # 4.1 创建目录
    # 4.2 生成所有文件
    # 4.3 验证
    pass

# 5. 主函数
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--task-ids', nargs='+', type=int)
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--auto-prepare', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    # 批量转换
    for task_id in task_ids:
        convert_task(task_id)

        if args.auto_prepare:
            # 自动运行 prepare.py
            run_prepare(task_id)

if __name__ == '__main__':
    main()
```

### Step 5: 实现 auto-prepare 功能

**作用**: 转换后自动准备数据，避免手动操作

**实现**:
```python
import subprocess

def run_prepare(competition_id: str, data_dir: Path):
    """自动运行数据准备脚本"""
    prepare_script = data_dir / competition_id / "prepare.py"

    if not prepare_script.exists():
        print(f"⚠ Prepare script not found: {prepare_script}")
        return False

    print(f"📦 Auto-preparing data for {competition_id}...")

    try:
        result = subprocess.run(
            ["python", str(prepare_script)],
            cwd=str(data_dir / competition_id),
            timeout=60,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"✅ Data prepared successfully!")
            return True
        else:
            print(f"❌ Prepare failed: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print(f"❌ Prepare timeout (60s)")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
```

### Step 6: 验证转换结果

**验证清单**:
- [ ] 所有必需文件都已创建
- [ ] config.yaml 格式正确
- [ ] prepare.py 可以成功运行
- [ ] public/ 和 private/ 目录包含正确的文件
- [ ] grade.py 可以正确评分

**自动化验证脚本**:
```python
def verify_competition(competition_dir: Path):
    """验证比赛文件完整性"""
    required_files = [
        'config.yaml',
        'description.md',
        'grade.py',
        'prepare.py'
    ]

    for file in required_files:
        assert (competition_dir / file).exists(), f"Missing {file}"

    print("✅ All files present")
```

### Step 7: 运行测试

**测试流程**:
```bash
# 1. 转换单个任务
python convert_<source>_to_mlebench.py --task-ids 0 --auto-prepare

# 2. 验证数据文件
ls <data-dir>/<competition-id>/prepared/public/
ls <data-dir>/<competition-id>/prepared/private/

# 3. 运行比赛测试
cd /home/aiops/liufan/projects/DeepModeling
python main.py \
  --benchmark <benchmark-name> \
  --competitions <competition-id> \
  --max-steps 5

# 4. 检查结果
cat runs/benchmark_results/*/results.json
```

## 🎨 常见数据格式转换模式

### 模式 1: 表格数据 (CSV)

**源格式**:
```
data/
  train.csv
  test.csv
  answers.csv
```

**prepare.py 模板**:
```python
def prepare(raw: Path, public: Path, private: Path):
    # 读取数据
    train = pd.read_csv(raw / "train.csv")
    test = pd.read_csv(raw / "test.csv")
    answers = pd.read_csv(raw / "answers.csv")

    # 保存到 public
    train.to_csv(public / "train.csv", index=False)
    test.to_csv(public / "test.csv", index=False)

    # 创建提交样本
    sample = pd.DataFrame({"id": test["id"], "target": 0})
    sample.to_csv(public / "sample_submission.csv", index=False)

    # 保存答案到 private
    answers.to_csv(private / "answer.csv", index=False)
```

### 模式 2: 数组数据 (NumPy)

**源格式**:
```
data/
  train_data.npy
  train_labels.npy
  test_data.npy
  test_labels.npy
```

**prepare.py 模板**:
```python
import numpy as np

def prepare(raw: Path, public: Path, private: Path):
    # 加载数据
    X_train = np.load(raw / "train_data.npy")
    y_train = np.load(raw / "train_labels.npy")
    X_test = np.load(raw / "test_data.npy")
    y_test = np.load(raw / "test_labels.npy")

    # 保存到 public
    np.save(public / "train_data.npy", X_train)
    np.save(public / "train_labels.npy", y_train)
    np.save(public / "test_data.npy", X_test)

    # 创建提交样本
    sample_df = pd.DataFrame({
        "id": range(len(y_test)),
        "label": 0
    })
    sample_df.to_csv(public / "sample_submission.csv", index=False)

    # 保存答案
    answer_df = pd.DataFrame({
        "id": range(len(y_test)),
        "label": y_test
    })
    answer_df.to_csv(private / "test_labels.csv", index=False)
```

### 模式 3: JSON 数据

**源格式**:
```
tasks.json
answers.json
datasets/
```

**prepare.py 模板**:
```python
import json

def prepare(raw: Path, public: Path, private: Path):
    # 加载任务定义
    with open(raw / "tasks.json") as f:
        tasks = json.load(f)

    with open(raw / "answers.json") as f:
        answers = json.load(f)

    # 加载和处理数据集
    # ... (具体逻辑取决于数据格式)

    # 保存处理后的数据
    # ...
```

### 模式 4: 文本答案格式

**适用场景**: DABench 风格的答案格式 `@key[value]`

**grade.py 模板**:
```python
import re

def parse_answer(answer_str: str) -> dict:
    """解析 @key[value] 格式的答案"""
    pattern = r'@(\w+)\[([^\]]+)\]'
    matches = re.findall(pattern, answer_str)
    return {key: value for key, value in matches}

def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    """精确匹配评分"""
    total = len(answers)
    correct = 0

    for idx, row in answers.iterrows():
        true_answer = parse_answer(row['answer'])
        pred_answer = parse_answer(submission.loc[idx, 'answer'])

        if true_answer == pred_answer:
            correct += 1

    return correct / total
```

## 🚀 高级特性

### 特性 1: 多评估指标支持

有些任务可能需要多个评估指标。

**实现**:
```python
# grade.py
def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    """返回主要指标"""
    accuracy = calculate_accuracy(submission, answers)
    return accuracy

def grade_detailed(submission: pd.DataFrame, answers: pd.DataFrame) -> dict:
    """返回详细指标"""
    return {
        "accuracy": calculate_accuracy(submission, answers),
        "f1": calculate_f1(submission, answers),
        "precision": calculate_precision(submission, answers),
        "recall": calculate_recall(submission, answers)
    }
```

### 特性 2: 数据集版本控制

使用 checksums.yaml 确保数据一致性。

**生成 checksums**:
```python
import hashlib

def calculate_md5(file_path: Path) -> str:
    """计算文件 MD5"""
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5.update(chunk)
    return md5.hexdigest()

def generate_checksums(data_dir: Path) -> dict:
    """生成所有数据文件的校验和"""
    checksums = {"public": {}, "private": {}}

    for file in (data_dir / "public").glob("*"):
        checksums["public"][file.name] = calculate_md5(file)

    for file in (data_dir / "private").glob("*"):
        checksums["private"][file.name] = calculate_md5(file)

    return checksums
```

### 特性 3: 并行转换

对于大量任务，使用多进程加速转换。

**实现**:
```python
from multiprocessing import Pool

def convert_task_wrapper(args):
    """包装函数用于多进程"""
    task_id, config = args
    try:
        convert_task(task_id, config)
        return task_id, True
    except Exception as e:
        return task_id, False

def batch_convert(task_ids: list, num_workers: int = 4):
    """并行转换多个任务"""
    with Pool(num_workers) as pool:
        results = pool.map(convert_task_wrapper, task_ids)

    success = [tid for tid, ok in results if ok]
    failed = [tid for tid, ok in results if not ok]

    print(f"✅ Success: {len(success)}")
    print(f"❌ Failed: {len(failed)}")
```

## 📊 质量检查清单

### 转换前检查
- [ ] 源数据集完整下载
- [ ] 了解数据格式和结构
- [ ] 明确评估指标
- [ ] 确定答案位置

### 转换后检查
- [ ] 所有必需文件存在
- [ ] config.yaml 格式正确
- [ ] description.md 描述清晰
- [ ] prepare.py 可以运行
- [ ] grade.py 逻辑正确
- [ ] 数据文件生成正确

### 运行时检查
- [ ] 比赛可以成功加载
- [ ] Agent 能理解任务描述
- [ ] 提交文件格式正确
- [ ] 评分结果合理
- [ ] 无错误或异常

## 💡 最佳实践

### 1. 渐进式开发
- 先转换 1-2 个任务测试
- 验证完整流程后再批量转换
- 使用 `--dry-run` 预览转换

### 2. 详细的日志输出
```python
print(f"✅ Success: {message}")
print(f"❌ Error: {message}")
print(f"⚠ Warning: {message}")
print(f"📦 Processing: {message}")
print(f"🔍 Found: {message}")
```

### 3. 错误处理
```python
try:
    # 主要逻辑
    pass
except FileNotFoundError as e:
    print(f"❌ File not found: {e}")
    # 降级处理
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
```

### 4. 数据验证
```python
# 在 prepare.py 中添加验证
assert (public / "train.csv").exists(), "Training data missing"
assert len(train) > 0, "Training data is empty"
assert set(train.columns) == expected_columns, "Column mismatch"
```

### 5. 文档优先
- README.md 写清楚使用方法
- 添加示例命令
- 记录常见问题和解决方案

## 🔗 参考资源

- **DABench 转换示例**: `/home/aiops/liufan/projects/data_science_agent_toolkit/examples/dabench_to_mlebench/`
- **MLE-Bench 文档**: `/home/aiops/liufan/projects/DeepModeling/benchmarks/mlebench/`
- **配置示例**: `/home/aiops/liufan/projects/DeepModeling/benchmarks/mlebench/competitions/ethanol-concentration/`

## 📝 总结

转换任意 benchmark 到 MLE-Bench 格式的核心是：
1. **理解源数据结构**
2. **标准化到六个核心文件**
3. **实现 prepare 和 grade 函数**
4. **自动化批量转换流程**
5. **充分测试和验证**

遵循本方法论，可以高效、标准化地将任何数据集转换为 DeepModeling/MLE-Bench 格式。

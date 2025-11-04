# ScienceBench 数据准备指南

## 📂 数据组织结构

ScienceBench 的数据按照 MLE-Bench 标准组织：

```
项目结构:
├── ScienceAgent-bench/benchmark/
│   └── datasets/                           # 源数据（只读）
│       ├── clintox/
│       │   ├── clintox_train.csv
│       │   └── clintox_test.csv
│       └── ...
│
├── DeepModeling/
│   ├── benchmarks/sciencebench/competitions/
│   │   └── sciencebench-001-clintox-nn/   # 比赛定义
│   │       ├── config.yaml
│   │       ├── description.md
│   │       ├── grade.py
│   │       └── prepare.py                  # ⭐ 数据准备脚本
│   │
│   └── data/competitions/                  # 准备后的数据（由 prepare.py 生成）
│       └── sciencebench-001-clintox-nn/
│           └── prepared/
│               ├── public/                 # 公开数据
│               │   ├── clintox_train.csv
│               │   ├── clintox_test.csv
│               │   └── sample_submission.csv
│               └── private/                # 私有数据（答案）
│                   └── answer.csv
```

## 🚀 数据准备流程

### 步骤 1: 转换比赛定义

首先转换比赛定义（如果还没转换）：

```bash
cd /home/aiops/liufan/projects/DeepModeling/examples/scienceagentbench-to-mlebench

# 转换单个任务
python convert_scienceagent_to_mlebench.py --instance-ids 1

# 或批量转换
python convert_scienceagent_to_mlebench.py --all
```

**输出**: 在 `benchmarks/sciencebench/competitions/` 下创建比赛目录

### 步骤 2: 准备数据

运行数据准备脚本：

```bash
cd /home/aiops/liufan/projects/DeepModeling/examples/scienceagentbench-to-mlebench

# 准备单个比赛的数据
python prepare_data.py --competitions sciencebench-001-clintox-nn

# 准备多个比赛的数据
python prepare_data.py --competitions sciencebench-001-clintox-nn sciencebench-002-mat-feature-select

# 准备所有比赛的数据
python prepare_data.py --all
```

**输出**: 在 `data/competitions/<comp-id>/prepared/` 下创建 public/ 和 private/ 目录

### 步骤 3: 验证数据

```bash
# 检查数据目录
ls -la /home/aiops/liufan/projects/DeepModeling/data/competitions/sciencebench-001-clintox-nn/prepared/

# 应该看到:
# prepared/
#   ├── public/
#   │   ├── clintox_train.csv
#   │   ├── clintox_test.csv
#   │   └── sample_submission.csv
#   └── private/
#       └── answer.csv

# 查看文件内容
head -5 /home/aiops/liufan/projects/DeepModeling/data/competitions/sciencebench-001-clintox-nn/prepared/public/sample_submission.csv
```

## 📊 数据准备脚本使用

### 列出所有比赛

```bash
python prepare_data.py --list
```

**输出**:
```
Available Competitions (1)
============================================================

✅ sciencebench-001-clintox-nn  # ✅ = 数据已准备
❌ sciencebench-002-xxx         # ❌ = 数据未准备
```

### 准备单个比赛

```bash
python prepare_data.py --competitions sciencebench-001-clintox-nn
```

**输出示例**:
```
============================================================
Preparing data for: sciencebench-001-clintox-nn
============================================================
Dataset name: clintox
Raw data: /home/aiops/liufan/projects/ScienceAgent-bench/benchmark/datasets/clintox
Data dir: /home/aiops/liufan/projects/DeepModeling/data/competitions/sciencebench-001-clintox-nn
✓ Created data directories

📦 Running prepare function...
Copying data files to public directory...
  Copied: clintox_test.csv
  Copied: clintox_train.csv
Created sample_submission.csv
Created answer.csv

✅ Data preparation completed!

📊 Generated files:
  Public:  3 files
    - clintox_test.csv
    - sample_submission.csv
    - clintox_train.csv
  Private: 1 files
    - answer.csv
```

### 准备所有比赛

```bash
python prepare_data.py --all
```

这将批量准备所有已转换的比赛的数据。

## 🔧 自定义数据集名称

如果自动推断的数据集名称不正确，可以手动指定：

```bash
python prepare_data.py --competitions sciencebench-001-xxx --dataset-name custom_dataset_name
```

## 📍 关键路径说明

| 路径类型 | 位置 | 说明 |
|---------|------|------|
| **源数据** | `/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/datasets/` | 原始数据，只读，不修改 |
| **比赛定义** | `/home/aiops/liufan/projects/DeepModeling/benchmarks/sciencebench/competitions/` | 比赛配置和准备脚本 |
| **准备后数据** | `/home/aiops/liufan/projects/DeepModeling/data/competitions/` | public/ 和 private/ 数据 |

## 🎯 config.yaml 中的路径

在 config.yaml 中，数据路径是相对于数据根目录的：

```yaml
dataset:
  answers: sciencebench-001-clintox-nn/prepared/private/answer.csv
  sample_submission: sciencebench-001-clintox-nn/prepared/public/sample_submission.csv
```

当运行比赛时，指定数据根目录：

```bash
cd /home/aiops/liufan/projects/DeepModeling

python main.py \
  --benchmark sciencebench \
  --data-dir /home/aiops/liufan/projects/DeepModeling/data/competitions \
  --competitions sciencebench-001-clintox-nn
```

## 🔍 数据准备工作流程详解

### prepare.py 做了什么？

每个比赛的 `prepare.py` 会：

1. **读取原始数据** (从 `ScienceAgent-bench/benchmark/datasets/`)
2. **处理和清洗数据**
3. **创建训练/测试分割** (如需要)
4. **生成 public/ 目录**:
   - `train.csv` 或数据文件
   - `test.csv` (无答案)
   - `sample_submission.csv` (提交模板)
5. **生成 private/ 目录**:
   - `answer.csv` (测试集答案，用于评分)

### 数据准备脚本做了什么？

`prepare_data.py` 会：

1. **找到比赛定义** (在 `benchmarks/sciencebench/competitions/`)
2. **推断数据集名称** (从 comp_id)
3. **创建数据目录** (`data/competitions/<comp-id>/prepared/`)
4. **调用 prepare.py** (执行数据准备逻辑)
5. **验证生成的文件**

## 💡 常见问题

### Q: 为什么数据不在 ScienceAgent-bench 目录下？

**A**: 按照 MLE-bench 的标准，数据应该在独立的数据目录中，与比赛定义分离。这样设计的好处：
- ✅ 清晰的职责分离
- ✅ 可以有多个数据副本
- ✅ 不污染源数据目录

### Q: 可以把数据放在其他位置吗？

**A**: 可以！只需在运行比赛时指定 `--data-dir`:

```bash
# 使用自定义数据目录
python main.py \
  --benchmark sciencebench \
  --data-dir /path/to/your/data \
  --competitions sciencebench-001-clintox-nn
```

### Q: 如何重新准备数据？

**A**: 直接重新运行准备脚本：

```bash
python prepare_data.py --competitions sciencebench-001-clintox-nn
```

它会覆盖旧数据。

### Q: prepare.py 失败了怎么办？

**A**: 检查：
1. 源数据是否存在
2. 数据集名称是否正确
3. 准备脚本的逻辑是否正确

可以手动运行 prepare.py 调试：

```python
from pathlib import Path
import sys
sys.path.insert(0, '/path/to/competition')

from prepare import prepare

raw = Path('/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/datasets/clintox')
public = Path('/tmp/test_public')
private = Path('/tmp/test_private')

public.mkdir(parents=True, exist_ok=True)
private.mkdir(parents=True, exist_ok=True)

prepare(raw, public, private)
```

## 📈 批量准备所有任务的数据

```bash
# 第一步：转换所有比赛定义
cd /home/aiops/liufan/projects/DeepModeling/examples/scienceagentbench-to-mlebench
python convert_scienceagent_to_mlebench.py --all

# 第二步：准备所有数据
python prepare_data.py --all

# 预计耗时: 约 5-10 分钟（取决于数据大小）
```

## 🎉 验证完成

数据准备完成后，你应该能看到：

```bash
# 列出所有准备好的数据
ls /home/aiops/liufan/projects/DeepModeling/data/competitions/

# 输出示例:
# sciencebench-001-clintox-nn/
# sciencebench-002-mat-feature-select/
# ...

# 检查单个比赛的数据
ls /home/aiops/liufan/projects/DeepModeling/data/competitions/sciencebench-001-clintox-nn/prepared/

# 输出:
# public/
# private/
```

现在可以运行比赛了！🚀

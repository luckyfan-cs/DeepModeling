# Test Scripts Overview

本目录包含用于测试各个 benchmark 的脚本集合。

## 📋 脚本总览

### 1. 采样测试脚本（Sample Tests）

这些脚本对每个 benchmark 进行代表性采样测试：

| 脚本名称 | Benchmark | 任务数 | 采样率 | 说明 |
|---------|-----------|--------|--------|------|
| `test_engineeringbench_sample.sh` | Engineering | 30 | 30% | 工程领域任务 |
| `test_mathmodelingbench_sample.sh` | Math Modeling | 145 | 11% | 数学建模任务（4种类型）|
| `test_sciencebench_sample.sh` | Science | 35 | 34% | 科学计算任务（多领域）|
| `test_mlebench_dabench_sample.sh` | MLE DA-Bench | 33 | 13% | 数据分析任务 |
| `run_all_sample_tests.sh` | 全部 | 243 | 14% | **运行所有采样测试** |

**总计**: 从 1755 个任务中采样 243 个任务

### 2. MLEBench 精选任务脚本

精选的 5 个 Kaggle 竞赛任务，覆盖不同的机器学习领域：

| 脚本名称 | 任务数 | 说明 |
|---------|--------|------|
| `test_mlebench_selected.sh` | 5 | 批量运行5个精选任务 |
| `test_mlebench_individual.sh` | 1 | 单独运行某个精选任务（需传入编号1-5）|

**精选任务列表**:
1. aptos2019-blindness-detection - 医疗影像（糖尿病视网膜病变）
2. plant-pathology-2020-fgvc7 - 计算机视觉（植物病理学）
3. us-patent-phrase-to-phrase-matching - NLP（专利短语匹配）
4. new-york-city-taxi-fare-prediction - 回归预测（出租车票价）
5. tabular-playground-series-dec-2021 - 表格数据竞赛

### 3. 验证脚本

| 脚本名称 | 说明 |
|---------|------|
| `verify_sample_tasks.sh` | 验证所有采样任务是否存在 |
| `verify_mlebench_selected.sh` | 验证MLEBench精选任务是否存在 |

### 4. 其他脚本

| 脚本名称 | 说明 |
|---------|------|
| `engineeringbench.sh` | Engineering 单任务示例 |
| `mathmodeling.sh` | Math Modeling 单任务示例 |
| `sciencebench.sh` | Science 单任务示例 |
| `mlebench.sh` | MLEBench 单任务示例 |

## 🚀 快速开始

### 运行所有采样测试（推荐用于全面测试）
```bash
cd /home/aiops/liufan/projects/DeepModeling
./job_scripts/run_all_sample_tests.sh
```

### 运行单个 Benchmark 采样测试
```bash
cd /home/aiops/liufan/projects/DeepModeling

# 运行 Engineering Benchmark (30 个任务)
./job_scripts/test_engineeringbench_sample.sh

# 运行 Math Modeling Benchmark (145 个任务)
./job_scripts/test_mathmodelingbench_sample.sh

# 运行 Science Benchmark (35 个任务)
./job_scripts/test_sciencebench_sample.sh

# 运行 MLE DA-Bench (33 个任务)
./job_scripts/test_mlebench_dabench_sample.sh
```

### 运行 MLEBench 精选任务
```bash
cd /home/aiops/liufan/projects/DeepModeling

# 批量运行所有5个精选任务
./job_scripts/test_mlebench_selected.sh

# 单独运行某个任务（1-5）
./job_scripts/test_mlebench_individual.sh 1  # 糖尿病视网膜病变检测
./job_scripts/test_mlebench_individual.sh 2  # 植物病理学
./job_scripts/test_mlebench_individual.sh 3  # 专利短语匹配
./job_scripts/test_mlebench_individual.sh 4  # 出租车票价预测
./job_scripts/test_mlebench_individual.sh 5  # 表格数据竞赛
```

### 验证任务是否存在
```bash
cd /home/aiops/liufan/projects/DeepModeling

# 验证采样任务
./job_scripts/verify_sample_tasks.sh

# 验证精选任务
./job_scripts/verify_mlebench_selected.sh
```

## 📊 测试覆盖

### 按 Benchmark 分类

```
总任务数: 1755 + 5 (精选) = 1760
采样任务数: 243
采样率: 14%

Engineering:        100 任务 →  30 采样 (30%)
Math Modeling:     1294 任务 → 145 采样 (11%)
Science:            103 任务 →  35 采样 (34%)
MLE (DA-Bench):     258 任务 →  33 采样 (13%)
MLE (精选):           5 任务 →   5 全量 (100%)
```

### 按任务类型分类

- **工程计算**: industry-0 到 industry-99
- **数学建模**: bwor, mamo-easy, mamo-complex, mamo-ode
- **科学计算**: 材料、生物、化学、地球科学等
- **数据分析**: 相关性、离群值、统计、特征工程等
- **机器学习**: 计算机视觉、NLP、回归、分类

## 📖 详细文档

- [SAMPLE_TESTS_README.md](SAMPLE_TESTS_README.md) - 采样测试详细说明
- [MLEBENCH_SELECTED_README.md](MLEBENCH_SELECTED_README.md) - MLEBench 精选任务详细说明

## ⚙️ 配置说明

所有脚本使用以下基本命令格式：

```bash
python main.py \
  --workflow scientific \
  --benchmark <benchmark_name> \
  --data-dir <data_directory> \
  --task <task1> <task2> ...
```

### 参数说明

- `--workflow`: 工作流类型（通常为 `scientific`）
- `--benchmark`: Benchmark 名称（mle, mathmodeling, engineeringbench, sciencebench）
- `--data-dir`: 数据目录路径
- `--task`: 要运行的任务列表（支持批量）

## 💡 最佳实践

1. **首次运行**: 建议先运行验证脚本确保所有任务存在
2. **快速测试**: 使用精选任务脚本快速验证系统是否正常
3. **全面测试**: 使用采样测试脚本进行全面的性能评估
4. **单任务调试**: 使用 individual 脚本单独运行某个任务进行调试

## 🔧 故障排除

### 任务未找到
```bash
# 运行验证脚本检查
./job_scripts/verify_sample_tasks.sh
./job_scripts/verify_mlebench_selected.sh
```

### 数据目录问题
确保数据目录存在且包含必要文件：
```bash
ls -la ./data/engineering-bench/competitions
ls -la ./benchmarks/mlebench/competitions
```

### 权限问题
添加执行权限：
```bash
chmod +x job_scripts/*.sh
```

## 📝 结果查看

测试结果保存在：
```
runs/benchmark_results/
├── scientific_on_engineeringbench/
├── scientific_on_mathmodeling/
├── scientific_on_sciencebench/
└── scientific_on_mle/
```

每个目录包含：
- 任务运行日志
- 评分结果
- 模型输出
- 元数据文件

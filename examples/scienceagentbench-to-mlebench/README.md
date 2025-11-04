# ScienceAgent-bench 到 MLE-Bench 批量转换工具

## 📋 概述

这个工具可以批量将 ScienceAgent-bench 的科学计算任务转换为 MLE-Bench 格式的比赛。

## 🌟 特性

- ✅ 自动扫描 ScienceAgent-bench 任务
- ✅ 生成标准 MLE-Bench 格式文件
- ✅ 支持批量转换
- ✅ 自动数据准备功能
- ✅ 任务元数据提取

## 🚀 快速使用

### 两步流程

#### 步骤 1: 转换比赛定义

```bash
# 列出所有可用任务
python convert_scienceagent_to_mlebench.py --list

# 转换单个任务
python convert_scienceagent_to_mlebench.py --instance-ids 1

# 转换多个任务
python convert_scienceagent_to_mlebench.py --instance-ids 1 2 3

# 批量转换所有任务
python convert_scienceagent_to_mlebench.py --all
```

#### 步骤 2: 准备数据 ⭐

```bash
# 准备单个任务的数据
python prepare_data.py --competitions sciencebench-001-clintox-nn

# 准备多个任务的数据
python prepare_data.py --competitions sciencebench-001-clintox-nn sciencebench-002-xxx

# 准备所有任务的数据
python prepare_data.py --all

# 查看数据准备状态
python prepare_data.py --list
```

## 📁 源数据结构

ScienceAgent-bench 的数据结构：

```
/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/
├── datasets/                    # 数据集目录
│   ├── CoralSponge/
│   ├── dili/
│   ├── ocean_glacier/
│   └── ...
├── gold_programs/               # 参考程序 (102 tasks)
│   ├── 3k.py
│   ├── BBBC002_cell-count.py
│   ├── BurnScar.py
│   └── ...
├── eval_programs/               # 评估程序
│   ├── 3k_eval.py
│   ├── BBBC002_cell_count_eval.py
│   └── ...
└── scoring_rubrics/             # 评分标准
    ├── 3k_rubric.json
    ├── BBBC002_cell-count_rubric.json
    └── ...
```

## 📊 生成的文件结构

### 1. 比赛注册目录

```
/home/aiops/liufan/projects/DeepModeling/benchmarks/sciencebench/competitions/
└── sciencebench-01-<task-name>/
    ├── config.yaml         # 比赛配置
    ├── description.md      # 任务描述
    ├── grade.py            # 评分函数
    ├── prepare.py          # 数据准备函数
    ├── leaderboard.csv     # 排行榜
    └── checksums.yaml      # 数据校验
```

### 2. 源数据目录（只读，不修改）

```
/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/
└── datasets/                    # 原始数据（只读）
    ├── clintox/
    │   ├── clintox_train.csv
    │   └── clintox_test.csv
    └── ...
```

### 3. 准备后的数据目录

```
/home/aiops/liufan/projects/DeepModeling/data/competitions/
└── sciencebench-001-clintox-nn/
    └── prepared/
        ├── public/              # 公开数据（由 prepare.py 生成）
        │   ├── clintox_train.csv
        │   ├── clintox_test.csv
        │   └── sample_submission.csv
        └── private/             # 私有数据（由 prepare.py 生成）
            └── answer.csv
```

## 🎯 任务类型和映射

ScienceAgent-bench 包含多种科学任务类型：

### Biology & Medicine
- **3k**: Single-cell RNA-seq analysis
- **BBBC002_cell-count**: Cell counting from microscopy images
- **biopsykit_***: Physiological signal analysis
- **clintox**: Clinical toxicity prediction
- **dili**: Drug-induced liver injury prediction

### Climate & Geoscience
- **BurnScar**: Burn scar detection
- **EOF_***: Empirical Orthogonal Function analysis
- **ocean_glacier**: Glacier modeling (OGGM)
- **Flooding**: Flood area analysis
- **UrbanHeat**: Urban heat island analysis
- **WaterQuality**: Water quality monitoring

### Neuroscience & Psychology
- **CogSci_***: Cognitive science modeling (JNMF)
- **EDR_analyze**: Electrodermal response analysis
- **EOG_analyze**: Electrooculography analysis
- **HRV_analyze**: Heart rate variability analysis
- **thingseeg2**: EEG signal classification

### Chemistry & Drug Discovery
- **admet_ai**: ADMET property prediction
- **antibioticsai_filter**: Antibiotic candidate filtering
- **compound_filter**: Chemical compound filtering
- **drugex_vis**: Drug generation visualization
- **MD_KNN/MD_RF**: Molecular descriptor models

## 🔧 转换逻辑

### Task ID 生成规则

```python
sciencebench-<seq-number>-<task-name-normalized>
```

示例：
- `3k` → `sciencebench-01-3k`
- `BBBC002_cell-count` → `sciencebench-02-bbbc002-cell-count`
- `ocean_glacier` → `sciencebench-03-ocean-glacier`

### 评分方式映射

根据任务类型自动选择评分方式：

| 任务后缀/类型 | 评分方式 | grade.py 实现 |
|--------------|---------|--------------|
| `*_plot` | visual_similarity | 图像相似度对比 |
| `*_vis` | visual_similarity | 图像相似度对比 |
| `*_count` | rmse | RMSE 评分 |
| `*_models` | accuracy | 分类准确率 |
| `*_RF/*_KNN/*_SVM` | accuracy | 分类准确率 |
| `*_analyze` | rmse | RMSE 评分 |
| default | exact_match | 精确匹配 |

### 数据准备逻辑

```python
def prepare(raw: Path, public: Path, private: Path):
    """
    准备 ScienceAgent 任务数据

    Args:
        raw: /home/aiops/liufan/projects/ScienceAgent-bench/benchmark/datasets/<task-dataset>
        public: <task>/public
        private: <task>/private
    """
    # 1. 识别数据集类型
    # 2. 加载数据文件
    # 3. 创建训练/测试分割（如需要）
    # 4. 生成 sample_submission
    # 5. 保存答案到 private
```

## 💡 使用示例

### 示例 1: 转换单个任务

```bash
python convert_scienceagent_to_mlebench.py --task-names 3k --auto-prepare
```

**输出**:
```
Converting 1 task(s)...
⚡ Auto-prepare mode enabled

============================================================
Converting Task: 3k -> sciencebench-01-3k
============================================================
Category: Biology
Type: Single-cell RNA-seq analysis
✓ Created competition directory
✓ Created config.yaml
✓ Created description.md
✓ Created grade.py (metric: accuracy)
✓ Created prepare.py
✓ Created leaderboard.csv

📦 Auto-preparing data for sciencebench-01-3k...
✅ Data prepared successfully!
```

### 示例 2: 批量转换生物学任务

```bash
python convert_scienceagent_to_mlebench.py \
  --task-names 3k BBBC002_cell-count biopsykit_imu clintox \
  --auto-prepare
```

### 示例 3: 转换所有任务

```bash
# 先预览
python convert_scienceagent_to_mlebench.py --all --dry-run

# 确认后执行
python convert_scienceagent_to_mlebench.py --all --auto-prepare
```

## 🏃 运行转换后的比赛

```bash
cd /home/aiops/liufan/projects/DeepModeling

# 运行单个任务
python main.py \
  --benchmark sciencebench \
  --competitions sciencebench-01-3k

# 运行多个任务
python main.py \
  --benchmark sciencebench \
  --competitions sciencebench-01-3k sciencebench-02-bbbc002-cell-count

# 指定数据目录
python main.py \
  --benchmark sciencebench \
  --data-dir /home/aiops/liufan/projects/ScienceAgent-bench/benchmark \
  --competitions sciencebench-01-3k
```

## 🎯 命令行参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--task-names` | 指定任务名称 | `--task-names 3k BurnScar` |
| `--all` | 转换所有任务 | `--all` |
| `--auto-prepare` | 自动准备数据 ⭐ | `--auto-prepare` |
| `--dry-run` | 预览转换（不创建文件） | `--dry-run` |
| `--list` | 列出所有可用任务 | `--list` |
| `--category` | 按类别过滤 | `--category biology` |

## 🔍 验证转换结果

```bash
# 检查比赛定义
ls /home/aiops/liufan/projects/DeepModeling/benchmarks/sciencebench/competitions/sciencebench-01-3k/

# 检查数据（如果使用了 --auto-prepare）
ls /home/aiops/liufan/projects/ScienceAgent-bench/benchmark/sciencebench-01-3k/public/
ls /home/aiops/liufan/projects/ScienceAgent-bench/benchmark/sciencebench-01-3k/private/
```

## 📈 任务统计

ScienceAgent-bench 共有 **102 个任务**，分布在以下领域：

- 🧬 **Biology & Medicine**: ~25 tasks
- 🌍 **Climate & Geoscience**: ~20 tasks
- 🧠 **Neuroscience**: ~15 tasks
- ⚗️ **Chemistry**: ~20 tasks
- 📊 **Other Scientific Domains**: ~22 tasks

## 🐛 故障排除

### 问题 1: 数据集路径找不到

**错误**: `Dataset not found: datasets/xxx`

**解决**:
```bash
# 确认 ScienceAgent-bench 数据已下载
ls /home/aiops/liufan/projects/ScienceAgent-bench/benchmark/datasets/
```

### 问题 2: 任务名称不匹配

**错误**: `Task not found: xxx`

**解决**:
```bash
# 列出所有可用任务
python convert_scienceagent_to_mlebench.py --list
```

### 问题 3: Auto-prepare 失败

**检查**:
- 原始数据文件是否存在
- prepare.py 逻辑是否正确
- 数据格式是否符合预期

**手动调试**:
```bash
cd /home/aiops/liufan/projects/ScienceAgent-bench/benchmark/sciencebench-01-xxx
python prepare.py  # 手动运行查看详细错误
```

## 💡 最佳实践

1. **分类别转换**: 先转换一个类别的任务，验证后再转换其他
2. **小批量测试**: 每次转换 3-5 个任务，便于调试
3. **使用 auto-prepare**: 避免手动准备数据
4. **验证结果**: 转换后运行一次比赛测试

## 📚 相关文档

- **方法论**: `/home/aiops/liufan/projects/DeepModeling/examples/anybench-to-deepmodelingbench/METHODOLOGY.md`
- **ScienceBench 文档**: `/home/aiops/liufan/projects/DeepModeling/benchmarks/sciencebench/README.md`
- **DABench 转换参考**: `/home/aiops/liufan/projects/data_science_agent_toolkit/examples/dabench_to_mlebench/`

## 🎉 完整工作流

```bash
# 1. 列出任务
python convert_scienceagent_to_mlebench.py --list --category biology

# 2. 转换任务
python convert_scienceagent_to_mlebench.py \
  --task-names 3k BBBC002_cell-count \
  --auto-prepare

# 3. 验证结果
ls /home/aiops/liufan/projects/DeepModeling/benchmarks/sciencebench/competitions/

# 4. 运行比赛
cd /home/aiops/liufan/projects/DeepModeling
python main.py \
  --benchmark sciencebench \
  --competitions sciencebench-01-3k

# 5. 查看结果
cat runs/benchmark_results/*/results.json
```

完成！🚀

## ⚠️ 注意事项

1. **数据位置**: ScienceAgent-bench 的数据保持在原位置，不移动到 DeepModeling/data
2. **文件完整性**: 部分 gold_programs 和 eval_programs 可能为空，需要手动实现
3. **评估逻辑**: rubric 文件需要转换为 Python 评分函数
4. **依赖包**: 某些任务可能需要特定的科学计算库（如 oggm, biopsykit）

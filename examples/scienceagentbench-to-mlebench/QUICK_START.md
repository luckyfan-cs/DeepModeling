# ScienceAgent-bench 转换快速开始

## 🚀 5分钟快速开始

### 步骤 1: 列出所有任务

```bash
cd /home/aiops/liufan/projects/DeepModeling/examples/scienceagentbench-to-mlebench
python convert_scienceagent_to_mlebench.py --list
```

**输出**: 显示 102 个任务，按领域分类

### 步骤 2: 转换一个简单任务

```bash
# 转换 Task 1 (Computational Chemistry - Clintox)
python convert_scienceagent_to_mlebench.py --instance-ids 1
```

**生成位置**: `/home/aiops/liufan/projects/DeepModeling/benchmarks/sciencebench/competitions/sciencebench-001-clintox-nn/`

### 步骤 3: 准备数据 ⭐

```bash
# 准备数据
python prepare_data.py --competitions sciencebench-001-clintox-nn
```

**数据位置**: `/home/aiops/liufan/projects/DeepModeling/data/competitions/sciencebench-001-clintox-nn/prepared/`

### 步骤 4: 查看生成的文件

```bash
ls /home/aiops/liufan/projects/DeepModeling/benchmarks/sciencebench/competitions/sciencebench-001-clintox-nn/
```

**应该看到**:
- `config.yaml` - 比赛配置
- `description.md` - 任务描述（路径已清理）
- `prepare.py` - 数据准备脚本
- `grade.py` - 评分函数
- `leaderboard.csv` - 排行榜
- `checksums.yaml` - 数据校验

### 步骤 4: 查看清理后的任务描述

```bash
head -20 /home/aiops/liufan/projects/DeepModeling/benchmarks/sciencebench/competitions/sciencebench-001-clintox-nn/description.md
```

**注意**: 原始的 `"pred_results/clintox_test_pred.csv"` 路径已被清理为通用描述

## 📊 批量转换示例

### 转换化学领域任务

```bash
# 先预览
python convert_scienceagent_to_mlebench.py --category "Chemistry" --dry-run

# 实际转换
python convert_scienceagent_to_mlebench.py --category "Chemistry"
```

### 转换生物信息学任务

```bash
python convert_scienceagent_to_mlebench.py --category "Bioinformatics"
```

### 转换前 10 个任务

```bash
python convert_scienceagent_to_mlebench.py --instance-ids 1 2 3 4 5 6 7 8 9 10
```

### 转换所有任务

```bash
# 强烈建议先 dry-run
python convert_scienceagent_to_mlebench.py --all --dry-run

# 确认后执行
python convert_scienceagent_to_mlebench.py --all
```

## 🔍 验证转换质量

### 检查路径清理

```bash
# 原始任务说明（包含具体路径）
python -c "
import pandas as pd
df = pd.read_csv('/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/ScienceAgentBench.csv')
print(df.iloc[0]['task_inst'])
"

# 清理后的描述（通用描述）
cat /home/aiops/liufan/projects/DeepModeling/benchmarks/sciencebench/competitions/sciencebench-001-clintox-nn/description.md | grep -A5 "Task Description"
```

### 检查文件完整性

```bash
# 检查所有生成的比赛
ls /home/aiops/liufan/projects/DeepModeling/benchmarks/sciencebench/competitions/

# 检查每个比赛的文件
for dir in /home/aiops/liufan/projects/DeepModeling/benchmarks/sciencebench/competitions/*/; do
    echo "Checking $dir"
    ls "$dir" | wc -l
done
```

## 📈 转换统计

### 任务分布

- **总任务数**: 102
- **Computational Chemistry**: 20 tasks
- **Geographical Information Science**: 27 tasks
- **Bioinformatics**: 27 tasks
- **Psychology and Cognitive Science**: 28 tasks

### 评估指标分布

转换脚本会自动推断评估指标：
- `accuracy`: 分类任务
- `rmse`: 回归任务
- `visual_similarity`: 可视化任务
- `exact_match`: 其他任务

查看生成的指标：
```bash
grep "name:" /home/aiops/liufan/projects/DeepModeling/benchmarks/sciencebench/competitions/*/config.yaml | sort | uniq -c
```

## 💡 常见用例

### 用例 1: 只转换可视化任务

```bash
# 可视化任务通常包含 "Data Visualization" 子类别
python -c "
import pandas as pd
df = pd.read_csv('/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/ScienceAgentBench.csv')
vis_tasks = df[df['subtask_categories'].str.contains('Visualization', na=False)]
print('Visualization task IDs:', vis_tasks['instance_id'].tolist())
"

# 然后转换这些任务
python convert_scienceagent_to_mlebench.py --instance-ids 4 6 7 8 9 10 ...
```

### 用例 2: 只转换机器学习任务

```bash
python -c "
import pandas as pd
df = pd.read_csv('/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/ScienceAgentBench.csv')
ml_tasks = df[df['subtask_categories'].str.contains('Machine Learning|Deep Learning', na=False)]
print('ML task IDs:', ml_tasks['instance_id'].tolist())
"
```

### 用例 3: 按 GitHub 源分组转换

```bash
python -c "
import pandas as pd
df = pd.read_csv('/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/ScienceAgentBench.csv')
print(df.groupby('github_name')['instance_id'].apply(list))
"
```

## 🎯 下一步

转换完成后，你可以：

1. **运行比赛**:
```bash
cd /home/aiops/liufan/projects/DeepModeling
python main.py --benchmark sciencebench --competitions sciencebench-001-clintox-nn
```

2. **批量运行多个任务**:
```bash
python main.py \
  --benchmark sciencebench \
  --competitions sciencebench-001-clintox-nn sciencebench-002-mat-feature-select
```

3. **准备数据** (如需要):
```bash
cd /home/aiops/liufan/projects/ScienceAgent-bench/benchmark
# 数据准备逻辑需要根据实际数据集调整
```

## 📚 相关文档

- **详细 README**: [README.md](README.md)
- **转换方法论**: [../../anybench-to-deepmodelingbench/METHODOLOGY.md](../../anybench-to-deepmodelingbench/METHODOLOGY.md)
- **ScienceBench 文档**: [../../benchmarks/sciencebench/README.md](../../benchmarks/sciencebench/README.md)

## ✨ 关键特性

- ✅ **自动路径清理**: task_inst 中的具体路径被清理
- ✅ **智能指标推断**: 根据任务类型自动选择评估指标
- ✅ **完整元数据保留**: 保留领域知识和数据预览
- ✅ **批量处理**: 支持转换所有 102 个任务
- ✅ **Dry-run 模式**: 先预览再执行

## 🎉 完成!

现在你已经成功将 ScienceAgent-bench 转换为 MLE-Bench 格式！

所有任务的路径描述都已经清理，可以在 DeepModeling 框架中运行了。

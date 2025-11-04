# ScienceAgent-bench 转换速查表

## 🚀 常用命令

```bash
# 进入脚本目录
cd /home/aiops/liufan/projects/DeepModeling/examples/scienceagentbench-to-mlebench
```

### 列出任务
```bash
# 列出所有任务
python convert_scienceagent_to_mlebench.py --list

# 按领域过滤
python convert_scienceagent_to_mlebench.py --list --category "Chemistry"
```

### 转换任务
```bash
# 单个任务
python convert_scienceagent_to_mlebench.py --instance-ids 1

# 多个任务
python convert_scienceagent_to_mlebench.py --instance-ids 1 2 3 4 5

# 按领域
python convert_scienceagent_to_mlebench.py --category "Chemistry"

# 所有任务（预览）
python convert_scienceagent_to_mlebench.py --all --dry-run

# 所有任务（执行）
python convert_scienceagent_to_mlebench.py --all
```

### 准备数据
```bash
# 单个比赛
python prepare_data.py --competitions sciencebench-001-clintox-nn

# 多个比赛
python prepare_data.py --competitions sciencebench-001-clintox-nn sciencebench-002-xxx

# 所有比赛
python prepare_data.py --all

# 查看准备状态
python prepare_data.py --list
```

### 验证转换
```bash
# 检查生成的任务数
ls /home/aiops/liufan/projects/DeepModeling/benchmarks/sciencebench/competitions/ | wc -l

# 查看任务文件
ls /home/aiops/liufan/projects/DeepModeling/benchmarks/sciencebench/competitions/sciencebench-001-clintox-nn/

# 验证路径清理
cat /home/aiops/liufan/projects/DeepModeling/benchmarks/sciencebench/competitions/sciencebench-001-clintox-nn/description.md | grep -A5 "Task Description"
```

## 📂 关键路径

| 项目 | 路径 |
|------|------|
| **转换脚本** | `/home/aiops/liufan/projects/DeepModeling/examples/scienceagentbench-to-mlebench/` |
| **比赛定义** | `/home/aiops/liufan/projects/DeepModeling/benchmarks/sciencebench/competitions/` |
| **准备后数据** | `/home/aiops/liufan/projects/DeepModeling/data/competitions/` |
| **源数据** | `/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/datasets/` |
| **元数据CSV** | `/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/ScienceAgentBench.csv` |

## 📊 任务分布

| 领域 | 任务数 | Instance ID 范围 |
|------|--------|-----------------|
| Computational Chemistry | 20 | 1, 2, 3, 9, 16, 17, ... |
| Geographical Information Science | 27 | 4, 10, 14, 21, 23, ... |
| Bioinformatics | 27 | 5, 6, 7, 8, 11, 12, ... |
| Psychology and Cognitive Science | 28 | 24, 25, 29, 34, 35, ... |

## 🎯 核心特性

### ✅ 路径清理
- **原始**: `Save to "pred_results/clintox_test_pred.csv"`
- **清理后**: `Save the results to the output file`

### ✅ 评估指标
- **可视化任务** → `visual_similarity`
- **分类任务** → `accuracy`
- **回归任务** → `rmse`
- **其他任务** → `exact_match`

### ✅ 生成的文件（每个任务）
1. `config.yaml` - 比赛配置
2. `description.md` - 任务描述（路径已清理）
3. `grade.py` - 评分函数
4. `prepare.py` - 数据准备
5. `leaderboard.csv` - 排行榜
6. `checksums.yaml` - 数据校验

## 🔍 常见查询

### 查找特定类型的任务
```bash
# 可视化任务
python -c "
import pandas as pd
df = pd.read_csv('/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/ScienceAgentBench.csv')
vis = df[df['subtask_categories'].str.contains('Visualization', na=False)]
print('Visualization tasks:', vis['instance_id'].tolist())
"

# 深度学习任务
python -c "
import pandas as pd
df = pd.read_csv('/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/ScienceAgentBench.csv')
dl = df[df['subtask_categories'].str.contains('Deep Learning', na=False)]
print('Deep Learning tasks:', dl['instance_id'].tolist())
"
```

### 检查转换质量
```bash
# 检查文件完整性
for dir in /home/aiops/liufan/projects/DeepModeling/benchmarks/sciencebench/competitions/*/; do
    count=$(ls "$dir" | wc -l)
    if [ $count -ne 6 ]; then
        echo "⚠ $(basename $dir): $count files (expected 6)"
    fi
done

# 检查评估指标分布
grep "name:" /home/aiops/liufan/projects/DeepModeling/benchmarks/sciencebench/competitions/*/config.yaml | awk '{print $2}' | sort | uniq -c

# 验证路径是否已清理
cat /home/aiops/liufan/projects/DeepModeling/benchmarks/sciencebench/competitions/*/description.md | grep -i "pred_results" | wc -l
# 应该输出 0
```

## 📚 文档快速链接

| 文档 | 用途 |
|------|------|
| [METHODOLOGY.md](../anybench-to-deepmodelingbench/METHODOLOGY.md) | 通用转换方法论 |
| [README.md](README.md) | 详细使用文档 |
| [QUICK_START.md](QUICK_START.md) | 快速开始指南 |
| [CONVERSION_SUMMARY.md](CONVERSION_SUMMARY.md) | 转换总结 |
| [PROJECT_COMPLETE.md](PROJECT_COMPLETE.md) | 项目完成报告 |

## 💡 快速提示

### 转换前
1. 确保 ScienceAgentBench.csv 存在
2. 使用 `--list` 预览任务
3. 使用 `--dry-run` 测试转换逻辑

### 转换中
1. 从单个任务开始测试
2. 逐步增加任务数量
3. 检查生成的文件

### 转换后
1. 验证文件完整性
2. 检查路径清理效果
3. 查看评估指标分布
4. 测试运行比赛

## 🐛 常见问题

### Q: 路径没有被清理？
**A**: 检查正则表达式是否匹配你的路径格式

### Q: 评估指标不对？
**A**: 手动编辑 config.yaml 中的 `grader.name`

### Q: prepare.py 失败？
**A**: 检查原始数据路径是否正确

### Q: 转换失败？
**A**: 查看错误信息，检查 CSV 文件格式

## 🎉 完成

现在你可以开始批量转换所有 102 个任务了！

```bash
python convert_scienceagent_to_mlebench.py --all
```

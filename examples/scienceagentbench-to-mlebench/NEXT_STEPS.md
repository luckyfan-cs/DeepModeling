# 🚀 下一步行动指南

## ✅ 已完成

**Clintox 任务 (sciencebench-001-clintox-nn)** 已完全修复：
- ✅ 使用 gold_results 作为数据来源
- ✅ test.csv 和 sample_submission.csv 格式一致
- ✅ 完整测试集在 private/
- ✅ ROC-AUC 评分逻辑正确
- ✅ 所有验证通过

## 🎯 立即可做的事

### 1. 测试 Clintox 任务

```bash
cd /home/aiops/liufan/projects/DeepModeling

# 运行 Clintox 任务测试
python main.py \
  --benchmark sciencebench \
  --data-dir data/competitions \
  --competitions sciencebench-001-clintox-nn \
  --max-steps 10
```

### 2. 检查运行结果

```bash
# 查看结果
cat runs/benchmark_results/*/results.json

# 查看日志
tail -100 runs/benchmark_results/*/agent.log
```

## 📋 后续任务

### Phase 1: 完善转换脚本（推荐）

**目标**: 将 Clintox 的修复逻辑应用到所有任务

**步骤**:

1. **更新主转换脚本**
   ```bash
   cd /home/aiops/liufan/projects/DeepModeling/examples/scienceagentbench-to-mlebench

   # 编辑 convert_scienceagent_to_mlebench.py
   # 或创建新版本 convert_scienceagent_to_mlebench_v3.py
   ```

2. **关键改进点**:
   - ✅ 自动查找 gold_results 文件
   - ✅ 分析 eval_programs 提取评分逻辑
   - ✅ 生成格式一致的 test.csv 和 sample_submission.csv
   - ✅ 将完整测试集放在 private/

3. **参考已完成的修复**:
   - `fix_clintox_v2.py` - 修复逻辑
   - `PROBLEM_ANALYSIS.md` - 问题分析
   - `FINAL_FIX_SUMMARY.md` - 完整方案

### Phase 2: 分析不同任务类型

**ScienceAgent-bench 包含多种任务类型**:

1. **CSV 输出任务** (如 Clintox)
   - 数据格式: CSV
   - 评分方式: ROC-AUC, RMSE, Accuracy 等
   - 示例: clintox, mat_diffusion, compound_elastic 等

2. **图像输出任务**
   - 数据格式: PNG, JPG
   - 评分方式: 图像相似度 (SSIM, 哈希距离等)
   - 示例: plot_temperature, glacier_area, elk_analysis 等

3. **JSON 输出任务**
   - 数据格式: JSON
   - 评分方式: 结构匹配、数值比较
   - 示例: 部分特征工程任务

**建议**:
```bash
# 1. 统计任务类型
cd /home/aiops/liufan/projects/ScienceAgent-bench/benchmark

# 统计 CSV 任务
ls eval_programs/gold_results/*.csv | wc -l

# 统计图像任务
ls eval_programs/gold_results/*.png | wc -l

# 统计 JSON 任务
ls eval_programs/gold_results/*.json | wc -l
```

### Phase 3: 批量转换

**按类型逐步转换**:

1. **先转换 CSV 类任务**（最简单）
   ```bash
   # 找到所有 CSV gold_results
   ls /home/aiops/liufan/projects/ScienceAgent-bench/benchmark/eval_programs/gold_results/*.csv

   # 转换这些任务
   # 例如: instance_id 1, 2, 3, ...
   ```

2. **再转换图像类任务**
   ```bash
   # 图像任务需要特殊处理
   # 参考图像在 private/
   # 评分需要图像比较逻辑
   ```

3. **最后转换 JSON 类任务**
   ```bash
   # JSON 任务格式多样
   # 需要具体分析每个任务
   ```

### Phase 4: 验证和测试

**对于每个转换的任务**:
1. 验证数据格式
2. 验证文件完整性
3. 运行测试
4. 检查评分逻辑

## 💡 快速参考

### 当前正确的数据结构模板

```
data/competitions/{competition-id}/prepared/
├── public/
│   ├── train.csv              # 训练数据（完整）
│   ├── test.csv               # 测试特征（标签为空）
│   └── sample_submission.csv  # 提交模板（格式与 test.csv 一致）
└── private/
    └── test.csv               # 测试集答案（从 gold_results 复制）
```

### 正确的 prepare.py 模板

```python
def prepare(raw: Path, public: Path, private: Path):
    # 1. 找到 gold_results
    gold_path = Path(".../eval_programs/gold_results/xxx_gold.csv")
    gold = pd.read_csv(gold_path)

    # 2. 训练数据
    train = pd.read_csv(raw / "train.csv")
    train.to_csv(public / "train.csv", index=False)

    # 3. 测试数据（标签为空，格式与 gold 一致）
    test_public = gold.copy()
    for col in label_columns:
        test_public[col] = ''  # 或 NaN
    test_public.to_csv(public / "test.csv", index=False)

    # 4. Sample submission（格式与 test 一致）
    sample = gold.copy()
    for col in label_columns:
        sample[col] = 0  # 默认值
    sample.to_csv(public / "sample_submission.csv", index=False)

    # 5. Private（完整的 gold）
    gold.to_csv(private / "test.csv", index=False)
```

### 正确的 config.yaml 模板

```yaml
dataset:
  answers: {competition-id}/prepared/private/test.csv
  sample_submission: {competition-id}/prepared/public/sample_submission.csv

grader:
  name: {metric}  # roc_auc, rmse, accuracy, etc.
  grade_fn: mlebench.benchmarks.sciencebench.competitions.{competition-id}.grade:grade
```

## 📚 参考文档

### 核心文档
1. **METHODOLOGY.md** - 通用转换方法论
2. **PROBLEM_ANALYSIS.md** - 问题根本原因分析
3. **FINAL_FIX_SUMMARY.md** - Clintox 完整修复方案

### 脚本
1. **fix_clintox_v2.py** - Clintox 修复脚本（可作为模板）
2. **prepare_data.py** - 数据准备脚本
3. **convert_scienceagent_to_mlebench.py** - 主转换脚本（需要更新）

## 🎯 推荐的工作顺序

1. ✅ **测试 Clintox** - 验证修复是否完全正确
2. **更新转换脚本** - 应用 Clintox 的修复逻辑
3. **转换 2-3 个 CSV 任务** - 测试批量转换
4. **验证这些任务** - 确保逻辑正确
5. **批量转换所有 CSV 任务** - ~30-40 个
6. **处理图像任务** - ~20-30 个
7. **处理其他类型任务** - 剩余任务

## ⚠️ 注意事项

1. **数据完整性**: 确保每个 gold_results 文件都存在
2. **格式一致性**: test.csv 和 sample_submission.csv 必须格式一致
3. **评分逻辑**: 从 eval_programs 中提取正确的评分方式
4. **阈值**: 某些任务有性能阈值（如 Clintox 的 0.77）

---

**当前状态**: ✅ Clintox 任务已完全修复
**下一步**: 测试 Clintox，然后批量应用修复逻辑到其他任务

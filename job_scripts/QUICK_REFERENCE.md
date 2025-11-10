# Quick Reference - 测试脚本快速参考

## 🎯 推荐使用场景

| 场景 | 推荐脚本 | 预计时间 |
|------|---------|---------|
| **快速验证系统** | `test_mlebench_individual.sh 4` | 短 (~分钟级) |
| **功能测试** | `test_mlebench_selected.sh` | 中等 (~小时级) |
| **采样评估** | `run_all_sample_tests.sh` | 长 (~数小时) |
| **单任务调试** | `test_mlebench_individual.sh <N>` | 短-中等 |

## 📝 常用命令

### 1. 最常用：运行所有采样测试
```bash
cd /home/aiops/liufan/projects/DeepModeling
./job_scripts/run_all_sample_tests.sh
```
**包含**: 243 个任务，覆盖 4 个 benchmark

---

### 2. 快速测试：MLEBench 精选任务
```bash
# 运行所有5个精选任务
./job_scripts/test_mlebench_selected.sh

# 或单独运行某个任务
./job_scripts/test_mlebench_individual.sh 4  # 出租车票价预测（最快）
```

---

### 3. 单个 Benchmark 测试
```bash
# Engineering (30 任务)
./job_scripts/test_engineeringbench_sample.sh

# Math Modeling (145 任务) - 最大数据集
./job_scripts/test_mathmodelingbench_sample.sh

# Science (35 任务)
./job_scripts/test_sciencebench_sample.sh

# DA-Bench (33 任务)
./job_scripts/test_mlebench_dabench_sample.sh
```

---

### 4. 验证任务
```bash
# 验证采样任务
./job_scripts/verify_sample_tasks.sh

# 验证精选任务
./job_scripts/verify_mlebench_selected.sh
```

## 🏷️ MLEBench 精选任务编号

```bash
./job_scripts/test_mlebench_individual.sh <编号>
```

| 编号 | 任务名称 | 类型 | 难度 |
|-----|---------|------|------|
| 1 | aptos2019-blindness-detection | 医疗影像 | 中 |
| 2 | plant-pathology-2020-fgvc7 | 计算机视觉 | 中 |
| 3 | us-patent-phrase-to-phrase-matching | NLP | 中-高 |
| 4 | new-york-city-taxi-fare-prediction | 回归 | 低-中 |
| 5 | tabular-playground-series-dec-2021 | 表格数据 | 低-中 |

**推荐首次测试**: 编号 4 或 5（运行最快）

## 📊 数据量总览

```
┌─────────────────────┬───────────┬──────────┬─────────┐
│ Benchmark           │ 总任务数  │ 采样数   │ 采样率  │
├─────────────────────┼───────────┼──────────┼─────────┤
│ Engineering         │    100    │    30    │   30%   │
│ Math Modeling       │   1294    │   145    │   11%   │
│ Science             │    103    │    35    │   34%   │
│ MLE (DA-Bench)      │    258    │    33    │   13%   │
│ MLE (精选)          │      5    │     5    │  100%   │
├─────────────────────┼───────────┼──────────┼─────────┤
│ 总计                │   1760    │   248    │   14%   │
└─────────────────────┴───────────┴──────────┴─────────┘
```

## 🔍 故障排查

### 问题：任务未找到
```bash
# 解决方案：运行验证脚本
./job_scripts/verify_sample_tasks.sh
```

### 问题：权限被拒绝
```bash
# 解决方案：添加执行权限
chmod +x job_scripts/*.sh
```

### 问题：数据目录不存在
```bash
# 解决方案：检查数据目录
ls ./data/engineering-bench/competitions
ls ./benchmarks/mlebench/competitions
```

## 📍 结果位置

```
runs/benchmark_results/
└── scientific_on_<benchmark>/
    ├── <task_id>/
    │   ├── metadata.json
    │   ├── logs/
    │   └── outputs/
    └── results.csv
```

## 🎓 使用建议

1. **首次使用**: 先运行 `verify_*.sh` 验证任务
2. **快速测试**: 使用 `test_mlebench_individual.sh 4`
3. **深度测试**: 使用 `run_all_sample_tests.sh`
4. **调试单任务**: 从脚本中复制命令手动运行

## 📚 详细文档

- 📄 [README_TEST_SCRIPTS.md](README_TEST_SCRIPTS.md) - 完整脚本文档
- 📄 [SAMPLE_TESTS_README.md](SAMPLE_TESTS_README.md) - 采样测试详情
- 📄 [MLEBENCH_SELECTED_README.md](MLEBENCH_SELECTED_README.md) - 精选任务详情

## ⚡ 一键命令合集

```bash
# 进入项目目录
cd /home/aiops/liufan/projects/DeepModeling

# 验证所有任务
./job_scripts/verify_sample_tasks.sh && ./job_scripts/verify_mlebench_selected.sh

# 快速测试（5个任务）
./job_scripts/test_mlebench_selected.sh

# 完整采样测试（243个任务）
./job_scripts/run_all_sample_tests.sh

# 查看结果
ls -lh runs/benchmark_results/
```

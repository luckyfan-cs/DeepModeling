# Benchmark Sample Test Scripts

这些脚本用于对四个 benchmark 进行代表性采样测试，每个脚本会批量运行多个任务。

## 快速总览

| Benchmark | 总任务数 | 采样数量 | 采样率 | 脚本名称 |
|-----------|---------|---------|--------|----------|
| Engineering | 100 | 30 | 30% | test_engineeringbench_sample.sh |
| Math Modeling | 1294 | 145 | 11% | test_mathmodelingbench_sample.sh |
| Science | 103 | 35 | 34% | test_sciencebench_sample.sh |
| MLE (DA-Bench) | 258 | 33 | 13% | test_mlebench_dabench_sample.sh |
| **总计** | **1755** | **243** | **14%** | - |

## 脚本概览

### 1. test_engineeringbench_sample.sh
- **总任务数**: 100 个 (industry-0 到 industry-99)
- **采样数量**: 30 个任务 (30% 采样率)
- **采样策略**: 均匀分布，每隔 3 个任务采样一次
- **任务列表**: industry-0, 3, 6, 9, ..., 84, 87 (共 30 个)

### 2. test_mathmodelingbench_sample.sh
- **总任务数**: 1294 个
  - bwor: 82 个任务 (0-81)
  - mamo-easy: 652 个任务 (0-651, 数量最多)
  - mamo-complex: 211 个任务 (0-210)
  - mamo-ode: 346 个任务 (0-345)
- **采样数量**: 145 个任务 (~11% 采样率)
- **采样策略**: 覆盖所有任务类型，按比例均匀采样
  - bwor: 17 个 (~21%，每隔 5 个采样)
  - mamo-easy: 66 个 (~10%，每隔 10 个采样)
  - mamo-complex: 27 个 (~13%，每隔 8 个采样)
  - mamo-ode: 35 个 (~10%，每隔 10 个采样)

### 3. test_sciencebench_sample.sh
- **总任务数**: 103 个 (sciencebench-001 到 sciencebench-102)
- **采样数量**: 35 个任务 (~34% 采样率)
- **采样策略**: 覆盖不同科学领域，每隔 3 个任务采样一次
- **领域覆盖**:
  - 药物/化学: clintox-nn, drug-property-model, compound-filter 等
  - 材料科学: elk-new, charge-density-difference, phonon-dos 等
  - 生物医学: single-cell-analysis, eeg/ecg/eog-processing, hrv-analyze 等
  - 地球科学: ocean-profiles, flowline, mountainlion 等
  - 数据分析: violin, dendrogram, spatial, pca 等

### 4. test_mlebench_dabench_sample.sh
- **总任务数**: 258 个 (dabench-0 到 dabench-760，非连续编号)
- **采样数量**: 33 个任务 (~13% 采样率)
- **采样策略**: 每隔 8 个任务采样一次
- **任务类型覆盖**:
  - 相关性分析: correlation-coefficient, correlation-analysis 等
  - 离群值检测: identify-outliers, outlier-detection 等
  - 统计分析: mean-standard-deviation, distribution-analysis 等
  - 特征工程: feature-engineering, generate-feature 等
  - 数据预处理: data-preprocessing, comprehensive-data 等
  - 机器学习: machine-learning-techniques, develop-machine-learning 等

## 使用方法

### 运行所有测试（推荐）
一次性运行所有 243 个采样任务：
```bash
cd /home/aiops/liufan/projects/DeepModeling
./job_scripts/run_all_sample_tests.sh
```

### 运行单个测试脚本
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

## MLEBench 精选任务测试

除了上述采样测试外，我们还提供了针对 MLEBench 的精选任务测试脚本：

### test_mlebench_selected.sh
- **任务数量**: 5 个精选的 Kaggle 竞赛任务
- **任务列表**:
  1. aptos2019-blindness-detection (医疗影像)
  2. plant-pathology-2020-fgvc7 (计算机视觉)
  3. us-patent-phrase-to-phrase-matching (NLP)
  4. new-york-city-taxi-fare-prediction (回归预测)
  5. tabular-playground-series-dec-2021 (表格数据)

### 运行 MLEBench 精选任务
```bash
# 一次性运行所有5个任务
./job_scripts/test_mlebench_selected.sh

# 单独运行某个任务（传入任务编号 1-5）
./job_scripts/test_mlebench_individual.sh 1  # 运行糖尿病视网膜病变检测
./job_scripts/test_mlebench_individual.sh 3  # 运行专利短语匹配
```

详细说明请参考 [MLEBENCH_SELECTED_README.md](MLEBENCH_SELECTED_README.md)

## 注意事项

1. 所有脚本都使用批量模式，一次性运行多个任务
2. 采样策略考虑了数据量和任务类型的代表性
3. 运行前确保数据目录存在且配置正确
4. 结果将保存在 `runs/benchmark_results/` 目录下
5. MLEBench 精选任务可能需要较长运行时间，建议使用 GPU

## 目录结构

```
/home/aiops/liufan/projects/DeepModeling/
├── job_scripts/
│   ├── test_engineeringbench_sample.sh
│   ├── test_mathmodelingbench_sample.sh
│   └── test_sciencebench_sample.sh
├── data/
│   ├── engineering-bench/competitions/
│   ├── mathmodeling-bench/
│   └── science-bench/competitions/
└── main.py
```

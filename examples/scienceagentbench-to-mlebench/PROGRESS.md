# ScienceBench 转换进度追踪

## 已完成任务 (3/102)

### ✅ 任务 1: sciencebench-001-clintox-nn
- **类型**: CSV输出（分类任务）
- **领域**: Computational Chemistry
- **评分**: ROC-AUC (阈值 >= 0.77)
- **状态**: 完成
- **位置**: 
  - 注册端: `/home/aiops/liufan/projects/DeepModeling/benchmarks/sciencebench/competitions/sciencebench-001-clintox-nn/`
  - 数据端: `/home/aiops/liufan/projects/ScienceAgent-bench/competitions/sciencebench-001-clintox-nn/`

### ✅ 任务 36: sciencebench-036-eeg-processing-vis1
- **类型**: PNG图像输出（可视化任务）
- **领域**: Psychology and Cognitive Science
- **评分**: 图像相似度 (阈值 >= 60/100)
- **状态**: 完成
- **位置**:
  - 注册端: `/home/aiops/liufan/projects/DeepModeling/benchmarks/sciencebench/competitions/sciencebench-036-eeg-processing-vis1/`
  - 数据端: `/home/aiops/liufan/projects/ScienceAgent-bench/competitions/sciencebench-036-eeg-processing-vis1/`

### ✅ 任务 38: sciencebench-038-fingerprint-similarity-vis
- **类型**: PNG图像输出（可视化任务）
- **领域**: Computational Chemistry
- **评分**: 图像相似度 (阈值 >= 60/100)
- **状态**: 完成
- **位置**:
  - 注册端: `/home/aiops/liufan/projects/DeepModeling/benchmarks/sciencebench/competitions/sciencebench-038-fingerprint-similarity-vis/`
  - 数据端: `/home/aiops/liufan/projects/ScienceAgent-bench/competitions/sciencebench-038-fingerprint-similarity-vis/`

## 处理模式

✅ **单个任务处理** - 每次处理一个任务，确保质量  
❌ **批量处理** - 不使用批量转换脚本

## 任务分类

根据ScienceAgent-bench的102个任务，按输出类型分类：

### 1. CSV输出任务 (~40个)
- 示例: clintox_nn (已完成 ✅)
- 评分: 数值指标 (准确率, ROC-AUC, RMSE等)

### 2. 图像输出任务 (~30个)  
- 示例: eeg_processing_vis1 (已完成 ✅), fingerprint_similarity_vis (已完成 ✅)
- 评分: 图像相似度

### 3. JSON输出任务 (~20个)
- 评分: 结构化数据比较

### 4. 其他格式 (~12个)
- 文本、数组等

## 已完成任务汇总

| ID | 任务名 | 类型 | 领域 | 状态 |
|----|--------|------|------|------|
| 1 | clintox-nn | CSV | Chemistry | ✅ |
| 36 | eeg-processing-vis1 | 图像 | Psychology | ✅ |
| 38 | fingerprint-similarity-vis | 图像 | Chemistry | ✅ |

## 下一步

等待下一个任务指派。

---

**最后更新**: 2025-11-06 07:18  
**完成进度**: 3/102 (2.94%)  
**注册端根目录**: `/home/aiops/liufan/projects/DeepModeling/benchmarks/sciencebench/competitions/`  
**数据端根目录**: `/home/aiops/liufan/projects/ScienceAgent-bench/competitions/`

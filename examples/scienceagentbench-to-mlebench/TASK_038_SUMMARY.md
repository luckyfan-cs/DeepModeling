# sciencebench-038-fingerprint-similarity-vis - 完成总结

## ✅ 已完成

### 1. 注册端文件
**位置**: `/home/aiops/liufan/projects/DeepModeling/benchmarks/sciencebench/competitions/sciencebench-038-fingerprint-similarity-vis/`

- ✅ config.yaml (734B)
- ✅ description.md (1.4KB)
- ✅ grade.py (2.9KB)
- ✅ prepare.py (2.3KB)
- ✅ leaderboard.csv
- ✅ checksums.yaml

### 2. 数据端准备
**位置**: `/home/aiops/liufan/projects/ScienceAgent-bench/competitions/sciencebench-038-fingerprint-similarity-vis/`

```
prepared/
├── public/              # Agent可见数据
│   ├── top.pdb                    # 蛋白结构拓扑 (501KB)
│   ├── traj.xtc                   # 轨迹文件 (4.7MB)
│   └── sample_submission.png      # 占位符提交
└── private/            # 仅用于评分
    └── ligand_similarity_gold.png  # 金标准图像 (25KB)
```

### 3. 验证结果
- ✅ 数据准备成功
- ✅ 在ScienceBenchmark框架中成功加载
- ✅ 数据准备状态：prepared=True

## 任务特点

**类型**: 图像输出（可视化任务）  
**领域**: Computational Chemistry  
**输入**: 分子动力学轨迹数据（PDB + XTC）  
**输出**: PNG图像（Tanimoto相似度可视化）  
**评分**: 图像相似度（阈值≥60）

### 核心技术

- **ProLIF**: 蛋白-配体相互作用指纹分析
- **MDAnalysis**: 分子动力学轨迹分析
- **Tanimoto相似度**: 指纹相似度度量
- 分析前10帧的配体-蛋白相互作用

## 使用示例

```bash
cd /home/aiops/liufan/projects/DeepModeling

python main.py \
  --workflow scientific \
  --benchmark sciencebench \
  --data-dir /home/aiops/liufan/projects/ScienceAgent-bench/competitions \
  --task sciencebench-038-fingerprint-similarity-vis \
  --llm-model deepseek-chat
```

## 与其他任务的对比

| 特性 | Clintox (任务1) | EEG (任务36) | Fingerprint (任务38) |
|------|----------------|--------------|---------------------|
| 输出类型 | CSV | PNG图像 | PNG图像 |
| 输入数据 | CSV (化合物) | CSV (脑电) | PDB+XTC (轨迹) |
| 评分方式 | ROC-AUC | 图像相似度 | 图像相似度 |
| 领域 | 化学 | 心理学 | 化学 |
| 数据大小 | ~200KB | ~900KB | ~5.2MB |

## 状态

| 项目 | 状态 |
|------|------|
| 注册端创建 | ✅ |
| 数据端准备 | ✅ |
| 框架集成 | ✅ |
| Agent测试 | ⏳ |

---

**完成时间**: 2025-11-06 07:17  
**Instance ID**: 38  
**任务域**: Computational Chemistry  
**进度**: 3/102 (2.94%)

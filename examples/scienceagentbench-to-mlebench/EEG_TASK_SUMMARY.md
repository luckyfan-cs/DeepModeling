# EEG Processing Task (sciencebench-036) - 完成总结

## ✅ 已完成

### 1. 注册端文件创建
**位置**: `/home/aiops/liufan/projects/DeepModeling/benchmarks/sciencebench/competitions/sciencebench-036-eeg-processing-vis1/`

创建的文件：
- ✅ `config.yaml` - 竞赛配置（700字节）
- ✅ `description.md` - 任务描述（2.3KB）
- ✅ `grade.py` - 评分函数，使用图像相似度（4.6KB）
- ✅ `prepare.py` - 数据准备脚本（2.3KB）
- ✅ `leaderboard.csv` - 排行榜占位符
- ✅ `checksums.yaml` - 校验和文件
- ✅ `README.md` - 任务说明文档

### 2. 数据端准备
**位置**: `/home/aiops/liufan/projects/ScienceAgent-bench/competitions/sciencebench-036-eeg-processing-vis1/`

数据结构：
```
prepared/
├── public/              # Agent可见数据
│   ├── eeg_muse_example.csv          # EEG数据 (889KB, ~23k行)
│   └── sample_submission.png          # 占位符提交
└── private/            # 仅用于评分
    └── biopsykit_eeg_processing_vis1_gold.png  # 金标准图像 (114KB)
```

### 3. 评分函数测试
- ✅ 测试grading函数（相同图像对比）
- ✅ 返回分数：1.0（100%相似度）
- ✅ 评分逻辑：PSNR + 相关系数，阈值>=60

### 4. 框架集成验证
- ✅ 在ScienceBenchmark中成功加载
- ✅ 数据准备状态：prepared=True
- ✅ 元数据正确关联（instance_id=36）

## 任务特点

### 输入
- **数据类型**: CSV文件
- **数据大小**: 889KB
- **特征**: 时间戳 + 5个EEG通道（TP9, AF7, AF8, TP10, Right AUX）
- **数据点**: ~23,000个测量值

### 输出
- **格式**: PNG图像
- **尺寸**: ~1000x500像素
- **内容**: 4个频段（Delta, Theta, Alpha, Beta）的20点移动平均线图

### 评估方法
- **类型**: 图像相似度比较
- **指标**: 
  - PSNR (Peak Signal-to-Noise Ratio)
  - 相关系数 (Correlation Coefficient)
- **阈值**: 综合得分 >= 60/100
- **返回**: 二元分数（1.0通过，0.0失败）

## 关键差异：图像任务 vs CSV任务

| 特性 | CSV任务（如Clintox） | 图像任务（EEG） |
|------|---------------------|----------------|
| 输出格式 | CSV文件 | PNG图像 |
| 评分方式 | ROC-AUC等数值指标 | 图像相似度 |
| sample_submission | CSV格式数据 | 占位符PNG |
| 答案文件 | private/test.csv | private/*.png |
| grader实现 | 数值比较 | 图像比较 |

## 使用示例

```bash
cd /home/aiops/liufan/projects/DeepModeling

# 运行EEG处理任务
python main.py \
  --workflow scientific \
  --benchmark sciencebench \
  --data-dir /home/aiops/liufan/projects/ScienceAgent-bench/competitions \
  --task sciencebench-036-eeg-processing-vis1 \
  --llm-model deepseek-chat
```

## 技术实现细节

### grade.py核心函数

```python
def calculate_image_similarity(pred_image, gold_image):
    # 1. 归一化图像 (0-1范围)
    # 2. 计算MSE和PSNR
    # 3. 计算像素相关系数
    # 4. 加权平均: 0.6*PSNR + 0.4*相关性
    # 5. 返回0-100的分数
    
def grade(submission, answers):
    # 加载图像 → 计算相似度 → 阈值判断
    # 返回: 1.0 (通过) 或 0.0 (失败)
```

### prepare.py流程

1. 从ScienceAgent-bench复制EEG数据到public/
2. 生成sample_submission.png占位符
3. 复制gold result到private/
4. 验证所有文件存在

## 依赖库

Agent执行环境需要：
- `numpy` - 数组处理
- `pandas` - CSV读取
- `Pillow (PIL)` - 图像处理
- `matplotlib` / `seaborn` - 绘图
- `BioPsyKit` (可选) - EEG信号处理专用库

## 状态

| 项目 | 状态 |
|------|------|
| 注册端创建 | ✅ 完成 |
| 数据端准备 | ✅ 完成 |
| 评分函数测试 | ✅ 通过 |
| 框架集成 | ✅ 验证 |
| Agent测试运行 | ⏳ 待进行 |

## 下一步

建议下一步处理的任务类型：
1. **CSV输出任务** - 类似Clintox的数值预测任务
2. **更多图像任务** - 其他可视化任务
3. **JSON输出任务** - 结构化数据输出

---

**完成时间**: 2025-11-06 07:06  
**Instance ID**: 36  
**任务域**: Psychology and Cognitive Science  
**难度**: 中等

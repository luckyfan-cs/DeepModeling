# MLEBench Selected Tasks Test Script

本脚本用于运行 5 个精选的 MLEBench 竞赛任务，涵盖不同的机器学习领域。

## 任务列表

| 任务名称 | 描述 | 类型 |
|---------|------|------|
| aptos2019-blindness-detection | APTOS 2019 糖尿病视网膜病变检测 | 计算机视觉 - 图像分类 |
| plant-pathology-2020-fgvc7 | 植物病理学 2020 - 叶片病害分类 | 计算机视觉 - 多类别分类 |
| us-patent-phrase-to-phrase-matching | 美国专利短语匹配 | NLP - 语义相似度 |
| new-york-city-taxi-fare-prediction | 纽约市出租车票价预测 | 回归 - 时空预测 |
| tabular-playground-series-dec-2021 | 表格数据游乐场系列 (2021年12月) | 表格数据 - 分类/回归 |

## 任务详情

### 1. aptos2019-blindness-detection
- **领域**: 医疗影像
- **任务**: 糖尿病视网膜病变严重程度分类 (5个等级)
- **数据类型**: 视网膜图像
- **评估指标**: 通常为 Quadratic Weighted Kappa

### 2. plant-pathology-2020-fgvc7
- **领域**: 农业 AI
- **任务**: 识别苹果叶片的健康状况和疾病类型
- **数据类型**: 植物叶片图像
- **评估指标**: 多标签分类准确度

### 3. us-patent-phrase-to-phrase-matching
- **领域**: 自然语言处理
- **任务**: 判断专利文档中两个短语的语义相似度
- **数据类型**: 文本对
- **评估指标**: Pearson 相关系数

### 4. new-york-city-taxi-fare-prediction
- **领域**: 时空数据分析
- **任务**: 根据上车/下车地点、时间等预测出租车费用
- **数据类型**: 表格数据 (地理位置、时间戳)
- **评估指标**: RMSE (Root Mean Squared Error)

### 5. tabular-playground-series-dec-2021
- **领域**: 表格数据竞赛
- **任务**: Kaggle Playground 系列合成数据集挑战
- **数据类型**: 表格数据
- **评估指标**: 根据具体任务而定

## 使用方法

### 运行测试脚本
```bash
cd /home/aiops/liufan/projects/DeepModeling
./job_scripts/test_mlebench_selected.sh
```

### 单独运行某个任务
```bash
cd /home/aiops/liufan/projects/DeepModeling

# 运行视网膜病变检测任务
python main.py --workflow scientific --benchmark mle --data-dir ./benchmarks/mlebench/competitions --task aptos2019-blindness-detection

# 运行植物病理学任务
python main.py --workflow scientific --benchmark mle --data-dir ./benchmarks/mlebench/competitions --task plant-pathology-2020-fgvc7
```

## 预期运行时间

根据任务复杂度，预计运行时间：
- **计算机视觉任务** (aptos2019, plant-pathology): 较长 (数据集较大，模型训练时间长)
- **NLP 任务** (us-patent-matching): 中等
- **回归任务** (taxi-fare): 较短到中等
- **表格数据任务** (tabular-playground): 短到中等

**总预计时间**: 根据硬件配置和数据集大小，可能需要数小时到数天不等。

## 注意事项

1. 确保有足够的磁盘空间存储数据集和模型
2. 计算机视觉任务建议使用 GPU 加速
3. 结果将保存在 `runs/benchmark_results/` 目录下
4. 每个任务的详细日志和输出将分别保存

## 数据准备

在运行前，确保：
- MLEBench 数据已正确下载到 `./benchmarks/mlebench/competitions/` 目录
- 每个任务目录包含必要的数据文件和配置文件

## 扩展使用

### 添加更多任务
如需测试其他 MLEBench 任务，可以编辑脚本并在 `--task` 参数后添加任务名称：

```bash
python main.py \
  --workflow scientific \
  --benchmark mle \
  --data-dir ./benchmarks/mlebench/competitions \
  --task \
    task1 \
    task2 \
    task3 \
    your-new-task
```

### 查看可用任务
```bash
ls /home/aiops/liufan/projects/DeepModeling/benchmarks/mlebench/competitions/
```

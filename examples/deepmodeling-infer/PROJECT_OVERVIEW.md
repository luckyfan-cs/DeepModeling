# DeepModeling Inference - 项目概览

## 项目目标

创建一个**纯推理框架**，用于测试已训练好的 SFT（Supervised Fine-Tuning）和 RL（Reinforcement Learning）模型，无需依赖训练框架。

## 核心特点

### 1. 简化依赖
- ❌ 不依赖 Agent-Lightning
- ❌ 不依赖 VERL
- ❌ 不依赖 Ray
- ❌ 不需要 reward function（仅用基准原生评分）
- ✅ 只需要基础的推理依赖

### 2. 灵活的模型加载
- **API 模式**（推荐）：通过 OpenAI 兼容的 API endpoint 调用模型
- **本地模式**：直接使用 transformers 加载模型
- 支持任何 HuggingFace 兼容的模型

### 3. 完整的评测流程
- 自动加载基准任务
- 执行 Scientific Method 工作流
- 沙箱环境中运行代码
- 使用基准原生评分系统
- 保存详细的推理日志

## 与训练框架的对比

| 特性 | deepmodeling-rl（训练） | deepmodeling-infer（推理） |
|------|------------------------|--------------------------|
| **目的** | 训练模型 | 测试模型 |
| **依赖** | Agent-Lightning + VERL + Ray | 最小化依赖 |
| **模型加载** | VERL 分布式 | 本地或 API |
| **奖励函数** | 必需（用于 RL 训练） | 不需要 |
| **输出** | Model checkpoints | 推理结果 + 评分 |
| **使用场景** | 模型开发阶段 | 模型评估阶段 |
| **资源需求** | 高（需要多 GPU） | 中（可用 CPU API） |

## 项目结构

```
deepmodeling-infer/
├── src/
│   ├── __init__.py          # 包初始化
│   ├── config.py            # 推理配置（无训练配置）
│   ├── infer.py             # 推理主脚本（无 RL 训练代码）
│   ├── utils.py             # 工具函数（仅评分，无 reward）
│   └── data_utils.py        # 数据加载（从 rl 版本复制）
├── scripts/
│   ├── quickstart.sh        # 快速启动
│   └── run_infer.sh         # 完整运行脚本
├── README.md                # 完整文档
├── QUICKSTART.md            # 快速开始指南
├── PROJECT_OVERVIEW.md      # 本文件
└── requirements.txt         # 最小化依赖
```

## 核心组件

### 1. DeepModelingInferenceAgent (infer.py)

主推理类，负责：
- 加载和调用 LLM（本地或 API）
- 执行 Scientific Method 工作流
- 管理沙箱环境
- 保存推理结果

关键方法：
```python
agent = DeepModelingInferenceAgent(
    model_path="your-model",
    api_endpoint="http://localhost:8000",
    max_turns=10,
    temperature=0.0
)

result = agent.run_inference(task)
```

### 2. BenchmarkGrader (utils.py)

评分系统，支持：
- Engineering Benchmark
- Science Benchmark
- MLE Benchmark
- MathModeling Benchmark

关键方法：
```python
grader = get_grader()
score = grader.grade_submission(task, submission_path)
```

### 3. Task Loading (data_utils.py)

任务加载，支持：
- 从基准加载任务
- 预定义的训练/验证集划分
- 自定义任务子集

```python
tasks = load_benchmark_tasks(
    benchmark="engineering",
    competitions=["industry-0", "industry-1"],
    limit=10
)
```

## 使用流程

### 典型工作流

```
1. 准备模型
   ├── 训练好的 SFT 模型
   └── 或训练好的 RL 模型

2. 部署模型（可选）
   └── 使用 vLLM 部署为 API

3. 运行推理
   ├── 加载任务
   ├── 执行推理
   └── 自动评分

4. 查看结果
   ├── 汇总结果（results/）
   └── 详细日志（workspace_infer/）
```

### 最简单的例子

```bash
# 1. 部署模型（如果使用 API 模式）
python -m vllm.entrypoints.openai.api_server \
    --model /path/to/model \
    --port 8000

# 2. 运行推理
python -m src.infer \
    --api-endpoint http://localhost:8000 \
    --task-id industry-0

# 3. 查看结果
cat results/summary_*.json
```

## 评分机制

### 使用基准原生评分

推理框架**不使用** reward function，而是直接使用基准的原生评分：

```python
# 每个基准都有自己的评分函数
from benchmarks.engineeringbench.grade import grade_csv

# 自动调用正确的评分函数
report = grade_csv(submission_path, competition)
score = report.score  # 原生分数
```

### 分数标准化

为了统一比较，分数会标准化为"越高越好"格式：

```python
def normalize_score(score, is_lower_better):
    if is_lower_better:
        return 1.0 / (1.0 + score)  # MAE, RMSE 等
    else:
        return score  # Accuracy, F1 等
```

## 输出格式

### 1. 任务级别结果

每个任务生成：
- `conversation.jsonl` - 完整对话历史
- `run_metadata.json` - 运行元数据
- `submission.csv` - 生成的提交文件

### 2. 汇总结果

```json
{
  "total_tasks": 10,
  "successful": 8,
  "failed": 2,
  "avg_turns": 6.5,
  "avg_grade": 0.7234,
  "results": [...]
}
```

## 扩展性

### 添加新基准

1. 在 `utils.py` 中添加加载逻辑：

```python
# 在 BenchmarkGrader._load_grading_modules() 中
try:
    from benchmarks.newbench.grade import grade_csv
    from benchmarks.newbench.registry import registry
    self._grading_functions["newbench"] = grade_csv
    self._registries["newbench"] = registry
except ImportError as e:
    logger.warning(f"Failed to load newbench: {e}")
```

2. 在 `data_utils.py` 中添加数据加载：

```python
DEFAULT_DATA_ROOTS = {
    "newbench": PROJECT_ROOT / "benchmarks" / "newbench" / "competitions",
}

def _load_newbench_tasks(...):
    # 实现任务加载逻辑
    pass
```

### 自定义推理流程

继承 `DeepModelingInferenceAgent` 并覆盖方法：

```python
class CustomAgent(DeepModelingInferenceAgent):
    def run_inference(self, task):
        # 自定义推理逻辑
        result = super().run_inference(task)
        # 后处理
        return result
```

## 性能考虑

### 推荐配置

**单 GPU 测试**：
```bash
# vLLM + API 模式
vllm --model your-model --gpu-memory-utilization 0.9
```

**多 GPU 推理**：
```bash
# vLLM Tensor Parallel
vllm --model your-model --tensor-parallel-size 2
```

**CPU 推理**（不推荐，很慢）：
```bash
# 使用本地模型 + CPU
python -m src.infer --use-local-model --model-path your-model
```

### 批量测试优化

```bash
# 并行运行多个推理（需要足够内存）
for i in {0..4}; do
    python -m src.infer \
        --api-endpoint http://localhost:8000 \
        --task-id industry-$i \
        --output-dir results/task_$i &
done
wait
```

## 常见应用场景

### 1. 模型对比

```bash
# SFT vs RL
./compare_models.sh \
    --sft-model /path/to/sft \
    --rl-model /path/to/rl \
    --tasks industry-0 industry-1 industry-2
```

### 2. 超参数测试

```bash
# 测试不同温度
for temp in 0.0 0.3 0.7 1.0; do
    python -m src.infer \
        --temperature $temp \
        --output-dir results/temp_$temp
done
```

### 3. 持续评估

```bash
# 定期测试最新 checkpoint
cron: 0 */6 * * * /path/to/run_eval.sh
```

## 故障排查

### 常见问题

1. **找不到数据**
   - 检查 `DEFAULT_DATA_ROOTS` 配置
   - 使用 `--data-root` 指定路径

2. **模型调用失败**
   - 验证 API endpoint
   - 检查模型格式兼容性

3. **评分失败**
   - 检查提交文件格式
   - 查看基准特定要求

4. **内存不足**
   - 使用 API 模式
   - 减少 `max_turns`
   - 使用量化模型

## 未来改进

可能的增强功能：
- [ ] 添加批量并行推理
- [ ] 支持更多模型格式
- [ ] 集成更多基准
- [ ] 添加结果可视化
- [ ] 支持增量评估

## 维护者

DeepModeling 团队

## 许可证

与 DeepModeling 项目相同

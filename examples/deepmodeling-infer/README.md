# DeepModeling Inference Framework

纯推理框架，用于测试已训练好的 SFT 和 RL 模型，无需训练环境。

## 功能特点

- **纯推理**：只包含推理功能，不依赖训练框架（Agent-Lightning/VERL）
- **模型灵活性**：支持本地模型和 API endpoint
- **多基准测试**：支持 Engineering, Science, MLE, MathModeling 等基准
- **自动评分**：使用基准的原生评分系统
- **详细日志**：保存完整的推理过程和结果

## 目录结构

```
deepmodeling-infer/
├── src/
│   ├── __init__.py          # 包初始化
│   ├── config.py            # 推理配置
│   ├── infer.py             # 推理主脚本
│   ├── utils.py             # 工具函数（评分等）
│   └── data_utils.py        # 数据加载
├── scripts/
│   ├── quickstart.sh        # 快速启动脚本
│   └── run_infer.sh         # 完整运行脚本
├── logs/                    # 日志目录
├── workspace_infer/         # 工作空间（自动创建）
├── results/                 # 结果目录（自动创建）
├── README.md
└── requirements.txt
```

## 安装依赖

```bash
# 基础依赖
pip install -r requirements.txt

# 如果使用本地模型
pip install transformers torch accelerate

# 如果需要特定基准
# Engineering/Science/MLE/MathModeling 基准已包含在 DeepModeling 项目中
```

## 快速开始

### 1. 使用 API Endpoint（推荐）

适用于已部署的模型服务（如 vLLM, TGI 等）：

```bash
# 单个任务测试
./scripts/quickstart.sh Qwen/Qwen2.5-7B-Instruct industry-0 \
    --api-endpoint http://localhost:8000

# 多任务测试（限制3个）
./scripts/quickstart.sh Qwen/Qwen2.5-7B-Instruct \
    --api-endpoint http://localhost:8000 \
    --task-limit 3
```

### 2. 使用本地模型

适用于直接加载模型权重：

```bash
# 单个任务测试
./scripts/quickstart.sh /path/to/model industry-0 \
    --use-local-model

# 多任务测试
./scripts/quickstart.sh /path/to/model \
    --use-local-model \
    --task-limit 3
```

## 详细使用

### 命令行参数

```bash
python -m src.infer --help
```

主要参数：

**模型配置**：
- `--model-path`: 模型路径或 HuggingFace 模型名
- `--api-endpoint`: API endpoint（OpenAI 兼容格式）
- `--use-local-model`: 本地加载模型（需要 transformers）

**Agent 配置**：
- `--max-turns`: 最大轮数（默认：10）
- `--temperature`: 采样温度（默认：0.0，贪婪采样）
- `--sandbox-timeout`: 沙箱超时时间（秒，默认：600）

**任务配置**：
- `--benchmark`: 基准名称（默认：engineering）
- `--task-id`: 单个任务 ID
- `--competitions`: 多个任务 ID 列表
- `--task-limit`: 任务数量限制
- `--data-root`: 数据根目录（可选）

**输出配置**：
- `--workspace-dir`: 工作空间目录（默认：./workspace_infer）
- `--output-dir`: 结果输出目录（默认：./results）
- `--log-level`: 日志级别（默认：INFO）

### 使用示例

#### 1. 测试单个任务（API模式）

```bash
python -m src.infer \
    --model-path Qwen/Qwen2.5-7B-Instruct \
    --api-endpoint http://localhost:8000 \
    --task-id industry-0 \
    --max-turns 10 \
    --temperature 0.0
```

#### 2. 测试多个任务（本地模型）

```bash
python -m src.infer \
    --model-path /path/to/model \
    --use-local-model \
    --benchmark engineering \
    --competitions industry-0 industry-1 industry-2 \
    --max-turns 10
```

#### 3. 测试 Science Benchmark

```bash
python -m src.infer \
    --model-path your-model \
    --api-endpoint http://localhost:8000 \
    --benchmark science \
    --task-limit 5
```

#### 4. 批量测试（限制任务数）

```bash
python -m src.infer \
    --model-path your-model \
    --api-endpoint http://localhost:8000 \
    --benchmark engineering \
    --task-limit 10 \
    --max-turns 8 \
    --temperature 0.1
```

## 输出结果

### 1. 工作空间（workspace_infer/）

每个任务运行会创建独立的工作空间：

```
workspace_infer/
└── infer_run_industry_0_abc12345/
    ├── sandbox_workdir/         # 沙箱工作目录
    │   ├── data/                # 链接的数据目录
    │   └── submission.csv       # 生成的提交文件
    └── artifacts/
        └── telemetry/
            ├── conversation.jsonl    # 完整对话历史
            └── run_metadata.json     # 运行元数据
```

### 2. 结果摘要（results/）

汇总所有任务的结果：

```json
{
  "total_tasks": 5,
  "successful": 4,
  "failed": 1,
  "avg_turns": 6.2,
  "avg_grade": 0.7823,
  "results": [
    {
      "task_id": "industry-0",
      "run_name": "infer_run_industry_0_abc12345",
      "success": true,
      "num_turns": 6,
      "grade_score": 0.85,
      "duration_seconds": 245.3
    },
    ...
  ],
  "config": {
    "model_path": "Qwen/Qwen2.5-7B-Instruct",
    "benchmark": "engineering",
    "max_turns": 10,
    "temperature": 0.0
  }
}
```

### 3. 运行元数据

每个任务的详细元数据（`run_metadata.json`）：

```json
{
  "run_name": "infer_run_industry_0_abc12345",
  "workflow": "inference_scientific_method",
  "task": {
    "task_id": "industry-0",
    "benchmark": "engineering",
    "prompt": "..."
  },
  "summary": {
    "success": true,
    "num_turns": 6,
    "output_exists": true,
    "grade_score": 0.85
  },
  "timeline": {
    "started_at_utc": "2025-01-10T10:00:00Z",
    "ended_at_utc": "2025-01-10T10:04:05Z",
    "duration_seconds": 245.3
  },
  "model_info": {
    "model_path": "Qwen/Qwen2.5-7B-Instruct",
    "temperature": 0.0,
    "max_turns": 10
  }
}
```

## 评分机制

推理框架使用基准的原生评分系统：

1. **自动评分**：每个任务完成后自动调用对应基准的评分函数
2. **标准化**：分数标准化为"越高越好"格式
3. **详细报告**：保存完整的评分报告和元数据

支持的基准：
- Engineering Benchmark
- Science Benchmark
- MLE Benchmark
- MathModeling Benchmark

## 性能优化

### 使用 vLLM 部署模型（推荐）

```bash
# 启动 vLLM 服务
python -m vllm.entrypoints.openai.api_server \
    --model /path/to/model \
    --host 0.0.0.0 \
    --port 8000 \
    --tensor-parallel-size 2

# 使用 API endpoint 进行推理
python -m src.infer \
    --model-path model-name \
    --api-endpoint http://localhost:8000 \
    --task-limit 10
```

### 批量测试

```bash
# 测试所有 engineering tasks
python -m src.infer \
    --model-path your-model \
    --api-endpoint http://localhost:8000 \
    --benchmark engineering

# 测试特定子集
python -m src.infer \
    --model-path your-model \
    --api-endpoint http://localhost:8000 \
    --competitions industry-0 industry-1 industry-2 industry-3
```

## 对比 SFT 和 RL 模型

```bash
# 测试 SFT 模型
python -m src.infer \
    --model-path /path/to/sft-model \
    --api-endpoint http://localhost:8000 \
    --task-limit 10 \
    --output-dir ./results/sft

# 测试 RL 模型
python -m src.infer \
    --model-path /path/to/rl-model \
    --api-endpoint http://localhost:8000 \
    --task-limit 10 \
    --output-dir ./results/rl

# 比较结果
python scripts/compare_results.py \
    ./results/sft/summary_*.json \
    ./results/rl/summary_*.json
```

## 常见问题

### Q1: 如何使用训练好的 checkpoint？

```bash
# 如果是 HuggingFace 格式
python -m src.infer \
    --model-path /path/to/checkpoint \
    --use-local-model

# 如果是 VERL 训练的 checkpoint，先转换为 HF 格式
# 然后使用上面的命令
```

### Q2: 内存不足怎么办？

```bash
# 方案1：使用 API endpoint + vLLM（推荐）
# vLLM 提供高效的推理加速和内存优化

# 方案2：使用量化模型
# 加载 4-bit 或 8-bit 量化模型
```

### Q3: 如何调试单个任务？

```bash
# 使用 --log-level DEBUG 查看详细日志
python -m src.infer \
    --model-path your-model \
    --task-id industry-0 \
    --log-level DEBUG

# 查看工作空间中的详细输出
ls workspace_infer/infer_run_*/
cat workspace_infer/infer_run_*/artifacts/telemetry/conversation.jsonl
```

### Q4: 如何自定义评分？

编辑 `src/utils.py` 中的 `BenchmarkGrader` 类，添加自定义评分逻辑。

## 与训练框架的区别

| 特性 | deepmodeling-rl（训练） | deepmodeling-infer（推理） |
|------|------------------------|--------------------------|
| 依赖 | Agent-Lightning, VERL, Ray | 无训练依赖 |
| 用途 | 训练和评估 | 仅推理和测试 |
| 模型加载 | VERL 分布式加载 | 本地或 API |
| 奖励函数 | 用于 RL 训练 | 不需要 |
| 输出 | Checkpoints + 训练日志 | 推理结果 + 评分 |

## 贡献

欢迎提交 Issue 和 Pull Request！

## License

与 DeepModeling 项目相同。

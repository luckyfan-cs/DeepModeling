# 部署和使用指南

## 完整工作流程

```
1. 训练模型 (SFT/RL)
   ↓
2. 部署模型为 API (vLLM/LLM Lite)
   ↓
3. 运行推理测试
   ↓
4. 查看评测结果
```

---

## 步骤 1: 部署模型为 API

### 方式 A: 使用 vLLM（推荐）

vLLM 提供高性能推理加速和 OpenAI 兼容 API。

#### 安装 vLLM

```bash
pip install vllm
```

#### 部署模型

```bash
# 单 GPU 部署
python -m vllm.entrypoints.openai.api_server \
    --model /path/to/your/model \
    --host 0.0.0.0 \
    --port 8000 \
    --gpu-memory-utilization 0.9

# 多 GPU 部署（Tensor Parallel）
python -m vllm.entrypoints.openai.api_server \
    --model /path/to/your/model \
    --host 0.0.0.0 \
    --port 8000 \
    --tensor-parallel-size 2 \
    --gpu-memory-utilization 0.9

# 后台运行
nohup python -m vllm.entrypoints.openai.api_server \
    --model /path/to/your/model \
    --port 8000 \
    > vllm.log 2>&1 &
```

#### 验证部署

```bash
# 测试 API 是否正常
curl http://localhost:8000/v1/models

# 测试生成
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "your-model",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### 方式 B: 使用 LLM Lite

如果您的项目使用 LLM Lite 进行部署：

```bash
# 假设您有 LLM Lite 的部署脚本
llm-lite deploy \
    --model /path/to/model \
    --port 8000 \
    --backend vllm

# 验证
curl http://localhost:8000/health
```

### 方式 C: 使用 TGI (Text Generation Inference)

```bash
# Docker 部署
docker run --gpus all --shm-size 1g -p 8000:80 \
    -v /path/to/model:/data \
    ghcr.io/huggingface/text-generation-inference:latest \
    --model-id /data
```

---

## 步骤 2: 运行推理测试

### 使用兼容的 main.py 接口

```bash
cd /home/aiops/liufan/projects/DeepModeling/examples/deepmodeling-infer
```

#### 示例 1: 测试单个任务

```bash
python main.py \
    --workflow scientific \
    --benchmark engineering \
    --llm-api http://localhost:8000 \
    --task industry-0
```

#### 示例 2: 测试 MathModeling 任务

```bash
python main.py \
    --workflow scientific \
    --benchmark mathmodeling \
    --data-dir "/home/aiops/liufan/projects/DeepModeling/data/mathmodeling-bench/competitions" \
    --llm-api http://localhost:8000 \
    --task mathmodeling-0
```

#### 示例 3: 批量测试（限制 5 个任务）

```bash
python main.py \
    --workflow scientific \
    --benchmark engineering \
    --llm-api http://localhost:8000 \
    --task-limit 5 \
    --max-turns 10 \
    --temperature 0.0
```

#### 示例 4: 测试多个指定任务

```bash
python main.py \
    --workflow scientific \
    --benchmark engineering \
    --llm-api http://localhost:8000 \
    --competitions industry-0 industry-1 industry-2 \
    --max-turns 8
```

#### 示例 5: 使用 OpenAI 格式模型名

```bash
python main.py \
    --workflow scientific \
    --benchmark science \
    --llm-model openai/deepseek-ai/DeepSeek-V3-Terminus \
    --task sciencebench-001
```

---

## 步骤 3: 查看结果

### 实时监控

```bash
# 监控 vLLM 日志
tail -f vllm.log

# 监控推理日志
tail -f workspace_infer/*/artifacts/telemetry/run_metadata.json
```

### 查看汇总结果

```bash
# 查看最新的汇总结果
cat results/summary_*.json | jq .

# 提取关键指标
cat results/summary_*.json | jq '{
  total: .total_tasks,
  successful: .successful,
  success_rate: (.successful / .total_tasks * 100),
  avg_grade: .avg_grade,
  avg_turns: .avg_turns
}'
```

### 查看单个任务详情

```bash
# 列出所有运行
ls workspace_infer/

# 查看特定任务的元数据
cat workspace_infer/infer_run_industry_0_*/artifacts/telemetry/run_metadata.json | jq .

# 查看对话历史
cat workspace_infer/infer_run_industry_0_*/artifacts/telemetry/conversation.jsonl
```

---

## 完整使用示例

### 场景 1: 快速测试 SFT 模型

```bash
# 1. 部署 SFT 模型
python -m vllm.entrypoints.openai.api_server \
    --model /path/to/sft-model \
    --port 8000 &

# 等待服务启动
sleep 10

# 2. 运行测试
python main.py \
    --workflow scientific \
    --benchmark engineering \
    --llm-api http://localhost:8000 \
    --task-limit 3 \
    --max-turns 5

# 3. 查看结果
cat results/summary_*.json | jq .
```

### 场景 2: 对比 SFT 和 RL 模型

```bash
# 测试 SFT 模型
python -m vllm.entrypoints.openai.api_server \
    --model /path/to/sft-model \
    --port 8000 &

python main.py \
    --workflow scientific \
    --benchmark engineering \
    --llm-api http://localhost:8000 \
    --task-limit 10 \
    --output-dir results/sft

# 停止 SFT 服务
pkill -f vllm

# 测试 RL 模型
python -m vllm.entrypoints.openai.api_server \
    --model /path/to/rl-model \
    --port 8000 &

python main.py \
    --workflow scientific \
    --benchmark engineering \
    --llm-api http://localhost:8000 \
    --task-limit 10 \
    --output-dir results/rl

# 比较结果
echo "SFT Results:"
cat results/sft/summary_*.json | jq '{avg_grade, success_rate: (.successful/.total_tasks*100)}'

echo "RL Results:"
cat results/rl/summary_*.json | jq '{avg_grade, success_rate: (.successful/.total_tasks*100)}'
```

### 场景 3: 不同基准测试

```bash
# Engineering Benchmark
python main.py --workflow scientific --benchmark engineering \
    --llm-api http://localhost:8000 --task-limit 5

# MathModeling Benchmark
python main.py --workflow scientific --benchmark mathmodeling \
    --llm-api http://localhost:8000 --task-limit 5

# Science Benchmark
python main.py --workflow scientific --benchmark science \
    --llm-api http://localhost:8000 --task-limit 5

# 汇总所有结果
for dir in results/*/; do
    echo "Benchmark: $(basename $dir)"
    cat $dir/summary_*.json | jq '{avg_grade, successful, total_tasks}'
done
```

---

## 高级配置

### 调整推理参数

```bash
# 更多轮次
python main.py \
    --llm-api http://localhost:8000 \
    --benchmark engineering \
    --task industry-0 \
    --max-turns 20

# 更高温度（增加随机性）
python main.py \
    --llm-api http://localhost:8000 \
    --benchmark engineering \
    --task industry-0 \
    --temperature 0.7

# 更长超时时间
python main.py \
    --llm-api http://localhost:8000 \
    --benchmark engineering \
    --task industry-0 \
    --sandbox-timeout 1200
```

### 自定义数据路径

```bash
python main.py \
    --workflow scientific \
    --benchmark engineering \
    --data-dir /custom/path/to/competitions \
    --llm-api http://localhost:8000 \
    --task industry-0
```

### 调试模式

```bash
python main.py \
    --workflow scientific \
    --benchmark engineering \
    --llm-api http://localhost:8000 \
    --task industry-0 \
    --log-level DEBUG
```

---

## 命令行参数完整列表

```bash
python main.py --help
```

### 必需参数

- `--workflow`: 工作流类型（目前只支持 `scientific`）
- `--benchmark`: 基准名称（`engineering`, `mathmodeling`, `science`, `mle`）
- `--llm-model` 或 `--llm-api`: LLM 模型名或 API endpoint
- `--task` 或 `--competitions` 或 `--task-limit`: 任务选择

### 可选参数

- `--data-dir`: 数据目录
- `--max-turns`: 最大轮数（默认 10）
- `--temperature`: 采样温度（默认 0.0）
- `--sandbox-timeout`: 沙箱超时（默认 600 秒）
- `--workspace-dir`: 工作空间目录
- `--output-dir`: 输出目录
- `--use-local-model`: 使用本地模型
- `--log-level`: 日志级别

---

## 故障排查

### 问题 1: API 连接失败

```bash
# 检查 vLLM 是否运行
curl http://localhost:8000/v1/models

# 检查端口占用
lsof -i :8000

# 查看 vLLM 日志
tail -f vllm.log
```

### 问题 2: 找不到数据

```bash
# 检查数据路径
ls /home/aiops/liufan/projects/DeepModeling/benchmarks/engineeringbench/competitions/

# 使用 --data-dir 指定正确路径
python main.py --data-dir /path/to/data ...
```

### 问题 3: 推理超时

```bash
# 增加超时时间
python main.py --sandbox-timeout 1800 ...

# 减少最大轮数
python main.py --max-turns 5 ...
```

### 问题 4: 内存不足

```bash
# 使用更小的 GPU 内存利用率
python -m vllm.entrypoints.openai.api_server \
    --model your-model \
    --gpu-memory-utilization 0.7

# 或使用量化模型
python -m vllm.entrypoints.openai.api_server \
    --model your-model \
    --quantization awq
```

---

## 性能优化建议

1. **使用 vLLM**: 比原生 transformers 快 10-20x
2. **Tensor Parallel**: 多 GPU 加速
3. **批量测试**: 一次部署，测试多个任务
4. **合理设置 max-turns**: 避免过多无效轮次
5. **使用贪婪采样**: `--temperature 0.0` 保证确定性

---

## 监控和日志

### 实时监控推理进度

```bash
# 方式 1: 查看推理日志
tail -f workspace_infer/*/artifacts/telemetry/run_metadata.json

# 方式 2: 监控 API 调用
tail -f vllm.log | grep "POST /v1/chat/completions"

# 方式 3: 使用 watch 命令
watch -n 1 'ls workspace_infer/ | wc -l'
```

### 性能分析

```bash
# 统计每个任务的耗时
cat results/summary_*.json | jq '.results[] | {
  task_id,
  duration: .duration_seconds,
  turns: .num_turns,
  grade: .grade_score
}'

# 计算平均每轮耗时
cat results/summary_*.json | jq '
  .results[] | 
  select(.duration_seconds and .num_turns) | 
  {task_id, avg_per_turn: (.duration_seconds / .num_turns)}
'
```

---

## 总结

这个推理框架提供了完整的模型测试流程：

1. ✅ **灵活部署**: 支持 vLLM, LLM Lite, TGI 等
2. ✅ **兼容接口**: 与现有命令行接口兼容
3. ✅ **自动评分**: 使用基准原生评分系统
4. ✅ **详细日志**: 完整的推理过程记录
5. ✅ **批量测试**: 高效的批量评测能力

开始使用：

```bash
# 1. 部署模型
python -m vllm.entrypoints.openai.api_server --model your-model --port 8000 &

# 2. 运行测试
python main.py --workflow scientific --benchmark engineering \
    --llm-api http://localhost:8000 --task industry-0

# 3. 查看结果
cat results/summary_*.json | jq .
```

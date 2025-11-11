# 快速开始指南

## 1. 准备工作

确保你已经：
- 安装了 DeepModeling 项目的依赖
- 准备了基准数据（在 `DeepModeling/benchmarks/` 下）
- 有一个训练好的模型（SFT 或 RL）

```bash
# 安装推理依赖
cd /path/to/DeepModeling/examples/deepmodeling-infer
pip install -r requirements.txt

# 如果使用本地模型，额外安装
pip install transformers torch accelerate
```

## 2. 最简单的测试

### 使用 API Endpoint（推荐）

如果你有一个运行中的模型服务（如 vLLM）：

```bash
# 测试单个任务
python -m src.infer \
    --api-endpoint http://localhost:8000 \
    --task-id industry-0

# 或使用快速启动脚本
./scripts/quickstart.sh dummy industry-0 --api-endpoint http://localhost:8000
```

### 使用本地模型

```bash
# 测试单个任务
python -m src.infer \
    --model-path /path/to/your/model \
    --use-local-model \
    --task-id industry-0
```

## 3. 部署模型服务（推荐使用 vLLM）

```bash
# 安装 vLLM
pip install vllm

# 启动服务
python -m vllm.entrypoints.openai.api_server \
    --model /home/aiops/liufan/projects/models/dm-sft-Qwen2.5-7B-Instruct/merged \
    --host 0.0.0.0 \
    --port 8000 \
    --tensor-parallel-size 1

# 在另一个终端运行推理
cd /path/to/DeepModeling/examples/deepmodeling-infer
python -m src.infer \
    --api-endpoint http://localhost:8000 \
    --task-limit 5
```

## 4. 批量测试

```bash
# 测试 5 个任务
python -m src.infer \
    --api-endpoint http://localhost:8000 \
    --benchmark engineering \
    --task-limit 5 \
    --max-turns 10

# 测试特定任务集
# 例如：engineering benchmark 下的 industry-3 任务
python -m src.infer \
    --api-endpoint http://localhost:8000 \
    --model-path /home/aiops/liufan/projects/models/dm-sft-Qwen2.5-7B-Instruct/merged \
    --data-dir /home/aiops/liufan/projects/DeepModeling/data/engineering-bench/competitions \
    --benchmark engineering \
    --competitions industry-3


#  例如：mathmodeling benchmark 下的 bwor-0 任务
python -m src.infer \
    --api-endpoint http://localhost:8000 \
    --model-path /home/aiops/liufan/projects/models/dm-sft-Qwen2.5-7B-Instruct/merged \
    --data-dir /home/aiops/liufan/projects/DeepModeling/data/mathmodeling-bench/competitions \
    --benchmark mathmodeling \
    --competitions bwor-0 mamo-easy-0 mamo-complex-0 mamo-ode-0

# 例如：mle benchmark 下的 dabench-0-mean-fare 任务
python -m src.infer \
    --api-endpoint http://localhost:8000 \
    --model-path /home/aiops/liufan/projects/models/dm-sft-Qwen2.5-7B-Instruct/merged \
    --data-dir /home/aiops/liufan/projects/DSFlow/data/competitions \
    --benchmark mle \
    --competitions dabench-0-mean-fare
```

## 5. 查看结果

```bash
# 查看汇总结果
cat results/summary_*.json

# 查看单个任务的详细结果
ls workspace_infer/
cat workspace_infer/infer_run_*/artifacts/telemetry/run_metadata.json
```

## 6. 对比 SFT 和 RL 模型

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

# 比较平均分数
echo "SFT 平均分数:"
cat ./results/sft/summary_*.json | grep "avg_grade"

echo "RL 平均分数:"
cat ./results/rl/summary_*.json | grep "avg_grade"
```

## 7. 常见用法

### 调整推理参数

```bash
# 使用较高的温度（增加随机性）
python -m src.infer \
    --api-endpoint http://localhost:8000 \
    --task-id industry-0 \
    --temperature 0.7

# 减少最大轮数（加快测试）
python -m src.infer \
    --api-endpoint http://localhost:8000 \
    --task-limit 5 \
    --max-turns 5

# 增加沙箱超时时间
python -m src.infer \
    --api-endpoint http://localhost:8000 \
    --task-id industry-0 \
    --sandbox-timeout 1200
```

### 测试不同基准

```bash
# Engineering Benchmark
python -m src.infer \
    --api-endpoint http://localhost:8000 \
    --benchmark engineering \
    --task-limit 5

# Science Benchmark
python -m src.infer \
    --api-endpoint http://localhost:8000 \
    --benchmark science \
    --task-limit 5

# Math Modeling Benchmark
python -m src.infer \
    --api-endpoint http://localhost:8000 \
    --benchmark mathmodeling \
    --task-limit 5
```

## 8. 调试

```bash
# 查看详细日志
python -m src.infer \
    --api-endpoint http://localhost:8000 \
    --task-id industry-0 \
    --log-level DEBUG

# 检查单个任务的对话历史
cat workspace_infer/infer_run_industry_0_*/artifacts/telemetry/conversation.jsonl | jq .

# 查看生成的代码和输出
ls workspace_infer/infer_run_*/sandbox_workdir/
```

## 9. 性能优化

### 使用 GPU 加速

```bash
# vLLM 自动使用所有可用 GPU
python -m vllm.entrypoints.openai.api_server \
    --model /path/to/model \
    --tensor-parallel-size 2  # 使用 2 个 GPU

# 或使用多 GPU
python -m vllm.entrypoints.openai.api_server \
    --model /path/to/model \
    --tensor-parallel-size 4  # 使用 4 个 GPU
```

### 并行测试多个任务

```bash
# 启动多个推理进程（需要足够的 GPU 内存）
for i in 0 1 2 3; do
    python -m src.infer \
        --api-endpoint http://localhost:8000 \
        --task-id industry-$i \
        --output-dir results/parallel_$i &
done
wait

# 汇总结果
cat results/parallel_*/summary_*.json
```

## 10. 故障排查

### 问题：找不到数据

```bash
# 检查数据路径
ls /path/to/DeepModeling/benchmarks/engineeringbench/competitions/

# 指定自定义数据路径
python -m src.infer \
    --api-endpoint http://localhost:8000 \
    --data-root /custom/path/to/competitions
```

### 问题：模型调用失败

```bash
# 测试 API endpoint
curl http://localhost:8000/v1/models

# 使用本地模型作为备选
python -m src.infer \
    --model-path /path/to/model \
    --use-local-model \
    --task-id industry-0
```

### 问题：沙箱超时

```bash
# 增加超时时间
python -m src.infer \
    --api-endpoint http://localhost:8000 \
    --sandbox-timeout 1800  # 30 分钟
```

## 更多信息

查看完整文档：`README.md`

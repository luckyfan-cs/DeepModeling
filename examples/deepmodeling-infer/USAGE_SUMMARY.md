# 使用方式总结

deepmodeling-infer 提供多种使用方式，满足不同场景需求。

---

## 方式 1: 兼容的 main.py 接口（推荐）

**适用场景**: 与现有工作流兼容，熟悉的命令行接口

### 基本用法

```bash
python main.py --workflow scientific --benchmark <BENCHMARK> \
    --llm-api <API_ENDPOINT> --task <TASK_ID>
```

### 完整示例

```bash
# Engineering Benchmark
python main.py --workflow scientific --benchmark engineering \
    --llm-api http://localhost:8000 --task industry-0

# MathModeling Benchmark
python main.py --workflow scientific --benchmark mathmodeling \
    --data-dir "/path/to/data" \
    --llm-api http://localhost:8000 --task mathmodeling-0

# 批量测试
python main.py --workflow scientific --benchmark engineering \
    --llm-api http://localhost:8000 --task-limit 5
```

### 参数说明

- `--workflow scientific`: 工作流类型（固定）
- `--benchmark`: 基准名称（engineering, mathmodeling, science, mle）
- `--llm-api`: API endpoint
- `--task`: 单个任务 ID
- `--task-limit`: 批量测试任务数量
- `--data-dir`: 自定义数据目录（可选）

---

## 方式 2: 直接使用 src.infer 模块

**适用场景**: 需要更多控制选项，高级用法

### 基本用法

```bash
python -m src.infer --api-endpoint <ENDPOINT> --task-id <TASK>
```

### 完整示例

```bash
# API 模式
python -m src.infer \
    --api-endpoint http://localhost:8000 \
    --benchmark engineering \
    --task-id industry-0 \
    --max-turns 10 \
    --temperature 0.0

# 本地模型
python -m src.infer \
    --model-path /path/to/model \
    --use-local-model \
    --task-id industry-0

# 批量测试特定任务
python -m src.infer \
    --api-endpoint http://localhost:8000 \
    --competitions industry-0 industry-1 industry-2
```

---

## 方式 3: 一键部署和测试脚本

**适用场景**: 快速测试，自动化部署

### 基本用法

```bash
./deploy_and_test.sh --model <MODEL_PATH> --task <TASK_ID>
```

### 完整示例

```bash
# 部署模型并测试单个任务
./deploy_and_test.sh \
    --model /path/to/model \
    --task industry-0

# 部署并批量测试
./deploy_and_test.sh \
    --model /path/to/model \
    --task-limit 5 \
    --max-turns 8

# 使用已部署的 API
./deploy_and_test.sh \
    --skip-deploy \
    --port 8000 \
    --task industry-0

# 自定义配置
./deploy_and_test.sh \
    --model /path/to/model \
    --benchmark mathmodeling \
    --task mathmodeling-0 \
    --temperature 0.3 \
    --max-turns 15
```

### 特点

- ✅ 自动部署 vLLM
- ✅ 自动等待 API 就绪
- ✅ 自动验证 API
- ✅ 运行后提示清理

---

## 方式 4: 快速启动脚本

**适用场景**: 简单快速测试

### 基本用法

```bash
./scripts/quickstart.sh <MODEL_PATH> <TASK_ID> [options]
```

### 示例

```bash
# API 模式
./scripts/quickstart.sh dummy industry-0 --api-endpoint http://localhost:8000

# 本地模型
./scripts/quickstart.sh /path/to/model industry-0 --use-local-model

# 批量测试
./scripts/quickstart.sh dummy --api-endpoint http://localhost:8000 --task-limit 3
```

---

## 方式 5: Python 代码调用

**适用场景**: 集成到其他 Python 项目，自定义工作流

### 基本用法

```python
from src import DeepModelingInferenceAgent, load_benchmark_tasks

# 创建 agent
agent = DeepModelingInferenceAgent(
    api_endpoint="http://localhost:8000",
    max_turns=10,
    temperature=0.0,
)

# 加载任务
tasks = load_benchmark_tasks(
    benchmark="engineering",
    competitions=["industry-0"],
)

# 运行推理
result = agent.run_inference(tasks[0])

# 查看结果
print(f"Success: {result['success']}")
print(f"Grade: {result['grade_score']}")
```

### 完整示例

参考 `example_usage.py` 文件中的示例代码。

---

## 各种方式对比

| 方式 | 优点 | 缺点 | 适用场景 |
|-----|------|------|---------|
| main.py | 兼容现有接口 | 参数固定 | 日常使用 |
| src.infer | 灵活控制 | 命令较长 | 高级用法 |
| deploy_and_test.sh | 全自动 | 依赖 bash | 快速测试 |
| quickstart.sh | 简单快速 | 功能有限 | 初次尝试 |
| Python API | 完全控制 | 需要写代码 | 集成开发 |

---

## 常见使用场景

### 场景 1: 快速验证模型

```bash
# 最简单的方式
./deploy_and_test.sh --model /path/to/model --task industry-0
```

### 场景 2: 日常开发测试

```bash
# 使用 main.py
python main.py --workflow scientific --benchmark engineering \
    --llm-api http://localhost:8000 --task-limit 3
```

### 场景 3: 批量评测

```bash
# 使用 src.infer
python -m src.infer \
    --api-endpoint http://localhost:8000 \
    --benchmark engineering \
    --task-limit 20 \
    --output-dir results/batch_eval
```

### 场景 4: 对比不同模型

```bash
# SFT 模型
./deploy_and_test.sh --model /path/to/sft --task-limit 10
mv results results_sft

# RL 模型
./deploy_and_test.sh --model /path/to/rl --task-limit 10
mv results results_rl

# 比较
python scripts/compare_results.py results_sft results_rl
```

### 场景 5: 集成到 CI/CD

```bash
# 自动化测试脚本
#!/bin/bash
set -e

# 部署最新模型
./deploy_and_test.sh \
    --model /path/to/latest/checkpoint \
    --task-limit 5 \
    --max-turns 8

# 检查结果
SCORE=$(cat results/summary_*.json | jq '.avg_grade')
if (( $(echo "$SCORE < 0.7" | bc -l) )); then
    echo "Performance degradation detected!"
    exit 1
fi
```

---

## 推荐工作流

### 对于初学者

```bash
1. 使用 quickstart.sh 快速尝试
   ./scripts/quickstart.sh your-model task-id --api-endpoint http://localhost:8000

2. 查看结果
   cat results/summary_*.json | jq .

3. 查看详细日志
   ls workspace_infer/
```

### 对于日常使用

```bash
1. 部署模型（一次）
   python -m vllm.entrypoints.openai.api_server --model your-model --port 8000 &

2. 使用 main.py 进行测试（多次）
   python main.py --workflow scientific --benchmark engineering \
       --llm-api http://localhost:8000 --task industry-0

3. 需要时停止服务
   lsof -ti:8000 | xargs kill -9
```

### 对于批量评测

```bash
1. 使用自动化脚本
   ./deploy_and_test.sh --model your-model --task-limit 20

2. 或手动控制
   # 部署
   python -m vllm.entrypoints.openai.api_server --model your-model --port 8000 &
   
   # 批量测试
   python -m src.infer --api-endpoint http://localhost:8000 --task-limit 50
   
   # 停止
   lsof -ti:8000 | xargs kill -9
```

---

## 获取帮助

```bash
# main.py 帮助
python main.py --help

# src.infer 帮助
python -m src.infer --help

# deploy_and_test.sh 帮助
./deploy_and_test.sh --help

# quickstart.sh 帮助
./scripts/quickstart.sh
```

---

## 文档导航

- **README.md** - 完整功能文档
- **QUICKSTART.md** - 10 个快速开始示例
- **DEPLOYMENT_GUIDE.md** - 详细部署指南
- **PROJECT_OVERVIEW.md** - 项目架构设计
- **USAGE_SUMMARY.md** - 本文件，使用方式总结

---

## 总结

选择合适的方式：

- 🚀 **想要最快**: `./deploy_and_test.sh --model your-model --task task-id`
- 💼 **日常使用**: `python main.py --workflow scientific ...`
- 🔧 **高级控制**: `python -m src.infer ...`
- 🐍 **Python 集成**: 导入 `src` 模块使用

所有方式都支持相同的核心功能，只是接口和便利性不同。

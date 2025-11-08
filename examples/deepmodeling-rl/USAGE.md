# DeepModeling RL 使用指南

## 快速开始

### 最简单的方式

```bash
cd /home/aiops/liufan/projects/DeepModeling/examples/deepmodeling-rl
./quickstart.sh
```

这将运行一个快速测试（fast 模式），使用 `engineering_mini` split。

### 自定义运行

```bash
# 使用不同的 benchmark
./quickstart.sh mathmodeling standard

# 或直接使用 Python
python train_deepmodeling.py fast \
    --benchmark engineering \
    --split engineering_mini \
    --n-runners 1
```

## 核心架构

### 1. Agent（deepmodeling_agent.py）

**直接复用现有代码**：
- `ScientificWorkflow` 的 prompts（来自 `modeling/prompts/scientific_prompt.py`）
- Sandbox 执行（来自 `modeling/services/sandbox.py`）
- Workspace 管理（来自 `modeling/services/workspace.py`）
- ReviewResult 评估（来自 `modeling/models/formats.py`）

**关键特性**：
- 使用 LangGraph 实现多轮对话
- 支持 VERL endpoint 替换
- 同步执行（不需要 async）
- 每个实验自动创建独立workspace

### 2. Reward Function（reward_function.py）

奖励计算基于 ReviewResult：

```python
reward = execution_reward + quality_reward + thoroughness_reward + achievement_bonus

其中：
- execution_reward: 0.2 (成功) 或 -0.1 (失败)
- quality_reward: quality_score * 0.5 (0-0.5)
- thoroughness_reward: thoroughness_score * 0.3 (0-0.3)
- achievement_bonus: 1.0 (达到阈值) 或 0.0
```

### 3. Data Loading（data_utils.py）

**直接使用 Benchmark Registry**：
- 从 `benchmarks/engineeringbench/registry.py` 加载
- 自动读取 competition 的 description、public_dir
- 无需SFT数据转换，直接从prepared data加载

### 4. Training（train_deepmodeling.py）

Agent-lightning 标准流程：
1. 加载配置（config.py）
2. 加载数据（data_utils.py）
3. 创建 agent（LitDeepModelingAgent）
4. 创建 algorithm（VERL）
5. 训练（Trainer.fit）

## 配置选项

### Presets

- **fast**: CI/测试，1个epoch，小模型 (Qwen2.5-Coder-0.5B)
- **standard**: 日常训练，2个epoch，默认配置
- **advanced**: 长时间训练，4个epoch，更大batch

### Data Splits

**预定义 Splits**（推荐）：
- `engineering_mini`: 6个任务（4 train, 2 val）
- `engineering_valset`: 7个任务（5 train, 2 val）
- `mathmodeling_pair`: 2个任务（1 train, 1 val）

```bash
python train_deepmodeling.py standard --split engineering_mini
```

**动态划分**：
```bash
python train_deepmodeling.py standard \
    --benchmark engineering \
    --competitions industry-0 industry-1 industry-2 industry-10 \
    --val-ratio 0.25
```

### Agent 配置

```bash
python train_deepmodeling.py standard \
    --max-turns 5 \               # 每个任务最多5轮迭代
    --sandbox-timeout 600 \        # 10分钟超时
    --workspace-dir ./my_workspace # 自定义工作目录
```

### Model 配置

```bash
python train_deepmodeling.py standard \
    --model-path Qwen/Qwen2.5-Coder-1.5B-Instruct \
    --val-temperature 0.0  # 验证时的temperature
```

## 目录结构

训练后会生成：

```
examples/deepmodeling-rl/
├── workspace_rl/                    # Agent 执行工作区
│   ├── industry-0_turn_1_xxxxx/
│   │   ├── sandbox_workdir/         # 代码执行目录
│   │   └── artifacts/               # 结果文件
│   └── industry-1_turn_1_xxxxx/
├── checkpoints/                     # RL 模型 checkpoints
├── logs/                            # 训练日志
└── wandb/                           # Wandb 日志（如果启用）
```

## 实际案例

### 案例 1: 本地测试

```bash
# 快速测试（1个epoch，小模型）
python train_deepmodeling.py fast \
    --split engineering_mini \
    --n-runners 1 \
    --max-turns 2
```

### 案例 2: 标准训练

```bash
# 使用 engineering benchmark，自定义模型
python train_deepmodeling.py standard \
    --benchmark engineering \
    --split engineering_valset \
    --model-path Qwen/Qwen2.5-Coder-1.5B-Instruct \
    --n-runners 2 \
    --max-turns 5
```

### 案例 3: 高级训练

```bash
# 长时间训练，多个任务
python train_deepmodeling.py advanced \
    --benchmark engineering \
    --task-limit 20 \
    --val-ratio 0.15 \
    --model-path meta-llama/Llama-3.2-1B-Instruct \
    --n-runners 4 \
    --max-turns 10 \
    --sandbox-timeout 1200
```

## 监控训练

### Console 输出

训练期间会显示：
```
[Rollout xxx] Reward 1.250 | execution=0.20 quality=0.35 thoroughness=0.21 achievement=0.49
```

### Wandb（可选）

如果配置了 wandb，可以查看：
- `reward/mean`: 平均奖励
- `reward/max`: 最高奖励
- `success_rate`: 成功率
- `quality_score/mean`: 平均质量分数

## 调试技巧

### 1. 检查 workspace

```bash
# 查看最近的执行结果
ls -lt workspace_rl/ | head
cd workspace_rl/industry-0_turn_1_xxxxx/
cat artifacts/summary.json
```

### 2. 查看奖励计算

```python
# reward_function.py 有测试代码
python reward_function.py
```

### 3. 测试数据加载

```python
# data_utils.py 有示例代码
python data_utils.py
```

### 4. 单独测试 Agent

```python
from deepmodeling_agent import DeepModelingAgent, DeepModelingConfig
from pathlib import Path

config = DeepModelingConfig(debug=True)
agent = DeepModelingAgent(config=config)

task = {
    "task_id": "test-001",
    "prompt": "Solve this problem...",
    "io_instructions": "Save to submission.csv",
    "expected_output_path": "submission.csv",
    "eval_metric": "score",
    "threshold": 0.7,
}

result = agent.run_episode(task)
print(result["success"])
```

## 常见问题

### Q1: Out of memory

**方案**：
- 使用 `fast` preset
- 减少 `--n-runners`
- 减少 batch size（修改 config.py）
- 使用更小的模型

### Q2: 找不到数据

**方案**：
```bash
# 指定正确的 data root
python train_deepmodeling.py standard \
    --data-root /path/to/benchmarks/engineering-bench/competitions
```

### Q3: Sandbox 超时

**方案**：
```bash
# 增加超时时间
python train_deepmodeling.py standard \
    --sandbox-timeout 1200  # 20分钟
```

### Q4: 奖励太低

**检查**：
1. 模型是否正确加载？
2. Prompt 是否清晰？
3. 数据目录是否正确链接？
4. 查看 workspace 中的执行日志

## 与原有 DeepModeling 的关系

这个 RL 框架**直接复用**了 DeepModeling 的核心组件：

| 组件 | 来源 | 用途 |
|------|------|------|
| ScientificWorkflow | `modeling/workflows/search/scientific_workflow.py` | Prompts 和流程 |
| Prompts | `modeling/prompts/scientific_prompt.py` | 科学方法 prompts |
| SandboxService | `modeling/services/sandbox.py` | 代码执行 |
| WorkspaceService | `modeling/services/workspace.py` | 文件管理 |
| ReviewResult | `modeling/models/formats.py` | 结果评估 |
| Benchmarks | `modeling/benchmark/` | 任务加载 |

**区别**：
- RL: 使用 agent-lightning/VERL 训练循环
- 原框架: 使用 runner.py 单次执行

**兼容性**：
- RL 训练的模型可以直接用于原框架
- 原框架的 benchmark 数据可以直接用于 RL

## 下一步

1. **数据准备**: 确保 benchmark competitions 已 prepared
2. **快速测试**: `./quickstart.sh`
3. **调整配置**: 根据需求修改 preset 或参数
4. **监控训练**: 观察奖励和成功率
5. **评估模型**: 在验证集上测试

## 参考

- [Agent-lightning 文档](https://github.com/microsoft/agent-lightning)
- [DeepModeling 主文档](../../README.md)
- [Spider RL 示例](https://github.com/microsoft/agent-lightning/tree/main/examples/spider)

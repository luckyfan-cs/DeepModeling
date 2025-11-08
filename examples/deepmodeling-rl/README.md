# DeepModeling RL Training Framework

This directory contains the reinforcement learning (RL) training framework for DeepModeling agents using Agent-lightning.

## Overview

The framework trains agents to solve scientific computing tasks by:
1. Following the Scientific Method workflow (Phenomenon → Hypothesis → Model → Experiment → Observation → Inference)
2. Executing code in sandboxed environments
3. Receiving rewards based on execution results and solution quality

## Architecture

```
DeepModelingAgent (LangGraph)
    ├── Initial Planning (Phenomenon, Hypothesis, Model)
    ├── Experiment Loop (multi-turn)
    │   ├── Generate Experiment Code
    │   ├── Execute in Sandbox
    │   ├── Observe Results
    │   └── Infer Next Steps
    └── Conclusion

Reward Function
    ├── Execution Success (+0.2)
    ├── Quality Score (0-0.5)
    ├── Thoroughness Score (0-0.3)
    └── Achievement Bonus (+1.0 if passing threshold)
```

## Files

- `deepmodeling_agent.py` - Core agent implementation using LangGraph
- `train_deepmodeling.py` - Agent-lightning VERL training entrypoint
- `data_utils.py` - Helpers for loading DeepModeling benchmark tasks as RL episodes
- `config.py` - Training configuration presets (fast/standard/advanced)
- `reward_function.py` - Reward calculation based on sandbox results

## Setup

### 1. Install Dependencies

```bash
pip install agentlightning pandas pydantic
# VERL + RL training extras (includes trainer/runtime deps)
pip install "agentlightning[verl]"
# LangGraph runtime for the Scientific Method agent
pip install langgraph
```

> RL 训练依赖 Agent-Lightning/VERL 组件及 LangGraph runtime，因此要先安装 `agentlightning`、`agentlightning[verl]` 和 `langgraph`。

### 2. Verify Benchmark Data

The RL pipeline reuses the prepared DeepModeling benchmarks directly—no SFT to RL conversion is required. By default, `train_deepmodeling.py` looks for competitions under:

```
DeepModeling/data/engineering-bench/competitions
```

If your data lives elsewhere, pass `--data-root /path/to/competitions`.

### 3. Configure Training

`config.py` ships with three presets (`fast`, `standard`, `advanced`).
You can override the model checkpoint or other hyperparameters at runtime using CLI flags (e.g., `--model-path`, `--n-runners`, `--max-turns`).

## Training

### Quick Start (Fast Mode for Testing)

```bash
python train_deepmodeling.py fast --task-limit 2 --n-runners 1
```

### Standard Training

```bash
python train_deepmodeling.py standard \
    --benchmark engineering \
    --competitions industry-0 industry-1 industry-2 \
    --model-path Qwen/Qwen2.5-Coder-1.5B-Instruct \
    --n-runners 2
```

### Advanced Training

```bash
python train_deepmodeling.py advanced \
    --benchmark engineering \
    --data-root /mnt/benchmarks/engineering-bench/competitions \
    --model-path meta-llama/Llama-3.2-1B-Instruct \
    --max-turns 10 \
    --val-ratio 0.1
```

### Predefined Train/Val Splits

```bash
python train_deepmodeling.py fast --split engineering_mini --n-runners 1
```

Key CLI options:
- `--task-limit` / `--competitions` control which competitions are sampled.
- `--val-ratio` splits train/validation inside `data_utils.split_dataset`.
- `--workspace-dir`, `--sandbox-timeout`, `--max-turns` expose LangGraph agent knobs.
- `--split engineering_mini` (or other names from `data_utils.PREDEFINED_SPLITS`) loads a fixed train/val competition set without random sampling.
- `--min-train-tasks 4` guarantees至少拿到指定数量的训练任务，不足时会自动回退到 benchmark 池补齐。

## Reward Function

The reward is calculated based on multiple factors:

1. **Execution Success** (0.2): Whether the experiment code runs without errors
2. **Quality Score** (0.0-0.5): From ReviewResult, measuring solution quality
3. **Thoroughness Score** (0.0-0.3): From ReviewResult, measuring analysis depth
4. **Achievement Bonus** (1.0): If the solution passes the benchmark threshold

Total reward range: 0.0 to 2.0

### Reward Breakdown

```python
reward = base_reward + quality_reward + thoroughness_reward + achievement_bonus

where:
  base_reward = 0.2 if execution succeeds else 0.0
  quality_reward = quality_score * 0.5  # 0-0.5
  thoroughness_reward = thoroughness_score * 0.3  # 0-0.3
  achievement_bonus = 1.0 if passes threshold else 0.0
```

## Data Format

### Input Format (from SFT)

Each training example should contain:
```json
{
  "task_id": "sciencebench-001-clintox-nn",
  "description": "Task description...",
  "conversation": [
    {"role": "user", "content": "Task prompt"},
    {"role": "assistant", "content": "<Phenomenon>...</Phenomenon>..."},
    ...
  ],
  "artifacts": {
    "summary.json": {...},
    "experiment_reviews": [...]
  }
}
```

### RL Training Format

```json
{
  "prompt": "Task description and requirements",
  "task_id": "sciencebench-001-clintox-nn",
  "expected_output_path": "./submission.csv",
  "eval_metric": "f1_score",
  "threshold": 0.73,
  "data_dir": "/path/to/public/data"
}
```

`data_utils.load_benchmark_tasks()` generates dictionaries in this shape directly from DeepModeling benchmarks, so you can plug new competitions in without an intermediate conversion step.

## Monitoring

Training metrics are logged to:
- Console output
- Wandb (if enabled)

Key metrics:
- `reward/mean` - Average reward per episode
- `reward/max` - Maximum reward achieved
- `success_rate` - Percentage of successful executions
- `quality_score/mean` - Average quality score
- `achievement_rate` - Percentage passing threshold

## Checkpoints

Checkpoints are saved to:
```
checkpoints/
├── epoch_0/
├── epoch_1/
└── best/  # Best model based on validation reward
```

## Troubleshooting

### Out of Memory

Reduce batch size or enable gradient checkpointing:
```python
config["actor_rollout_ref"]["actor"]["ppo_micro_batch_size_per_gpu"] = 2
config["actor_rollout_ref"]["model"]["enable_gradient_checkpointing"] = True
```

### Sandbox Timeout

Increase sandbox timeout in config:
```python
config["sandbox"]["timeout"] = 600  # 10 minutes
```

### Low Reward

Check:
1. Is the SFT model properly trained?
2. Are the task prompts clear?
3. Is the reward function properly calibrated?

## Advanced Usage

### Custom Reward Function

Edit `reward_function.py` to customize reward calculation:

```python
def calculate_custom_reward(
    execution_result: ExecutionResult,
    review: Optional[ReviewResult],
    threshold: float
) -> float:
    # Your custom logic
    return reward
```

### Multi-GPU Training

```bash
torchrun --nproc_per_node=4 train_deepmodeling.py standard
```

### Resume from Checkpoint

```bash
python train_deepmodeling.py standard \
    --resume-from checkpoints/epoch_2
```

## Citation

If you use this framework, please cite:

```bibtex
@software{deepmodeling_rl,
  title={DeepModeling RL Training Framework},
  year={2025},
  url={https://github.com/your-org/DeepModeling}
}
```

## License

Same as DeepModeling project.

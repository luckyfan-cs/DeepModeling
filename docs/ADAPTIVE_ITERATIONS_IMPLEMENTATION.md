# 自适应轮数实现文档

## 概述

基于 [ADAPTIVE_ITERATIONS_PROPOSAL.md](ADAPTIVE_ITERATIONS_PROPOSAL.md) 中的方案设计，已实现**混合策略（方案 1 + 方案 3）**的自适应轮数功能。

## 实现的功能

### 1. 默认最大轮数调整

- **修改**: `max_iterations` 默认值从 3 改为 5
- **位置**: `scientific_workflow.py:109`
- **配置**: 可通过配置文件覆盖：`agent.search.max_iterations`

```python
max_iterations = self.agent_config.get("search", {}).get("max_iterations", 5)
```

### 2. 策略 1: 检测提前出现的 `<Conclusion>` 标签

**原理**:
- 正常情况下，`<Conclusion>` 只在最后一轮（iteration == max_iterations）出现
- 如果 LLM 在中间轮次就生成了 `<Conclusion>`，说明它认为任务已完成
- 检测到后立即终止循环

**实现位置**: `scientific_workflow.py:160-166`

```python
# Strategy 1: Check if LLM generated <Conclusion> early (before final iteration)
if '<Conclusion>' in response and i < max_iterations:
    logger.info(f"Early completion detected: <Conclusion> found at iteration {i}/{max_iterations}")
    # Add final observation and response, then stop
    assistant_response += f"\n<Observation>\n{observation}\n</Observation>\n"
    assistant_response += response
    break
```

**优势**:
- ✅ 简单直接，只需 6 行代码
- ✅ 让 LLM 自己判断是否完成
- ✅ 符合科学方法流程（Conclusion = 结束）

### 3. 策略 3: 基于 Observation 关键词匹配

**原理**:
- 分析 observation 中的成功标志和错误标志
- 如果检测到成功标志且没有错误，认为任务可能已完成
- 触发最后一轮让 LLM 生成 `<Conclusion>`

**实现位置**:
- 检测函数: `scientific_workflow.py:55-97`
- 应用逻辑: `scientific_workflow.py:183-197`

```python
def _is_task_completed(self, observation: str) -> bool:
    """Check if observation indicates task completion."""
    if not observation:
        return False

    observation_lower = observation.lower()

    # Success indicators
    success_indicators = [
        "successfully",
        "complete",
        "saved",
        "submission",
        "test passed",
        "all tests pass",
        "finished",
        "done",
    ]

    # Error indicators
    error_indicators = [
        "error",
        "failed",
        "exception",
        "traceback",
        "assertion",
    ]

    has_success = any(indicator in observation_lower for indicator in success_indicators)
    has_error = any(indicator in observation_lower for indicator in error_indicators)

    return has_success and not has_error
```

**应用**:
```python
# Strategy 3: Check if observation indicates task completion
if self._is_task_completed(observation):
    logger.info(f"Task completion detected in observation at iteration {i}/{max_iterations}")
    logger.info("Triggering final round to generate <Conclusion>")
    # Trigger final round by setting iteration = max_iterations
    final_prompt = create_continue_prompt(
        conversation_history=assistant_response,
        execution_output=observation,
        iteration=max_iterations,
        max_iterations=max_iterations
    )
    final_response = await self.llm_service.call(prompt=final_prompt)
    assistant_response += f"\n<Observation>\n{observation}\n</Observation>\n"
    assistant_response += final_response
    break
```

**优势**:
- ✅ 基于实际执行结果判断
- ✅ 不依赖 LLM 的主观判断
- ✅ 适用于有明确成功标志的任务

## 工作流程

```
第 1 轮: 初始分析
  ├─ Phenomenon, Hypothesis, Model, Experiment
  ├─ 执行实验
  └─ 获得 Observation

第 2-N 轮: 迭代优化
  ├─ 获取 LLM response (Inference + 新的 Hypothesis/Model/Experiment)
  │
  ├─ 【检查点 1】是否包含 <Conclusion>？
  │   └─ 是 → 提前终止 ✓
  │
  ├─ 添加 Observation 和 response
  │
  ├─ 提取并执行新的 Experiment
  │
  ├─ 【检查点 2】observation 是否显示任务完成？
  │   └─ 是 → 触发最后一轮生成 Conclusion → 终止 ✓
  │
  └─ 继续下一轮

最后一轮 (i == max_iterations):
  └─ 强制生成 <Conclusion>
```

## 日志输出

### 策略 1 触发时

```
INFO - --- Iteration 2/5 ---
INFO - Early completion detected: <Conclusion> found at iteration 2/5
INFO - Scientific discovery workflow completed
```

### 策略 3 触发时

```
INFO - --- Iteration 3/5 ---
INFO - Task completion detected in observation at iteration 3/5
INFO - Triggering final round to generate <Conclusion>
INFO - Scientific discovery workflow completed
```

### 正常完成（第 5 轮）

```
INFO - --- Iteration 5/5 ---
INFO - Scientific discovery workflow completed
```

## 测试场景

### 场景 1: 简单任务（第 2 轮完成）

**任务**: 计算 Titanic 数据集中的平均票价

```
轮 1: 加载数据 → 成功
轮 2: 计算平均值并保存 → observation: "Mean fare: 32.20\nSaved successfully"
      → _is_task_completed() 返回 True
      → 触发最后一轮生成 Conclusion
      → 提前终止 ✓
```

**实际轮数**: 2-3 轮（节省 2-3 轮）

### 场景 2: LLM 自主判断完成

**任务**: 数据探索和分析

```
轮 1: 数据加载和探索 → 成功
轮 2: 统计分析 → 成功
轮 3: LLM 生成 <Inference> 后直接生成 <Conclusion>
      → '<Conclusion>' in response 检测到
      → 立即终止 ✓
```

**实际轮数**: 3 轮（节省 2 轮）

### 场景 3: 复杂任务（需要全部 5 轮）

**任务**: 模型训练和优化

```
轮 1: 数据准备 → 成功
轮 2: 初始模型训练 → 准确率 0.75
轮 3: 超参数调优 → 准确率 0.82
轮 4: 特征工程 → 准确率 0.87
轮 5: 最终验证 → 强制生成 Conclusion
```

**实际轮数**: 5 轮（使用全部轮次）

### 场景 4: 失败任务

**任务**: 尝试训练模型但数据有问题

```
轮 1-4: 各种尝试 → 部分成功但 observation 中包含 "error"
       → _is_task_completed() 返回 False (有 error 标志)
       → 继续尝试
轮 5: 最后一轮 → 生成 <Conclusion>（总结失败原因）
```

**实际轮数**: 5 轮（不会误判提前终止）

## 配置参数

### 通过配置文件

编辑 `config.yaml`:

```yaml
agent:
  search:
    max_iterations: 5  # 最大轮数（默认 5）
```

### 运行时指定

```bash
python -m modeling.runner \
  --workflow scientific \
  --agent.search.max_iterations 8 \
  --benchmark titanic
```

## 代码统计

| 功能模块 | 代码行数 | 复杂度 |
|---------|---------|--------|
| `_is_task_completed()` 函数 | 42 行 | 低 |
| 策略 1 实现（Conclusion 检测） | 6 行 | 极低 |
| 策略 3 实现（Observation 检测） | 14 行 | 低 |
| **总计** | **~62 行** | **低** |

## 与提案对比

| 项目 | 提案推荐 | 实际实现 | 状态 |
|------|---------|---------|------|
| 策略 1 (Conclusion 检测) | ⭐⭐⭐⭐⭐ | ✅ 已实现 | 完成 |
| 策略 2 (TaskStatus 标签) | ⭐⭐⭐⭐ | ❌ 未实现 | 可选 |
| 策略 3 (关键词匹配) | ⭐⭐⭐ | ✅ 已实现 | 完成 |
| 策略 4 (连续成功) | ⭐⭐ | ❌ 未实现 | 不推荐 |
| 混合方案 (1+3) | ⭐⭐⭐⭐⭐ | ✅ 已实现 | **完成** ✓ |
| 默认 max_iterations = 5 | 必须 | ✅ 已实现 | 完成 |

## 优势总结

✅ **智能自适应**: 简单任务可以在 2-3 轮完成，无需等待全部 5 轮
✅ **双重检测**: 结合 LLM 判断和执行结果分析
✅ **代码简洁**: 只增加约 62 行代码
✅ **向后兼容**: 不影响现有功能
✅ **可配置**: 支持自定义最大轮数
✅ **日志清晰**: 明确记录提前终止原因
✅ **鲁棒性好**: 避免误判（检查 error 标志）

## 未来扩展

如果需要更高的精确度，可以考虑实现**策略 2（TaskStatus 标签）**:

1. 修改提示词，要求 LLM 在 `<Inference>` 后添加 `<TaskStatus>complete/incomplete</TaskStatus>`
2. 解析 TaskStatus 标签判断是否继续
3. 提供更明确的任务完成信号

**实现难度**: 中等（约 40 行代码 + 提示词修改）
**推荐度**: ⭐⭐⭐⭐ （如果当前策略不够准确时考虑）

## 相关文档

- [ADAPTIVE_ITERATIONS_PROPOSAL.md](ADAPTIVE_ITERATIONS_PROPOSAL.md) - 完整的方案设计和对比
- [SCIENTIFIC_WORKFLOW_README.md](SCIENTIFIC_WORKFLOW_README.md) - Scientific Workflow 总体介绍
- [OBSERVATION_PROCESSING.md](OBSERVATION_PROCESSING.md) - Observation 处理机制

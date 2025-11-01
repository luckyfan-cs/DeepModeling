# Scientific Workflow 自适应轮数方案

## 当前问题

- **固定轮数**: max_iterations = 5，每次都执行完所有轮次
- **浪费资源**: 任务可能在第 2 轮就完成，但还要继续到第 5 轮
- **缺乏灵活性**: 无法根据任务完成情况自适应调整

## 提前终止的时机判断

### 方案 1: 检测提前出现的 `<Conclusion>` 标签（推荐 ⭐⭐⭐⭐⭐）

**原理**:
- 正常情况下，`<Conclusion>` 只在最后一轮出现
- 如果 LLM 在中间轮次就生成了 `<Conclusion>`，说明它认为任务已完成
- 检测到 `<Conclusion>` 后立即终止

**实现要点**:
```python
# 在循环中
response = await self.llm_service.call(prompt=continue_prompt)

# 检查是否包含 Conclusion（提前完成）
if '<Conclusion>' in response and i < max_iterations:
    logger.info(f"Task completed early at iteration {i}")
    # 添加 response（包含 Conclusion）
    assistant_response += f"\n<Observation>\n{observation}\n</Observation>\n"
    assistant_response += response
    break  # 提前终止
```

**优势**:
- ✅ 简单直接，不需要额外的 LLM 调用
- ✅ 让 LLM 自己判断是否完成
- ✅ 符合科学方法流程（Conclusion = 结束）

**劣势**:
- ❌ 依赖 LLM 的判断，可能误判

---

### 方案 2: 添加 `<TaskStatus>` 标签（推荐 ⭐⭐⭐⭐）

**原理**:
- 在提示词中要求 LLM 在每个 `<Inference>` 后添加 `<TaskStatus>complete/incomplete</TaskStatus>`
- 检测到 `complete` 时，进入最后一轮生成 Conclusion

**实现要点**:

修改提示词（`create_continue_prompt`）:
```python
"""
Now provide:
<Inference>
Analyze the observation and decide next steps
</Inference>

<TaskStatus>complete/incomplete</TaskStatus>

If incomplete, then start a new cycle with:
<Hypothesis>...</Hypothesis>
<Model>...</Model>
<Experiment>...</Experiment>

If complete, provide:
<Conclusion>...</Conclusion>
"""
```

代码检测:
```python
response = await self.llm_service.call(prompt=continue_prompt)

# 提取任务状态
task_status = extract_tag_content(response, "TaskStatus")

if task_status and "complete" in task_status.lower():
    logger.info(f"Task marked as complete at iteration {i}")
    # 如果已经有 Conclusion，直接结束
    if '<Conclusion>' in response:
        assistant_response += f"\n<Observation>\n{observation}\n</Observation>\n"
        assistant_response += response
        break
    # 否则，触发最后一轮生成 Conclusion
    # ... 调用 final prompt
```

**优势**:
- ✅ 显式的任务完成判断
- ✅ 更可控，有明确的标签
- ✅ 可以区分"完成"和"继续"两种状态

**劣势**:
- ❌ 需要修改提示词
- ❌ 增加了一个额外的标签

---

### 方案 3: 基于 Observation 关键词匹配（推荐 ⭐⭐⭐）

**原理**:
- 分析 observation 中的成功标志
- 如："saved successfully", "test passed", "all tests passed", "submission created"
- 如果检测到成功标志，且没有错误，则进入最后一轮

**实现要点**:
```python
def _is_task_completed(observation: str) -> bool:
    """Check if observation indicates task completion."""
    success_indicators = [
        "successfully",
        "complete",
        "saved",
        "submission",
        "test passed",
        "all tests pass",
        "finished",
    ]

    error_indicators = [
        "error",
        "failed",
        "exception",
        "traceback",
    ]

    has_success = any(indicator in observation.lower() for indicator in success_indicators)
    has_error = any(indicator in observation.lower() for indicator in error_indicators)

    return has_success and not has_error

# 在循环中
if _is_task_completed(observation):
    logger.info(f"Task appears completed based on observation at iteration {i}")
    # 进入最后一轮生成 Conclusion
    is_final_round = True
```

**优势**:
- ✅ 基于实际执行结果判断
- ✅ 不依赖 LLM 的主观判断
- ✅ 适用于有明确成功标志的任务

**劣势**:
- ❌ 关键词可能不全面
- ❌ 可能误判（如日志中包含 "error" 但实际成功）

---

### 方案 4: 基于连续成功执行（推荐 ⭐⭐）

**原理**:
- 如果连续 N 轮（如 2 轮）代码都执行成功（无错误）
- 且每轮都有输出
- 认为任务可能已完成，询问 LLM 是否需要继续

**实现要点**:
```python
consecutive_successes = 0

# 在循环中
if exec_result.success:
    consecutive_successes += 1
else:
    consecutive_successes = 0

if consecutive_successes >= 2:
    logger.info(f"Consecutive successes detected, may complete early")
    # 可以提示 LLM 判断是否需要继续
```

**优势**:
- ✅ 基于执行成功率
- ✅ 避免不必要的重复

**劣势**:
- ❌ 成功执行不一定等于任务完成
- ❌ 阈值难以确定

---

## 综合推荐方案（混合策略）

**结合方案 1 + 方案 3**:

```python
# 伪代码
for i in range(2, max_iterations + 1):
    response = await llm.call(continue_prompt)

    # 策略1: 检查是否提前生成 Conclusion
    if '<Conclusion>' in response and i < max_iterations:
        logger.info(f"Early completion detected (Conclusion found) at iteration {i}")
        assistant_response += f"\n<Observation>\n{observation}\n</Observation>\n"
        assistant_response += response
        break

    # 添加 response
    assistant_response += f"\n<Observation>\n{observation}\n</Observation>\n"
    assistant_response += response

    # 如果不是最后一轮
    if i < max_iterations:
        experiment_code = extract_tag_content(response, "Experiment")

        if experiment_code:
            exec_result = await execute(experiment_code)
            observation = process(exec_result.stdout)

            # 策略2: 检查 observation 是否显示任务完成
            if _is_task_completed(observation):
                logger.info(f"Task completion detected in observation at iteration {i}")
                # 触发最后一轮
                final_prompt = create_final_prompt(...)
                final_response = await llm.call(final_prompt)
                assistant_response += f"\n<Observation>\n{observation}\n</Observation>\n"
                assistant_response += final_response
                break
        else:
            # 没有实验代码，停止
            break
```

**优势**:
- ✅ 双重检测机制，更可靠
- ✅ 既有 LLM 的主观判断，也有客观的执行结果
- ✅ 灵活性高

---

## 实现细节

### 1. 修改位置

**文件**: `modeling/workflows/search/scientific_workflow.py`

**关键点**:
- 在 `for i in range(2, max_iterations + 1):` 循环中添加提前终止逻辑
- 添加检测函数（如 `_is_task_completed()`, `_should_stop_early()`）

### 2. 日志记录

```python
logger.info(f"Early termination triggered at iteration {i}/{max_iterations}")
logger.info(f"Reason: <Conclusion> detected / Task completion indicators found")
```

### 3. 提示词调整（可选）

如果使用方案 2，需要修改 `create_continue_prompt()`:
- 添加 `<TaskStatus>` 标签说明
- 让 LLM 判断任务是否完成

### 4. 配置参数（可选）

```python
class AgentSearchConfig(BaseModel):
    max_iterations: int = 5  # 最大轮数
    min_iterations: int = 2  # 最小轮数（至少执行 2 轮才能提前终止）
    early_stop_enabled: bool = True  # 是否启用提前终止
```

---

## 测试场景

### 场景 1: 简单任务（第 2 轮完成）
```
轮 1: 计算平均值 → 成功
轮 2: 保存结果 → 成功，生成 <Conclusion>
检测: 提前终止 ✓
```

### 场景 2: 复杂任务（第 4 轮完成）
```
轮 1: 数据分析 → 成功
轮 2: 模型训练 → 成功
轮 3: 参数调优 → 成功
轮 4: 最终验证 → 成功，生成 <Conclusion>
检测: 提前终止 ✓
```

### 场景 3: 失败任务（需要全部 5 轮）
```
轮 1-4: 各种尝试 → 部分成功但未完成
轮 5: 最后一轮 → 生成 <Conclusion>（总结失败原因）
检测: 执行完所有轮次
```

---

## 推荐实施步骤

### 阶段 1: 最小化实现（方案 1）
1. 在循环中检测 `<Conclusion>` 标签
2. 如果在非最后一轮检测到，立即 break
3. 添加日志记录

**代码量**: ~5 行
**风险**: 低
**效果**: 中等

### 阶段 2: 增强版（方案 1 + 方案 3）
1. 添加 `_is_task_completed()` 函数
2. 检测 observation 中的成功标志
3. 结合 Conclusion 检测

**代码量**: ~20 行
**风险**: 低
**效果**: 高

### 阶段 3: 完整版（方案 2）
1. 修改提示词，添加 `<TaskStatus>` 标签
2. 提取并判断任务状态
3. 根据状态决定是否继续

**代码量**: ~40 行
**风险**: 中
**效果**: 最高

---

## 总结对比

| 方案 | 实现难度 | 准确性 | 代码量 | 推荐度 |
|------|---------|--------|--------|--------|
| 方案 1: 检测 Conclusion | 简单 | 中 | 5 行 | ⭐⭐⭐⭐⭐ |
| 方案 2: TaskStatus 标签 | 中等 | 高 | 40 行 | ⭐⭐⭐⭐ |
| 方案 3: 关键词匹配 | 简单 | 中 | 15 行 | ⭐⭐⭐ |
| 方案 4: 连续成功 | 简单 | 低 | 10 行 | ⭐⭐ |
| **混合方案 (1+3)** | **中等** | **高** | **~25 行** | **⭐⭐⭐⭐⭐** |

---

## 我的建议

**推荐使用混合方案（方案 1 + 方案 3）**:

1. **主要检测**: 检查 response 中是否有 `<Conclusion>` 标签
2. **辅助检测**: 检查 observation 中的成功标志
3. **保底机制**: 最多执行 max_iterations = 5 轮

**优势**:
- 实现简单（~25 行代码）
- 准确性高（双重检测）
- 风险低（保留最大轮数限制）
- 灵活性好（可以逐步扩展）

**实施优先级**:
1. 先实现方案 1（5 分钟）
2. 测试验证
3. 再添加方案 3（10 分钟）
4. 如果需要更高精度，考虑方案 2

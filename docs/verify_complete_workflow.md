# 验证 Scientific Workflow 完整执行

## 问题诊断

### 之前的问题
从错误日志看，workflow 在第1轮就失败了：
```
[2025-11-01 07:21:27,529] [scientific_workflow.py:77] --- Iteration 1: Initial analysis ---
[2025-11-01 07:21:27,529] [runner.py:163] Task 'dabench-0-mean-fare' failed: ...
```

**原因**: LLM 调用参数错误 + 代码提取包含 markdown

**结果**: 没有执行完整的多轮，所以没有 Conclusion

### 现在已修复
- ✅ LLM 调用：使用正确的 `self.llm_service.call(prompt=...)`
- ✅ 代码提取：自动清理 markdown 标记
- ✅ 应该可以完整执行多轮

## 验证步骤

### 1. 运行 workflow

```bash
python main.py --workflow scientific --benchmark mle \
    --data-dir "/home/aiops/liufan/projects/DSFlow/data/competitions" \
    --llm-model openai/deepseek-ai/DeepSeek-V3.1-Terminus \
    --task dabench-0-mean-fare
```

### 2. 检查日志输出

应该看到：
```
[INFO] --- Iteration 1: Initial analysis ---
[INFO] --- Iteration 2 ---
[INFO] --- Iteration 3 ---  # 或更多轮
[INFO] Scientific discovery workflow completed
```

### 3. 检查 summary.json

```bash
# 查找最新的运行目录
cd runs/modeling_run_dabench_0_mean_fare_*/artifacts/

# 查看 summary.json
cat summary.json | jq '.'

# 检查是否包含 Conclusion
cat summary.json | jq '.[1].content' | grep -o "<Conclusion>"
```

### 4. 验证完整性

```bash
# 统计标签数量
cat summary.json | jq -r '.[1].content' | grep -o "<[^/>]*>" | sort | uniq -c
```

期望输出（max_iterations=3）：
```
  1 <Phenomenon>
  2 <Hypothesis>
  2 <Model>
  2 <Experiment>
  3 <Observation>
  2 <Inference>
  1 <Conclusion>   # ← 应该有这个！
```

## 代码逻辑确认

### 完整流程（max_iterations=3）

```python
assistant_response = ""

# 第1轮
response1 = llm.call(initial_prompt)
# → <Phenomenon><Hypothesis><Model><Experiment>
assistant_response += response1
# 执行 → observation1

# 第2轮 (i=2, i < max_iterations)
assistant_response += f"<Observation>{observation1}</Observation>"
response2 = llm.call(continue_prompt)
# → <Inference><Hypothesis><Model><Experiment>
assistant_response += response2
# 执行 → observation2

# 第3轮 (i=3, i == max_iterations)
assistant_response += f"<Observation>{observation2}</Observation>"
response3 = llm.call(final_prompt)
# → <Inference><Conclusion>  ← 包含 Conclusion
assistant_response += response3  # ← 添加到 assistant_response
assistant_response += f"<Observation>{observation2}</Observation>"

# 保存
conversation = [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": assistant_response}  # ← 包含 Conclusion
]
```

### 关键代码（scientific_workflow.py）

```python
# 第109行
response = await self.llm_service.call(prompt=continue_prompt)

# 第112-113行
assistant_response += f"\n<Observation>\n{observation}\n</Observation>\n"
assistant_response += response  # ← response 包含 Conclusion（最后一轮）

# 第129-132行
self.conversation.append({
    "role": "assistant",
    "content": assistant_response  # ← 保存完整内容
})
```

## 可能的问题

### 问题1: max_iterations 太小
```python
# 如果 max_iterations = 1 或 2
# 不会执行到最后一轮，没有 Conclusion
```

**解决**: 确保 `max_iterations >= 3`

### 问题2: 提前 break
```python
# 第117-123行
if i < max_iterations:
    experiment_code = extract_tag_content(response, "Experiment")
    if experiment_code:
        ...
    else:
        logger.warning(f"No experiment in iteration {i}, stopping")
        break  # ← 提前退出
```

**原因**: 倒数第二轮 LLM 没有生成 `<Experiment>` 标签

**解决**: 优化提示词，或检查 LLM 输出

### 问题3: LLM 没有生成 Conclusion

**原因**:
- 提示词不清晰
- LLM 输出被截断
- 格式错误

**解决**:
- 检查 LLM 的原始输出
- 增加 max_tokens
- 优化提示词

## 快速测试

运行测试脚本验证逻辑：

```bash
python debug_conclusion_saving.py
```

期望输出：
```
✓ <Conclusion>: 1 次
✓ Conclusion 已正确添加
```

## 总结

**代码逻辑是正确的**，Conclusion 应该被保存。

如果实际运行中没有 Conclusion，检查：
1. ✅ max_iterations >= 3
2. ✅ 所有轮次都成功执行（没有提前 break）
3. ✅ LLM 正确生成了 `<Conclusion>` 标签

**现在 bug 已修复，应该可以正常保存 Conclusion 了**！

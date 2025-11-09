# 对话历史传递修复

## 问题描述

之前的实现中，每次调用 LLM 时只发送单条消息，没有包含之前的对话历史。这导致模型在多轮对话中失去上下文。

## 修改内容

### 1. 修改 `_call_llm` 方法 ([src/agent.py:65-109](src/agent.py#L65-L109))

**之前**:
```python
def _call_llm(self, prompt: str, temperature: Optional[float] = None) -> str:
    # 只发送单条消息
    "messages": [{"role": "user", "content": prompt}]
```

**现在**:
```python
def _call_llm(
    self,
    prompt: str = None,
    messages: List[Dict[str, str]] = None,
    temperature: Optional[float] = None
) -> str:
    """Call LLM endpoint with conversation history support."""

    # 支持两种模式
    if messages is not None:
        # 使用完整对话历史
        api_messages = messages
    elif prompt is not None:
        # 第一轮：单条消息
        api_messages = [{"role": "user", "content": prompt}]
```

### 2. 修改 `run_episode` 中的调用逻辑 ([src/agent.py:294-318](src/agent.py#L294-L318))

**之前**:
```python
# 每轮都只发送新生成的 prompt
response = self._call_llm(prompt, temperature=llm_temperature)
```

**现在**:
```python
# 第一轮：发送初始 prompt
if num_turns == 1:
    current_messages = [{"role": "user", "content": prompt}]
else:
    # 后续轮：使用完整对话历史
    current_messages = conversation.copy()

# 使用完整历史调用 LLM
response = self._call_llm(messages=current_messages, temperature=llm_temperature)
```

### 3. 删除多余的 prompt 生成 ([src/agent.py:384-385](src/agent.py#L384-L385))

**之前**:
```python
# 执行后重新生成 prompt
prompt = create_continue_prompt(
    self._format_conversation(conversation),
    observation,
    num_turns,
    self.max_turns
)
```

**现在**:
```python
# 不需要重新生成 prompt
# observation 已经作为用户消息添加到 conversation
# 下一轮会自动包含在 messages 中
```

### 4. 简化错误处理 ([src/agent.py:340-348](src/agent.py#L340-L348))

**之前**:
```python
if not experiment:
    prompt = create_continue_prompt(...)
    continue
```

**现在**:
```python
if not experiment:
    # 直接添加反馈消息到对话历史
    feedback_msg = {
        "role": "user",
        "content": "No experiment code was provided. Please provide an <Experiment> block..."
    }
    conversation.append(feedback_msg)
    continue
```

## 对话流程

### 完整的多轮对话示例

```python
# Turn 1
messages = [
    {"role": "user", "content": "<initial prompt with task description>"}
]
# LLM response → added to conversation

# Turn 2
messages = [
    {"role": "user", "content": "<initial prompt>"},
    {"role": "assistant", "content": "<LLM response with Experiment>"},
    {"role": "user", "content": "<Observation>\nExecution succeeded...\n</Observation>"}
]
# LLM response → added to conversation

# Turn 3
messages = [
    {"role": "user", "content": "<initial prompt>"},
    {"role": "assistant", "content": "<first response>"},
    {"role": "user", "content": "<first observation>"},
    {"role": "assistant", "content": "<second response>"},
    {"role": "user", "content": "<second observation>"}
]
# ... and so on
```

## 优势

### 1. **保持上下文连贯性**
- 模型能看到所有之前的实验和观察
- 可以基于历史结果做出更好的决策

### 2. **符合 OpenAI API 标准**
- 使用标准的 messages 格式
- 明确区分 user 和 assistant 角色

### 3. **简化代码逻辑**
- 不需要手动格式化对话历史为文本
- 不需要每轮重新生成 continue prompt
- conversation 列表直接对应 API messages

### 4. **更好的调试体验**
- Telemetry 中保存完整的 messages 历史
- 可以清晰看到每轮的输入输出

## Conversation 结构

```python
# 初始化时就包含初始 prompt
conversation = [
    {"role": "user", "content": "<initial_prompt>"}
]

# Turn 1 后
conversation = [
    {"role": "user", "content": "<initial_prompt>"},
    {"role": "assistant", "content": "<response_1>"},
    {"role": "user", "content": "<observation_1>"}
]

# Turn 2 后
conversation = [
    {"role": "user", "content": "<initial_prompt>"},
    {"role": "assistant", "content": "<response_1>"},
    {"role": "user", "content": "<observation_1>"},
    {"role": "assistant", "content": "<response_2>"},
    {"role": "user", "content": "<observation_2>"}
]
# ... 以此类推
```

## 验证

运行测试确认修改正常工作：

```bash
cd /home/aiops/liufan/projects/DeepModeling/examples/deepmodeling-rl
python3 -c "from src.agent import SimpleDeepModelingAgent; agent = SimpleDeepModelingAgent('http://localhost:8000', 'test'); print('✓')"
```

## Telemetry 记录格式

`conversation.jsonl` 中每个事件包含完整的 messages：

```json
{
  "event": "llm_call",
  "turn": 1,
  "timestamp": "2025-11-09T...",
  "model": "...",
  "payload": {
    "temperature": 0.0,
    "max_tokens": 4096,
    "messages": [
      {"role": "user", "content": "<initial_prompt>"}
    ]
  }
}

// Turn 2 会包含完整历史
{
  "event": "llm_call",
  "turn": 2,
  "payload": {
    "messages": [
      {"role": "user", "content": "<initial_prompt>"},
      {"role": "assistant", "content": "<response_1>"},
      {"role": "user", "content": "<observation_1>"}
    ]
  }
}
```

**关键点**: telemetry 记录的是**实际发送给 LLM 的完整 messages**，包括所有历史对话。

## 注意事项

1. **Token 使用**: 由于每轮都发送完整历史，token 消耗会随轮次增加
2. **最大上下文**: 需要注意不超过模型的最大 context length
3. **初始 prompt**: 仍使用 `create_initial_prompt` 生成完整的科学方法指导
4. **Telemetry 真实性**: conversation.jsonl 记录的是真实发送给 LLM 的内容，便于调试和重现

## 与 Modeling Runner 的一致性

这个修改使 RL agent 的对话管理方式更接近标准的 LLM 应用实践，虽然 modeling runner 使用 workflow 驱动，但两者都正确维护了对话历史。

# Telemetry 记录验证 - 模型实际接收的消息

## 问题

需要验证：**telemetry 中记录的 messages 是否与模型实际接收到的完全一致？**

## 代码流程分析

### 关键代码路径 ([src/agent.py:293-313](src/agent.py#L293-L313))

```python
# Step 1: 准备要发送的消息
current_messages = conversation.copy()  # Line 296

# Step 2: 记录到 telemetry
telemetry_log.append({
    "event": "llm_call",
    "turn": num_turns,
    "payload": {
        "messages": current_messages,  # Line 307 - 记录
    }
})

# Step 3: 发送给 LLM
response = self._call_llm(messages=current_messages, ...)  # Line 313 - 发送
```

### _call_llm 内部 ([src/agent.py:84-98](src/agent.py#L84-L98))

```python
def _call_llm(self, messages=None, ...):
    api_messages = messages  # Line 86 - 直接赋值

    response = requests.post(
        f"{self.llm_endpoint}/v1/chat/completions",
        json={
            "messages": api_messages,  # Line 98 - 发送
        }
    )
```

## 验证结果

### ✅ 代码级验证

```python
# 使用同一个对象
telemetry_recorded = current_messages
api_sent = current_messages  # 通过 _call_llm 的 messages 参数

# 验证：
telemetry_recorded is api_sent  # True - 完全是同一个对象
```

### ✅ 数据流验证

```
conversation (list)
    ↓ .copy() (浅拷贝)
current_messages (list)
    ↓ (分支1) 记录到 telemetry
    ↓ (分支2) 传给 _call_llm
    ↓ (在 _call_llm 中) 直接赋值给 api_messages
    ↓ 序列化到 JSON
    ↓ 发送给 LLM API
```

**关键点**：
- telemetry 和 API 使用的是**同一个 Python 对象** (`current_messages`)
- JSON 序列化发生在 `requests.post()` 时，两者都经过相同的序列化过程
- **没有任何代码修改 `current_messages`**

### ✅ 实际示例

#### Turn 1
```json
// telemetry 记录
{
  "event": "llm_call",
  "turn": 1,
  "payload": {
    "messages": [
      {"role": "user", "content": "<initial_prompt>"}
    ]
  }
}

// API 实际接收（完全一致）
{
  "messages": [
    {"role": "user", "content": "<initial_prompt>"}
  ]
}
```

#### Turn 2（修复后）
```json
// telemetry 记录
{
  "event": "llm_call",
  "turn": 2,
  "payload": {
    "messages": [
      {"role": "user", "content": "<initial_prompt>"},     // ✓ 完整历史
      {"role": "assistant", "content": "<response_1>"},
      {"role": "user", "content": "<observation_1>"}
    ]
  }
}

// API 实际接收（完全一致）
{
  "messages": [
    {"role": "user", "content": "<initial_prompt>"},      // ✓ 完整历史
    {"role": "assistant", "content": "<response_1>"},
    {"role": "user", "content": "<observation_1>"}
  ]
}
```

## 一致性保证

### 1. **对象级一致性**
- ✅ telemetry 和 API 使用同一个 `current_messages` 对象
- ✅ 没有中间修改

### 2. **序列化一致性**
- ✅ telemetry 保存时使用 `json.dumps(telemetry_log)`
- ✅ API 发送时使用 `requests.post(json={...})`，内部也是 `json.dumps()`
- ✅ 两者使用相同的 JSON 序列化器

### 3. **时序一致性**
```python
# 代码执行顺序
1. current_messages = conversation.copy()     # 创建快照
2. telemetry_log.append({..., current_messages})  # 记录快照
3. _call_llm(messages=current_messages)       # 使用同一个快照
4. conversation.append(response)              # 添加回复（不影响快照）
```

**关键**：在记录和发送之间，`current_messages` **不会被修改**。

## 如何验证

### 方法 1: 代码审查
查看代码确认没有修改 `current_messages`：
```bash
grep -A 10 "current_messages" src/agent.py
# 确认只有 .copy() 和传递，没有修改操作
```

### 方法 2: 对比 telemetry 和日志
如果 LLM API 有请求日志，可以对比：
```bash
# telemetry 中的 messages
jq '.payload.messages' conversation.jsonl

# API 日志中的 messages（如果有）
# 应该完全一致
```

### 方法 3: 添加调试日志
```python
# 在 src/agent.py 中添加
import hashlib

# 记录前
msg_hash_before = hashlib.md5(json.dumps(current_messages, sort_keys=True).encode()).hexdigest()
telemetry_log.append({..., "messages": current_messages})

# 发送前
msg_hash_send = hashlib.md5(json.dumps(current_messages, sort_keys=True).encode()).hexdigest()
assert msg_hash_before == msg_hash_send, "Messages changed!"
```

## 结论

### ✅ **是的，完全一致**

**模型实际接收的 messages** 与 **telemetry 记录的 messages** **完全一致**，因为：

1. **使用同一个对象** - `current_messages` 在记录和发送时是同一个引用
2. **没有中间修改** - 在创建快照后，没有任何代码修改它
3. **相同的序列化** - 都使用 Python 的 `json.dumps()`
4. **正确的时序** - 快照在添加新消息之前创建

### 可追溯性

通过 telemetry 中的 `conversation.jsonl`，你可以：

- ✅ **精确重现** 每次 LLM 调用的输入
- ✅ **调试问题** 看到模型接收到的确切内容
- ✅ **验证历史** 确认对话上下文是否正确传递
- ✅ **分析行为** 理解模型为什么给出某个回复

### 注意事项

唯一的例外情况：
- 如果 `conversation.copy()` 中的字典对象在记录后被修改（**当前代码不会发生**）
- 如果 `_call_llm` 修改了传入的 messages（**当前代码不会发生**）

当前实现中，这两种情况都不存在，所以记录是 100% 准确的。

## 最佳实践建议

为了确保长期一致性，建议：

1. **不要修改 current_messages** - 保持它是只读快照
2. **使用深拷贝（如果需要）** - 虽然当前浅拷贝足够
3. **添加断言** - 在关键路径添加验证
4. **保留日志** - telemetry 是调试的关键证据

## 相关文档

- [CONVERSATION_HISTORY.md](CONVERSATION_HISTORY.md) - 对话历史实现
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - 项目结构
- [CHANGES.md](CHANGES.md) - 修改日志

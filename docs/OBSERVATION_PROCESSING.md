# Observation 处理机制

## 问题

执行实验时，输出结果可能非常长，例如：
- 训练模型时有大量重复的 epoch 日志
- 大规模数据处理产生冗长输出
- 错误堆栈跟踪很长

这会导致：
- Context 溢出（超过 LLM 的 token 限制）
- 降低处理效率
- 难以关注关键信息

## 解决方案

参考 `modeling/utils/context.py`，使用两个工具函数处理 observation：

### 1. summarize_repetitive_logs()

**功能**: 总结重复的连续日志行

**示例**:
```python
# 输入（重复的训练日志）
Epoch 1/100 - loss: 0.5234
Epoch 2/100 - loss: 0.4876
Epoch 3/100 - loss: 0.4653
...
Epoch 100/100 - loss: 0.4001

# 如果某行重复 >= 3 次，会被总结
<Epoch 1/100 - loss: 0.5234 (repeated 100 times)>
```

### 2. truncate_output()

**功能**: 截断超长输出，保留开头和结尾

**参数**:
- `max_chars`: 最大字符数（默认 16,000）

**示例**:
```python
# 输入: 117,894 字符的超长输出
Line 1: ...
Line 2: ...
...
Line 1000: ...

# 输出: 16,000 字符，保留开头和结尾
Line 1: ...
Line 2: ...
[前 8000 字符]

... [TRUNCATED: 101,894 characters omitted to prevent context overflow] ...

Line 998: ...
Line 999: ...
Line 1000: ...
[后 8000 字符]
```

## 实现

### 修改位置

**文件**: `modeling/workflows/search/scientific_workflow.py`

### 添加导入

```python
from modeling.utils.context import summarize_repetitive_logs, truncate_output
```

### 处理 observation

**第1轮（第92-97行）**:
```python
# Execute experiment
exec_result = await self.execute_op(code=experiment_code, mode="script")
raw_observation = exec_result.stdout if exec_result.success else exec_result.stderr

# Process observation: summarize repetitive logs and truncate if too long
observation = summarize_repetitive_logs(raw_observation)
observation = truncate_output(observation)
```

**第2-N轮（第124-129行）**:
```python
exec_result = await self.execute_op(code=experiment_code, mode="script")
raw_observation = exec_result.stdout if exec_result.success else exec_result.stderr

# Process observation: summarize repetitive logs and truncate if too long
observation = summarize_repetitive_logs(raw_observation)
observation = truncate_output(observation)
```

## 处理流程

```
原始输出 (可能很长)
    ↓
summarize_repetitive_logs()  # 总结重复行
    ↓
truncate_output()  # 如果还是太长，截断
    ↓
处理后的 observation (不超过 16,000 字符)
```

## 配置参数

在 `modeling/utils/context.py` 中定义：

```python
MAX_OUTPUT_CHARS = 16000  # 最大字符数
```

可以根据需要调整这个值。

## 效果对比

### 处理前

```xml
<Observation>
Epoch 1/1000 - loss: 0.5234, accuracy: 0.7821
Epoch 2/1000 - loss: 0.4876, accuracy: 0.8012
Epoch 3/1000 - loss: 0.4653, accuracy: 0.8143
...（1000 行）
Epoch 1000/1000 - loss: 0.4001, accuracy: 0.9234
Training complete!
</Observation>
```
**问题**: 太长，可能超过 LLM context 限制

### 处理后（总结）

```xml
<Observation>
<Epoch 1/1000 - loss: 0.5234, accuracy: 0.7821 (repeated 1000 times)>
Training complete!
</Observation>
```
**如果每行都不同，则总结不起作用**

### 处理后（截断）

```xml
<Observation>
Epoch 1/1000 - loss: 0.5234, accuracy: 0.7821
Epoch 2/1000 - loss: 0.4876, accuracy: 0.8012
...
Epoch 100/1000 - loss: 0.4543, accuracy: 0.8234

... [TRUNCATED: 85,000 characters omitted to prevent context overflow] ...

Epoch 901/1000 - loss: 0.4103, accuracy: 0.9134
...
Epoch 1000/1000 - loss: 0.4001, accuracy: 0.9234
Training complete!
</Observation>
```
**优势**: 保留了开头（初始 epoch）和结尾（最终 epoch + 完成信息）

## 实际应用场景

### 1. 模型训练

**原始输出**: 1000 个 epoch 的训练日志
**处理后**: 保留前 50 epoch + 后 50 epoch + 最终结果

### 2. 大规模数据分析

**原始输出**: 打印了 10,000 行数据
**处理后**: 保留前 4,000 行 + 后 4,000 行

### 3. 错误信息

**原始输出**: 超长的堆栈跟踪
**处理后**: 保留关键的错误信息（开头和结尾）

## 日志

当 observation 被截断时，会记录警告日志：

```
[WARNING] Output truncated from 117894 to 16000 characters.
```

## 测试

运行测试脚本验证功能：

```bash
python test_observation_truncation.py
```

## 优势

✅ **防止 context 溢出** - 限制 observation 大小
✅ **保留关键信息** - 开头和结尾通常最重要
✅ **减少 token 使用** - 降低 LLM API 成本
✅ **提高效率** - 更快的处理速度
✅ **自动处理** - 无需手动干预

## 总结

通过组合使用 `summarize_repetitive_logs()` 和 `truncate_output()`，scientific workflow 现在可以：

1. 自动处理超长的实验输出
2. 总结重复的训练日志
3. 截断过长的内容，保留最重要的部分
4. 确保不会超过 LLM 的 context 限制

这使得 workflow 可以处理更复杂的机器学习任务，如模型训练、超参数调优等。

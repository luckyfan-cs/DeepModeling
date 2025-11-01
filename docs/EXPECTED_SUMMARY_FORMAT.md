# Scientific Workflow - 预期的 summary.json 格式

## 完整的多轮对话格式

### summary.json 结构

```json
[
  {
    "role": "user",
    "content": "任务描述\n\nI/O Requirements:\n输出要求"
  },
  {
    "role": "assistant",
    "content": "完整的多轮科学发现过程（所有轮次拼接在一起）"
  }
]
```

## 详细示例（3轮迭代）

### 完整的 content 字段内容

```xml
<Phenomenon>
第1轮：问题观察
泰坦尼克数据集包含乘客信息和票价数据
</Phenomenon>

<Hypothesis>
第1轮：假设
可以使用 pandas 计算平均票价
</Hypothesis>

<Model>
第1轮：模型
mean_fare = df['Fare'].mean()
</Model>

<Experiment>
第1轮：实验代码
import pandas as pd
df = pd.read_csv('train.csv')
mean_fare = df['Fare'].mean()
print(f'Mean fare: {mean_fare}')
</Experiment>

<Observation>
第1轮：观察结果（系统自动插入）
Mean fare: 32.204208
</Observation>

<Inference>
第2轮：推理
平均票价为 32.20，需要保存到文件
</Inference>

<Hypothesis>
第2轮：新假设
将结果保存到 output.txt
</Hypothesis>

<Model>
第2轮：模型
使用 Python 文件写入
</Model>

<Experiment>
第2轮：实验代码
with open('output.txt', 'w') as f:
    f.write('32.20')
print('Saved to output.txt')
</Experiment>

<Observation>
第2轮：观察结果（系统自动插入）
Saved to output.txt
</Observation>

<Inference>
第3轮：最终推理
成功保存结果到文件
</Inference>

<Conclusion>
第3轮：结论
泰坦尼克数据集的平均票价为 32.20 美元，已成功保存到 output.txt
</Conclusion>

<Observation>
第3轮：最终观察（系统自动插入）
Saved to output.txt
</Observation>
```

## 标签出现次数统计

| 标签 | 出现次数 | 说明 |
|------|---------|------|
| `<Phenomenon>` | 1 | 只在第1轮出现 |
| `<Hypothesis>` | N-1 | 每轮都有（除了最后一轮） |
| `<Model>` | N-1 | 每轮都有（除了最后一轮） |
| `<Experiment>` | N-1 | 每轮都有（除了最后一轮） |
| `<Observation>` | N | 每次实验后都有，最后重复一次 |
| `<Inference>` | N-1 | 从第2轮开始每轮都有 |
| `<Conclusion>` | 1 | 只在最后一轮 |

其中 N = max_iterations

## 代码实现逻辑

```python
assistant_response = ""

# 第1轮
response1 = await llm.call(initial_prompt)
# → <Phenomenon><Hypothesis><Model><Experiment>
assistant_response += response1
# 执行实验 → observation1

# 第2轮
assistant_response += f"<Observation>{observation1}</Observation>"
response2 = await llm.call(continue_prompt)
# → <Inference><Hypothesis><Model><Experiment>
assistant_response += response2
# 执行实验 → observation2

# 第3轮（最后）
assistant_response += f"<Observation>{observation2}</Observation>"
response3 = await llm.call(final_prompt)
# → <Inference><Conclusion>
assistant_response += response3
assistant_response += f"<Observation>{observation2}</Observation>"

# 保存
conversation = [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": assistant_response}  # 完整的多轮内容
]
```

## 验证要点

检查 summary.json 是否正确：

```python
import json

with open('summary.json', 'r') as f:
    data = json.load(f)

content = data[1]['content']  # assistant 的完整回复

# 验证多轮
assert '<Phenomenon>' in content, "应包含 Phenomenon"
assert '<Conclusion>' in content, "应包含 Conclusion"
assert content.count('<Experiment>') >= 2, "应有多个 Experiment"
assert content.count('<Observation>') >= 2, "应有多个 Observation"
```

## 常见问题

### Q: 为什么只有1轮？

可能原因：
1. `max_iterations = 1` （默认应该是3或5）
2. 第2轮没有生成 `<Experiment>` 标签，提前终止
3. 代码执行失败，workflow 提前返回

### Q: Observation 为什么重复？

最后一轮会重复添加最终的 Observation，这是有意为之，确保格式完整。

### Q: 如何确认是多轮？

查看：
- `<Hypothesis>` 和 `<Model>` 出现多次
- `<Observation>` 出现多次
- 有 `<Inference>` 标签（从第2轮开始）

## 实际文件位置

```
runs/modeling_run_YYYYMMDD_HHMMSS/artifacts/
├── summary.json           # 标准对话格式
└── summary_readable.txt   # 人类可读格式
```

## 调试提示

如果发现只有1轮，检查：

```bash
# 1. 查看配置
grep -r "max_iterations" modeling/config.py

# 2. 查看日志
# 应该看到多个 "--- Iteration N ---"

# 3. 查看保存的文件
cat runs/modeling_run_*/artifacts/summary.json | jq '.[1].content' | grep -c "<Experiment>"
# 应该 >= 2
```

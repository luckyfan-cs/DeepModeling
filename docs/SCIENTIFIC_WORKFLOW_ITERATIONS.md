# Scientific Workflow 迭代轮数说明

## 轮数控制机制

### 配置位置

轮数由 `max_iterations` 参数控制，定义在：

**文件**: `modeling/config.py`
```python
class AgentSearchConfig(BaseModel):
    max_iterations: int = 5  # 默认 5 轮
```

### 代码读取

**文件**: `modeling/workflows/search/scientific_workflow.py`
```python
max_iterations = self.agent_config.get("search", {}).get("max_iterations", 3)
```

⚠️ **注意**: 代码中的默认值是 3，但配置中的默认值是 5，存在不一致。

## 每轮包含的内容

### 第 1 轮（初始分析）
```
User Message (用户消息):
  - 任务描述
  - I/O 要求

LLM 生成:
  <Phenomenon>问题分析</Phenomenon>
  <Hypothesis>假设</Hypothesis>
  <Model>模型</Model>
  <Experiment>代码</Experiment>

系统执行:
  - 执行 <Experiment> 中的代码
  - 获取执行结果

系统插入:
  <Observation>执行结果</Observation>
```

### 第 2 到 N-1 轮（迭代改进）
```
LLM 看到:
  - 之前的完整对话历史
  - 最新的 <Observation>

LLM 生成:
  <Inference>分析观察结果</Inference>
  <Hypothesis>新的或改进的假设</Hypothesis>
  <Model>更新的模型</Model>
  <Experiment>新代码</Experiment>

系统执行:
  - 执行新的 <Experiment>
  - 获取新的执行结果

系统插入:
  <Observation>新的执行结果</Observation>
```

### 第 N 轮（最终轮）
```
LLM 看到:
  - 完整对话历史
  - 最后一次 <Observation>

LLM 生成:
  <Inference>最终分析</Inference>
  <Conclusion>综合所有发现，给出最终答案</Conclusion>

系统插入:
  <Observation>最后的执行结果</Observation>
```

## 如何设置轮数

### 方法 1: 通过配置文件

创建或修改 `config.yaml`:
```yaml
agent:
  search:
    max_iterations: 5  # 设置为 5 轮
```

### 方法 2: 通过代码

```python
from modeling.config import ModelingConfig, AgentConfig, AgentSearchConfig

config = ModelingConfig()
config.agent.search.max_iterations = 5  # 设置为 5 轮
```

### 方法 3: 在测试脚本中

```python
config = ModelingConfig(
    llm=LLMConfig(model="gpt-4o-mini"),
    workflow=WorkflowConfig(name="scientific")
)

# 设置轮数
config.agent.search.max_iterations = 3
```

## 轮数建议

| 场景 | 推荐轮数 | 说明 |
|------|---------|------|
| **快速测试** | 2-3 轮 | 验证工作流是否正常 |
| **简单问题** | 3-4 轮 | 直接的数据分析任务 |
| **中等复杂度** | 5-6 轮 | 需要多次尝试和改进 |
| **复杂研究** | 7-10 轮 | 需要深入探索和优化 |

## 完整流程示例（3 轮）

```
轮数 1:
  用户: "分析泰坦尼克数据集，计算平均票价"
  LLM: <Phenomenon> <Hypothesis> <Model> <Experiment>代码1</Experiment>
  系统: 执行代码1 → <Observation>结果1</Observation>

轮数 2:
  LLM: <Inference> <Hypothesis> <Model> <Experiment>代码2</Experiment>
  系统: 执行代码2 → <Observation>结果2</Observation>

轮数 3 (最终):
  LLM: <Inference> <Conclusion>最终答案</Conclusion>
  系统: <Observation>最终结果</Observation>
```

## 代码执行逻辑

```python
# 第 1 轮
response = await llm_service.call(initial_prompt)
experiment_code = extract_tag_content(response, "Experiment")
exec_result = await execute_op(code=experiment_code)
observation = exec_result.stdout

# 第 2 到 max_iterations 轮
for i in range(2, max_iterations + 1):
    # 添加上一轮的 Observation
    assistant_response += f"<Observation>{observation}</Observation>"

    # 获取继续提示
    continue_prompt = create_continue_prompt(
        conversation_history=assistant_response,
        execution_output=observation,
        iteration=i,
        max_iterations=max_iterations
    )

    response = await llm_service.call(continue_prompt)

    if i < max_iterations:
        # 非最后一轮：提取并执行实验
        experiment_code = extract_tag_content(response, "Experiment")
        exec_result = await execute_op(code=experiment_code)
        observation = exec_result.stdout
    else:
        # 最后一轮：只添加 Observation，不再执行
        assistant_response += f"<Observation>{observation}</Observation>"
```

## 提前终止

如果在中间轮次没有找到 `<Experiment>` 标签，工作流会提前终止：

```python
if i < max_iterations:
    experiment_code = extract_tag_content(response, "Experiment")
    if experiment_code:
        # 执行实验
    else:
        logger.warning(f"No experiment in iteration {i}, stopping")
        break  # 提前终止
```

## 实际示例输出

设置 `max_iterations = 3`:

```json
[
  {
    "role": "user",
    "content": "计算泰坦尼克数据集的平均票价\n\nI/O Requirements:\n保存到 output.txt"
  },
  {
    "role": "assistant",
    "content": "<Phenomenon>\n数据集包含乘客信息和票价\n</Phenomenon>\n\n<Hypothesis>\n平均票价可以通过 pandas 计算\n</Hypothesis>\n\n<Model>\nmean_fare = df['Fare'].mean()\n</Model>\n\n<Experiment>\nimport pandas as pd\ndf = pd.read_csv('train.csv')\nmean_fare = df['Fare'].mean()\nprint(f'Mean fare: {mean_fare}')\n</Experiment>\n\n<Observation>\nMean fare: 32.204208\n</Observation>\n\n<Inference>\n平均票价为 32.20，需要保存到文件\n</Inference>\n\n<Hypothesis>\n保存结果到 output.txt\n</Hypothesis>\n\n<Model>\n使用 Python 文件写入\n</Model>\n\n<Experiment>\nwith open('output.txt', 'w') as f:\n    f.write('32.20')\nprint('Saved')\n</Experiment>\n\n<Observation>\nSaved\n</Observation>\n\n<Inference>\n成功保存结果\n</Inference>\n\n<Conclusion>\n泰坦尼克数据集的平均票价为 32.20，已保存到 output.txt\n</Conclusion>"
  }
]
```

## 总结

- **默认值**: 5 轮（配置文件）/ 3 轮（代码回退）
- **配置路径**: `config.agent.search.max_iterations`
- **每轮包含**: Phenomenon/Hypothesis/Model/Experiment → Observation → Inference
- **最后一轮**: 不执行新实验，生成 Conclusion
- **提前终止**: 如果没有 Experiment 标签

调整 `max_iterations` 来控制科学发现的深度和迭代次数！

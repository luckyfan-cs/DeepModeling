# Scientific Workflow 所有 Bug 修复总结

## 修复概览

在实现 Scientific Workflow 过程中发现并修复了 2 个关键 bug：

1. **LLM 调用参数错误** - 没有参考 AIDE 实现，自己创建了错误的包装方法
2. **代码提取包含 Markdown** - 从 `<Experiment>` 标签提取的代码包含 ``` 标记

---

## Bug #1: LLM 调用参数错误

### 问题
```
TypeError: LLMService.call() got an unexpected keyword argument 'messages'
```

### 根本原因
❌ **闭门造车** - 没有参考 AIDE workflow 的实现，自己创建了错误的 `_call_llm()` 方法

```python
# ❌ 错误实现
async def _call_llm(self, prompt: str) -> str:
    messages = [{"role": "user", "content": prompt}]
    response = await self.llm_service.call(
        messages=messages,      # 不存在的参数
        temperature=0.7,        # 不支持
        response_format=None    # 不支持
    )
    return response
```

### 解决方案
✅ **参考 AIDE** - 直接使用 `llm_service`，删除不必要的包装方法

```python
# ✅ 正确实现
response = await self.llm_service.call(prompt=initial_prompt)
```

### 修改文件
- `modeling/workflows/search/scientific_workflow.py`
  - 删除 `_call_llm()` 方法
  - 直接使用 `self.llm_service.call(prompt=...)`

### 学到的教训
**不要闭门造车！应该：**
- ✅ 参考 AIDE workflow 的实现
- ✅ 使用已有的模块和 operators
- ✅ 遵循项目现有模式

详见: [BUGFIX_SCIENTIFIC_WORKFLOW.md](BUGFIX_SCIENTIFIC_WORKFLOW.md)

---

## Bug #2: 代码提取包含 Markdown 标记

### 问题
```
File "..._sandbox_script_....py", line 1
    ```python
    ^
SyntaxError: invalid syntax
```

### 根本原因
LLM 在 `<Experiment>` 标签内仍然使用 markdown 格式：

```xml
<Experiment>
```python
import pandas as pd
df = pd.read_csv('data.csv')
```
</Experiment>
```

### 解决方案

#### 1. 添加清理函数
```python
def _clean_code_block(text: str) -> str:
    """Remove markdown code block markers from code."""
    import re
    # Remove ```python or ```py or ``` at the start
    text = re.sub(r'^```(?:python|py)?\s*\n?', '', text, flags=re.MULTILINE)
    # Remove ``` at the end
    text = re.sub(r'\n?```\s*$', '', text)
    return text.strip()
```

#### 2. 自动清理
```python
def extract_tag_content(text: str, tag: str) -> Optional[str]:
    # ... extract content ...
    if tag == "Experiment":
        content = _clean_code_block(content)
    return content
```

#### 3. 更新提示词
```
IMPORTANT: In <Experiment> tags, write pure Python code directly.
Do NOT use markdown code blocks like ```python.
```

### 修改文件
- `modeling/prompts/scientific_prompt.py`
  - 添加 `_clean_code_block()` 函数
  - 修改 `extract_tag_content()` 自动清理
  - 更新提示词

### 学到的教训
**防御式编程：**
- ✅ 提示词层面指示 LLM
- ✅ 代码层面自动清理
- ✅ 双重保护机制
- ✅ 参考已有的 `parse_plan_and_code()` 实现

详见: [BUGFIX_CODE_EXTRACTION.md](BUGFIX_CODE_EXTRACTION.md)

---

## 完整修改列表

### 文件修改
1. **modeling/workflows/search/scientific_workflow.py**
   - 删除 `_call_llm()` 方法
   - 改用直接调用 `self.llm_service.call()`

2. **modeling/prompts/scientific_prompt.py**
   - 添加 `_clean_code_block()` 函数
   - 修改 `extract_tag_content()` 自动清理 Experiment 标签
   - 更新提示词明确要求纯 Python 代码

### 依赖安装
```bash
pip install tenacity
```

---

## 验证测试

### 测试 1: LLM 调用
```bash
python test_llm_call_fix.py
```
```
✓ LLMService.call 签名验证通过
✓ Scientific 直接使用 llm_service.call()
✓ 不使用包装方法
✓ 修复完成！
```

### 测试 2: 代码提取
```bash
python test_code_extraction.py
```
```
✓ Markdown cleaning works!
✓ 修复成功！现在可以正确执行代码了。
```

---

## 核心原则总结

### ✅ 应该做的
1. **参考已有实现** - 查看 AIDE 怎么做的
2. **使用已有模块** - 不重复造轮子
3. **遵循项目模式** - 保持代码风格一致
4. **防御式编程** - 提示词 + 代码双重保护
5. **阅读源码** - 理解现有功能的实现

### ❌ 不应该做的
1. **闭门造车** - 不看已有代码就自己实现
2. **重复造轮子** - 创建不必要的包装方法
3. **猜测 API** - 不确定参数就随便传
4. **忽略错误** - 看到错误不查源码
5. **过度自信** - 假设 LLM 会完全按提示词输出

---

## 对比：修复前后

| 方面 | 修复前 ❌ | 修复后 ✅ |
|------|----------|----------|
| LLM 调用 | 自定义 `_call_llm()` 包装 | 直接使用 `llm_service.call()` |
| 参数传递 | `messages=...` (错误) | `prompt=...` (正确) |
| 代码提取 | 包含 ``` 标记 | 自动清理标记 |
| 提示词 | 没有明确说明 | 明确要求纯代码 |
| 代码风格 | 自成一派 | 遵循 AIDE 模式 |

---

## 现在可以运行了！

```bash
python main.py --workflow scientific --benchmark mle \
    --mle-data-dir "/home/aiops/liufan/projects/DSFlow/data/competitions" \
    --llm-model openai/deepseek-ai/DeepSeek-V3.1-Terminus \
    --mle-competitions dabench-0-mean-fare
```

所有 bug 已修复，Scientific Discovery Workflow 可以正常工作！🎉

---

## 相关文档

- [BUGFIX_SCIENTIFIC_WORKFLOW.md](BUGFIX_SCIENTIFIC_WORKFLOW.md) - LLM 调用修复详情
- [BUGFIX_CODE_EXTRACTION.md](BUGFIX_CODE_EXTRACTION.md) - 代码提取修复详情
- [REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md) - 重构对比详情
- [QUICK_START_SCIENTIFIC.md](QUICK_START_SCIENTIFIC.md) - 快速入门指南
- [SCIENTIFIC_WORKFLOW_README.md](SCIENTIFIC_WORKFLOW_README.md) - 完整文档

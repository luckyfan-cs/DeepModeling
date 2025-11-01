# Bug Fix: Code Extraction from Experiment Tags

## 问题描述

执行 scientific workflow 时，从 `<Experiment>` 标签提取的代码包含 markdown 代码块标记，导致执行失败：

```
File "..._sandbox_script_....py", line 1
    ```python
    ^
SyntaxError: invalid syntax
```

## 根本原因

LLM 在 `<Experiment>` 标签内生成代码时，仍然使用了 markdown 格式：

```xml
<Experiment>
```python
import pandas as pd
df = pd.read_csv('data.csv')
```
</Experiment>
```

`extract_tag_content()` 函数只是简单提取标签内容，没有清理 markdown 标记。

## 解决方案

### 1. 添加代码清理函数

在 `modeling/prompts/scientific_prompt.py` 中添加：

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

### 2. 在提取时自动清理

修改 `extract_tag_content()` 函数：

```python
def extract_tag_content(text: str, tag: str) -> Optional[str]:
    """Extract content from XML tag."""
    import re
    pattern = f'<{tag}>(.*?)</{tag}>'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        content = match.group(1).strip()

        # For Experiment tag, clean up markdown code blocks
        if tag == "Experiment":
            content = _clean_code_block(content)

        return content
    return None
```

### 3. 更新提示词

在 `create_initial_prompt()` 中明确指示：

```python
<Experiment>
Python code only - no markdown code blocks, no ```, just pure Python code
</Experiment>

IMPORTANT: In <Experiment> tags, write pure Python code directly. Do NOT use markdown code blocks like ```python.
```

## 测试验证

```bash
python test_code_extraction.py
```

测试结果：
```
=== Test 1: With ```python ===
Extracted code:
import pandas as pd
import numpy as np
df = pd.read_csv('data.csv')
print(df.head())

Starts with 'import': True
No ``` markers: True

✓ Markdown cleaning works!
✓ 修复成功！现在可以正确执行代码了。
```

## 修改文件

**文件**: `modeling/prompts/scientific_prompt.py`

**修改**:
1. 添加 `_clean_code_block()` 函数 (行 95-102)
2. 修改 `extract_tag_content()` 自动清理 Experiment 标签 (行 87-89)
3. 更新提示词明确要求纯 Python 代码 (行 22-25)

## 双重保护机制

这个修复采用**防御式编程**：

1. **提示词层面** - 明确告诉 LLM 不要使用 markdown
2. **代码层面** - 即使 LLM 仍然使用 markdown，也会自动清理

## 参考

类似的代码提取逻辑在 `modeling/utils/parsing.py` 的 `parse_plan_and_code()` 函数中：

```python
code_match = re.search(r"```(?:python|py)?\n(.*?)\n```", response, re.DOTALL)
if code_match:
    code = code_match.group(1).strip()  # 只提取代码块内的内容
```

我们的实现遵循了相同的模式。

## 总结

- ✅ 添加了 markdown 代码块清理函数
- ✅ 在 Experiment 标签提取时自动清理
- ✅ 更新提示词明确要求
- ✅ 双重保护机制确保代码可执行
- ✅ 参考了项目中已有的代码解析模式

现在 `<Experiment>` 标签中的代码可以正确提取和执行了！

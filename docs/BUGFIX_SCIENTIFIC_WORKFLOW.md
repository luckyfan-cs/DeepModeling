# Scientific Workflow Bug Fix

## 问题描述

运行 scientific workflow 时遇到错误：
```
TypeError: LLMService.call() got an unexpected keyword argument 'messages'
```

## 根本原因

在 `modeling/workflows/search/scientific_workflow.py` 中，没有参考 AIDE workflow 的实现，自己创建了错误的 `_call_llm()` 包装方法，使用了不存在的参数。

### 错误代码：
```python
async def _call_llm(self, prompt: str) -> str:
    """Call LLM and return raw response."""
    messages = [{"role": "user", "content": prompt}]

    response = await self.llm_service.call(
        messages=messages,           # ❌ 错误：不存在的参数
        temperature=0.7,             # ❌ 错误：不存在的参数
        response_format=None         # ❌ 错误：不存在的参数
    )

    return response
```

### LLMService.call 的实际签名：
```python
async def call(
    self,
    prompt: str,                      # ✅ 正确参数
    system_message: Optional[str] = None,
    max_retries: Optional[int] = None
) -> str:
```

## 解决方案

**参考 AIDE workflow 的实现方式**，直接使用已有的 `llm_service`，不自己创建包装方法。

### 修复步骤：

1. **移除自定义的包装方法** `_call_llm()`
2. **直接使用** `self.llm_service.call(prompt=...)`
3. **遵循 AIDE 的模式**：使用已有模块，不重复造轮子

### 修复后的代码：
```python
# 直接调用 llm_service，就像 AIDE 中的 operators 一样
response = await self.llm_service.call(prompt=initial_prompt)  # ✅ 正确
```

## 修改文件

**文件**: `modeling/workflows/search/scientific_workflow.py`

**修改内容**:
1. **删除** `_call_llm()` 包装方法 (行 139-142)
2. **替换** 所有 `await self._call_llm(prompt)` 为 `await self.llm_service.call(prompt=prompt)`
3. **直接使用** 已有的 `llm_service`，参考 AIDE workflow 的实现

## 参考实现

AIDE workflow 使用 `GenerateCodeAndPlanOperator`，它内部正确调用了 LLM：

```python
# 在 aide_workflow.py 中
plan, code = await self.generate_op(system_prompt=prompt)

# GenerateCodeAndPlanOperator 内部
response = await self.llm_service.call(prompt=user_prompt, system_message=system_prompt)
```

## 验证

运行测试脚本验证修复：
```bash
python test_llm_call_fix.py
```

预期输出：
```
✓ LLMService.call 签名验证
✓ 所有参数验证通过
✓ ScientificWorkflow 现在使用正确的调用方式
✓ 修复完成！可以运行了。
```

## 额外依赖

运行过程中发现缺少 `tenacity` 包，已安装：
```bash
pip install tenacity
```

## 测试

修复后可以正常运行：
```bash
python main.py --workflow scientific --benchmark mle \
    --mle-data-dir "/path/to/data" \
    --llm-model openai/deepseek-ai/DeepSeek-V3.1-Terminus \
    --mle-competitions dabench-0-mean-fare
```

## 关键学习点

**不要闭门造车！** 应该：
- ✅ 参考 AIDE workflow 的实现
- ✅ 使用已有的模块和 operators
- ✅ 不要自己创建不必要的包装方法
- ✅ 遵循项目的现有模式

## 总结

- ✅ **删除了自定义的包装方法** `_call_llm()`
- ✅ **直接使用** `self.llm_service.call(prompt=...)`，就像 AIDE 的 operators 一样
- ✅ 修复了参数错误：使用 `prompt` 而非 `messages`
- ✅ 简化了代码逻辑，遵循已有模式
- ✅ 安装了缺失的 `tenacity` 依赖

**核心原则**：使用已有模块，参考 AIDE 实现，不重复造轮子！

## 后续修复：代码提取问题

### 问题
从 `<Experiment>` 标签提取的代码包含 markdown 标记 ``` ，导致执行失败。

### 解决方案
1. 添加 `_clean_code_block()` 函数移除 markdown 标记
2. 在 `extract_tag_content()` 中自动清理 Experiment 标签
3. 更新提示词明确要求纯 Python 代码

详见: [BUGFIX_CODE_EXTRACTION.md](BUGFIX_CODE_EXTRACTION.md)

---

现在 Scientific workflow 可以正常运行了！

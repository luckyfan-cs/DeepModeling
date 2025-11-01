# Scientific Workflow 重构总结

## 核心原则：不要闭门造车

遵循项目现有模式，参考 AIDE workflow 的实现，使用已有模块。

## 重构对比

### ❌ 重构前（错误做法）

```python
class ScientificWorkflow(ModelingWorkflow):
    def __init__(self, operators, services, agent_config, benchmark=None):
        super().__init__(operators, services, agent_config)
        self.llm_service: LLMService = services["llm"]
        self.execute_op = operators["execute"]
        # ❌ 没有使用已有的 generate_op

    async def solve(self, description, io_instructions, data_dir, output_path):
        # ❌ 自己创建包装方法
        response = await self._call_llm(initial_prompt)

    # ❌ 闭门造车：自己实现 LLM 调用
    async def _call_llm(self, prompt: str) -> str:
        messages = [{"role": "user", "content": prompt}]  # ❌ 错误参数
        response = await self.llm_service.call(
            messages=messages,           # ❌ 不存在的参数
            temperature=0.7,             # ❌ 不支持的参数
            response_format=None         # ❌ 不支持的参数
        )
        return response
```

**问题**：
1. 没有参考 AIDE 的实现
2. 自己创建了不必要的包装方法
3. 使用了错误的参数
4. 重复造轮子

### ✅ 重构后（正确做法）

```python
class ScientificWorkflow(ModelingWorkflow):
    def __init__(self, operators, services, agent_config, benchmark=None):
        super().__init__(operators, services, agent_config)
        self.llm_service: LLMService = services["llm"]
        self.execute_op = operators["execute"]
        # ✅ 已有的 operators 在 factory 中注册：
        # "generate": GenerateCodeAndPlanOperator(llm_service=llm_service)

    async def solve(self, description, io_instructions, data_dir, output_path):
        # ✅ 直接使用 llm_service，就像 AIDE 的 operators 一样
        response = await self.llm_service.call(prompt=initial_prompt)

        # ✅ 使用已有的 execute_op
        exec_result = await self.execute_op(code=experiment_code, mode="script")

    # ✅ 不需要自己的包装方法
```

**优势**：
1. 参考了 AIDE workflow 的实现
2. 直接使用已有的 `llm_service`
3. 使用正确的参数 `prompt`
4. 代码更简洁，遵循项目模式

## 参考：AIDE Workflow 如何使用 LLM

### AIDE 的 operators

```python
# modeling/operators/llm_basic.py
class GenerateCodeAndPlanOperator(Operator):
    async def __call__(self, system_prompt: str, user_prompt: str = "") -> tuple[str, str]:
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        # ✅ 正确使用 llm_service
        response = await self.llm_service.call(full_prompt)
        plan, code = parse_plan_and_code(response)
        return plan, code
```

### AIDE workflow 如何使用

```python
# modeling/workflows/search/aide_workflow.py
class AIDEWorkflow(ModelingWorkflow):
    def __init__(self, operators, services, agent_config, benchmark=None):
        super().__init__(operators, services, agent_config)
        self.llm_service: LLMService = services["llm"]
        self.execute_op = self.operators["execute"]
        self.generate_op = self.operators["generate"]  # ✅ 使用已有 operator

    async def _execute_search_step(self, task_context, output_path):
        # ✅ 使用 generate_op
        plan, code = await self.generate_op(system_prompt=prompt)

        # ✅ 使用 execute_op
        exec_result = await self.execute_op(code=code, mode="script")
```

## Scientific Workflow 的正确用法

```python
# modeling/workflows/search/scientific_workflow.py
class ScientificWorkflow(ModelingWorkflow):
    def __init__(self, operators, services, agent_config, benchmark=None):
        super().__init__(operators, services, agent_config)
        # ✅ 直接保存 services 引用
        self.llm_service: LLMService = services["llm"]
        self.execute_op = operators["execute"]

    async def solve(self, description, io_instructions, data_dir, output_path):
        # 创建提示
        initial_prompt = create_initial_prompt(description, io_instructions)

        # ✅ 直接使用 llm_service.call()，就像 operators 内部做的那样
        response = await self.llm_service.call(prompt=initial_prompt)

        # 提取实验代码
        experiment_code = extract_tag_content(response, "Experiment")

        # ✅ 使用已有的 execute_op
        exec_result = await self.execute_op(code=experiment_code, mode="script")
```

## LLMService.call() 的正确签名

```python
# modeling/services/llm.py
class LLMService:
    async def call(
        self,
        prompt: str,                      # ✅ 必需参数
        system_message: Optional[str] = None,  # ✅ 可选参数
        max_retries: Optional[int] = None      # ✅ 可选参数
    ) -> str:
        """
        Makes a standard call to the LLM.

        Args:
            prompt: The user's prompt
            system_message: Optional system message
            max_retries: Max retry attempts

        Returns:
            The LLM's text response
        """
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})

        response = await self._make_llm_call_with_retries(messages, max_retries=retries)
        return response.choices[0].message.content
```

## 可用的 Operators

在 `modeling/operators/` 中：

1. **GenerateCodeAndPlanOperator** - 生成 plan 和 code
2. **ExecuteAndTestOperator** - 执行代码
3. **ReviewOperator** - 评审代码输出
4. **PlanOperator** - 创建结构化计划
5. **SummarizeOperator** - 生成摘要

所有这些 operators 内部都正确使用 `llm_service.call()`！

## 修复验证

```bash
# 验证修复
python -c "
from modeling.workflows.search.scientific_workflow import ScientificWorkflow

# ✅ 确认没有 _call_llm 方法
assert not hasattr(ScientificWorkflow, '_call_llm')
print('✓ 已移除自定义包装方法')

# ✅ 确认使用 llm_service
import inspect
source = inspect.getsource(ScientificWorkflow.solve)
assert 'self.llm_service.call(prompt=' in source
print('✓ 直接使用 llm_service.call()')
"
```

## 关键学习

### ✅ 应该做的
1. **参考已有实现** - 查看 AIDE workflow 怎么做的
2. **使用已有模块** - 直接用 `llm_service`、`execute_op` 等
3. **遵循项目模式** - 保持代码风格一致
4. **阅读源码** - 理解 operators 的内部实现

### ❌ 不应该做的
1. **闭门造车** - 不看已有代码就自己实现
2. **重复造轮子** - 创建不必要的包装方法
3. **猜测 API** - 不确定参数就随便传
4. **忽略错误** - 看到错误不查源码

## 总结

**核心原则**：
> 使用已有模块，参考 AIDE 实现，不重复造轮子！

**重构成果**：
- ✅ 删除了 `_call_llm()` 自定义包装方法
- ✅ 直接使用 `self.llm_service.call(prompt=...)`
- ✅ 遵循 AIDE workflow 的模式
- ✅ 代码更简洁、更易维护
- ✅ 与项目风格保持一致

**现在可以运行了**！🎉

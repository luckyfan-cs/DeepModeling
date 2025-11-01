import logging
from typing import Dict

from modeling.models.formats import Plan, ReviewResult, Task
from modeling.operators.base import Operator
from modeling.services.llm import LLMService
from modeling.utils.parsing import parse_plan_and_code
from modeling.utils.context import summarize_repetitive_logs

logger = logging.getLogger(__name__)

class GenerateCodeAndPlanOperator(Operator):
    """Generates a plan and corresponding code based on a prompt."""
    async def __call__(self, system_prompt: str, user_prompt: str = "") -> tuple[str, str]:
        if not self.llm_service:
            raise ValueError("LLMService is required for this operator.")

        logger.info("Generating new code and plan...")
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        
        # Use the new standard call method
        response = await self.llm_service.call(full_prompt)
        plan, code = parse_plan_and_code(response)

        if "# ERROR" in code:
            logger.warning("Failed to parse a valid code block from the LLM response.")
        else:
            logger.info("Successfully generated code and plan.")
        
        return plan, code

class PlanOperator(Operator):
    """Creates a structured, multi-step plan based on a user request."""
    async def __call__(self, user_request: str) -> Plan:
        if not self.llm_service:
            raise ValueError("LLMService is required for this operator.")
        
        logger.info(f"Generating a plan for request: '{user_request[:100]}...'")
        
        prompt = f"Create a structured JSON plan for this user request: {user_request}"
        # No more placeholder! This is a real structured call.
        try:
            plan_model = await self.llm_service.call_with_json(prompt, output_model=Plan)
        except Exception as e:
            logger.warning(f"Structured plan failed ({e}); falling back to text plan.")
            text = await self.llm_service.call(prompt)
            plan_model = Plan(tasks=[Task(task_id="1", instruction=text.strip(), dependent_task_ids=[])])
        logger.info(f"Successfully generated a plan with {len(plan_model.tasks)} tasks.")
        return plan_model

class ReviewOperator(Operator):
    """Reviews code execution output and provides a structured score and analysis."""
    async def __call__(self, prompt_context: Dict) -> ReviewResult:
        if not self.llm_service:
            raise ValueError("LLMService is required for this operator.")

        logger.info("Reviewing execution output...")
        
        raw_output = prompt_context.get('output', '# N/A')
        processed_output = summarize_repetitive_logs(raw_output)

        prompt = (
            "You are a multidisciplinary reviewer for autonomous agents. "
            "Tasks may involve data analysis, machine learning, scientific discovery, engineering workflows, or other problem-solving domains. "
            "Assess the execution results with rigor.\n\n"
            "Return a JSON object with the following keys:\n"
            "- is_buggy (bool): True if there is a clear failure, runtime error, or invalid result.\n"
            "- summary (str): 1-2 sentences summarizing the current state. If buggy, highlight the fault; otherwise, highlight findings or strengths.\n"
            "- metric_value (float | null): Best available quantitative score/metric. Use null when not applicable.\n"
            "- lower_is_better (bool): True if lower metric_value is preferable, otherwise False. Default to True when metric_value is null.\n"
            "- completion_state (\"blocked\" | \"in_progress\" | \"partial\" | \"complete\" | \"excellent\" | \"unknown\"): "
            "Your judgment of how far the task has progressed toward the goal. "
            "\"partial\" indicates some progress with gaps; \"excellent\" means the deliverable is complete and polished.\n"
            "- quality_score (float in [0,1]): Overall quality/performance of the current solution.\n"
            "- thoroughness_score (float in [0,1]): How comprehensive or insightful the work is relative to the task expectations.\n"
            "- should_continue (bool): True if another iteration is recommended for correctness, quality, or depth.\n"
            "- improvement_notes (str | null): Concrete next actions if should_continue is True; otherwise null.\n\n"
            "Ground your review in the provided task context, code, and output. "
            "Consider both correctness and opportunities for deeper insight or optimization.\n\n"
            f"# TASK\n{prompt_context.get('task', 'N/A')}\n\n"
            f"# CODE\n```python\n{prompt_context.get('code', '# N/A')}\n```\n\n"
            f"# OUTPUT\n```\n{processed_output}\n```"
        )

        # No more simulation! This is a real structured call.
        review_model = await self.llm_service.call_with_json(prompt, output_model=ReviewResult)
        return review_model

class SummarizeOperator(Operator):
    """Generates a concise summary of a completed phase or task."""
    async def __call__(self, context: str) -> str:
        if not self.llm_service:
            raise ValueError("LLMService is required for this operator.")

        logger.info("Generating summary...")
        prompt = f"Please provide a concise summary of the following events:\n\n{context}"
        summary = await self.llm_service.call(prompt)
        logger.info("Summary generated successfully.")
        return summary

# examples/deepmodeling-rl/deepmodeling_agent.py

"""DeepModeling Agent for RL training with Agent-lightning.

This agent implements the Scientific Method workflow:
- Phenomenon: Observe and describe the problem
- Hypothesis: Form initial hypothesis
- Model: Propose a solution approach
- Experiment: Write and execute code
- Observation: Analyze execution results
- Inference: Draw conclusions and iterate
- Conclusion: Final answer
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, cast
from dataclasses import dataclass

from langchain.chat_models import init_chat_model
from langchain_core.messages import AnyMessage, BaseMessage, HumanMessage, AIMessage
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.graph.state import CompiledStateGraph

# DeepModeling imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modeling.services.sandbox import SandboxService
from modeling.services.workspace import WorkspaceService
from modeling.models.formats import ReviewResult
from modeling.common.typing import ExecutionResult
from modeling.prompts.scientific_prompt import (
    create_initial_prompt,
    create_continue_prompt,
    extract_tag_content,
)
from modeling.utils.context import summarize_repetitive_logs, truncate_output

from reward_function import calculate_reward, calculate_detailed_reward

import agentlightning as agl

logger = agl.configure_logger(name=__name__)


class State(MessagesState):
    """State for DeepModeling agent workflow."""
    task_id: str
    task_description: str
    io_instructions: str
    expected_output_path: str
    eval_metric: str
    threshold: float
    data_dir: Optional[str]

    # Workflow tracking
    num_turns: int
    last_experiment_code: str
    last_observation: str
    last_observation_text: str
    last_review: Optional[ReviewResult]

    # Results
    final_answer: str
    success: bool
    messages: List[AnyMessage]


@dataclass
class DeepModelingConfig:
    """Configuration for DeepModeling agent."""
    sandbox_timeout: int = 600  # 10 minutes
    max_turns: int = 10
    workspace_dir: str = "./workspace"
    debug: bool = False


class DeepModelingAgent:
    """Agent for solving scientific computing tasks using RL."""

    def __init__(
        self,
        config: Optional[DeepModelingConfig] = None,
        verl_replacement: Optional[Dict[str, Any]] = None,
        endpoint: Optional[str] = None,
    ):
        self.config = config or DeepModelingConfig()
        self.workspace_base = Path(self.config.workspace_dir)
        self.workspace_base.mkdir(parents=True, exist_ok=True)

        # Initialize LLM
        if verl_replacement is not None:
            self.model_name: str = verl_replacement["model"]
            assert endpoint is not None, "Endpoint required for VERL training"
            self.llm = init_chat_model(
                self.model_name,
                model_provider="openai",
                openai_api_base=endpoint,
                openai_api_key=os.environ.get("OPENAI_API_KEY", "dummy"),
                temperature=verl_replacement.get("temperature", 0.7),
                max_retries=0,
                max_tokens=4096,
            )
        else:
            self.model_name = os.environ.get("MODEL", "gpt-4o-mini")
            self.llm = init_chat_model(
                self.model_name,
                model_provider="openai",
                openai_api_base=endpoint or os.environ.get("OPENAI_API_BASE"),
                openai_api_key=os.environ.get("OPENAI_API_KEY"),
                temperature=0.7,
                max_retries=1,
                max_tokens=4096,
            )

        # Build workflow graph
        self.graph = self._build_graph()

    def _extract_code_from_experiment(self, experiment: str) -> Optional[str]:
        """Extract Python code from experiment section."""
        # First try to extract from ```python blocks
        code_pattern = r"```python\s*(.*?)\s*```"
        match = re.search(code_pattern, experiment, re.DOTALL)
        if match:
            return match.group(1).strip()

        # Fall back to any ``` blocks
        code_pattern = r"```\s*(.*?)\s*```"
        match = re.search(code_pattern, experiment, re.DOTALL)
        if match:
            return match.group(1).strip()

        # If no code blocks, return the whole experiment content
        return experiment.strip()

    def _create_io_instructions(self, task_data: Dict[str, Any]) -> str:
        """Generate I/O contract shared with the prompt."""
        expected_output = task_data.get("expected_output_path", "submission.csv")
        eval_metric = task_data.get("eval_metric", "score")
        threshold = task_data.get("threshold", 0.0)
        data_dir = task_data.get("data_dir")

        lines = [
            f"- Save your final artifact to `{expected_output}`.",
            f"- Evaluation metric: {eval_metric} (target ≥ {threshold}).",
            "- Obey the Scientific Method tag order strictly: Phenomenon → Hypothesis → Model → Experiment → Observation → Inference → Conclusion.",
            "- Only place executable Python inside <Experiment> tags (no prose, no shell commands).",
        ]
        if data_dir:
            lines.append(f"- All prepared benchmark files are available under `{data_dir}` (read-only).")

        return "\n".join(lines)

    def _format_conversation_history(self, messages: List[AnyMessage]) -> str:
        """Render message history into a plain-text transcript for prompts."""
        history_parts: List[str] = []
        for msg in messages:
            role = "assistant" if isinstance(msg, AIMessage) else "user"
            content = msg.content if hasattr(msg, "content") else str(msg)
            history_parts.append(f"<{role.upper()}>:: {content}")
        return "\n\n".join(history_parts)

    def _should_finalize(self, review: Optional[ReviewResult]) -> bool:
        """Decide whether to trigger the concluding prompt based on review signals."""
        if not review:
            return False

        completion_state = getattr(review, "completion_state", "")
        quality_ok = (review.quality_score or 0.0) >= 0.7
        depth_ok = (review.thoroughness_score or 0.0) >= 0.6

        if completion_state in {"complete", "excellent"} and quality_ok:
            return True

        if (
            completion_state == "partial"
            and not review.should_continue
            and quality_ok
            and depth_ok
        ):
            return True

        return False

    def _execute_experiment(
        self,
        code: str,
        workspace: WorkspaceService,
    ) -> ExecutionResult:
        """Execute experiment code in sandbox."""
        try:
            # Create sandbox service
            sandbox = SandboxService(
                workspace=workspace,
                timeout=self.config.sandbox_timeout
            )

            # Execute code
            result = sandbox.run_script(code)

            return result

        except Exception as e:
            logger.error(f"Experiment execution failed: {e}")
            return ExecutionResult(
                success=False,
                stdout="",
                stderr=str(e),
                exc_type=type(e).__name__
            )

    def _evaluate_result(
        self,
        execution_result: ExecutionResult,
        output_path: str,
        workspace: WorkspaceService,
    ) -> ReviewResult:
        """Evaluate execution result and create review."""
        success = execution_result.success

        # Check if output file exists
        expected_file = workspace.get_path("sandbox_workdir") / output_path
        output_exists = expected_file.exists()

        # Simple quality assessment
        if success and output_exists:
            quality_score = 0.7
            thoroughness_score = 0.6
            should_continue = False
            completion_state = "complete"
        elif success and not output_exists:
            quality_score = 0.3
            thoroughness_score = 0.5
            should_continue = True
            completion_state = "in_progress"
        else:
            quality_score = 0.1
            thoroughness_score = 0.2
            should_continue = True
            completion_state = "blocked"

        # Create review
        review = ReviewResult(
            is_buggy=not success,
            summary=f"Execution {'succeeded' if success else 'failed'}. Output file {'exists' if output_exists else 'missing'}.",
            metric_value=None,
            completion_state=completion_state,
            quality_score=quality_score,
            thoroughness_score=thoroughness_score,
            should_continue=should_continue,
            improvement_notes=execution_result.stderr if not success else None,
        )

        return review

    def invoke_initial_prompt(self, state: State) -> Dict[str, Any]:
        """Generate initial scientific investigation."""
        prompt = create_initial_prompt(
            instruction=state["task_description"],
            io_instructions=state["io_instructions"],
        )

        try:
            response = self.llm.invoke(prompt)
            content = response.content if hasattr(response, 'content') else str(response)

            return {
                "messages": state["messages"] + [AIMessage(content=content)],
                "num_turns": 1,
            }
        except Exception as e:
            logger.error(f"LLM invocation failed: {e}")
            return {
                "messages": state["messages"] + [AIMessage(content=f"Error: {e}")],
                "num_turns": 1,
            }

    def check_for_experiment(self, state: State) -> Literal["execute", "continue", "end"]:
        """Check if there's an experiment to execute."""
        last_message = state["messages"][-1]
        content = last_message.content if hasattr(last_message, 'content') else str(last_message)

        # Check for conclusion
        if extract_tag_content(content, "Conclusion"):
            return "end"

        # Check for experiment
        experiment = extract_tag_content(content, "Experiment")
        if experiment:
            return "execute"

        # Check turn limit
        if state["num_turns"] >= self.config.max_turns:
            return "end"

        return "continue"

    def execute_experiment_node(self, state: State) -> Dict[str, Any]:
        """Execute the experiment code."""
        last_message = state["messages"][-1]
        content = last_message.content if hasattr(last_message, 'content') else str(last_message)

        # Extract experiment code
        experiment = extract_tag_content(content, "Experiment")
        if not experiment:
            return {
                "last_observation": "No experiment found",
                "last_observation_text": "No experiment found",
                "last_experiment_code": "",
            }

        code = self._extract_code_from_experiment(experiment)
        if not code:
            return {
                "last_observation": "No code found in experiment",
                "last_observation_text": "No code found in experiment",
                "last_experiment_code": "",
            }

        # Create workspace for this task
        workspace = WorkspaceService(
            run_name=f"{state['task_id']}_turn_{state['num_turns']}",
            base_dir=self.workspace_base
        )

        data_dir = state.get("data_dir")
        if data_dir:
            try:
                workspace.link_data_to_workspace(Path(data_dir))
            except Exception as link_error:
                logger.error(f"Failed to link data directory '{data_dir}': {link_error}")

        # Execute code
        result = self._execute_experiment(code, workspace)

        # Evaluate result
        review = self._evaluate_result(
            result,
            state["expected_output_path"],
            workspace
        )

        # Format observation
        raw_stream = result.stdout if result.success else result.stderr
        processed_output = summarize_repetitive_logs(raw_stream or "")
        processed_output = truncate_output(processed_output)

        observation_lines = [
            f"Execution {'succeeded' if result.success else 'failed'}.",
            processed_output or "No stdout/stderr captured.",
        ]
        observation_text = "\n".join(observation_lines).strip()
        observation = f"<Observation>\n{observation_text}\n</Observation>"

        return {
            "last_experiment_code": code,
            "last_observation": observation,
            "last_observation_text": observation_text,
            "last_review": review,
            "messages": state["messages"] + [HumanMessage(content=observation)],
        }

    def continue_investigation(self, state: State) -> Dict[str, Any]:
        """Continue the scientific investigation based on results."""
        review = state.get("last_review")

        conversation_history = self._format_conversation_history(state["messages"])
        observation_text = state.get("last_observation_text", state.get("last_observation", "No observation"))

        iteration_index = min(state["num_turns"] + 1, self.config.max_turns)
        if self._should_finalize(review):
            iteration_index = self.config.max_turns

        prompt = create_continue_prompt(
            conversation_history=conversation_history,
            execution_output=observation_text,
            iteration=iteration_index,
            max_iterations=self.config.max_turns,
        )

        try:
            response = self.llm.invoke(prompt)
            content = response.content if hasattr(response, 'content') else str(response)

            return {
                "messages": state["messages"] + [AIMessage(content=content)],
                "num_turns": state["num_turns"] + 1,
            }
        except Exception as e:
            logger.error(f"LLM invocation failed: {e}")
            return {
                "messages": state["messages"] + [AIMessage(content=f"Error: {e}")],
                "num_turns": state["num_turns"] + 1,
            }

    def finalize(self, state: State) -> Dict[str, Any]:
        """Extract final conclusion."""
        last_message = state["messages"][-1]
        content = last_message.content if hasattr(last_message, 'content') else str(last_message)

        conclusion = extract_tag_content(content, "Conclusion")
        if not conclusion:
            conclusion = "Investigation incomplete."

        # Determine success based on last review
        review = state.get("last_review")
        success = False
        if review:
            success = (
                not review.is_buggy and
                review.quality_score > 0.6 and
                review.completion_state in ["complete", "excellent"]
            )

        return {
            "final_answer": conclusion,
            "success": success,
        }

    def _build_graph(self) -> CompiledStateGraph:
        """Build the LangGraph workflow."""
        workflow = StateGraph(State)

        # Add nodes
        workflow.add_node("initial", self.invoke_initial_prompt)
        workflow.add_node("execute", self.execute_experiment_node)
        workflow.add_node("continue", self.continue_investigation)
        workflow.add_node("finalize", self.finalize)

        # Add edges
        workflow.add_edge(START, "initial")
        workflow.add_conditional_edges(
            "initial",
            self.check_for_experiment,
            {
                "execute": "execute",
                "continue": "continue",
                "end": "finalize",
            }
        )
        workflow.add_conditional_edges(
            "execute",
            self.check_for_experiment,
            {
                "execute": "execute",
                "continue": "continue",
                "end": "finalize",
            }
        )
        workflow.add_conditional_edges(
            "continue",
            self.check_for_experiment,
            {
                "execute": "execute",
                "continue": "continue",
                "end": "finalize",
            }
        )
        workflow.add_edge("finalize", END)

        return workflow.compile()

    def run_episode(self, task_data: Dict[str, Any]) -> State:
        """Run a complete episode for one task."""
        initial_state: State = {
            "task_id": task_data["task_id"],
            "task_description": task_data["prompt"],
            "io_instructions": self._create_io_instructions(task_data),
            "expected_output_path": task_data.get("expected_output_path", "submission.csv"),
            "eval_metric": task_data.get("eval_metric", "score"),
            "threshold": task_data.get("threshold", 0.7),
            "data_dir": task_data.get("data_dir"),
            "num_turns": 0,
            "last_experiment_code": "",
            "last_observation": "",
            "last_observation_text": "",
            "last_review": None,
            "final_answer": "",
            "success": False,
            "messages": [],
        }

        # Run the graph synchronously
        final_state = self.graph.invoke(initial_state)

        return final_state


# Agent-lightning integration
class LitDeepModelingAgent(agl.LitAgent[Dict[str, Any]]):
    """Agent-Lightning compatible wrapper around DeepModelingAgent."""

    def __init__(
        self,
        config: Optional[DeepModelingConfig] = None,
        val_temperature: Optional[float] = None,
    ) -> None:
        super().__init__()
        self.config = config or DeepModelingConfig()
        self.val_temperature = val_temperature

    def rollout(
        self,
        task: Dict[str, Any],
        resources: agl.NamedResources,
        rollout: agl.Rollout,
    ) -> float | None:
        """Execute one RL rollout and return the scalar reward."""

        try:
            llm: agl.LLM = cast(agl.LLM, resources["main_llm"])
        except KeyError:
            logger.error("main_llm resource missing; cannot execute rollout")
            return 0.0

        deep_agent = self._build_deepmodeling_agent(llm, rollout)
        final_state = deep_agent.run_episode(task)

        agent_output = self._final_state_to_output(final_state)
        reward = calculate_reward(agent_output, task)
        breakdown = calculate_detailed_reward(agent_output, task)

        logger.info(
            "[Rollout %s] Reward %.3f | execution=%.2f quality=%.2f thoroughness=%.2f achievement=%.2f",
            rollout.rollout_id,
            reward,
            breakdown["execution"],
            breakdown["quality"],
            breakdown["thoroughness"],
            breakdown["achievement"],
        )

        return reward

    def _build_deepmodeling_agent(self, llm: agl.LLM, rollout: agl.Rollout) -> DeepModelingAgent:
        """Instantiate DeepModelingAgent bound to VERL LLM endpoint."""

        endpoint = llm.get_base_url(
            rollout.rollout_id,
            rollout.attempt.attempt_id if getattr(rollout, "attempt", None) else None,
        )

        sampling = dict(llm.sampling_parameters)
        if rollout.mode != "train" and self.val_temperature is not None:
            sampling["temperature"] = self.val_temperature

        verl_replacement = {"model": llm.model, **sampling}

        return DeepModelingAgent(
            config=self.config,
            verl_replacement=verl_replacement,
            endpoint=endpoint,
        )

    def _final_state_to_output(self, final_state: State) -> Dict[str, Any]:
        """Convert LangGraph state into reward calculation payload."""

        serialized_messages: List[Dict[str, str]] = []
        for msg in final_state["messages"]:
            role = "assistant" if isinstance(msg, AIMessage) else "user"
            content = msg.content if hasattr(msg, "content") else str(msg)
            serialized_messages.append({"role": role, "content": content})

        return {
            "messages": serialized_messages,
            "success": final_state.get("success", False),
            "task_id": final_state.get("task_id", "unknown-task"),
            "last_review": final_state.get("last_review"),
        }

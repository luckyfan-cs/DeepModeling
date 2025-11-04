# modeling/workflows/search/scientific_workflow.py

import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Any, List

from modeling.workflows.base import ModelingWorkflow
from modeling.services.llm import LLMService
from modeling.benchmark.benchmark import BaseBenchmark
from modeling.models.formats import ReviewResult

from modeling.prompts.scientific_prompt import (
    create_initial_prompt,
    create_continue_prompt,
    extract_tag_content,
)
from modeling.utils.context import summarize_repetitive_logs, truncate_output

logger = logging.getLogger(__name__)


class ScientificWorkflow(ModelingWorkflow):
    """
    Scientific discovery workflow using strict XML tag format.

    Format:
    <Phenomenon>...</Phenomenon>
    <Hypothesis>...</Hypothesis>
    <Model>...</Model>
    <Experiment>code only</Experiment>
    <Observation>execution results</Observation>
    <Inference>...</Inference>
    <Conclusion>final answer</Conclusion>
    """

    def __init__(
        self,
        operators: Dict[str, Any],
        services: Dict[str, Any],
        agent_config: Dict[str, Any],
        benchmark: Optional[BaseBenchmark] = None
    ):
        super().__init__(operators, services, agent_config)
        self.llm_service: LLMService = services["llm"]
        self.sandbox_service = services["sandbox"]
        self.workspace_service = services.get("workspace")
        self.benchmark = benchmark

        self.execute_op = operators["execute"]
        self.review_op = operators.get("review")
        self.last_review: Optional[ReviewResult] = None

        # Store conversation history
        self.conversation: List[Dict[str, str]] = []
        # Collect review telemetry for each experiment iteration
        self.experiment_reviews: List[Dict[str, Any]] = []

    async def _evaluate_with_review(
        self,
        description: str,
        io_instructions: str,
        experiment_code: Optional[str],
        observation: str
    ) -> Optional[ReviewResult]:
        """
        Run the review operator on the latest execution output to determine completion status.

        Returns:
            ReviewResult if review succeeds, otherwise None.
        """
        if not self.review_op:
            return None

        if not experiment_code:
            logger.debug("Skipping review: no experiment code for evaluation.")
            return None

        if not observation:
            logger.debug("Skipping review: empty observation.")
            return None

        review_context = {
            "task": {
                "description": description,
                "io_instructions": io_instructions
            },
            "code": experiment_code,
            "output": observation
        }

        try:
            review = await self.review_op(prompt_context=review_context)
        except Exception as exc:
            logger.warning(f"Review evaluation failed: {exc}")
            return None

        self.last_review = review
        logger.info(
            "Review result -> is_buggy: %s, completion_state: %s, should_continue: %s",
            review.is_buggy,
            review.completion_state,
            review.should_continue
        )
        logger.info(
            "Review scores -> quality: %.2f, thoroughness: %.2f, metric: %s (lower_is_better=%s)",
            review.quality_score,
            review.thoroughness_score,
            review.metric_value,
            review.lower_is_better
        )
        if review.improvement_notes:
            logger.info("Review improvement notes: %s", review.improvement_notes)
        logger.debug("Review summary: %s", review.summary)
        return review

    async def solve(
        self,
        description: str,
        io_instructions: str,
        data_dir: Path,
        output_path: Path
    ) -> None:
        """Main entry point for scientific discovery workflow."""
        logger.info("ScientificWorkflow starting with XML tag format")

        max_iterations = self.agent_config.get("search", {}).get("max_iterations", 5)

        # User message
        user_message = f"{description}\n\nI/O Requirements:\n{io_instructions}"
        self.conversation.append({
            "role": "user",
            "content": user_message
        })

        # Assistant's complete response will be built incrementally
        assistant_response = ""

        # Iteration 1: Initial cycle
        logger.info("--- Iteration 1: Initial analysis ---")

        # Get initial response with Phenomenon, Hypothesis, Model, Experiment
        initial_prompt = create_initial_prompt(description, io_instructions)
        response = await self.llm_service.call(prompt=initial_prompt)
        assistant_response += response

        # Extract and execute experiment
        experiment_code = extract_tag_content(response, "Experiment")
        if not experiment_code:
            logger.error("No <Experiment> tag found in response")
            return

        # Execute experiment
        exec_result = await self.execute_op(code=experiment_code, mode="script")
        raw_observation = exec_result.stdout if exec_result.success else exec_result.stderr

        # Process observation: summarize repetitive logs and truncate if too long
        observation = summarize_repetitive_logs(raw_observation)
        observation = truncate_output(observation)

        workflow_completed = False

        async def handle_review_completion(executed_code: Optional[str], iteration_index: int) -> bool:
            nonlocal assistant_response, workflow_completed

            review = await self._evaluate_with_review(
                description=description,
                io_instructions=io_instructions,
                experiment_code=executed_code,
                observation=observation
            )
            if not review:
                return False

            self._record_experiment_review(
                iteration=iteration_index,
                experiment_code=executed_code,
                observation=observation,
                review=review
            )
            self._mark_latest_review(finalized=False)

            if review.is_buggy:
                logger.info("Reviewer flagged issues; continuing iterations for improvements.")
                return False

            if review.should_continue:
                logger.info(
                    "Reviewer recommends continuing to improve quality or depth. Notes: %s",
                    review.improvement_notes or "n/a"
                )
                return False

            completion_state = review.completion_state
            quality_ok = review.quality_score >= 0.7
            depth_ok = review.thoroughness_score >= 0.6

            should_finalize = (
                completion_state in {"complete", "excellent"}
                and quality_ok
            ) or (
                completion_state == "partial"
                and not review.should_continue
                and quality_ok
                and depth_ok
            )

            if not should_finalize:
                logger.info(
                    "Reviewer does not yet consider the solution finish-worthy "
                    "(completion_state=%s, quality_ok=%s, thoroughness_ok=%s).",
                    completion_state,
                    quality_ok,
                    depth_ok
                )
                return False

            logger.info("Reviewer indicates task is complete. Generating final conclusion.")
            final_prompt = create_continue_prompt(
                conversation_history=assistant_response,
                execution_output=observation,
                iteration=max_iterations,
                max_iterations=max_iterations
            )
            final_response = await self.llm_service.call(prompt=final_prompt)
            assistant_response += f"\n<Observation>\n{observation}\n</Observation>\n"
            assistant_response += final_response
            workflow_completed = True
            self._mark_latest_review(finalized=True)
            return True

        await handle_review_completion(experiment_code, iteration_index=1)

        if not workflow_completed:
            # Subsequent iterations
            for i in range(2, max_iterations + 1):
                if workflow_completed:
                    break

                logger.info(f"--- Iteration {i}/{max_iterations} ---")

                # Build conversation history for context
                history = assistant_response

                # Get continuation with Observation, Inference, and next cycle
                continue_prompt = create_continue_prompt(
                    conversation_history=history,
                    execution_output=observation,
                    iteration=i,
                    max_iterations=max_iterations
                )

                response = await self.llm_service.call(prompt=continue_prompt)

                # Add Observation tag
                assistant_response += f"\n<Observation>\n{observation}\n</Observation>\n"
                assistant_response += response

                # Extract experiment from new cycle (if not last iteration)
                if i < max_iterations:
                    experiment_code = extract_tag_content(response, "Experiment")
                    if experiment_code:
                        exec_result = await self.execute_op(code=experiment_code, mode="script")
                        raw_observation = exec_result.stdout if exec_result.success else exec_result.stderr

                        # Process observation: summarize repetitive logs and truncate if too long
                        observation = summarize_repetitive_logs(raw_observation)
                        observation = truncate_output(observation)

                        await handle_review_completion(experiment_code, iteration_index=i)
                        if workflow_completed:
                            break
                    else:
                        logger.warning(f"No experiment in iteration {i}, stopping")
                        break

        # Add assistant's complete response to conversation
        self.conversation.append({
            "role": "assistant",
            "content": assistant_response
        })

        # Save conversation
        await self._save_conversation()
        await self._save_experiment_review_log()

        logger.info("Scientific discovery workflow completed")

    async def _save_conversation(self) -> None:
        """Save conversation to summary.json."""
        if not self.workspace_service:
            return

        artifacts_dir = self.workspace_service.get_path("artifacts")
        artifacts_dir.mkdir(parents=True, exist_ok=True)

        summary_file = artifacts_dir / "summary.json"

        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(self.conversation, f, indent=2, ensure_ascii=False)

        logger.info(f"Saved conversation to {summary_file}")

        # Also save a human-readable version
        readable_file = artifacts_dir / "summary_readable.txt"
        with open(readable_file, 'w', encoding='utf-8') as f:
            for msg in self.conversation:
                f.write(f"=== {msg['role'].upper()} ===\n")
                f.write(msg['content'])
                f.write("\n\n" + "="*80 + "\n\n")

        logger.info(f"Saved readable summary to {readable_file}")

    def _record_experiment_review(
        self,
        *,
        iteration: int,
        experiment_code: Optional[str],
        observation: str,
        review: ReviewResult
    ) -> None:
        """Record a structured review entry for telemetry."""
        record = {
            "iteration": iteration,
            "timestamp_utc": datetime.utcnow().isoformat() + "Z",
            "experiment_code": experiment_code,
            "observation": observation,
            "review": review.model_dump(mode="json"),
        }
        self.experiment_reviews.append(record)

    def _mark_latest_review(self, **fields: Any) -> None:
        """Annotate the most recent review record with additional metadata."""
        if not self.experiment_reviews:
            return
        self.experiment_reviews[-1].update(fields)

    async def _save_experiment_review_log(self) -> None:
        """Persist experiment review telemetry as JSONL in the artifacts directory."""
        if not self.workspace_service or not self.experiment_reviews:
            return

        telemetry_rel_path = "telemetry/experiment_reviews.jsonl"
        content = "\n".join(json.dumps(record, ensure_ascii=False) for record in self.experiment_reviews)
        if content:
            content += "\n"

        self.workspace_service.write_file(content, "artifacts", telemetry_rel_path)
        telemetry_abs_path = self.workspace_service.get_path("artifacts") / telemetry_rel_path
        logger.info(f"Saved experiment review telemetry to {telemetry_abs_path}")

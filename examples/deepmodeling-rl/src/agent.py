"""Simplified DeepModeling Agent for RL training - No LangChain dependency.

Simple multi-turn loop using regex to extract:
Phenomenon → Hypothesis → Model → Experiment → Observation → Inference → Conclusion

Reward based on execution success and grading score.
"""

from __future__ import annotations

import os
import sys
import uuid
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
import agentlightning as agl

# Add DeepModeling root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

# Import from modeling
from modeling.prompts.scientific_prompt import (
    create_initial_prompt,
    create_continue_prompt,
    extract_tag_content,
)
from modeling.services.sandbox import SandboxService
from modeling.services.workspace import WorkspaceService
from modeling.tasks.handlers import ScienceTaskHandler
from modeling.models.task import TaskDefinition
from modeling.utils.context import summarize_repetitive_logs, truncate_output

# Import local utilities and reward function
from .utils import get_grader, build_episode_metadata, format_conversation, write_jsonl
from .reward_function import calculate_reward, calculate_detailed_reward

logger = agl.configure_logger(name=__name__)


class SimpleDeepModelingAgent:
    """Simple agent using regex extraction and direct LLM calls."""

    def __init__(
        self,
        llm_endpoint: str,
        model_name: str,
        max_turns: int = 10,
        workspace_dir: str = "./workspace_rl",
        sandbox_timeout: int = 600,
        temperature: float = 0.7,
    ):
        self.llm_endpoint = llm_endpoint
        self.model_name = model_name
        self.max_turns = max_turns
        self.workspace_base = Path(workspace_dir)
        self.workspace_base.mkdir(parents=True, exist_ok=True)
        self.sandbox_timeout = sandbox_timeout
        self.temperature = temperature

    def _call_llm(
        self,
        prompt: str = None,
        messages: List[Dict[str, str]] = None,
        temperature: Optional[float] = None
    ) -> str:
        """Call LLM endpoint (OpenAI compatible).

        Args:
            prompt: Single prompt string (for first turn)
            messages: Full conversation history (for subsequent turns)
            temperature: Sampling temperature

        Returns:
            LLM response content
        """
        llm_temperature = temperature if temperature is not None else self.temperature

        # Build messages list
        if messages is not None:
            # Use provided conversation history
            api_messages = messages
        elif prompt is not None:
            # First turn: single user message
            api_messages = [{"role": "user", "content": prompt}]
        else:
            raise ValueError("Either prompt or messages must be provided")

        try:
            response = requests.post(
                f"{self.llm_endpoint}/v1/chat/completions",
                json={
                    "model": self.model_name,
                    "messages": api_messages,
                    "temperature": llm_temperature,
                    "max_tokens": 4096,
                },
                timeout=120,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            return f"Error calling LLM: {e}"

    def _prepare_task_io(
        self,
        task: Dict[str, Any],
        output_submission_path: str
    ) -> tuple[str, str, Path, Path]:
        """Prepare task I/O using ScienceTaskHandler from modeling.

        Args:
            task: Task dictionary
            output_submission_path: Full path for submission file (like benchmark does)

        Returns: (description, io_instructions, data_dir, output_path)
        """
        # Use the same TaskHandler as modeling/runner.py
        handler = ScienceTaskHandler()

        # Convert task dict to TaskDefinition format (same as benchmark does)
        task_def = TaskDefinition(
            task_id=task["task_id"],
            task_type="science",
            payload={
                "description": task["prompt"],
                "public_data_dir": task["data_dir"],
                "output_submission_path": output_submission_path,  # Use full path
                "metadata": {
                    "eval_metric": task.get("eval_metric", "score"),
                    "threshold": task.get("threshold", 0.7),
                }
            }
        )

        # Use handler to prepare input (same as runner.py does)
        description, io_instructions, data_dir, output_path = handler.prepare_input(task_def)

        return description, io_instructions, data_dir, output_path

    def _execute_code(
        self,
        code: str,
        workspace: WorkspaceService,
    ) -> tuple[bool, str]:
        """Execute code in sandbox and return (success, output)."""
        try:
            sandbox = SandboxService(
                workspace=workspace,
                timeout=self.sandbox_timeout
            )
            result = sandbox.run_script(code)

            output = result.stdout if result.success else result.stderr
            output = summarize_repetitive_logs(output or "")
            output = truncate_output(output)

            return result.success, output

        except Exception as e:
            logger.error(f"Code execution failed: {e}")
            return False, str(e)

    def _grade_submission(self, task: Dict[str, Any], submission_path: Path) -> Optional[float]:
        """Grade the submission using benchmark's grade function.

        Args:
            task: Task data with benchmark info
            submission_path: Path to submission file

        Returns:
            Grade score (float) or None if grading fails
        """
        grader = get_grader()
        return grader.grade_submission(task, submission_path)

    def _persist_episode_metadata(
        self,
        *,
        workspace: WorkspaceService,
        task: Dict[str, Any],
        run_name: str,
        description: str,
        io_instructions: str,
        conversation: List[Dict[str, str]],
        telemetry_log: Optional[List[Dict[str, Any]]] = None,
        success: bool,
        num_turns: int,
        started_at: datetime,
        ended_at: datetime,
        duration_seconds: float,
        output_path: Path,
        grade_score: Optional[float],
    ) -> None:
        """Persist episode metadata to workspace."""
        try:
            workspace_dir = workspace.get_path("run_dir")

            # Build metadata using utility function
            metadata = build_episode_metadata(
                run_name=run_name,
                workspace_dir=workspace_dir,
                task=task,
                description=description,
                io_instructions=io_instructions,
                output_path=output_path,
                success=success,
                num_turns=num_turns,
                started_at=started_at,
                ended_at=ended_at,
                duration_seconds=duration_seconds,
                grade_score=grade_score,
            )

            # Save conversation history
            conversation_path = f"telemetry/conversation.jsonl"
            conversation_data = telemetry_log if telemetry_log is not None else conversation
            lines = [json.dumps(item, ensure_ascii=False) for item in conversation_data]
            workspace.write_file("\n".join(lines), "artifacts", conversation_path)

            # Save run metadata
            metadata_path = f"telemetry/run_metadata.json"
            workspace.write_file(
                json.dumps(metadata, ensure_ascii=False, indent=2),
                "artifacts",
                metadata_path
            )

            logger.info(f"[EPISODE] Metadata saved to {workspace_dir}")

        except Exception as e:
            logger.error(f"[EPISODE] Failed to persist metadata: {e}", exc_info=True)

    def run_episode(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Run one episode for a task."""
        task_id = task["task_id"]

        # Generate unique run name with UUID (same format as runner.py: modeling_run_{task_id}_{uuid})
        safe_task_id = "".join(c if c.isalnum() else "_" for c in task_id)
        unique_suffix = uuid.uuid4().hex[:8]
        run_name = f"modeling_run_{safe_task_id}_{unique_suffix}"

        # Create output submission path (same format as benchmark does)
        # Format: {workspace_base}/submission_{task_id}_{uuid}.csv
        submission_unique_id = uuid.uuid4().hex[:6]
        output_filename = f"submission_{task_id}_{submission_unique_id}.csv"
        output_submission_path = str((Path(self.workspace_base) / output_filename).absolute())

        logger.info(f"[EPISODE] Starting episode: run_name={run_name}, task_id={task_id}")
        logger.info(f"[EPISODE] Output path: {output_submission_path}")

        # Prepare task I/O using TaskHandler (same as runner.py)
        description, io_instructions, data_dir, output_path = self._prepare_task_io(
            task, output_submission_path
        )

        # Create initial prompt with full description and I/O instructions
        # (scientific_prompt.py already has complete guidance)
        prompt = create_initial_prompt(description, io_instructions)

        # Initialize conversation with the initial user prompt
        conversation = [{"role": "user", "content": prompt}]
        telemetry_log: List[Dict[str, Any]] = []
        num_turns = 0
        success = False
        started_at = datetime.utcnow()

        # Create workspace for this episode (one workspace per episode, like runner.py)
        workspace = WorkspaceService(
            run_name=run_name,
            base_dir=self.workspace_base
        )

        # Link data directory once at the beginning
        if data_dir:
            try:
                workspace.link_data_to_workspace(data_dir)
                logger.info(f"[EPISODE] Linked data directory: {data_dir}")
            except Exception as e:
                logger.error(f"[EPISODE] Failed to link data: {e}")

        # Multi-turn loop
        while num_turns < self.max_turns:
            num_turns += 1
            logger.info(f"[TURN {num_turns}/{self.max_turns}] Calling LLM...")

            llm_temperature = self.temperature

            # Use full conversation history (which includes the initial prompt)
            current_messages = conversation.copy()

            telemetry_log.append(
                {
                    "event": "llm_call",
                    "turn": num_turns,
                    "timestamp": datetime.utcnow().isoformat(),
                    "model": self.model_name,
                    "payload": {
                        "temperature": llm_temperature,
                        "max_tokens": 4096,
                        "messages": current_messages,
                    },
                }
            )

            # Call LLM with conversation history
            response = self._call_llm(messages=current_messages, temperature=llm_temperature)
            conversation.append({"role": "assistant", "content": response})
            telemetry_log.append(
                {
                    "event": "llm_response",
                    "turn": num_turns,
                    "timestamp": datetime.utcnow().isoformat(),
                    "model": self.model_name,
                    "payload": {
                        "content": response,
                    },
                }
            )

            # Check for Conclusion (early termination)
            conclusion = extract_tag_content(response, "Conclusion")
            if conclusion:
                logger.info(f"[TURN {num_turns}] Found Conclusion, ending episode")
                success = True
                break

            # Extract and execute Experiment
            experiment = extract_tag_content(response, "Experiment")
            if not experiment:
                logger.warning(f"[TURN {num_turns}] No Experiment found, continuing...")
                # Add feedback message to conversation
                feedback_msg = {
                    "role": "user",
                    "content": f"No experiment code was provided. Please provide an <Experiment> block with Python code. (Turn {num_turns}/{self.max_turns})"
                }
                conversation.append(feedback_msg)
                continue

            logger.info(f"[TURN {num_turns}] Executing experiment ({len(experiment)} chars)")

            # Execute code
            exec_success, exec_output = self._execute_code(experiment, workspace)

            observation = f"Execution {'succeeded' if exec_success else 'failed'}.\n{exec_output}"
            observation_entry = {"role": "user", "content": f"<Observation>\n{observation}\n</Observation>"}
            conversation.append(observation_entry)
            telemetry_log.append(
                {
                    "event": "observation",
                    "turn": num_turns,
                    "timestamp": datetime.utcnow().isoformat(),
                    "payload": {
                        "execution_success": exec_success,
                        "content": observation_entry["content"],
                    },
                }
            )

            logger.info(f"[TURN {num_turns}] Execution: {'✓' if exec_success else '✗'}")

            # Check if output file exists and copy it (like runner.py does)
            sandbox_workdir = workspace.get_path("sandbox_workdir")
            generated_file = sandbox_workdir / output_path.name
            if generated_file.exists():
                logger.info(f"[TURN {num_turns}] Output file created: {output_path.name}")
                # Copy to expected location
                output_path.parent.mkdir(parents=True, exist_ok=True)
                if generated_file.resolve() != output_path.resolve():
                    shutil.copy(generated_file, output_path)
                    logger.info(f"[TURN {num_turns}] Copied output to: {output_path}")
                success = True

            # Next turn will automatically use the updated conversation history
            # (observation has been appended to conversation at line 358)

        ended_at = datetime.utcnow()
        duration_sec = (ended_at - started_at).total_seconds()

        logger.info(f"[EPISODE] Completed {num_turns} turns, success={success}, duration={duration_sec:.2f}s")

        # Grade the submission if output exists
        grade_score = None
        if output_path.exists():
            grade_score = self._grade_submission(task, output_path)
            if grade_score is not None:
                logger.info(f"[EPISODE] Grade score: {grade_score:.4f}")

        # Persist run metadata (like runner.py does)
        self._persist_episode_metadata(
            workspace=workspace,
            task=task,
            run_name=run_name,
            description=description,
            io_instructions=io_instructions,
            conversation=conversation,
            telemetry_log=telemetry_log,
            success=success,
            num_turns=num_turns,
            started_at=started_at,
            ended_at=ended_at,
            duration_seconds=duration_sec,
            output_path=output_path,
            grade_score=grade_score,
        )

        return {
            "task_id": task_id,
            "run_name": run_name,
            "messages": conversation,
            "success": success,
            "num_turns": num_turns,
            "grade_score": grade_score,
            "duration_seconds": duration_sec,
        }

    def _format_conversation(self, messages: List[Dict[str, str]]) -> str:
        """Format conversation history as text."""
        return format_conversation(messages)


# Agent-Lightning integration
class LitDeepModelingAgent(agl.LitAgent[Dict[str, Any]]):
    """Agent-Lightning wrapper for SimpleDeepModelingAgent."""

    def __init__(
        self,
        max_turns: int = 10,
        train_temperature: float = 0.7,
        val_temperature: Optional[float] = None,
    ):
        super().__init__()
        self.max_turns = max_turns
        self.train_temperature = train_temperature
        self.val_temperature = val_temperature

    def rollout(
        self,
        task: Dict[str, Any],
        resources: agl.NamedResources,
        rollout: agl.Rollout,
    ) -> float | None:
        """Execute one RL rollout and return reward."""

        logger.info("=" * 80)
        logger.info("[ROLLOUT START] rollout_id=%s, task=%s, mode=%s",
                   rollout.rollout_id, task.get("task_id", "unknown"), rollout.mode)
        logger.info("=" * 80)

        # Get LLM resource
        try:
            llm: agl.LLM = resources["main_llm"]
            logger.info("[ROLLOUT] LLM: model=%s", llm.model)
        except KeyError:
            logger.error("[ROLLOUT] No main_llm resource")
            return 0.0

        # Get endpoint
        endpoint = llm.get_base_url(
            rollout.rollout_id,
            rollout.attempt.attempt_id if hasattr(rollout, "attempt") else None,
        )

        # Build agent
        logger.info("[ROLLOUT] Building agent...")
        agent_temperature = (
            self.val_temperature if rollout.mode == "val" and self.val_temperature is not None else self.train_temperature
        )

        agent = SimpleDeepModelingAgent(
            llm_endpoint=endpoint,
            model_name=llm.model,
            max_turns=self.max_turns,
            workspace_dir="./workspace_rl",
            sandbox_timeout=600,
            temperature=agent_temperature,
        )

        # Run episode
        logger.info("[ROLLOUT] Running episode...")
        result = agent.run_episode(task)

        # Calculate reward (now includes grade_score if available)
        logger.info("[ROLLOUT] Calculating reward...")
        reward = calculate_reward(result, task)
        breakdown = calculate_detailed_reward(result, task)

        logger.info("=" * 80)
        logger.info(
            "[ROLLOUT COMPLETE] rollout_id=%s | Reward=%.3f | exec=%.2f qual=%.2f thor=%.2f achv=%.2f | grade=%.4f",
            rollout.rollout_id,
            reward,
            breakdown["execution"],
            breakdown["quality"],
            breakdown["thoroughness"],
            breakdown["achievement"],
            result.get("grade_score") or 0.0,
        )
        logger.info("=" * 80)

        return reward

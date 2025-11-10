#!/usr/bin/env python3
"""Inference script for DeepModeling agent - Test SFT and RL trained models."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import uuid
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

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

# Import local utilities
from .config import create_infer_config, DEFAULT_INFER_CONFIG

# Import local data utilities and grading
from .data_utils import load_benchmark_tasks, DEFAULT_DATA_ROOTS
from .utils import get_grader, format_conversation

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


class DeepModelingInferenceAgent:
    """Inference agent for testing trained models."""

    def __init__(
        self,
        model_path: str = None,
        api_endpoint: str = None,
        max_turns: int = 10,
        workspace_dir: str = "./workspace_infer",
        sandbox_timeout: int = 600,
        temperature: float = 0.0,
        use_local_model: bool = False,
    ):
        """Initialize inference agent.

        Args:
            model_path: Path to model or HF model name
            api_endpoint: API endpoint (if using API)
            max_turns: Maximum turns per episode
            workspace_dir: Workspace directory
            sandbox_timeout: Sandbox timeout in seconds
            temperature: Sampling temperature
            use_local_model: Whether to load model locally (vs API)
        """
        self.model_path = model_path or DEFAULT_INFER_CONFIG["model"]["path"]
        self.api_endpoint = api_endpoint
        self.max_turns = max_turns
        self.workspace_base = Path(workspace_dir)
        self.workspace_base.mkdir(parents=True, exist_ok=True)
        self.sandbox_timeout = sandbox_timeout
        self.temperature = temperature
        self.use_local_model = use_local_model

        # Load model locally if requested
        self.model = None
        self.tokenizer = None
        if use_local_model and not api_endpoint:
            self._load_local_model()

    def _load_local_model(self):
        """Load model locally using transformers."""
        logger.info(f"Loading model from {self.model_path}...")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                torch_dtype=torch.float16,
                device_map="auto",
            )
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise

    def _call_llm(
        self,
        prompt: str = None,
        messages: List[Dict[str, str]] = None,
        temperature: Optional[float] = None
    ) -> str:
        """Call LLM (either local or API).

        Args:
            prompt: Single prompt string
            messages: Full conversation history
            temperature: Sampling temperature

        Returns:
            LLM response content
        """
        llm_temperature = temperature if temperature is not None else self.temperature

        # Build messages list
        if messages is not None:
            api_messages = messages
        elif prompt is not None:
            api_messages = [{"role": "user", "content": prompt}]
        else:
            raise ValueError("Either prompt or messages must be provided")

        # Use local model if loaded
        if self.use_local_model and self.model is not None:
            return self._call_local_model(api_messages, llm_temperature)

        # Otherwise use API
        if not self.api_endpoint:
            raise ValueError("No API endpoint provided and local model not loaded")

        return self._call_api(api_messages, llm_temperature)

    def _call_local_model(
        self,
        messages: List[Dict[str, str]],
        temperature: float
    ) -> str:
        """Call local model using transformers."""
        try:
            # Apply chat template
            text = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )

            # Tokenize
            inputs = self.tokenizer(text, return_tensors="pt").to(self.model.device)

            # Generate
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=4096,
                    temperature=temperature if temperature > 0 else None,
                    do_sample=temperature > 0,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                )

            # Decode
            response = self.tokenizer.decode(
                outputs[0][inputs['input_ids'].shape[1]:],
                skip_special_tokens=True
            )

            return response

        except Exception as e:
            logger.error(f"Local model call failed: {e}")
            return f"Error calling local model: {e}"

    def _call_api(
        self,
        messages: List[Dict[str, str]],
        temperature: float
    ) -> str:
        """Call API endpoint (OpenAI compatible)."""
        try:
            response = requests.post(
                f"{self.api_endpoint}/v1/chat/completions",
                json={
                    "model": self.model_path,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": 16384,
                },
                timeout=120,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"API call failed: {e}")
            return f"Error calling API: {e}"

    def _prepare_task_io(
        self,
        task: Dict[str, Any],
        output_submission_path: str
    ) -> tuple[str, str, Path, Path]:
        """Prepare task I/O using ScienceTaskHandler."""
        handler = ScienceTaskHandler()

        task_def = TaskDefinition(
            task_id=task["task_id"],
            task_type="science",
            payload={
                "description": task["prompt"],
                "public_data_dir": task["data_dir"],
                "output_submission_path": output_submission_path,
                "metadata": {
                    "eval_metric": task.get("eval_metric", "score"),
                    "threshold": task.get("threshold", 0.7),
                }
            }
        )

        description, io_instructions, data_dir, output_path = handler.prepare_input(task_def)
        return description, io_instructions, data_dir, output_path

    def _execute_code(
        self,
        code: str,
        workspace: WorkspaceService,
    ) -> tuple[bool, str]:
        """Execute code in sandbox."""
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
        """Grade the submission using benchmark grader."""
        grader = get_grader()
        return grader.grade_submission(task, submission_path)

    def _save_results(
        self,
        workspace: WorkspaceService,
        task: Dict[str, Any],
        run_name: str,
        description: str,
        io_instructions: str,
        conversation: List[Dict[str, str]],
        success: bool,
        num_turns: int,
        started_at: datetime,
        ended_at: datetime,
        duration_seconds: float,
        output_path: Path,
        grade_score: Optional[float],
    ) -> None:
        """Save inference results."""
        try:
            workspace_dir = workspace.get_path("run_dir")

            # Build metadata
            metadata = {
                "run_name": run_name,
                "workspace_dir": str(workspace_dir),
                "workflow": "inference_scientific_method",
                "task": {
                    "task_id": task["task_id"],
                    "benchmark": task.get("benchmark", "unknown"),
                    "prompt": task.get("prompt", ""),
                },
                "task_context": {
                    "description": description,
                    "io_instructions": io_instructions,
                    "data_dir": str(task.get("data_dir")) if task.get("data_dir") else None,
                    "expected_output_path": str(output_path),
                },
                "timeline": {
                    "started_at_utc": started_at.isoformat() + "Z",
                    "ended_at_utc": ended_at.isoformat() + "Z",
                    "duration_seconds": duration_seconds,
                },
                "summary": {
                    "success": success,
                    "num_turns": num_turns,
                    "output_exists": output_path.exists(),
                    "grade_score": grade_score,
                },
                "model_info": {
                    "model_path": self.model_path,
                    "temperature": self.temperature,
                    "max_turns": self.max_turns,
                    "use_local_model": self.use_local_model,
                },
            }

            # Save conversation
            conversation_path = "telemetry/conversation.jsonl"
            lines = [json.dumps(item, ensure_ascii=False) for item in conversation]
            workspace.write_file("\n".join(lines), "artifacts", conversation_path)

            # Save metadata
            metadata_path = "telemetry/run_metadata.json"
            workspace.write_file(
                json.dumps(metadata, ensure_ascii=False, indent=2),
                "artifacts",
                metadata_path
            )

            logger.info(f"[RESULTS] Saved to {workspace_dir}")

        except Exception as e:
            logger.error(f"[RESULTS] Failed to save: {e}", exc_info=True)

    def run_inference(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Run inference on a single task.

        Args:
            task: Task dictionary with task_id, prompt, data_dir, etc.

        Returns:
            Dictionary with inference results
        """
        task_id = task["task_id"]

        # Generate unique run name
        safe_task_id = "".join(c if c.isalnum() else "_" for c in task_id)
        unique_suffix = uuid.uuid4().hex[:8]
        run_name = f"infer_run_{safe_task_id}_{unique_suffix}"

        # Create output submission path
        submission_unique_id = uuid.uuid4().hex[:6]
        output_filename = f"submission_{task_id}_{submission_unique_id}.csv"
        output_submission_path = str((Path(self.workspace_base) / output_filename).absolute())

        logger.info(f"[INFER] Starting: run_name={run_name}, task_id={task_id}")
        logger.info(f"[INFER] Output: {output_submission_path}")

        # Prepare task
        description, io_instructions, data_dir, output_path = self._prepare_task_io(
            task, output_submission_path
        )

        # Create initial prompt
        prompt = create_initial_prompt(description, io_instructions)

        # Initialize conversation
        conversation = [{"role": "user", "content": prompt}]
        num_turns = 0
        success = False
        started_at = datetime.utcnow()

        # Create workspace
        workspace = WorkspaceService(
            run_name=run_name,
            base_dir=self.workspace_base
        )

        # Link data directory
        if data_dir:
            try:
                workspace.link_data_to_workspace(data_dir)
                logger.info(f"[INFER] Linked data: {data_dir}")
            except Exception as e:
                logger.error(f"[INFER] Failed to link data: {e}")

        # Multi-turn loop
        while num_turns < self.max_turns:
            num_turns += 1
            logger.info(f"[TURN {num_turns}/{self.max_turns}] Calling LLM...")

            # Call LLM
            response = self._call_llm(messages=conversation.copy())
            conversation.append({"role": "assistant", "content": response})

            # Check for Conclusion
            conclusion = extract_tag_content(response, "Conclusion")
            if conclusion:
                logger.info(f"[TURN {num_turns}] Conclusion found, ending")
                success = True
                break

            # Extract Experiment
            experiment = extract_tag_content(response, "Experiment")
            if not experiment:
                logger.warning(f"[TURN {num_turns}] No Experiment found")
                feedback_msg = {
                    "role": "user",
                    "content": f"No experiment code provided. Please provide <Experiment> block. (Turn {num_turns}/{self.max_turns})"
                }
                conversation.append(feedback_msg)
                continue

            logger.info(f"[TURN {num_turns}] Executing experiment ({len(experiment)} chars)")

            # Execute code
            exec_success, exec_output = self._execute_code(experiment, workspace)

            observation = f"Execution {'succeeded' if exec_success else 'failed'}.\n{exec_output}"
            observation_entry = {"role": "user", "content": f"<Observation>\n{observation}\n</Observation>"}
            conversation.append(observation_entry)

            logger.info(f"[TURN {num_turns}] Execution: {'✓' if exec_success else '✗'}")

            # Check if output file exists
            sandbox_workdir = workspace.get_path("sandbox_workdir")
            generated_file = sandbox_workdir / output_path.name
            if generated_file.exists():
                logger.info(f"[TURN {num_turns}] Output file created: {output_path.name}")
                output_path.parent.mkdir(parents=True, exist_ok=True)
                if generated_file.resolve() != output_path.resolve():
                    shutil.copy(generated_file, output_path)
                    logger.info(f"[TURN {num_turns}] Copied to: {output_path}")
                success = True

        ended_at = datetime.utcnow()
        duration_sec = (ended_at - started_at).total_seconds()

        logger.info(f"[INFER] Completed {num_turns} turns, success={success}, duration={duration_sec:.2f}s")

        # Grade submission
        grade_score = None
        if output_path.exists():
            grade_score = self._grade_submission(task, output_path)
            if grade_score is not None:
                logger.info(f"[INFER] Grade score: {grade_score:.4f}")

        # Prepare result
        result = {
            "task_id": task_id,
            "run_name": run_name,
            "messages": conversation,
            "success": success,
            "num_turns": num_turns,
            "grade_score": grade_score,
            "duration_seconds": duration_sec,
        }

        # Save results
        self._save_results(
            workspace=workspace,
            task=task,
            run_name=run_name,
            description=description,
            io_instructions=io_instructions,
            conversation=conversation,
            success=success,
            num_turns=num_turns,
            started_at=started_at,
            ended_at=ended_at,
            duration_seconds=duration_sec,
            output_path=output_path,
            grade_score=grade_score,
        )

        return result


def parse_args():
    parser = argparse.ArgumentParser(description="DeepModeling Inference - Test trained models")

    # Model configuration
    parser.add_argument("--model-path", type=str, help="Path to model or HF model name")
    parser.add_argument("--api-endpoint", type=str, help="API endpoint (OpenAI compatible)")
    parser.add_argument("--use-local-model", action="store_true", help="Load model locally")

    # Agent configuration
    parser.add_argument("--max-turns", type=int, default=10, help="Max turns per task")
    parser.add_argument("--temperature", type=float, default=0.0, help="Sampling temperature")
    parser.add_argument("--sandbox-timeout", type=int, default=600, help="Sandbox timeout (seconds)")
    parser.add_argument("--workspace-dir", type=str, default="./workspace_infer", help="Workspace directory")

    # Task configuration
    parser.add_argument("--benchmark", type=str, default="engineering", help="Benchmark name")
    parser.add_argument("--data-root", type=Path, help="Data root directory")
    parser.add_argument("--task-id", type=str, help="Single task ID to run")
    parser.add_argument("--competitions", nargs="*", help="Competition IDs to run")
    parser.add_argument("--task-limit", type=int, help="Limit number of tasks")

    # Output configuration
    parser.add_argument("--output-dir", type=Path, default=Path("./results"), help="Output directory for results")
    parser.add_argument("--log-level", type=str, default="INFO", help="Logging level")

    return parser.parse_args()


def main():
    args = parse_args()

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, args.log_level.upper()),
        format='[%(levelname)s] %(message)s'
    )

    # Load tasks
    logger.info(f"Loading tasks from benchmark: {args.benchmark}")

    if args.task_id:
        # Single task mode
        logger.info(f"Running single task: {args.task_id}")
        tasks = load_benchmark_tasks(
            args.benchmark,
            data_root=args.data_root,
            competitions=[args.task_id],
            limit=1,
        )
    else:
        # Multiple tasks mode
        tasks = load_benchmark_tasks(
            args.benchmark,
            data_root=args.data_root,
            competitions=args.competitions,
            limit=args.task_limit,
        )

    if not tasks:
        logger.error("No tasks loaded!")
        return

    logger.info(f"Loaded {len(tasks)} tasks")

    # Create agent
    agent = DeepModelingInferenceAgent(
        model_path=args.model_path,
        api_endpoint=args.api_endpoint,
        max_turns=args.max_turns,
        workspace_dir=args.workspace_dir,
        sandbox_timeout=args.sandbox_timeout,
        temperature=args.temperature,
        use_local_model=args.use_local_model,
    )

    # Run inference on all tasks
    results = []
    for i, task in enumerate(tasks):
        logger.info(f"\n{'='*80}")
        logger.info(f"Task {i+1}/{len(tasks)}: {task['task_id']}")
        logger.info(f"{'='*80}")

        try:
            result = agent.run_inference(task)
            results.append(result)
        except Exception as e:
            logger.error(f"Failed to run task {task['task_id']}: {e}", exc_info=True)
            results.append({
                "task_id": task["task_id"],
                "error": str(e),
                "success": False,
            })

    # Save summary
    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = args.output_dir / f"summary_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"

    summary = {
        "total_tasks": len(tasks),
        "successful": sum(1 for r in results if r.get("success", False)),
        "failed": sum(1 for r in results if not r.get("success", False)),
        "avg_turns": sum(r.get("num_turns", 0) for r in results) / len(results) if results else 0,
        "avg_grade": sum(r.get("grade_score", 0) for r in results if r.get("grade_score") is not None) /
                     max(1, sum(1 for r in results if r.get("grade_score") is not None)),
        "results": results,
        "config": {
            "model_path": args.model_path,
            "benchmark": args.benchmark,
            "max_turns": args.max_turns,
            "temperature": args.temperature,
        }
    }

    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    logger.info(f"\n{'='*80}")
    logger.info(f"INFERENCE COMPLETE")
    logger.info(f"{'='*80}")
    logger.info(f"Total tasks: {summary['total_tasks']}")
    logger.info(f"Successful: {summary['successful']}")
    logger.info(f"Failed: {summary['failed']}")
    logger.info(f"Average turns: {summary['avg_turns']:.2f}")
    logger.info(f"Average grade: {summary['avg_grade']:.4f}")
    logger.info(f"Summary saved to: {summary_path}")


if __name__ == "__main__":
    main()

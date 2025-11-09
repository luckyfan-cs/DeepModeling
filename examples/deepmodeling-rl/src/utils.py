"""Utility functions for DeepModeling RL training."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .data_utils import DEFAULT_DATA_ROOTS

logger = logging.getLogger(__name__)

_custom_data_roots: Dict[str, Path] = {}


# ============================================================================
# Benchmark Grading Support
# ============================================================================

class BenchmarkGrader:
    """Centralized grading support for all benchmarks."""

    def __init__(self):
        """Initialize grading functions for all benchmarks."""
        self._grading_functions = {}
        self._registries = {}
        self._load_grading_modules()

    def _load_grading_modules(self):
        """Load grading functions and registries for all benchmarks."""

        # Engineering Benchmark
        try:
            from benchmarks.engineeringbench.grade import grade_csv
            from benchmarks.engineeringbench import registry as engineering_module

            data_root = _custom_data_roots.get("engineering", DEFAULT_DATA_ROOTS["engineering"])
            engineering_registry = engineering_module.Registry(data_root)
            engineering_module.registry = engineering_registry

            self._grading_functions["engineering"] = grade_csv
            self._registries["engineering"] = engineering_registry
            logger.info("Loaded engineeringbench grading support (data_root=%s)", data_root)
        except ImportError as e:
            logger.warning(f"Failed to load engineeringbench: {e}")

        # Math Modeling Benchmark
        try:
            from benchmarks.mathmodelingbench.grade import grade_csv
            from benchmarks.mathmodelingbench import registry
            self._grading_functions["mathmodeling"] = grade_csv
            self._registries["mathmodeling"] = registry
            logger.info("Loaded mathmodelingbench grading support")
        except ImportError as e:
            logger.warning(f"Failed to load mathmodelingbench: {e}")

        # MLE Benchmark
        try:
            from benchmarks.mlebench.grade import grade_csv
            from benchmarks.mlebench.registry import registry
            self._grading_functions["mle"] = grade_csv
            self._registries["mle"] = registry
            logger.info("Loaded mlebench grading support")
        except ImportError as e:
            logger.warning(f"Failed to load mlebench: {e}")

        # Science Benchmark
        try:
            from benchmarks.sciencebench.grade import grade_csv
            from benchmarks.sciencebench.registry import registry
            self._grading_functions["science"] = grade_csv
            self._registries["science"] = registry
            logger.info("Loaded sciencebench grading support")
        except ImportError as e:
            logger.warning(f"Failed to load sciencebench: {e}")

    def is_supported(self, benchmark: str) -> bool:
        """Check if a benchmark is supported."""
        return benchmark in self._grading_functions

    def grade_submission(
        self,
        task: Dict[str, Any],
        submission_path: Path
    ) -> Optional[float]:
        """Grade a submission and return normalized score.

        Args:
            task: Task data with benchmark info
            submission_path: Path to submission file

        Returns:
            Normalized score (higher is better) or None if grading fails
        """
        if not submission_path.exists():
            logger.warning(f"[GRADE] Submission file not found: {submission_path}")
            return None

        benchmark = task.get("benchmark", "engineering")
        competition_id = task["task_id"]

        if not self.is_supported(benchmark):
            logger.warning(f"[GRADE] No grading support for benchmark '{benchmark}'")
            return None

        try:
            # Get grading function and registry
            grade_fn = self._grading_functions[benchmark]
            registry = self._registries[benchmark]

            # Load competition and grade
            competition = registry.get_competition(competition_id)
            logger.info(f"[GRADE] Grading {competition_id} using {benchmark} benchmark...")

            report = grade_fn(submission_path, competition)

            score = report.score if report.score is not None else 0.0
            is_lower_better = getattr(report, 'is_lower_better', False)

            logger.info(f"[GRADE] Score: {score}, Lower is better: {is_lower_better}")

            # Normalize score for reward (higher is better)
            normalized_score = normalize_score(score, is_lower_better)

            return normalized_score

        except Exception as e:
            logger.error(f"[GRADE] Grading failed for {benchmark}: {e}", exc_info=True)
            return None


# Global grader instance
_grader = None


def set_benchmark_data_root(benchmark: str, data_root: Path | str) -> None:
    """Override the data root used when grading a benchmark."""

    resolved = Path(data_root).resolve()
    _custom_data_roots[benchmark.lower()] = resolved

    global _grader
    _grader = None  # Force reinitialization with new paths
    logger.info("Set %s benchmark data root to %s", benchmark, resolved)


def get_grader() -> BenchmarkGrader:
    """Get or create the global grader instance."""
    global _grader
    if _grader is None:
        _grader = BenchmarkGrader()
    return _grader


# ============================================================================
# Score Normalization
# ============================================================================

def normalize_score(score: float, is_lower_better: bool) -> float:
    """Normalize score to higher-is-better format.

    Args:
        score: Raw score value
        is_lower_better: Whether lower scores are better

    Returns:
        Normalized score where higher is always better
    """
    if is_lower_better:
        # For metrics like MAE, RMSE where lower is better
        # Use 1/(1+score) to invert: 0->1, infinity->0
        return 1.0 / (1.0 + score) if score > 0 else 1.0
    else:
        # For metrics like accuracy where higher is better
        return score


# ============================================================================
# Conversation Formatting
# ============================================================================

def format_conversation(messages: List[Dict[str, str]]) -> str:
    """Format conversation history as text.

    Args:
        messages: List of message dicts with 'role' and 'content'

    Returns:
        Formatted conversation string
    """
    lines = []
    for msg in messages:
        role = msg["role"].upper()
        content = msg["content"]
        lines.append(f"<{role}>\n{content}\n</{role}>")
    return "\n\n".join(lines)


# ============================================================================
# JSONL Writing
# ============================================================================

def write_jsonl(data: List[Dict[str, Any]], output_path: Path) -> None:
    """Write list of dicts as JSONL file.

    Args:
        data: List of dictionaries to write
        output_path: Path to output JSONL file
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [json.dumps(item, ensure_ascii=False) for item in data]
    content = "\n".join(lines)

    output_path.write_text(content, encoding="utf-8")


# ============================================================================
# Episode Metadata Builder
# ============================================================================

def build_episode_metadata(
    *,
    run_name: str,
    workspace_dir: Path,
    task: Dict[str, Any],
    description: str,
    io_instructions: str,
    output_path: Path,
    success: bool,
    num_turns: int,
    started_at,
    ended_at,
    duration_seconds: float,
    grade_score: Optional[float],
) -> Dict[str, Any]:
    """Build episode metadata structure.

    Args:
        run_name: Unique run name
        workspace_dir: Workspace directory path
        task: Original task data
        description: Task description
        io_instructions: I/O instructions
        output_path: Expected output file path
        success: Whether episode succeeded
        num_turns: Number of turns executed
        started_at: Start timestamp
        ended_at: End timestamp
        duration_seconds: Total duration
        grade_score: Grading score (if available)

    Returns:
        Metadata dictionary
    """
    return {
        "run_name": run_name,
        "workspace_dir": str(workspace_dir),
        "workflow": "rl_scientific_method",
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
    }

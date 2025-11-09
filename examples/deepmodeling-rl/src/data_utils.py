"""Utilities for building RL training datasets from DeepModeling benchmarks."""

from __future__ import annotations

import logging
import sys
import textwrap
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

# Add DeepModeling root to Python path for benchmarks import
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from benchmarks.engineeringbench.registry import Registry

logger = logging.getLogger(__name__)

DEFAULT_DATA_ROOTS = {
    "engineering": PROJECT_ROOT / "data" / "engineering-bench" / "competitions",
    "mathmodeling": PROJECT_ROOT / "data" / "mathmodeling-bench" / "competitions",
}

PREDEFINED_SPLITS = {
    "engineering_mini": {
        "benchmark": "engineering",
        "train": [
            "industry-0",
            "industry-1",
            "industry-2",
            "industry-3",
            "industry-6",
            "industry-7",
            "industry-8",
            "industry-9",
            "industry-10",
            "industry-11",
            "industry-12",
            "industry-13",
            "industry-14",
            "industry-15",
            "industry-16",
            "industry-17",
        ],
        "val": [
            "industry-4",
            "industry-5",
            "industry-18",
            "industry-19",
        ],
    },
    "engineering_valset": {
        "benchmark": "engineering",
        "train": [
            "industry-10",
            "industry-11",
            "industry-12",
            "industry-13",
            "industry-14",
        ],
        "val": [
            "industry-15",
            "industry-16",
        ],
    },
    "mathmodeling_pair": {
        "benchmark": "mathmodeling",
        "train": [
            "mamo-complex-0",
        ],
        "val": [
            "mamo-complex-1",
        ],
    },
}


def load_benchmark_tasks(
    benchmark: str = "engineering",
    *,
    data_root: Optional[Path | str] = None,
    competitions: Optional[Sequence[str]] = None,
    limit: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """Load RL tasks from the specified benchmark."""

    benchmark_key = benchmark.lower()
    if benchmark_key not in DEFAULT_DATA_ROOTS:
        raise ValueError(f"Unsupported benchmark '{benchmark}'.")

    resolved_root = Path(data_root) if data_root else DEFAULT_DATA_ROOTS[benchmark_key]

    if benchmark_key == "engineering":
        return _load_engineering_tasks(resolved_root, competitions, limit)

    raise ValueError(f"Benchmark '{benchmark}' is not implemented yet.")


def load_predefined_split(
    split_name: str,
    *,
    data_root: Optional[Path | str] = None,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Load tasks according to a named train/val split."""

    try:
        split = PREDEFINED_SPLITS[split_name]
    except KeyError as exc:
        raise ValueError(f"Unknown split '{split_name}'. Available: {list(PREDEFINED_SPLITS)}") from exc

    benchmark = split["benchmark"]
    split_specific_root = split.get("data_root")
    resolved_root = Path(split_specific_root) if split_specific_root else data_root

    train_ids = split.get("train", [])
    val_ids = split.get("val", [])

    train_tasks = load_benchmark_tasks(
        benchmark,
        data_root=resolved_root,
        competitions=train_ids or None,
    )

    val_tasks = load_benchmark_tasks(
        benchmark,
        data_root=resolved_root,
        competitions=val_ids or None,
    ) if val_ids else []

    return train_tasks, val_tasks


def split_dataset(
    tasks: List[Dict[str, Any]],
    val_ratio: float = 0.2,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Split tasks into train/validation lists."""

    if not tasks:
        return [], []

    if val_ratio <= 0 or len(tasks) < 2:
        return tasks, []

    val_count = max(1, int(len(tasks) * val_ratio))
    val_count = min(val_count, len(tasks) - 1)

    val_tasks = tasks[:val_count]
    train_tasks = tasks[val_count:]

    return train_tasks, val_tasks


def _load_engineering_tasks(
    data_root: Path,
    competitions: Optional[Sequence[str]],
    limit: Optional[int],
) -> List[Dict[str, Any]]:
    """Load prepared engineering-bench competitions as RL tasks."""

    registry = Registry(data_root)
    competition_ids = list(competitions) if competitions else registry.list_competition_ids()
    competition_ids = sorted(dict.fromkeys(competition_ids))

    tasks: List[Dict[str, Any]] = []
    for competition_id in competition_ids:
        try:
            competition = registry.get_competition(competition_id)
        except Exception as exc:
            logger.warning("Skipping %s: %s", competition_id, exc)
            continue

        public_dir = competition.public_dir
        if not public_dir.exists():
            logger.warning("Public data directory missing for %s at %s", competition_id, public_dir)
            continue

        prompt = _format_engineering_prompt(
            competition.description,
            public_dir,
            Path(competition.sample_submission).name,
        )

        tasks.append(
            {
                "task_id": competition.id,
                "benchmark": "engineering",
                "competition_id": competition.id,
                "prompt": prompt,
                "data_dir": str(public_dir),
                "expected_output_path": "submission.csv",
                "eval_metric": "leaderboard_score",
                "threshold": 0.75,
            }
        )

        if limit and len(tasks) >= limit:
            break

    if not tasks:
        logger.warning("No engineering tasks loaded from %s", data_root)

    return tasks


def _format_engineering_prompt(description: str, public_dir: Path, sample_name: str) -> str:
    """Compose the natural language prompt for Kaggle-style competitions."""

    return textwrap.dedent(
        f"""
        {description.strip()}

        Additional instructions:
        - All prepared input files are located under `{public_dir}`.
        - Use `{sample_name}` as the schema reference for your prediction file.
        - Save your final predictions to `submission.csv` in the current working directory.
        - Keep the Scientific Method structure in your reasoning before running experiments.
        """
    ).strip()


__all__ = [
    "load_benchmark_tasks",
    "load_predefined_split",
    "split_dataset",
    "DEFAULT_DATA_ROOTS",
    "PREDEFINED_SPLITS",
    "PROJECT_ROOT",
]

#!/usr/bin/env python3
"""Train the DeepModeling agent with Agent-Lightning VERL."""

from __future__ import annotations

import argparse
import logging
import os
import random
import sys
from pathlib import Path
from typing import List

# Add DeepModeling root to Python path for benchmarks import
_DEEPMODELING_ROOT = Path(__file__).resolve().parents[2]
if str(_DEEPMODELING_ROOT) not in sys.path:
    sys.path.insert(0, str(_DEEPMODELING_ROOT))

import agentlightning as agl

from config import resolve_config
from data_utils import (
    PREDEFINED_SPLITS,
    load_benchmark_tasks,
    load_predefined_split,
    split_dataset,
)
from deepmodeling_agent import DeepModelingConfig, LitDeepModelingAgent

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train the DeepModeling RL agent with Agent-Lightning")

    parser.add_argument("config", choices=["fast", "standard", "advanced"], help="Training preset to use")
    parser.add_argument("--benchmark", default="engineering", help="Benchmark to turn into RL tasks (default: engineering)")
    parser.add_argument("--split", choices=sorted(PREDEFINED_SPLITS.keys()), help="Use a predefined train/val split")
    parser.add_argument("--data-root", type=Path, help="Override path to prepared benchmark data")
    parser.add_argument("--competitions", nargs="*", help="Subset of competition IDs to load")
    parser.add_argument("--task-limit", type=int, help="Optional cap on the number of tasks to load")
    parser.add_argument(
        "--min-train-tasks",
        type=int,
        default=4,
        help="Ensure at least this many training tasks by falling back to the benchmark pool when needed",
    )
    parser.add_argument("--val-ratio", type=float, default=0.2, help="Fraction of tasks reserved for validation")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for shuffling tasks")
    parser.add_argument("--workspace-dir", type=Path, default=Path("./workspace_rl"), help="Base directory for sandboxes")
    parser.add_argument("--sandbox-timeout", type=int, default=600, help="Sandbox timeout in seconds")
    parser.add_argument("--max-turns", type=int, default=3, help="Maximum Scientific Method iterations per task")
    parser.add_argument("--model-path", type=str, help="Override the HF model path used for VERL actor/ref")
    parser.add_argument("--val-temperature", type=float, default=0.0, help="Temperature for validation/test rollouts")
    parser.add_argument("--n-runners", type=int, default=1, help="Number of parallel Agent-Lightning runners")
    parser.add_argument("--agent-match", type=str, help="Optional agent adapter match value")
    parser.add_argument("--log-level", default="INFO", help="Python logging level")

    return parser.parse_args()


def configure_logging(log_level: str) -> None:
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    logging.basicConfig(level=numeric_level, format="[%(levelname)s] %(message)s")


def _ensure_min_train_tasks(
    train_tasks: List[dict],
    *,
    min_required: int,
    benchmark: str,
    data_root: Path | None,
) -> List[dict]:
    if len(train_tasks) >= max(1, min_required):
        return train_tasks

    logger.warning(
        "Train dataset only has %d tasks (<%d). Adding fallback competitions from benchmark '%s'.",
        len(train_tasks),
        min_required,
        benchmark,
    )

    fallback = load_benchmark_tasks(benchmark, data_root=data_root)
    existing_ids = {task["task_id"] for task in train_tasks}
    for task in fallback:
        if task["task_id"] in existing_ids:
            continue
        train_tasks.append(task)
        existing_ids.add(task["task_id"])
        if len(train_tasks) >= max(1, min_required):
            break

    if len(train_tasks) < max(1, min_required):
        logger.error(
            "Only %d training tasks available after fallback; consider preparing more competitions or lowering --min-train-tasks",
            len(train_tasks),
        )

    return train_tasks


def prepare_datasets(args: argparse.Namespace) -> tuple[List[dict], List[dict]]:
    if args.split:
        train_tasks, val_tasks = load_predefined_split(args.split, data_root=args.data_root)
        if args.task_limit:
            train_tasks = train_tasks[: args.task_limit]
        logger.info(
            "Loaded predefined split '%s': %d train / %d val tasks",
            args.split,
            len(train_tasks),
            len(val_tasks),
        )
        if not train_tasks:
            logger.warning("Split '%s' produced no training tasks before fallback.", args.split)

        split_benchmark = (
            (train_tasks[0]["benchmark"] if train_tasks else None)
            or (val_tasks[0]["benchmark"] if val_tasks else None)
            or args.benchmark
        )
        train_tasks = _ensure_min_train_tasks(
            train_tasks,
            min_required=args.min_train_tasks,
            benchmark=split_benchmark,
            data_root=args.data_root,
        )
        return train_tasks, val_tasks

    tasks = load_benchmark_tasks(
        args.benchmark,
        data_root=args.data_root,
        competitions=args.competitions,
        limit=args.task_limit,
    )

    if not tasks:
        raise RuntimeError("No tasks were loaded. Check your --benchmark/--data-root settings.")

    random.Random(args.seed).shuffle(tasks)
    train_tasks, val_tasks = split_dataset(tasks, args.val_ratio)

    train_tasks = _ensure_min_train_tasks(
        train_tasks,
        min_required=args.min_train_tasks,
        benchmark=args.benchmark,
        data_root=args.data_root,
    )

    logger.info(
        "Prepared %d tasks (%d train / %d val) from benchmark '%s'",
        len(tasks),
        len(train_tasks),
        len(val_tasks),
        args.benchmark,
    )

    return train_tasks, val_tasks


def maybe_override_model_path(config: dict, model_path: str | None) -> None:
    if model_path:
        config["actor_rollout_ref"]["model"]["path"] = model_path
        logger.info("Using custom model path: %s", model_path)


def _ensure_ray_init(config: dict) -> None:
    """Ensure ray_init config exists.

    Note: VERL's ray_init only supports num_cpus and timeline_json_file.
    Other Ray settings are handled by VERL internally.
    """
    if "ray_init" not in config:
        # If ray_init is missing, add minimal defaults (only valid VERL keys)
        config["ray_init"] = {
            "num_cpus": max((os.cpu_count() or 2) - 1, 1),
        }
    # If ray_init exists (from config.py), we trust those values


def main() -> None:
    args = parse_args()
    configure_logging(args.log_level)

    config = resolve_config(args.config)
    maybe_override_model_path(config, args.model_path)
    _ensure_ray_init(config)

    train_tasks, val_tasks = prepare_datasets(args)

    dm_config = DeepModelingConfig(
        sandbox_timeout=args.sandbox_timeout,
        max_turns=args.max_turns,
        workspace_dir=str(args.workspace_dir),
    )

    agent = LitDeepModelingAgent(
        config=dm_config,
        val_temperature=args.val_temperature,
    )

    algorithm = agl.VERL(config)
    adapter = {"agent_match": args.agent_match or f"deepmodeling-{args.config}"}
    trainer = agl.Trainer(n_runners=args.n_runners, algorithm=algorithm, adapter=adapter)

    val_dataset = val_tasks if val_tasks else None

    logger.info(
        "Starting training with config='%s', runners=%d, agent_match='%s'",
        args.config,
        args.n_runners,
        adapter["agent_match"],
    )

    trainer.fit(agent, train_dataset=train_tasks, val_dataset=val_dataset)


if __name__ == "__main__":
    main()

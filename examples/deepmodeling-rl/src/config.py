"""Training configuration presets for DeepModeling RL runs."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any, Dict
import multiprocessing as mp
import os


def _resolve_gpus_per_node(default: int = 8) -> int:
    """Return the GPU count (default 8) while tolerating bad env input."""

    raw_value = os.environ.get("DM_NUM_GPUS")
    if raw_value is None:
        return default
    try:
        parsed = int(raw_value)
    except ValueError:
        return default
    return max(parsed, 1)


GPUS_PER_NODE = _resolve_gpus_per_node()
PER_GPU_TRAIN_BATCH = 1
TRAIN_BATCH_SIZE = max(PER_GPU_TRAIN_BATCH * GPUS_PER_NODE, 1)
PPO_MICRO_BATCH_SIZE = max(PER_GPU_TRAIN_BATCH, 1)
PPO_MINI_BATCH_SIZE = max(TRAIN_BATCH_SIZE, 1)


BASE_RL_CONFIG: Dict[str, Any] = {
    "algorithm": {
        "adv_estimator": "grpo",
        "use_kl_in_reward": False,
    },
    "ray_init": {
        "num_cpus": max((mp.cpu_count() or 2) - 1, 1),
        # Note: VERL's ray_init only supports num_cpus and timeline_json_file
        # Other Ray settings like num_gpus are handled by VERL internally via trainer.n_gpus_per_node
    },
    "data": {
        "train_batch_size": TRAIN_BATCH_SIZE,  # Divisible by GPUS_PER_NODE
        "max_prompt_length": 4096,
        "max_response_length": 2048,
        "truncation": "error",
    },
    "actor_rollout_ref": {
        "rollout": {
            "tensor_model_parallel_size": 1,
            "n": 2,
            "log_prob_micro_batch_size_per_gpu": PPO_MICRO_BATCH_SIZE,
            "multi_turn": {"format": "hermes"},
            "name": "vllm",
            "gpu_memory_utilization": 0.6,
            "mode": "async",  # Agent mode requires async rollouts when using the LLM proxy
        },
        "actor": {
            "ppo_mini_batch_size": PPO_MINI_BATCH_SIZE,
            "ppo_micro_batch_size_per_gpu": PPO_MICRO_BATCH_SIZE,
            "optim": {"lr": 1e-6},
            "use_kl_loss": False,
            "kl_loss_coef": 0.0,
            "entropy_coeff": 0.0,
            "clip_ratio_low": 0.2,
            "clip_ratio_high": 0.3,
            "fsdp_config": {
                "param_offload": True,
                "optimizer_offload": True,
            },
        },
        "ref": {
            "log_prob_micro_batch_size_per_gpu": 4,
            "fsdp_config": {"param_offload": True},
        },
        "model": {
            "path": "/home/aiops/liufan/projects/models/Qwen2.5-7B-Instruct",
            "use_remove_padding": True,
            "enable_gradient_checkpointing": True,
        },
    },
    "trainer": {
        "n_gpus_per_node": GPUS_PER_NODE,  # Single-node, multi-GPU (default: 8)
        "val_before_train": True,
        "critic_warmup": 0,
        "logger": ["console"],
        "project_name": "DeepModeling-RL",
        "experiment_name": "deepmodeling",
        "nnodes": 1,
        "test_freq": 16,
        "total_epochs": 2,
    },
}


def config_train_fast() -> Dict[str, Any]:
    """Configuration tuned for smoke tests and CI."""

    config = deepcopy(BASE_RL_CONFIG)
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    config["trainer"].update(
        {
            "project_name": "DeepModeling-RL-CI",
            "experiment_name": f"deepmodeling_fast_{timestamp}",
            "total_epochs": 1,
            "total_training_steps": 1,
            "test_freq": 1,
        }
    )
    config["actor_rollout_ref"]["rollout"]["n"] = 1
    config["actor_rollout_ref"]["model"]["path"] = "/home/aiops/liufan/projects/models/Qwen2.5-7B-Instruct"
    return config


def config_train_standard() -> Dict[str, Any]:
    """Default configuration for daily training."""

    config = deepcopy(BASE_RL_CONFIG)
    timestamp = datetime.utcnow().strftime("%Y%m%d")
    config["trainer"].update(
        {
            "project_name": "DeepModeling-RL",
            "experiment_name": f"deepmodeling_standard_{timestamp}",
            "total_epochs": 2,
            "test_freq": 8,
        }
    )
    return config


def config_train_advanced() -> Dict[str, Any]:
    """More exhaustive configuration for longer runs or larger models."""

    config = deepcopy(BASE_RL_CONFIG)
    config["actor_rollout_ref"]["rollout"]["gpu_memory_utilization"] = 0.9
    config["actor_rollout_ref"]["actor"]["ppo_mini_batch_size"] = 32
    config["actor_rollout_ref"]["actor"]["ppo_micro_batch_size_per_gpu"] = 4
    config["actor_rollout_ref"]["actor"]["optim"]["lr"] = 5e-7
    config["trainer"].update(
        {
            "project_name": "DeepModeling-RL-Advanced",
            "experiment_name": "deepmodeling_advanced",
            "total_epochs": 4,
            "test_freq": 6,
        }
    )
    return config


CONFIG_BUILDERS = {
    "fast": config_train_fast,
    "standard": config_train_standard,
    "advanced": config_train_advanced,
}


def resolve_config(mode: str) -> Dict[str, Any]:
    """Return a config dictionary for the requested mode."""

    try:
        builder = CONFIG_BUILDERS[mode]
    except KeyError as exc:
        raise ValueError(f"Unknown training mode '{mode}'") from exc
    return builder()


__all__ = [
    "BASE_RL_CONFIG",
    "config_train_fast",
    "config_train_standard",
    "config_train_advanced",
    "resolve_config",
]

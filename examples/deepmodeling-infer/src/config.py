"""Configuration for DeepModeling inference."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict


# Default inference configurations
DEFAULT_INFER_CONFIG: Dict[str, Any] = {
    # Model configuration
    "model": {
        "path": "/home/aiops/liufan/projects/models/Qwen2.5-7B-Instruct",  # Default model path
        "api_endpoint": None,  # If using API endpoint instead of local model
    },

    # Agent configuration
    "agent": {
        "max_turns": 10,  # Maximum number of scientific method iterations
        "temperature": 0.0,  # Temperature for inference (0.0 = greedy)
        "sandbox_timeout": 600,  # Sandbox execution timeout (seconds)
    },

    # Workspace configuration
    "workspace": {
        "base_dir": "./workspace_infer",  # Base directory for workspaces
    },

    # Benchmark configuration
    "benchmark": {
        "name": "engineering",  # Default benchmark to use
        "data_root": None,  # Will use default data root if None
    },
}


def create_infer_config(
    model_path: str = None,
    api_endpoint: str = None,
    max_turns: int = None,
    temperature: float = None,
    sandbox_timeout: int = None,
    workspace_dir: str = None,
    benchmark: str = None,
    data_root: Path = None,
) -> Dict[str, Any]:
    """Create inference configuration with optional overrides.

    Args:
        model_path: Path to model checkpoint or HF model name
        api_endpoint: API endpoint for LLM (if using API instead of local)
        max_turns: Maximum number of turns per episode
        temperature: Sampling temperature
        sandbox_timeout: Timeout for sandbox execution
        workspace_dir: Base directory for workspaces
        benchmark: Benchmark name
        data_root: Root directory for benchmark data

    Returns:
        Configuration dictionary
    """
    config = {
        "model": {
            "path": model_path or DEFAULT_INFER_CONFIG["model"]["path"],
            "api_endpoint": api_endpoint or DEFAULT_INFER_CONFIG["model"]["api_endpoint"],
        },
        "agent": {
            "max_turns": max_turns or DEFAULT_INFER_CONFIG["agent"]["max_turns"],
            "temperature": temperature if temperature is not None else DEFAULT_INFER_CONFIG["agent"]["temperature"],
            "sandbox_timeout": sandbox_timeout or DEFAULT_INFER_CONFIG["agent"]["sandbox_timeout"],
        },
        "workspace": {
            "base_dir": workspace_dir or DEFAULT_INFER_CONFIG["workspace"]["base_dir"],
        },
        "benchmark": {
            "name": benchmark or DEFAULT_INFER_CONFIG["benchmark"]["name"],
            "data_root": str(data_root) if data_root else DEFAULT_INFER_CONFIG["benchmark"]["data_root"],
        },
    }

    return config


__all__ = [
    "DEFAULT_INFER_CONFIG",
    "create_infer_config",
]

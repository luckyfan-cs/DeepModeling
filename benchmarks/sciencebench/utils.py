import importlib
import logging
import yaml
from logging import Logger
from pathlib import Path
from typing import Any, Callable


def get_logger(name: str) -> Logger:
    """Get a logger instance"""
    return logging.getLogger(name)


def get_module_dir() -> Path:
    """Returns an absolute path to the sciencebench module."""
    path = Path(__file__).parent.resolve()
    assert path.name == "sciencebench", \
        f"Expected the module directory to be `sciencebench`, but got `{path.name}`."
    return path


def get_repo_dir() -> Path:
    """Returns an absolute path to the repository directory."""
    return get_module_dir().parent


def load_yaml(path: Path) -> dict:
    """Load a YAML file and return its content as a dictionary."""
    with open(path, "r") as f:
        return yaml.safe_load(f)


def import_fn(fn_string: str) -> Callable:
    """
    Import a function from a string.

    Args:
        fn_string: String in the format 'module.path:function_name'

    Returns:
        The imported function
    """
    module_path, fn_name = fn_string.rsplit(":", 1)

    # Handle benchmarks prefix
    if module_path.startswith("benchmarks."):
        # Module path is relative to benchmarks directory
        module = importlib.import_module(module_path, package="benchmarks")
    else:
        module = importlib.import_module(module_path)

    return getattr(module, fn_name)

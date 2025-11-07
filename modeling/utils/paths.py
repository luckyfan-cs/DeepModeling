# modeling/utils/paths.py

"""
Centralized path management for the Modeling framework.
Provides consistent and maintainable access to project directories.
"""

from pathlib import Path
from typing import Optional


def get_project_root() -> Path:
    """
    Get the root directory of the DeepModeling project.

    Returns:
        Path: Absolute path to the project root directory
    """
    # This file is at: modeling/utils/paths.py
    # So project root is 2 levels up
    return Path(__file__).resolve().parent.parent.parent


def get_benchmarks_dir(benchmark_name: Optional[str] = None) -> Path:
    """
    Get the benchmarks directory or a specific benchmark subdirectory.

    Args:
        benchmark_name: Optional name of specific benchmark (e.g., 'mlebench', 'sciencebench')

    Returns:
        Path: Path to benchmarks directory or specific benchmark
    """
    benchmarks_path = get_project_root() / "benchmarks"

    if benchmark_name:
        return benchmarks_path / benchmark_name
    return benchmarks_path


def get_data_dir(data_name: Optional[str] = None) -> Path:
    """
    Get the data directory or a specific data subdirectory.

    Args:
        data_name: Optional name of specific data directory

    Returns:
        Path: Path to data directory or specific subdirectory
    """
    data_path = get_project_root() / "data"

    if data_name:
        return data_path / data_name
    return data_path


def get_config_file() -> Path:
    """
    Get the path to the main config.yaml file.

    Returns:
        Path: Path to config.yaml
    """
    return get_project_root() / "config.yaml"


def get_modeling_dir() -> Path:
    """
    Get the modeling framework directory.

    Returns:
        Path: Path to modeling directory
    """
    return Path(__file__).resolve().parent.parent


def get_runs_dir() -> Path:
    """
    Get the runs output directory.

    Returns:
        Path: Path to runs directory
    """
    return get_project_root() / "runs"


# For backward compatibility, expose commonly used paths as module-level constants
PROJECT_ROOT = get_project_root()
BENCHMARKS_DIR = get_benchmarks_dir()
DATA_DIR = get_data_dir()
CONFIG_FILE = get_config_file()
MODELING_DIR = get_modeling_dir()
RUNS_DIR = get_runs_dir()

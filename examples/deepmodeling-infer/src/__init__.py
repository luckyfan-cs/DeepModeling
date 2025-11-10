"""DeepModeling Inference Package - Test trained SFT and RL models."""

from .config import create_infer_config, DEFAULT_INFER_CONFIG
from .infer import DeepModelingInferenceAgent
from .utils import get_grader, set_benchmark_data_root
from .data_utils import load_benchmark_tasks, DEFAULT_DATA_ROOTS

__version__ = "1.0.0"

__all__ = [
    "DeepModelingInferenceAgent",
    "create_infer_config",
    "DEFAULT_INFER_CONFIG",
    "load_benchmark_tasks",
    "get_grader",
    "set_benchmark_data_root",
    "DEFAULT_DATA_ROOTS",
]

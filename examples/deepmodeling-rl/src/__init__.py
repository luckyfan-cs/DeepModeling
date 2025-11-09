"""DeepModeling RL Training Framework.

A reinforcement learning training framework for DeepModeling agents,
supporting multiple benchmarks including engineering, mathmodeling, mle, and science.
"""

__version__ = "0.1.0"

from .agent import SimpleDeepModelingAgent, LitDeepModelingAgent
from .reward_function import calculate_reward, calculate_detailed_reward
from .utils import get_grader, BenchmarkGrader

__all__ = [
    "SimpleDeepModelingAgent",
    "LitDeepModelingAgent",
    "calculate_reward",
    "calculate_detailed_reward",
    "get_grader",
    "BenchmarkGrader",
]

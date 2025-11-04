"""
Grading function for ScienceBench task 85
"""

import pandas as pd
import numpy as np
from pathlib import Path


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    """
    Grade submission using exact match.

    Args:
        submission: DataFrame with predictions
        answers: DataFrame with ground truth

    Returns:
        Match ratio (0-1)
    """
    # 逐元素比较
    if submission.shape != answers.shape:
        print(f"Shape mismatch: submission {submission.shape} vs answers {answers.shape}")
        return 0.0

    # 计算匹配比例
    matches = (submission.values == answers.values).sum()
    total = submission.size

    return matches / total if total > 0 else 0.0

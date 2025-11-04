"""
Grading function for ScienceBench task 19
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics import accuracy_score


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    """
    Grade submission using accuracy metric.

    Args:
        submission: DataFrame with predictions
        answers: DataFrame with ground truth

    Returns:
        Accuracy score (0-1)
    """
    # 对齐数据
    if 'id' in submission.columns and 'id' in answers.columns:
        merged = pd.merge(answers, submission, on='id', suffixes=('_true', '_pred'))

        # 找到预测列
        pred_col = [c for c in merged.columns if c.endswith('_pred')][0]
        true_col = pred_col.replace('_pred', '_true')

        return accuracy_score(merged[true_col], merged[pred_col])
    else:
        # 简单比较
        return float(np.mean(submission.values == answers.values))

"""
Grading function for ScienceBench task 29
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics import mean_squared_error


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    """
    Grade submission using RMSE metric (lower is better).

    Args:
        submission: DataFrame with predictions
        answers: DataFrame with ground truth

    Returns:
        Negative RMSE (higher is better for consistency)
    """
    # 对齐数据
    if 'id' in submission.columns and 'id' in answers.columns:
        merged = pd.merge(answers, submission, on='id', suffixes=('_true', '_pred'))

        # 找到预测列
        pred_col = [c for c in merged.columns if c.endswith('_pred')][0]
        true_col = pred_col.replace('_pred', '_true')

        rmse = mean_squared_error(merged[true_col], merged[pred_col], squared=False)
        return -rmse  # 负数，因为更高的分数更好
    else:
        # 简单 RMSE
        rmse = np.sqrt(np.mean((submission.values - answers.values) ** 2))
        return -rmse

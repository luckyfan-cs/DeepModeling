"""
Grading function for ScienceBench Task 102: refractive_index_prediction
Based on eval_programs/eval_refractive_index_prediction.py
"""

import pandas as pd
import numpy as np


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    """
    Grade submission using Mean Absolute Error (MAE) metric.

    Lower MAE is better. The score is inverted to make higher better.

    Args:
        submission: DataFrame with columns [id or index, refractive_index]
        answers: DataFrame with columns [id or index, refractive_index]

    Returns:
        float: Normalized score (higher is better)
    """
    try:
        # Check for refractive_index column
        if 'refractive_index' not in submission.columns:
            print(f"Missing column. Expected 'refractive_index', Got: {list(submission.columns)}")
            return 0.0

        if 'refractive_index' not in answers.columns:
            print(f"Missing column in answers. Expected 'refractive_index', Got: {list(answers.columns)}")
            return 0.0

        # Calculate MAE
        y_pred = submission['refractive_index'].values
        y_true = answers['refractive_index'].values

        if len(y_pred) != len(y_true):
            print(f"Length mismatch: submission has {len(y_pred)} rows, answers has {len(y_true)} rows")
            return 0.0

        mae = np.abs(y_pred - y_true).mean()

        print(f"Mean Absolute Error (MAE): {mae:.6f}")
        print(f"Threshold for passing: MAE < 0.78")

        # Convert MAE to a score where lower MAE = higher score
        # Original threshold: MAE < 0.78
        # Score = 1 if MAE = 0, score approaches 0 as MAE increases
        # Use inverse scoring: score = max(0, 1 - MAE/threshold)
        threshold = 0.78
        if mae < threshold:
            # Good performance: normalize to 0.5-1.0 range
            score = 1.0 - (mae / threshold) * 0.5
        else:
            # Poor performance: normalize to 0.0-0.5 range
            score = max(0.0, 0.5 * (1.0 - (mae - threshold) / threshold))

        print(f"Normalized score: {score:.4f}")

        return float(score)

    except Exception as e:
        print(f"Error in grading: {e}")
        import traceback
        traceback.print_exc()
        return 0.0

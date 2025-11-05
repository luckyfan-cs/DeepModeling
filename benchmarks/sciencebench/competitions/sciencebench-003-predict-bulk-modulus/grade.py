"""Grading function for ScienceBench task 3 (predict bulk modulus)."""

from pathlib import Path

import pandas as pd
from sklearn.metrics import root_mean_squared_error


THRESHOLD = 24.0


def _round_numeric(df: pd.DataFrame, decimals: int = 4) -> pd.DataFrame:
    if df.empty:
        return df
    return df.round(decimals=decimals)


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    """Match the original evaluation: data correctness + RMSE threshold."""

    submission = submission.copy()
    answers = answers.copy()

    # Ensure required columns exist
    required_cols = {"material_id", "K_VRH"}
    if not required_cols.issubset(submission.columns) or not required_cols.issubset(answers.columns):
        print(f"Missing required columns. Submission columns: {submission.columns}")
        return 0.0

    submission = submission["material_id"].to_frame().join(submission[["K_VRH"]])
    answers = answers["material_id"].to_frame().join(answers[["K_VRH"]])

    data_correctness = list(submission["material_id"]) == list(answers["material_id"])
    if not data_correctness:
        print("material_id ordering mismatch between submission and answers")
        return 0.0

    pred = _round_numeric(submission[["K_VRH"]])
    gold = _round_numeric(answers[["K_VRH"]])

    rmse = root_mean_squared_error(gold, pred)
    print(f"RMSE: {rmse}")

    if rmse <= THRESHOLD:
        return 1.0
    return 0.0

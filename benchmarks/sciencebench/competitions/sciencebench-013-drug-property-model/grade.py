"""Grading function for ScienceBench Task 13 (HIV property prediction)."""

from __future__ import annotations

import pandas as pd
from sklearn.metrics import f1_score

REQUIRED_COLUMNS = {"smiles", "HIV_active"}
F1_THRESHOLD = 0.43


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    """
    Evaluate predictions using F1 score with ordering validation.

    Args:
        submission: DataFrame produced by the participant.
        answers: Ground-truth DataFrame provided by the benchmark.

    Returns:
        1.0 if the SMILES ordering matches and F1 >= threshold; otherwise 0.0.
    """
    if submission.empty:
        print("Submission is empty.")
        return 0.0

    if not REQUIRED_COLUMNS.issubset(submission.columns):
        print(f"Submission missing required columns: {REQUIRED_COLUMNS - set(submission.columns)}")
        return 0.0

    if not REQUIRED_COLUMNS.issubset(answers.columns):
        print("Answer file is missing required columns.")
        return 0.0

    # Ensure ordering matches exactly.
    if list(submission["smiles"]) != list(answers["smiles"]):
        print("SMILES ordering mismatch.")
        return 0.0

    # Compute F1 score on the aligned columns.
    metric = f1_score(answers["HIV_active"].values, submission["HIV_active"].values)
    print(f"F1 score: {metric}")

    return 1.0 if metric >= F1_THRESHOLD else 0.0

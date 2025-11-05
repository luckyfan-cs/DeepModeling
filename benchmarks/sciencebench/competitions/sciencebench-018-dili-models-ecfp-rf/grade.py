"""Grading function for ScienceBench Task 18 (DILI RF models)."""

from __future__ import annotations

import pandas as pd
from sklearn.metrics import f1_score

REQUIRED_COLUMNS = {"standardised_smiles", "label"}


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    """Return the F1 score between submission and answers."""
    if submission.empty:
        print("Submission is empty.")
        return 0.0
    if answers.empty:
        print("Answer data is empty.")
        return 0.0

    if not REQUIRED_COLUMNS.issubset(submission.columns):
        print(f"Submission missing columns: {REQUIRED_COLUMNS - set(submission.columns)}")
        return 0.0
    if not REQUIRED_COLUMNS.issubset(answers.columns):
        print("Answers missing required columns.")
        return 0.0

    if list(submission["standardised_smiles"]) != list(answers["standardised_smiles"]):
        print("SMILES ordering mismatch.")
        return 0.0

    f1 = f1_score(answers["label"].values, submission["label"].values, pos_label="DILI")
    print(f"F1 score: {f1}")
    return float(f1)

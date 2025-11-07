"""
Grading logic for ScienceBench task 67 (cognitive pattern similarity).
"""

from __future__ import annotations

import pandas as pd

EXPECTED_COLUMNS = {"conscientiousness", "openness"}


def _listify(df: pd.DataFrame) -> list:
    if not EXPECTED_COLUMNS.issubset(df.columns):
        raise ValueError(f"Submission must include columns: {', '.join(sorted(EXPECTED_COLUMNS))}")
    rounded = df.copy()
    numeric_cols = [col for col in EXPECTED_COLUMNS if pd.api.types.is_numeric_dtype(df[col])]
    rounded[numeric_cols] = rounded[numeric_cols].round()
    return rounded["conscientiousness"].tolist() + rounded["openness"].tolist()


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    submission_vector = _listify(submission)
    answers_vector = _listify(answers)

    if len(submission_vector) != len(answers_vector):
        print("Vector length mismatch between submission and answers.")
        return 0.0

    matches = sum(int(a == b) for a, b in zip(submission_vector, answers_vector))
    total = len(answers_vector)
    if matches != total:
        print(f"Matched {matches} of {total} rounded entries.")
        return 0.0

    return 1.0

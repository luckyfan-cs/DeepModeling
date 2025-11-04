import re
import pandas as pd

TAG = 'profit'
PATTERN = re.compile(rf"@{TAG}\[(?P<value>-?\d+(?:\.\d+)?)\]", re.IGNORECASE)


def _extract_value(cell: str) -> float:
    if not isinstance(cell, str):
        return float("nan")
    match = PATTERN.search(cell.strip())
    if not match:
        return float("nan")
    return float(match.group("value"))



def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    try:
        submitted = _extract_value(submission.iloc[0]["answer"])
    except Exception:
        submitted = float("nan")
    try:
        expected = _extract_value(answers.iloc[0]["answer"])
    except Exception:
        expected = float("nan")
    if pd.isna(submitted) or pd.isna(expected):
        return 0.0
    return 1.0 if abs(submitted - expected) <= 1e-2 else 0.0

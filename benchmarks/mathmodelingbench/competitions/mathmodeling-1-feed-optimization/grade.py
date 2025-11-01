import re
import pandas as pd

COST_PATTERN = re.compile(r"@cost\[(?P<value>-?\d+(?:\.\d+)?)\]", re.IGNORECASE)


def _extract_cost(cell: str) -> float:
    if not isinstance(cell, str):
        return float("nan")
    match = COST_PATTERN.search(cell.strip())
    if not match:
        return float("nan")
    return float(match.group("value"))


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    try:
        submitted_value = _extract_cost(submission.iloc[0]["answer"])
    except Exception:
        submitted_value = float("nan")

    try:
        expected_value = _extract_cost(answers.iloc[0]["answer"])
    except Exception:
        expected_value = float("nan")

    if pd.isna(submitted_value) or pd.isna(expected_value):
        return 0.0

    return 1.0 if abs(submitted_value - expected_value) <= 1e-2 else 0.0

import re
import pandas as pd


PROFIT_PATTERN = re.compile(r"@profit\[(?P<value>-?\d+(?:\.\d+)?)\]", re.IGNORECASE)


def _extract_profit(cell: str) -> float:
    if not isinstance(cell, str):
        return float("nan")
    match = PROFIT_PATTERN.search(cell.strip())
    if not match:
        return float("nan")
    return float(match.group("value"))


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    """Return 1.0 when the submitted profit matches the reference answer within tolerance."""
    try:
        submitted_value = _extract_profit(submission.iloc[0]["answer"])
    except Exception:
        submitted_value = float("nan")

    try:
        expected_value = _extract_profit(answers.iloc[0]["answer"])
    except Exception:
        expected_value = float("nan")

    if pd.isna(submitted_value) or pd.isna(expected_value):
        return 0.0

    return 1.0 if abs(submitted_value - expected_value) <= 1e-2 else 0.0

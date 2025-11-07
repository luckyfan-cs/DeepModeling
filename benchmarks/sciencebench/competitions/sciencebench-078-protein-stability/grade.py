"""
Grading function for ScienceBench task 78 (protein stability prediction).
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.metrics import mean_absolute_error

EXPECTED_FILENAME = "pucci-proteins_test_pred.csv"
THRESHOLD = 11.0


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[5]


def _pred_path() -> Path:
    return Path("pred_results") / EXPECTED_FILENAME


def _gold_path() -> Path:
    return _repo_root() / "ScienceAgent-bench" / "benchmark" / "eval_programs" / "gold_results" / "pucci-proteins_test_gold.csv"


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    pred_path = _pred_path()
    gold_path = _gold_path()

    if not pred_path.exists():
        print(f"Submission file not found: {pred_path}")
        return 0.0
    if not gold_path.exists():
        raise FileNotFoundError(f"Gold file missing: {gold_path}")

    pred_df = pd.read_csv(pred_path)
    gold_df = pd.read_csv(gold_path)

    if "deltaTm" not in pred_df.columns or "deltaTm" not in gold_df.columns:
        raise ValueError("Both prediction and gold CSVs must contain a 'deltaTm' column.")

    if len(pred_df) != len(gold_df):
        print(f"Row count mismatch: submission {len(pred_df)} vs gold {len(gold_df)}")
        return 0.0

    metric = mean_absolute_error(gold_df["deltaTm"], pred_df["deltaTm"])
    print(f"Mean absolute error: {metric}")

    return 1.0 if metric <= THRESHOLD else 0.0

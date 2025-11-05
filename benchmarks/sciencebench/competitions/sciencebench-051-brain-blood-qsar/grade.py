"""Grading function for ScienceBench Task 51 (brain-blood QSAR)."""

from pathlib import Path

import pandas as pd
from sklearn.metrics import balanced_accuracy_score

SUBMISSION_PATH = Path("pred_results/brain_blood_qsar.csv")
GOLD_PATH = Path("benchmark/eval_programs/gold_results/brain_blood_qsar_gold.csv")
BAL_ACC_THRESHOLD = 0.70


def _load_labels(path: Path) -> pd.Series:
    if not path.exists():
        raise FileNotFoundError(f"Required CSV missing: {path}")
    df = pd.read_csv(path)
    if "label" not in df.columns:
        raise ValueError("Submission file must contain a 'label' column")
    return df["label"]


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    pred = _load_labels(SUBMISSION_PATH)
    gold = _load_labels(GOLD_PATH)

    if len(pred) != len(gold):
        print(f"Row count mismatch: {len(pred)} vs {len(gold)}")
        return 0.0

    metric = balanced_accuracy_score(gold, pred)
    print(f"Balanced Accuracy: {metric}")
    return 1.0 if metric >= BAL_ACC_THRESHOLD else 0.0

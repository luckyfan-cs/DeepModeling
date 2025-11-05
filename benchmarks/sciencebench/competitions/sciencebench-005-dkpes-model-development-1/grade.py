"""
Grading function for ScienceBench task 5 (DKPES model development).

Mirrors the original ScienceAgentBench evaluation:
1. Verify the `index` column matches between submission and gold labels.
2. Compute ROC-AUC on `Signal-inhibition` and require >= 0.91 to pass.
"""

import pandas as pd
from sklearn.metrics import roc_auc_score

EXPECTED_COLUMNS = {"index", "Signal-inhibition"}
THRESHOLD = 0.91


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    if not EXPECTED_COLUMNS.issubset(submission.columns):
        raise ValueError(f"Submission must contain columns: {EXPECTED_COLUMNS}")
    if not EXPECTED_COLUMNS.issubset(answers.columns):
        raise ValueError(f"Answers must contain columns: {EXPECTED_COLUMNS}")

    submission = submission.reset_index(drop=True)
    answers = answers.reset_index(drop=True)

    if list(submission["index"]) != list(answers["index"]):
        print("Index mismatch between submission and gold.")
        return 0.0

    try:
        auc = roc_auc_score(
            answers["Signal-inhibition"].astype(float),
            submission["Signal-inhibition"].astype(float),
        )
    except ValueError as exc:
        print(f"Failed to compute ROC-AUC: {exc}")
        return 0.0

    print(f"ROC-AUC: {auc}")
    return 1.0 if auc >= THRESHOLD else 0.0

"""Grading function for ScienceBench Task 19 (DILI SVM models)."""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import f1_score

OUTPUT_FILES = {
    "all": Path("pred_results/all_SVM.csv"),
    "MCNC": Path("pred_results/MCNC_SVM.csv"),
    "MCLCNC": Path("pred_results/MCLCNC_SVM.csv"),
}
GOLD_PATH = Path("benchmark/eval_programs/gold_results/test_DILI_gold.csv")
F1_THRESHOLD = 0.73


def _load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Expected submission file missing: {path}")
    return pd.read_csv(path)


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    """Return 1.0 when ordering is correct and mean F1 ≥ threshold."""

    gold_df = _load_csv(GOLD_PATH)

    f1_scores = []
    data_correctness = True

    for split, file_path in OUTPUT_FILES.items():
        pred_df = _load_csv(file_path)
        required_cols = {"standardised_smiles", "label"}
        if not required_cols.issubset(pred_df.columns):
            print(f"[{split}] missing columns: {pred_df.columns}")
            return 0.0

        if list(pred_df["standardised_smiles"]) != list(gold_df["standardised_smiles"]):
            print(f"[{split}] SMILES ordering mismatch")
            data_correctness = False
            f1_scores.append(0.0)
            continue

        f1 = f1_score(gold_df["label"].values, pred_df["label"].values, pos_label="DILI")
        print(f"[{split}] F1 score: {f1}")
        f1_scores.append(f1)

    if not data_correctness:
        return 0.0

    mean_f1 = float(np.mean(f1_scores)) if f1_scores else 0.0
    print(f"Mean F1: {mean_f1}")
    return 1.0 if mean_f1 >= F1_THRESHOLD else 0.0

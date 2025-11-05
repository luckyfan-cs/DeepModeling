"""Grading function for ScienceBench Task 40 (MD RF models)."""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import f1_score

OUTPUT_FILES = {
    "all": Path("pred_results/MD_all_RF.csv"),
    "MCNC": Path("pred_results/MD_MCNC_RF.csv"),
    "MCLCNC": Path("pred_results/MD_MCLCNC_RF.csv"),
}
GOLD_PATH = Path("benchmark/eval_programs/gold_results/MD_gold.csv")
F1_THRESHOLD = 0.73


def _load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Expected submission file missing: {path}")
    return pd.read_csv(path)


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    gold_df = _load_csv(GOLD_PATH)

    f1_scores = []
    for split, file_path in OUTPUT_FILES.items():
        pred_df = _load_csv(file_path)
        required_cols = {"label"}
        if not required_cols.issubset(pred_df.columns):
            print(f"[{split}] missing label column")
            return 0.0

        if len(pred_df) != len(gold_df):
            print(f"[{split}] row count mismatch: {len(pred_df)} vs {len(gold_df)}")
            return 0.0

        f1 = f1_score(gold_df["label"].values, pred_df["label"].values, pos_label="DILI")
        print(f"[{split}] F1 score: {f1}")
        f1_scores.append(f1)

    mean_f1 = float(np.mean(f1_scores)) if f1_scores else 0.0
    print(f"Mean F1: {mean_f1}")
    return 1.0 if mean_f1 >= F1_THRESHOLD else 0.0

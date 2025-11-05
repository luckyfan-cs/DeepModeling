"""Grading function for ScienceBench Task 22 (Papyrus filtering)."""

from pathlib import Path

import pandas as pd

SUBMISSION_PATH = Path("pred_results/papyrus_filtered.pkl")
GOLD_PATH = Path("benchmark/eval_programs/gold_results/papyrus_filtered_gold.pkl")


def _load_table(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Required pickle missing: {path}")
    return pd.read_pickle(path)


def _normalize(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    numeric_cols = df.select_dtypes(include=["number"]).columns
    df = df.copy()
    df[numeric_cols] = df[numeric_cols].round(3)
    return df.sort_values(by=["Activity_ID"]).reset_index(drop=True).astype(str)


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    pred = _normalize(_load_table(SUBMISSION_PATH))
    gold = _normalize(_load_table(GOLD_PATH))

    if pred.shape != gold.shape:
        print(f"Shape mismatch: submission {pred.shape} vs gold {gold.shape}")
        return 0.0

    mismatches = []
    for idx, gold_row in gold.iterrows():
        if not pred.iloc[idx].equals(gold_row):
            mismatches.append(idx)
            if len(mismatches) <= 3:
                print("Mismatch at index", idx)
                print("Pred:", list(pred.iloc[idx]))
                print("Gold:", list(gold_row))

    if mismatches:
        print(f"Total mismatched rows: {len(mismatches)}")
        return 0.0

    return 1.0

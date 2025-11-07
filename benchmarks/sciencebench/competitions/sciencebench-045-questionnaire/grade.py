"""Grading function for ScienceBench task 45 (questionnaire scoring)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

EXPECTED_FILE = "pred_results/questionnaire_pred.csv"
GOLD_FILE = Path("benchmark/eval_programs/gold_results/biopsykit_questionnaire_gold.csv")


def _load_table(data: Any) -> pd.DataFrame:
    if isinstance(data, pd.DataFrame):
        return data.copy()
    if isinstance(data, (str, Path)):
        df = pd.read_csv(data)
        if "subject" not in df.columns:
            df = pd.read_csv(data, header=None)
        return df
    raise TypeError(f"Unsupported submission type: {type(data)}")


def _prepare_frame(df: pd.DataFrame) -> pd.DataFrame:
    columns = list(df.columns)
    if "subject" not in columns:
        first = columns[0]
        df = df.rename(columns={first: "subject"})
        columns[0] = "subject"
    normalized = ["subject"] + [f"value_{i}" for i in range(1, len(columns))]
    rename_map = {old: new for old, new in zip(columns, normalized)}
    df = df.rename(columns=rename_map)
    return df.set_index("subject").sort_index()


def grade(submission: Any, answers: Any) -> float:
    try:
        pred_df = _load_table(submission)
    except TypeError:
        pred_path = Path(EXPECTED_FILE)
        if not pred_path.exists():
            raise FileNotFoundError(f"Expected prediction file missing: {EXPECTED_FILE}")
        pred_df = pd.read_csv(pred_path)

    try:
        gold_df = _load_table(answers)
    except TypeError:
        if not GOLD_FILE.exists():
            raise FileNotFoundError(f"Gold file not found: {GOLD_FILE}")
        gold_df = pd.read_csv(GOLD_FILE)

    pred_processed = _prepare_frame(pred_df)
    gold_processed = _prepare_frame(gold_df)

    if pred_processed.shape != gold_processed.shape:
        print(
            f"Shape mismatch: prediction {pred_processed.shape} vs gold {gold_processed.shape}"
        )
        return 0.0

    if list(pred_processed.columns) != list(gold_processed.columns):
        print("Column mismatch between prediction and gold reference.")
        return 0.0

    matches = (pred_processed == gold_processed).all(axis=1)
    if not matches.all():
        mismatched = matches[~matches].index.tolist()
        print(f"Rows with mismatched responses: {mismatched}")
        return 0.0

    return 1.0

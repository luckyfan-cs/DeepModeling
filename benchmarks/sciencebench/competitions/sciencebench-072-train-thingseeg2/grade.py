"""Grading logic for ScienceBench Task 72 (EEG2EEG subject transfer)."""

import base64
import io
from typing import Tuple

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

EXPECTED_FILENAME = "eeg2eeg_sub01tosub03_pred.npy"
REQUIRED_COLUMNS = {"file_name", "array_base64"}
SPEARMAN_THRESHOLD = 0.73


def _decode_array(payload: str) -> np.ndarray:
    """Decode a base64-encoded NumPy array."""
    if not isinstance(payload, str) or not payload.strip():
        raise ValueError("array_base64 must contain a non-empty string.")

    buffer = io.BytesIO(base64.b64decode(payload))
    buffer.seek(0)
    return np.load(buffer, allow_pickle=False)


def _extract_array(df: pd.DataFrame, source: str) -> Tuple[np.ndarray, bool]:
    """Fetch and decode the array for EXPECTED_FILENAME."""
    subset = df[df["file_name"] == EXPECTED_FILENAME]
    if subset.empty:
        print(f"Missing row for {EXPECTED_FILENAME} in {source}.")
        return np.empty((0,)), False

    encoded = subset.iloc[0]["array_base64"]
    return _decode_array(encoded), True


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    """
    Grade the submission by comparing Spearman correlation with the reference.
    """
    if not REQUIRED_COLUMNS.issubset(submission.columns):
        raise ValueError(f"Submission must contain columns: {REQUIRED_COLUMNS}")
    if not REQUIRED_COLUMNS.issubset(answers.columns):
        raise ValueError(f"Answers must contain columns: {REQUIRED_COLUMNS}")

    pred_array, ok_pred = _extract_array(submission, "submission")
    gold_array, ok_gold = _extract_array(answers, "answers")

    if not (ok_pred and ok_gold):
        print("Missing expected file entry in submission or answers.")
        return 0.0

    if pred_array.shape != gold_array.shape:
        print(f"Shape mismatch: submission {pred_array.shape} vs gold {gold_array.shape}")
        return 0.0

    corr = spearmanr(pred_array.ravel(), gold_array.ravel())[0]
    print(f"Spearman correlation: {corr}")

    if np.isnan(corr):
        return 0.0

    return 1.0 if corr >= SPEARMAN_THRESHOLD else 0.0

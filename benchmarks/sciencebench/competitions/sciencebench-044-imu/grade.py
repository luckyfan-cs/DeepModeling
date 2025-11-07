"""Grading function for ScienceBench task 44 (IMU sleep endpoints)."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Dict

import pandas as pd

EXPECTED_KEYS = {"sleep_onset", "wake_onset", "total_sleep_duration"}
GOLD_FILE = Path("benchmark/eval_programs/gold_results/biopsykit_imu_gold.json")


def _coerce_to_dict(data: Any) -> Dict[str, Any]:
    if isinstance(data, dict):
        return data
    if isinstance(data, (str, Path)):
        return json.loads(Path(data).read_text())
    if isinstance(data, pd.DataFrame):
        if EXPECTED_KEYS.issubset(data.columns):
            row = data.iloc[0]
            return {key: row[key] for key in EXPECTED_KEYS}
        if {"key", "value"}.issubset(data.columns):
            return dict(zip(data["key"], data["value"]))
    raise TypeError(f"Unsupported submission format: {type(data)}")


def _load_prediction(submission: Any) -> Dict[str, Any]:
    try:
        return _coerce_to_dict(submission)
    except TypeError:
        pred_path = Path("pred_results/imu_pred.json")
        if not pred_path.exists():
            raise FileNotFoundError("Expected prediction file missing: pred_results/imu_pred.json")
        return json.loads(pred_path.read_text())


def _load_answers(answers: Any) -> Dict[str, Any]:
    try:
        return _coerce_to_dict(answers)
    except TypeError:
        if not GOLD_FILE.exists():
            raise FileNotFoundError(f"Gold file not found: {GOLD_FILE}")
        return json.loads(GOLD_FILE.read_text())


def grade(submission: Any, answers: Any) -> float:
    pred = _load_prediction(submission)
    gold = _load_answers(answers)

    missing = EXPECTED_KEYS - pred.keys()
    if missing:
        print(f"Submission missing required keys: {sorted(missing)}")
        return 0.0

    for key in EXPECTED_KEYS:
        if key not in gold:
            print(f"Gold data missing key '{key}'.")
            return 0.0

    for key in EXPECTED_KEYS:
        pred_val = pred[key]
        gold_val = gold[key]
        if isinstance(gold_val, str):
            if pred_val != gold_val:
                print(f"String mismatch for '{key}': {pred_val} vs {gold_val}")
                return 0.0
        else:
            try:
                if not math.isclose(float(pred_val), float(gold_val), rel_tol=1e-5):
                    print(f"Numeric mismatch for '{key}': {pred_val} vs {gold_val}")
                    return 0.0
            except (TypeError, ValueError):
                print(f"Non-numeric value encountered for '{key}'.")
                return 0.0

    return 1.0

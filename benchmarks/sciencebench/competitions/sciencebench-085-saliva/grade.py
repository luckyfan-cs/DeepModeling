"""
Grading function for ScienceBench task 85 (BiopSyKit saliva analysis).
"""

from __future__ import annotations

import json
import math
from pathlib import Path

PRED_FILENAME = "saliva_pred.json"
GOLD_FILENAME = "biopsykit_saliva_gold.json"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[5]


def _pred_path() -> Path:
    return Path("pred_results") / PRED_FILENAME


def _gold_path() -> Path:
    return _repo_root() / "ScienceAgent-bench" / "benchmark" / "eval_programs" / "gold_results" / GOLD_FILENAME


def _load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Required file missing: {path}")
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _values_close(gold_value, pred_value) -> bool:
    if isinstance(gold_value, float):
        try:
            return math.isclose(gold_value, float(pred_value), rel_tol=1e-9, abs_tol=1e-9)
        except (TypeError, ValueError):
            return False
    return gold_value == pred_value


def grade(submission, answers) -> float:
    gold = _load_json(_gold_path())
    pred = _load_json(_pred_path())

    if set(gold.keys()) != set(pred.keys()):
        print("Subject keys do not match.")
        return 0.0

    for subject, gold_entry in gold.items():
        pred_entry = pred.get(subject)
        if set(gold_entry.keys()) != set(pred_entry.keys()):
            print(f"Field mismatch for subject {subject}.")
            return 0.0
        for key, gold_value in gold_entry.items():
            if not _values_close(gold_value, pred_entry.get(key)):
                print(f"Mismatch for subject {subject}, field '{key}'.")
                return 0.0

    return 1.0

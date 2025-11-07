"""Grader for ScienceBench task 92 (JNMF H importances)."""

from __future__ import annotations

import json
from pathlib import Path


PRED_FILENAME = "jnmf_h_importances.json"
GOLD_FILENAME = "jnmf_h_importances_gold.json"
TOLERANCE = 1e-4


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[5]


def _pred_path() -> Path:
    return Path("pred_results") / PRED_FILENAME


def _gold_path() -> Path:
    return (
        _repo_root()
        / "ScienceAgent-bench"
        / "benchmark"
        / "eval_programs"
        / "gold_results"
        / GOLD_FILENAME
    )


def _load_json(path: Path) -> dict[str, float]:
    if not path.exists():
        raise FileNotFoundError(f"Required file missing: {path}")
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _close(a: float, b: float) -> bool:
    return abs(a - b) <= TOLERANCE


def grade(submission, answers) -> float:
    gold = _load_json(_gold_path())
    pred = _load_json(_pred_path())

    if set(gold.keys()) != set(pred.keys()):
        print("Key mismatch between prediction and gold JSON.")
        return 0.0

    for key, gold_value in gold.items():
        pred_value = pred[key]
        if not _close(gold_value, pred_value):
            print(f"Value mismatch for '{key}': gold={gold_value}, pred={pred_value}")
            return 0.0

    return 1.0

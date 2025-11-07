"""Grader for ScienceBench task 97 (formation energy prediction)."""

from __future__ import annotations

from pathlib import Path

import numpy as np


PRED_FILENAME = "formation_energy_prediction_pred.txt"
GOLD_FILENAME = "formation_energy_prediction_gold.txt"
THRESHOLD = 0.1


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


def _load_array(path: Path) -> np.ndarray:
    if not path.exists():
        raise FileNotFoundError(f"Required file missing: {path}")
    return np.loadtxt(path)


def grade(submission, answers) -> float:
    pred = _load_array(_pred_path())
    gold = _load_array(_gold_path())

    if pred.shape != gold.shape:
        print(f"Shape mismatch: {pred.shape} vs {gold.shape}")
        return 0.0

    mse = float(np.mean((pred - gold) ** 2))
    print(f"MSE: {mse}")
    return 1.0 if mse <= THRESHOLD else 0.0

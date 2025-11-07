"""Grader for ScienceBench task 95 (synthetic feasibility modeling)."""

from __future__ import annotations

from pathlib import Path

import numpy as np


PRED_FILENAME = "tox21_mol_scscores_pred.npy"
GOLD_FILENAME = "tox21_mol_scscores_gold.npy"
THRESHOLD = 0.4


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
    return np.load(path)


def grade(submission, answers) -> float:
    pred = _load_array(_pred_path())
    gold = _load_array(_gold_path())

    if pred.shape != gold.shape:
        print(f"Shape mismatch: {pred.shape} vs {gold.shape}")
        return 0.0

    mse = float(np.mean((pred - gold) ** 2))
    print(f"MSE: {mse}")
    return 1.0 if mse <= THRESHOLD else 0.0

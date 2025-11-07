"""Grading function for ScienceBench Task 71 (ThingseEG2 linear mapping)."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

THRESHOLD = 0.6


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[5]


def _pred_path() -> Path:
    return Path("pred_results/linear_sub01tosub03_pred.npy")


def _train_sub3_path() -> Path:
    return _repo_root() / "ScienceAgent-bench" / "benchmark" / "datasets" / "thingseeg2" / "train" / "sub03.npy"


def _gold_path() -> Path:
    return _repo_root() / "ScienceAgent-bench" / "benchmark" / "eval_programs" / "gold_results" / "sub03.npy"


def _load(path: Path) -> np.ndarray:
    if not path.exists():
        raise FileNotFoundError(f"Required file missing: {path}")
    return np.load(path)


def _prepare_gold() -> np.ndarray:
    train = _load(_train_sub3_path())
    mean = train.mean()
    std = train.std()

    gold = _load(_gold_path())
    gold = (gold - mean) / std
    gold = np.transpose(gold, (1, 0, 2))
    gold = gold.reshape(200, 3400)
    return gold


def grade(submission, answers) -> float:
    pred = _load(_pred_path())
    gold = _prepare_gold()

    if pred.shape != gold.shape:
        print(f"Shape mismatch: submission {pred.shape} vs gold {gold.shape}")
        return 0.0

    corr = spearmanr(pred.flatten(), gold.flatten())[0]
    print(f"Spearman correlation: {corr}")
    return 1.0 if corr >= THRESHOLD else 0.0

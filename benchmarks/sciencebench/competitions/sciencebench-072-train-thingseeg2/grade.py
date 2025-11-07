"""
Grading function for ScienceBench task 72 (EEG2EEG subject transfer).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

THRESHOLD = 0.73
PRED_FILENAME = "eeg2eeg_sub01tosub03_pred.npy"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[5]


def _dataset_dir() -> Path:
    return _repo_root() / "ScienceAgent-bench" / "benchmark" / "datasets" / "thingseeg2"


def _gold_path() -> Path:
    return _repo_root() / "ScienceAgent-bench" / "benchmark" / "eval_programs" / "gold_results" / "sub03.npy"


def _pred_path() -> Path:
    return Path("pred_results") / PRED_FILENAME


def _load_array(path: Path) -> np.ndarray:
    if not path.exists():
        raise FileNotFoundError(f"Required file missing: {path}")
    return np.load(path)


def _prepare_gold() -> np.ndarray:
    dataset_dir = _dataset_dir()
    train = _load_array(dataset_dir / "train" / "sub03.npy")
    gold = _load_array(_gold_path())

    mean = train.mean()
    std = train.std()
    normalized = (gold - mean) / std
    reshaped = np.transpose(normalized, (1, 0, 2)).reshape(200, 3400)
    return reshaped


def grade(submission, answers) -> float:
    pred = _load_array(_pred_path())
    gold = _prepare_gold()

    if pred.shape != gold.shape:
        print(f"Shape mismatch: submission {pred.shape} vs gold {gold.shape}")
        return 0.0

    corr = spearmanr(pred.ravel(), gold.ravel())[0]
    print(f"Spearman correlation: {corr}")

    if np.isnan(corr):
        return 0.0
    return 1.0 if corr >= THRESHOLD else 0.0

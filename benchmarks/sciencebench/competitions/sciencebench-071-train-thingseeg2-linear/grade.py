"""Grading function for ScienceBench Task 71 (ThingseEG2 linear mapping)."""

from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

PRED_PATH = Path("pred_results/linear_sub01tosub03_pred.npy")
TRAIN_SUB3 = Path("benchmark/datasets/thingseeg2/train/sub03.npy")
GOLD_PATH = Path("benchmark/eval_programs/gold_results/sub03.npy")
THRESHOLD = 0.6


def _load(path: Path) -> np.ndarray:
    if not path.exists():
        raise FileNotFoundError(f"Required file missing: {path}")
    return np.load(path)


def _prepare_gold() -> np.ndarray:
    train = _load(TRAIN_SUB3)
    mean = train.mean()
    std = train.std()

    gold = _load(GOLD_PATH)
    gold = (gold - mean) / std
    gold = np.transpose(gold, (1, 0, 2))
    gold = gold.reshape(200, 3400)
    return gold


def grade(submission, answers) -> float:
    pred = _load(PRED_PATH)
    gold = _prepare_gold()

    if pred.shape != gold.shape:
        print(f"Shape mismatch: submission {pred.shape} vs gold {gold.shape}")
        return 0.0

    corr = spearmanr(pred.flatten(), gold.flatten())[0]
    print(f"Spearman correlation: {corr}")
    return 1.0 if corr >= THRESHOLD else 0.0

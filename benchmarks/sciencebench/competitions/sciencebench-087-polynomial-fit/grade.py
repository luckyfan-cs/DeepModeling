"""Grader for ScienceBench task 87 (polynomial fit)."""

from __future__ import annotations

import csv
from pathlib import Path


PRED_FILENAME = "polynomial_fit_pred.csv"
GOLD_FILENAME = "polynomial_fit_gold.csv"


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


def _load_sorted_csv(path: Path) -> tuple[list[str], list[list[str]]]:
    if not path.exists():
        raise FileNotFoundError(f"Required file missing: {path}")
    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        headers = next(reader)
        rows = sorted(reader)
    return headers, rows


def grade(submission, answers) -> float:
    pred_headers, pred_rows = _load_sorted_csv(_pred_path())
    gold_headers, gold_rows = _load_sorted_csv(_gold_path())

    if pred_headers != gold_headers:
        print("Header mismatch between prediction and gold.")
        return 0.0
    if pred_rows != gold_rows:
        print("Row contents differ from the gold reference.")
        return 0.0
    return 1.0

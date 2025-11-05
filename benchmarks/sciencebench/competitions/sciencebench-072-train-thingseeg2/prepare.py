"""Prepare data for ScienceBench Task 72 (EEG2EEG subject transfer)."""

import base64
import io
from pathlib import Path
import shutil
from typing import Tuple

import numpy as np
import pandas as pd

DATA_ROOT = Path("/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/datasets/thingseeg2")
GOLD_PATH = Path("/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/eval_programs/gold_results/sub03.npy")
EXPECTED_FILENAME = "eeg2eeg_sub01tosub03_pred.npy"

SOURCE_FILES = [
    DATA_ROOT / "train/sub01.npy",
    DATA_ROOT / "train/sub03.npy",
    DATA_ROOT / "test/sub01.npy",
]


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _encode_array(array: np.ndarray) -> str:
    buffer = io.BytesIO()
    np.save(buffer, array.astype(np.float32))
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("utf-8")


def _prepare_gold() -> Tuple[np.ndarray, float, float]:
    """Match the evaluation script: normalize and reshape the Subject 03 array."""
    train = np.load(DATA_ROOT / "train/sub03.npy")
    gold = np.load(GOLD_PATH)

    mean = float(train.mean())
    std = float(train.std())

    normalized = (gold - mean) / std
    reshaped = np.transpose(normalized, (1, 0, 2)).reshape(200, 3400)
    return reshaped.astype(np.float32), mean, std


def prepare(raw: Path, public: Path, private: Path) -> None:
    print("=" * 60)
    print("Preparing ScienceBench Task 72: EEG2EEG subject transfer")
    print("=" * 60)
    print("Public directory:", public)
    print("Private directory:", private)

    _ensure_dir(public)
    _ensure_dir(private)

    missing = [str(p) for p in SOURCE_FILES if not p.exists()]
    if not GOLD_PATH.exists():
        missing.append(str(GOLD_PATH))
    if missing:
        raise FileNotFoundError("Missing dataset files: " + ", ".join(missing))

    for file_path in SOURCE_FILES:
        target = public / file_path.relative_to(DATA_ROOT.parent)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, target)
    print("✓ Copied ThingseEG2 training and test arrays to public directory")

    gold_array, mean, std = _prepare_gold()
    sample_placeholder = np.zeros_like(gold_array, dtype=np.float32)

    sample_df = pd.DataFrame(
        [{"file_name": EXPECTED_FILENAME, "array_base64": _encode_array(sample_placeholder)}]
    )
    sample_df.to_csv(public / "sample_submission.csv", index=False)
    print("✓ Created sample_submission.csv with encoded zero array")

    answer_df = pd.DataFrame(
        [{"file_name": EXPECTED_FILENAME, "array_base64": _encode_array(gold_array)}]
    )
    answer_df.to_csv(private / "answer.csv", index=False)
    print("✓ Wrote answer.csv with encoded gold array")

    np.save(private / "answer.npy", gold_array)
    print("✓ Saved answer.npy for reference")

    shutil.copy2(GOLD_PATH, private / GOLD_PATH.name)
    print(f"✓ Copied gold array ({GOLD_PATH.name}) for diagnostics")

    stats_path = private / "metadata.txt"
    stats_path.write_text(
        f"Expected output: {EXPECTED_FILENAME}\n"
        f"Array shape after reshape: {gold_array.shape}\n"
        f"Mean (train sub03): {mean:.6f}\n"
        f"STD (train sub03): {std:.6f}\n",
        encoding="utf-8",
    )
    print("✓ Wrote metadata.txt with normalization statistics")

    print("Preparation complete.")

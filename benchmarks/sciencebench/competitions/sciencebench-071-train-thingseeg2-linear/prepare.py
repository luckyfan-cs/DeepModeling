"""Data preparation for ScienceBench Task 71 (ThingseEG2 linear mapping)."""

from pathlib import Path
import shutil
import numpy as np

DATA_DIR = Path("/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/datasets/thingseeg2")
SOURCE_FILES = [
    DATA_DIR / "train/sub01.npy",
    DATA_DIR / "train/sub03.npy",
    DATA_DIR / "test/sub01.npy",
]
GOLD_PATH = Path("/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/eval_programs/gold_results/sub03.npy")
OUTPUT_PATH = "pred_results/linear_sub01tosub03_pred.npy"


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _write_sample_submission(path: Path, gold: np.ndarray) -> None:
    sample = np.zeros_like(gold.reshape(200, 3400), dtype=np.float32)
    np.save(path / "sample_submission.npy", sample)


def _write_answer_summary(path: Path, gold: np.ndarray) -> None:
    np.save(path / "answer.npy", gold)


def prepare(raw: Path, public: Path, private: Path) -> None:
    print("=" * 60)
    print("Preparing ScienceBench Task 71: ThingseEG2 linear mapping")
    print("=" * 60)
    print("Public directory:", public)
    print("Private directory:", private)

    _ensure_dir(public)
    _ensure_dir(private)

    missing = [str(f) for f in SOURCE_FILES if not f.exists()]
    if missing:
        raise FileNotFoundError("Missing dataset files: " + ", ".join(missing))

    for file_path in SOURCE_FILES:
        target = public / file_path.relative_to(DATA_DIR.parent)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, target)
    print("✓ Copied ThingseEG2 train/test numpy files to public directory")

    gold = np.load(GOLD_PATH)
    # Gold array has shape (17, 200, 200); mimic evaluation reshape
    reshaped = np.transpose(gold, (1, 0, 2)).reshape(200, 3400)
    _write_sample_submission(public, reshaped)
    print("✓ Created sample_submission.npy with zeros")

    _write_answer_summary(private, reshaped)
    print("✓ Saved reshaped gold array for reference")

    manifest_path = private / "metadata.txt"
    manifest_path.write_text(
        "Expected submission: {}\nShape after reshape: {}\n".format(OUTPUT_PATH, reshaped.shape),
        encoding="utf-8"
    )
    print("✓ Wrote metadata.txt")

    print("Preparation complete. Expected submission file:", OUTPUT_PATH)


if __name__ == "__main__":
    raise SystemExit("Use this module via the benchmark preparation tooling.")

"""Data preparation for ScienceBench Task 51 (brain-blood QSAR)."""

from pathlib import Path
import shutil
import pandas as pd

DATA_DIR = Path("/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/datasets/brain-blood")
SOURCE_FILES = [
    DATA_DIR / "logBB.sdf",
    DATA_DIR / "logBB_test.sdf",
]
GOLD_PATH = Path("/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/eval_programs/gold_results/brain_blood_qsar_gold.csv")
OUTPUT_FILENAME = "pred_results/brain_blood_qsar.csv"


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _write_sample_submission(path: Path) -> None:
    sample_df = pd.DataFrame({
        "label": [0]
    })
    sample_df.to_csv(path / "sample_submission.csv", index=False)


def _write_answer_summary(path: Path, gold_df: pd.DataFrame) -> None:
    gold_df.to_csv(path / "answer.csv", index=False)


def prepare(raw: Path, public: Path, private: Path) -> None:
    print("=" * 60)
    print("Preparing ScienceBench Task 51: brain-blood QSAR")
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
    print("✓ Copied logBB training and test SDF files to public directory")

    _write_sample_submission(public)
    print("✓ Wrote sample_submission.csv")

    gold_df = pd.read_csv(GOLD_PATH)
    _write_answer_summary(private, gold_df)
    print("✓ Wrote answer.csv with gold labels")

    print("Preparation complete. Expected submission file:", OUTPUT_FILENAME)


if __name__ == "__main__":
    raise SystemExit("Use this module via the benchmark preparation tooling.")

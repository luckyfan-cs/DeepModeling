"""Data preparation for ScienceBench Task 22 (Papyrus filtering)."""

from pathlib import Path
import shutil
import pandas as pd

DATA_DIR = Path("/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/datasets/papyrus")
SOURCE_FILES = [
    DATA_DIR / "papyrus_unfiltered.pkl",
    DATA_DIR / "papyrus_protein_set.pkl",
]
GOLD_PATH = Path("/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/eval_programs/gold_results/papyrus_filtered_gold.pkl")
OUTPUT_FILENAME = "pred_results/papyrus_filtered.pkl"


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _write_sample_submission(path: Path) -> None:
    sample_path = path / "sample_submission.txt"
    sample_path.write_text("Create pred_results/papyrus_filtered.pkl with filtered Papyrus data (pickle format).\n", encoding="utf-8")


def _write_answer_metadata(path: Path, gold_df: pd.DataFrame) -> None:
    summary = {
        "rows": [len(gold_df)],
        "columns": [len(gold_df.columns)],
    }
    pd.DataFrame(summary).to_csv(path / "answer_summary.csv", index=False)


def prepare(raw: Path, public: Path, private: Path) -> None:
    print("=" * 60)
    print("Preparing ScienceBench Task 22: Papyrus filtering")
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
    print("✓ Copied Papyrus source pickles to public directory")

    _write_sample_submission(public)
    print("✓ Wrote sample_submission.txt instruction")

    gold_df = pd.read_pickle(GOLD_PATH)
    _write_answer_metadata(private, gold_df)
    print("✓ Wrote answer_summary.csv for reference")

    print("Preparation complete. Expected submission file:", OUTPUT_FILENAME)


if __name__ == "__main__":
    raise SystemExit("Use this module via the benchmark preparation tooling.")

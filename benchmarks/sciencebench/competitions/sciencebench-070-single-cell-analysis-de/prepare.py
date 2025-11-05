"""Data preparation for ScienceBench Task 70 (Heart Cell Atlas DE)."""

from pathlib import Path
import shutil
import base64
import pandas as pd

DATA_DIR = Path("/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/datasets/hca")
SOURCE_FILE = DATA_DIR / "hca_subsampled_20k.h5ad"
GOLD_IMAGE = Path("/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/eval_programs/gold_results/hca_cell_type_de_gold.png")
EXPECTED_FILENAME = "hca_cell_type_de.png"


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _encode_image(path: Path) -> str:
    if not path.exists():
        return ""
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def prepare(raw: Path, public: Path, private: Path) -> None:
    print("=" * 60)
    print("Preparing ScienceBench Task 70: differential expression dot plot")
    print("=" * 60)
    print("Public directory:", public)
    print("Private directory:", private)

    _ensure_dir(public)
    _ensure_dir(private)

    if not SOURCE_FILE.exists():
        raise FileNotFoundError(f"Missing dataset file: {SOURCE_FILE}")

    target = public / SOURCE_FILE.relative_to(DATA_DIR.parent)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SOURCE_FILE, target)
    print("✓ Copied hca_subsampled_20k.h5ad to public directory")

    sample_df = pd.DataFrame([
        {"file_name": EXPECTED_FILENAME, "image_base64": ""}
    ])
    sample_df.to_csv(public / "sample_submission.csv", index=False)
    print("✓ Wrote sample_submission.csv")

    encoded = _encode_image(GOLD_IMAGE)
    answer_df = pd.DataFrame([
        {"file_name": EXPECTED_FILENAME, "image_base64": encoded}
    ])
    answer_df.to_csv(private / "answer.csv", index=False)
    print("✓ Wrote answer.csv")

    if GOLD_IMAGE.exists():
        shutil.copy2(GOLD_IMAGE, private / GOLD_IMAGE.name)
        print("✓ Copied gold image for reference")

    print("Preparation complete. Expected submission file: pred_results/hca_cell_type_de.png")


if __name__ == "__main__":
    raise SystemExit("Use this module via the benchmark preparation tooling.")

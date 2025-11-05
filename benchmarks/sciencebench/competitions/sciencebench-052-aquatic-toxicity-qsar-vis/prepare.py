"""Data preparation for ScienceBench Task 52 (aquatic toxicity visualization)."""

from pathlib import Path
import shutil
import base64
import pandas as pd

DATA_DIR = Path("/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/datasets/aquatic_toxicity")
SOURCE_FILES = [
    DATA_DIR / "Tetrahymena_pyriformis_OCHEM.sdf",
    DATA_DIR / "Tetrahymena_pyriformis_OCHEM_test_ex.sdf",
]
GOLD_IMAGE = Path("/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/eval_programs/gold_results/aquatic_toxicity_qsar_vis_gold.png")
EXPECTED_FILENAME = "aquatic_toxicity_qsar_vis.png"


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _encode_image(path: Path) -> str:
    if not path.exists():
        return ""
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def prepare(raw: Path, public: Path, private: Path) -> None:
    print("=" * 60)
    print("Preparing ScienceBench Task 52: aquatic toxicity visualization")
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
    print("✓ Copied aquatic toxicity SDF files to public directory")

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

    print("Preparation complete. Expected submission file: pred_results/aquatic_toxicity_qsar_vis.png")


if __name__ == "__main__":
    raise SystemExit("Use this module via the benchmark preparation tooling.")

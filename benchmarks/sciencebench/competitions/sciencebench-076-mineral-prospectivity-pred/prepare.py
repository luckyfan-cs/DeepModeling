"""Prepare data for ScienceBench Task 76 (Mineral prospectivity map)."""

import base64
from pathlib import Path
import shutil
from typing import Iterable

import pandas as pd

EXPECTED_FILENAME = "mineral_prospectivity.png"
DATA_ROOT = Path("/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/datasets/MineralProspectivity")
GOLD_IMAGE = Path("/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/eval_programs/gold_results/mineral_prospectivity_gold.png")


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _copy_files(files: Iterable[Path], destination_root: Path) -> None:
    for file_path in files:
        rel = file_path.relative_to(DATA_ROOT.parent)
        target = destination_root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, target)


def _encode_image(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def prepare(raw: Path, public: Path, private: Path) -> None:
    print("=" * 60)
    print("Preparing ScienceBench Task 76: Mineral prospectivity map")
    print("=" * 60)
    print("Public directory:", public)
    print("Private directory:", private)

    _ensure_dir(public)
    _ensure_dir(private)

    if not DATA_ROOT.exists():
        raise FileNotFoundError(f"Missing dataset directory: {DATA_ROOT}")
    if not GOLD_IMAGE.exists():
        raise FileNotFoundError(f"Missing gold image: {GOLD_IMAGE}")

    data_files = sorted(p for p in DATA_ROOT.glob("*") if p.is_file())
    _copy_files(data_files, public)
    print(f"✓ Copied {len(data_files)} dataset files to public directory")

    gold_b64 = _encode_image(GOLD_IMAGE)
    shutil.copy2(GOLD_IMAGE, private / GOLD_IMAGE.name)
    print("✓ Copied gold image for diagnostics")

    sample_df = pd.DataFrame(
        [{"file_name": EXPECTED_FILENAME, "image_base64": ""}],
    )
    sample_df.to_csv(public / "sample_submission.csv", index=False)
    print("✓ Created sample_submission.csv")

    answer_df = pd.DataFrame(
        [{"file_name": EXPECTED_FILENAME, "image_base64": gold_b64}],
    )
    answer_df.to_csv(private / "answer.csv", index=False)
    print("✓ Created answer.csv with encoded gold image")

    print("Preparation complete.")

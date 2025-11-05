"""
Data preparation for ScienceBench Task 43: EOG_analyze
Dataset: biosignals
"""

import pandas as pd
import numpy as np
from pathlib import Path
import shutil


def prepare(raw: Path, public: Path, private: Path):
    """
    Prepare the EOG_analyze task data.

    Args:
        raw: Path to raw data directory
        public: Path to public directory (visible to participants)
        private: Path to private directory (used for grading)
    """
    print(f"=" * 60)
    print(f"Preparing ScienceBench Task 43: EOG_analyze")
    print(f"=" * 60)
    print(f"Raw directory: {raw}")
    print(f"Public directory: {public}")
    print(f"Private directory: {private}")

    # Source dataset path
    source_dir = Path("/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/datasets/biosignals")

    if not source_dir.exists():
        raise FileNotFoundError(f"Source dataset not found: {source_dir}")

    # Copy EOG data file to public
    eog_file = source_dir / "eog_100hz.csv"

    if not eog_file.exists():
        raise FileNotFoundError(f"Required data file not found: {eog_file}")

    print(f"\nCopying data files to public directory...")
    shutil.copy2(eog_file, public / "eog_100hz.csv")
    print(f"  ✓ Copied: eog_100hz.csv ({eog_file.stat().st_size / 1024:.1f} KB)")

    # Create sample_submission as a placeholder for image output
    sample_submission = pd.DataFrame({
        "output_file": ["EOG_analyze_pred.png"],
        "output_type": ["image/png"]
    })
    sample_submission.to_csv(public / "sample_submission.csv", index=False)
    print(f"\n✓ Created sample_submission.csv")

    # Copy gold result image to private for comparison
    gold_file = Path("/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/eval_programs/gold_results/EOG_analyze_gold.png")
    if gold_file.exists():
        shutil.copy2(gold_file, private / "EOG_analyze_gold.png")
        print(f"✓ Copied gold result image to private ({gold_file.stat().st_size / 1024:.1f} KB)")
    else:
        print(f"⚠ Warning: Gold result image not found at {gold_file}")

    # Create answer metadata file
    answer_meta = pd.DataFrame({
        "expected_file": ["EOG_analyze_pred.png"],
        "gold_file": ["EOG_analyze_gold.png"],
        "evaluation_method": ["visual_similarity"],
        "threshold": [60]
    })
    answer_meta.to_csv(private / "answer.csv", index=False)
    print(f"✓ Created answer.csv with evaluation metadata")

    print(f"\nData preparation completed!")
    print(f"  Public files: {sorted([f.name for f in public.glob('*')])}")
    print(f"  Private files: {sorted([f.name for f in private.glob('*')])}")

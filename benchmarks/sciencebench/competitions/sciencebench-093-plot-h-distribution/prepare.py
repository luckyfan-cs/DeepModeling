"""
Data preparation for ScienceBench Task 93: plot_h_distribution
Dataset: jnmf_visualization
"""

import pandas as pd
import numpy as np
from pathlib import Path
import shutil


def prepare(raw: Path, public: Path, private: Path):
    """
    Prepare the plot_h_distribution task data.

    Args:
        raw: Path to raw data directory
        public: Path to public directory (visible to participants)
        private: Path to private directory (used for grading)
    """
    print(f"=" * 60)
    print(f"Preparing ScienceBench Task 93: plot_h_distribution")
    print(f"=" * 60)
    print(f"Raw directory: {raw}")
    print(f"Public directory: {public}")
    print(f"Private directory: {private}")

    # Source dataset path
    source_dir = Path("/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/datasets/jnmf_visualization")

    if not source_dir.exists():
        raise FileNotFoundError(f"Source dataset not found: {source_dir}")

    # Copy all numpy files to public
    print(f"\nCopying data files to public directory...")
    for npy_file in source_dir.glob("*.npy"):
        shutil.copy2(npy_file, public / npy_file.name)
        print(f"  ✓ Copied: {npy_file.name}")

    # Create sample_submission as a placeholder
    # For image outputs, we just indicate the expected filename
    sample_submission = pd.DataFrame({
        "output_file": ["H_distribution_conscientiousness.png"],
        "output_type": ["image/png"]
    })
    sample_submission.to_csv(public / "sample_submission.csv", index=False)
    print(f"\n✓ Created sample_submission.csv")

    # Copy gold result image to private for comparison
    gold_file = Path("/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/eval_programs/gold_results/H_distribution_conscientiousness_gold.png")
    if gold_file.exists():
        shutil.copy2(gold_file, private / "H_distribution_conscientiousness_gold.png")
        print(f"✓ Copied gold result image to private")
    else:
        print(f"⚠ Warning: Gold result image not found at {gold_file}")

    # Create answer metadata file
    answer_meta = pd.DataFrame({
        "expected_file": ["H_distribution_conscientiousness.png"],
        "gold_file": ["H_distribution_conscientiousness_gold.png"],
        "evaluation_method": ["visual_similarity"],
        "threshold": [60]
    })
    answer_meta.to_csv(private / "answer.csv", index=False)
    print(f"✓ Created answer.csv with evaluation metadata")

    print(f"\nData preparation completed!")
    print(f"  Public files: {sorted([f.name for f in public.glob('*')])}")
    print(f"  Private files: {sorted([f.name for f in private.glob('*')])}")

"""
Data preparation for ScienceBench Task 102: refractive_index_prediction
Dataset: ref_index
"""

import pandas as pd
import numpy as np
from pathlib import Path
import shutil


def prepare(raw: Path, public: Path, private: Path):
    """
    Prepare the refractive_index_prediction task data.

    Args:
        raw: Path to raw data directory
        public: Path to public directory (visible to participants)
        private: Path to private directory (used for grading)
    """
    print(f"=" * 60)
    print(f"Preparing ScienceBench Task 102: refractive_index_prediction")
    print(f"=" * 60)
    print(f"Raw directory: {raw}")
    print(f"Public directory: {public}")
    print(f"Private directory: {private}")

    # Source dataset path
    source_dir = Path("/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/datasets/ref_index")

    if not source_dir.exists():
        raise FileNotFoundError(f"Source dataset not found: {source_dir}")

    # Copy training and test data to public
    # These are MODData format files (binary)
    train_file = source_dir / "md_ref_index_train"
    test_file = source_dir / "MP_2018.6"

    if not train_file.exists() or not test_file.exists():
        raise FileNotFoundError(f"Required data files not found in {source_dir}")

    print(f"\nCopying data files to public directory...")
    shutil.copy2(train_file, public / "md_ref_index_train")
    shutil.copy2(test_file, public / "MP_2018.6")
    print(f"  ✓ Copied: md_ref_index_train ({train_file.stat().st_size / 1024 / 1024:.1f} MB)")
    print(f"  ✓ Copied: MP_2018.6 ({test_file.stat().st_size / 1024 / 1024:.1f} MB)")

    # Create sample_submission
    # The output should be a CSV with refractive_index predictions
    # We don't know the exact number of samples without loading MODData,
    # so create a minimal template
    sample_submission = pd.DataFrame({
        "id": [0, 1, 2],
        "refractive_index": [1.5, 1.5, 1.5]  # Placeholder values
    })
    sample_submission.to_csv(public / "sample_submission.csv", index=False)
    print(f"\n✓ Created sample_submission.csv (template)")

    # Load gold results for answer
    gold_file = Path("/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/eval_programs/gold_results/ref_index_predictions_gold.csv")
    if gold_file.exists():
        gold_df = pd.read_csv(gold_file)
        gold_df.to_csv(private / "answer.csv", index=False)
        print(f"✓ Created answer.csv with {len(gold_df)} rows from gold results")
    else:
        print(f"⚠ Warning: Gold results not found at {gold_file}")
        answer = sample_submission.copy()
        answer.to_csv(private / "answer.csv", index=False)
        print(f"✓ Created placeholder answer.csv")

    print(f"\nData preparation completed!")
    print(f"  Public files: {sorted([f.name for f in public.glob('*')])}")
    print(f"  Private files: {sorted([f.name for f in private.glob('*')])}")

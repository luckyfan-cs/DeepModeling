#!/usr/bin/env python3
"""Batch convert all mathmodeling datasets to mathmodelingbench competitions."""
import subprocess
import sys
from pathlib import Path

# Configuration
DATASETS_DIR = Path("/home/aiops/liufan/projects/mathmodeling/datasets")
REGISTRY_ROOT = Path("/home/aiops/liufan/projects/DeepModeling/benchmarks/mathmodelingbench/competitions")
DATA_ROOT = Path("/home/aiops/liufan/projects/DeepModeling/data/mathmodeling-bench/competitions")
CONVERTER_SCRIPT = Path("/home/aiops/liufan/projects/DeepModeling/examples/mathmodleing-to-mlebech/convert_mathmodeling.py")

# Dataset configurations: (filename, prefix, start_index, default_tag)
DATASET_CONFIGS = [
    ("BWOR.json", "bwor", 0, "value"),
    ("IndustryOR.json", "industry", 0, "value"),
    ("mamo_easy_lp.jsonl", "mamo-easy", 0, "cost"),
    ("mamo_complex_lp.jsonl", "mamo-complex", 0, "cost"),
    ("mamo_ode.jsonl", "mamo-ode", 0, "value"),
]

def run_conversion(dataset_file: str, prefix: str, start_index: int, default_tag: str, dry_run: bool = False):
    """Run conversion for a single dataset."""
    dataset_path = DATASETS_DIR / dataset_file

    if not dataset_path.exists():
        print(f"⚠️  Dataset not found: {dataset_path}")
        return False

    print(f"\n{'='*80}")
    print(f"📊 Processing: {dataset_file}")
    print(f"   Prefix: {prefix}, Start Index: {start_index}, Tag: {default_tag}")
    print(f"{'='*80}\n")

    cmd = [
        sys.executable,
        str(CONVERTER_SCRIPT),
        "--dataset-file", str(dataset_path),
        "--registry-root", str(REGISTRY_ROOT),
        "--data-root", str(DATA_ROOT),
        "--competition-prefix", prefix,
        "--default-tag", default_tag,
        "--start-index", str(start_index),
    ]

    if dry_run:
        cmd.append("--dry-run")

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Warnings:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error processing {dataset_file}:")
        print(e.stdout)
        print(e.stderr)
        return False

def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")
    parser.add_argument("--dataset", help="Process only specific dataset (e.g., BWOR.json)")
    args = parser.parse_args()

    print("🚀 Batch Conversion Tool for MathModeling Datasets")
    print(f"{'='*80}\n")

    if args.dry_run:
        print("🔍 DRY RUN MODE - No files will be written\n")

    configs_to_process = DATASET_CONFIGS
    if args.dataset:
        configs_to_process = [c for c in DATASET_CONFIGS if c[0] == args.dataset]
        if not configs_to_process:
            print(f"❌ Dataset '{args.dataset}' not found in configuration")
            return 1

    success_count = 0
    fail_count = 0

    for dataset_file, prefix, start_index, default_tag in configs_to_process:
        if run_conversion(dataset_file, prefix, start_index, default_tag, args.dry_run):
            success_count += 1
        else:
            fail_count += 1

    print(f"\n{'='*80}")
    print(f"✅ Summary: {success_count} successful, {fail_count} failed")
    print(f"{'='*80}\n")

    return 0 if fail_count == 0 else 1

if __name__ == "__main__":
    sys.exit(main())

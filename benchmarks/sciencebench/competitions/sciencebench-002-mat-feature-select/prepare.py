"""
Data preparation for ScienceBench task 2
Dataset: mat_diffusion
"""

import json
import shutil
from pathlib import Path

import numpy as np
import pandas as pd


SOURCE_DATASET = "mat_diffusion"
GOLD_PATH = Path("/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/eval_programs/gold_results/mat_diffusion_features_gold.csv") if "/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/eval_programs/gold_results/mat_diffusion_features_gold.csv" else None
ANSWER_FILENAME = "answer.csv"
SAMPLE_FILENAME = "sample_submission.csv"


def load_gold_dataframe(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()

    if suffix == ".csv":
        return pd.read_csv(path)

    if suffix in {".json", ".jsonl"}:
        if suffix == ".jsonl":
            records = []
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        records.append(json.loads(line))
        else:
            with open(path, "r", encoding="utf-8") as f:
                payload = json.load(f)
            if isinstance(payload, list):
                records = payload
            elif isinstance(payload, dict):
                records = [payload]
            else:
                records = [{"value": payload}]

        return pd.json_normalize(records)

    if suffix in {".pkl", ".pickle"}:
        obj = pd.read_pickle(path)
        if isinstance(obj, pd.DataFrame):
            return obj.reset_index(drop=True)
        if isinstance(obj, dict):
            return pd.json_normalize(obj)
        if isinstance(obj, list):
            return pd.json_normalize(obj)
        return pd.DataFrame({"value": [obj]})

    if suffix in {".npy", ".npz"}:
        arr = np.load(path, allow_pickle=True)
        if isinstance(arr, np.ndarray):
            if arr.dtype.names is not None:
                return pd.DataFrame(arr.tolist())
            if arr.ndim == 1:
                return pd.DataFrame({"value": arr.tolist()})
            reshaped = arr.reshape(arr.shape[0], -1) if arr.ndim > 2 else arr
            return pd.DataFrame(reshaped)
        if isinstance(arr, dict):
            return pd.DataFrame(arr)
        return pd.DataFrame({"value": [arr]})

    if suffix in {".txt", ".tsv"}:
        if suffix == ".tsv":
            return pd.read_csv(path, sep="	")
        text = path.read_text(encoding="utf-8").splitlines()
        return pd.DataFrame({"value": text})

    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)

    raise ValueError(f"Unsupported gold result format: {suffix}")


def create_sample_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    sample = df.copy()
    for column in sample.columns:
        if pd.api.types.is_numeric_dtype(sample[column]):
            sample[column] = 0
        else:
            sample[column] = ""
    return sample.fillna("")


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def create_placeholder_files(public: Path, private: Path) -> None:
    ensure_directory(public)
    ensure_directory(private)

    pd.DataFrame({"info": ["Data not available"]}).to_csv(
        public / SAMPLE_FILENAME, index=False
    )

    pd.DataFrame({"info": ["Answer not available"]}).to_csv(
        private / ANSWER_FILENAME, index=False
    )

    print("Placeholder files created")


def prepare(raw: Path, public: Path, private: Path):
    """Prepare the ScienceAgent task data."""
    print("=" * 60)
    print("Preparing ScienceBench Task 2")
    print("Dataset:", SOURCE_DATASET)
    print("=" * 60)
    print("Raw directory:", raw)
    print("Public directory:", public)
    print("Private directory:", private)

    ensure_directory(public)
    ensure_directory(private)

    if raw.exists():
        print("
Copying data files to public directory...")
        file_count = 0
        for file in raw.rglob('*'):
            if file.is_file() and not file.name.startswith('.'):
                rel_path = file.relative_to(raw)
                target = public / rel_path
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file, target)
                file_count += 1
                if file_count <= 10:
                    print("  ✓ Copied:", rel_path)
        if file_count > 10:
            print("  ... and", file_count - 10, "more files")
        print("  Total files copied:", file_count)
    else:
        print("
⚠ Warning: Raw data directory not found:", raw)

    if GOLD_PATH and GOLD_PATH.exists():
        try:
            gold_df = load_gold_dataframe(GOLD_PATH)
            sample_df = create_sample_dataframe(gold_df)

            answer_path = private / ANSWER_FILENAME
            sample_path = public / SAMPLE_FILENAME

            gold_df.to_csv(answer_path, index=False)
            sample_df.to_csv(sample_path, index=False)

            print("✓ Created answer file:", answer_path)
            print("✓ Created sample submission:", sample_path)

            gold_copy = private / GOLD_PATH.name
            if GOLD_PATH != gold_copy:
                shutil.copy2(GOLD_PATH, gold_copy)
                print("✓ Copied original gold file:", gold_copy)

        except Exception as exc:
            print("⚠ Failed to process gold results:", exc)
            print("   Falling back to placeholder files")
            create_placeholder_files(public, private)
    else:
        print("⚠ Gold results not found; creating placeholder files")
        create_placeholder_files(public, private)

    print("
Data preparation completed!")
    public_list = [p.name for p in public.iterdir() if p.is_file()]
    private_list = [p.name for p in private.iterdir() if p.is_file()]
    print("  Public files:", public_list)
    print("  Private files:", private_list)

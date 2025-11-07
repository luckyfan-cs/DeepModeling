
"""
Grading logic for ScienceBench task 53 (mountainlion3 reclassification).
"""

from __future__ import annotations

import base64
from typing import Dict

import numpy as np
import pandas as pd

try:
    from rasterio.io import MemoryFile
except ImportError as exc:  # pragma: no cover - dependency should ship with benchmark
    raise RuntimeError("Task 53 grading requires the 'rasterio' package.") from exc

EXPECTED_FILES: Dict[str, float] = {
    "landCover_reclassified.tif": 0.70,
    "protected_status_reclassified.tif": 0.70,
}


def _load_raster_from_base64(blob: str) -> np.ndarray:
    if not isinstance(blob, str) or not blob.strip():
        raise ValueError("Empty image_base64 value encountered.")

    data = base64.b64decode(blob)
    with MemoryFile(data) as mem:
        with mem.open() as dataset:
            return dataset.read(1)


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    required_columns = {"file_name", "image_base64"}
    if not required_columns.issubset(submission.columns):
        raise ValueError(f"Submission must contain columns: {required_columns}")
    if not required_columns.issubset(answers.columns):
        raise ValueError(f"Answers must contain columns: {required_columns}")

    merged = pd.merge(
        answers.rename(columns={"image_base64": "image_base64_gold"}),
        submission.rename(columns={"image_base64": "image_base64_pred"}),
        on="file_name",
        how="inner",
    )

    if merged.empty:
        print("No matching files between submission and answers.")
        return 0.0

    ratios: Dict[str, float] = {}
    for row in merged.to_dict("records"):
        file_name = row.get("file_name")
        if file_name not in EXPECTED_FILES:
            continue

        pred = _load_raster_from_base64(row.get("image_base64_pred", ""))
        gold = _load_raster_from_base64(row.get("image_base64_gold", ""))

        if pred.shape != gold.shape:
            ratio = 0.0
        else:
            ratio = float(np.mean(pred == gold))
        ratios[file_name] = ratio
        print(f"[grade] {file_name} match ratio={ratio:.4f}")

    missing = sorted(set(EXPECTED_FILES) - ratios.keys())
    if missing:
        print(f"Missing expected raster(s): {', '.join(missing)}")
        return 0.0

    for file_name, threshold in EXPECTED_FILES.items():
        ratio = ratios[file_name]
        if ratio <= threshold:
            print(f"Match ratio for '{file_name}' ({ratio:.4f}) did not exceed {threshold:.2f}.")
            return 0.0

    return 1.0

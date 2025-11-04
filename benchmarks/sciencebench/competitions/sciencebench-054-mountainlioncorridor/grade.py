"""
Grading function for ScienceBench task 54

Image similarity is approximated via pixel-level comparison after decoding
base64 encoded submissions.
"""

import base64
import io
import numpy as np
import pandas as pd
from PIL import Image


EXPECTED_FILENAME = "mountainLionCorridor.png"


def _decode_image(data: str) -> Image.Image:
    if not isinstance(data, str) or not data.strip():
        raise ValueError("Empty image_base64 value")
    buffer = io.BytesIO(base64.b64decode(data))
    return Image.open(buffer).convert("RGB")


def _similarity_score(gold_img: Image.Image, pred_img: Image.Image) -> float:
    pred_resized = pred_img.resize(gold_img.size)
    gold_arr = np.asarray(gold_img, dtype=np.float32) / 255.0
    pred_arr = np.asarray(pred_resized, dtype=np.float32) / 255.0

    mse = float(np.mean((gold_arr - pred_arr) ** 2))
    return max(0.0, 1.0 - mse)


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
        return 0.0

    scores = []
    for _, row in merged.iterrows():
        try:
            gold_img = _decode_image(row["image_base64_gold"])
            pred_img = _decode_image(row["image_base64_pred"])
        except ValueError:
            scores.append(0.0)
            continue

        scores.append(_similarity_score(gold_img, pred_img))

    return float(np.mean(scores)) if scores else 0.0

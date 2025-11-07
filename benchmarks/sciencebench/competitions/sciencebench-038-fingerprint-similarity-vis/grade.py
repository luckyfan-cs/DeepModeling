"""
Grade fingerprint similarity visualization task using visual similarity.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from PIL import Image
from typing import Union


def calculate_image_similarity(pred_image: np.ndarray, gold_image: np.ndarray) -> float:
    """Calculate similarity between two images."""
    if pred_image.shape != gold_image.shape:
        pred_pil = Image.fromarray(pred_image)
        pred_pil = pred_pil.resize((gold_image.shape[1], gold_image.shape[0]), Image.LANCZOS)
        pred_image = np.array(pred_pil)

    pred_float = pred_image.astype(np.float32) / 255.0
    gold_float = gold_image.astype(np.float32) / 255.0

    mse = np.mean((pred_float - gold_float) ** 2)
    psnr = 100.0 if mse == 0 else 20 * np.log10(1.0 / np.sqrt(mse))

    pred_flat = pred_float.flatten()
    gold_flat = gold_float.flatten()
    correlation = np.corrcoef(pred_flat, gold_flat)[0, 1]

    psnr_normalized = min(100, max(0, (psnr - 20) * 5))
    correlation_normalized = (correlation + 1) * 50
    similarity_score = 0.6 * psnr_normalized + 0.4 * correlation_normalized

    return float(similarity_score)


def grade(submission: Union[pd.DataFrame, Path, str], answers: Union[pd.DataFrame, Path, str]) -> float:
    """Grade submission by comparing with gold standard image."""
    if isinstance(submission, (str, Path)):
        submission_path = Path(submission)
    elif isinstance(submission, pd.DataFrame):
        if 'path' in submission.columns:
            submission_path = Path(submission['path'].iloc[0])
        else:
            raise ValueError("DataFrame submission must have 'path' column")
    else:
        raise ValueError(f"Unsupported submission type: {type(submission)}")

    if isinstance(answers, (str, Path)):
        answers_path = Path(answers)
    elif isinstance(answers, pd.DataFrame):
        if 'path' in answers.columns:
            answers_path = Path(answers['path'].iloc[0])
        else:
            raise ValueError("DataFrame answers must have 'path' column")
    else:
        raise ValueError(f"Unsupported answers type: {type(answers)}")

    if not submission_path.exists():
        raise FileNotFoundError(f"Submission file not found: {submission_path}")
    if not answers_path.exists():
        raise FileNotFoundError(f"Gold standard file not found: {answers_path}")

    try:
        pred_image = Image.open(submission_path)
        pred_array = np.array(pred_image.convert('RGB'))
    except Exception as e:
        raise ValueError(f"Failed to load prediction image: {e}")

    try:
        gold_image = Image.open(answers_path)
        gold_array = np.array(gold_image.convert('RGB'))
    except Exception as e:
        raise ValueError(f"Failed to load gold standard image: {e}")

    similarity_score = calculate_image_similarity(pred_array, gold_array)
    threshold = 60.0

    return 1.0 if similarity_score >= threshold else 0.0

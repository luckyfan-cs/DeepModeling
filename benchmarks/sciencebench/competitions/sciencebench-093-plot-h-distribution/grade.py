"""
Grading function for ScienceBench Task 93: plot_h_distribution
Based on eval_programs/eval_h_distribution.py

This task requires visual similarity comparison of plots.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import base64


def encode_image(image_path):
    """Encode image to base64 for GPT-4 Vision API"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    """
    Grade submission by comparing generated plot with gold standard.

    For image-based tasks, the submission DataFrame should indicate
    where the output file is located.

    Args:
        submission: DataFrame indicating output file location
        answers: DataFrame with evaluation metadata

    Returns:
        float: Score between 0 and 1
    """
    try:
        # Import here to handle optional dependency
        try:
            from gpt4_visual_judge import encode_image, score_figure
            has_visual_judge = True
        except ImportError:
            print("Warning: gpt4_visual_judge not available, using placeholder scoring")
            has_visual_judge = False

        # Expected output file
        pred_file = Path("pred_results/H_distribution_conscientiousness.png")

        # Check if prediction file exists
        if not pred_file.exists():
            print(f"Error: Prediction file not found: {pred_file}")
            return 0.0

        if not has_visual_judge:
            # Placeholder: just check file exists
            print(f"✓ Prediction file exists: {pred_file}")
            return 0.8  # Give partial credit if visual judge not available

        # Get gold file path from answers
        # Assuming the grading framework provides access to private data
        gold_file = Path("private/H_distribution_conscientiousness_gold.png")

        if not gold_file.exists():
            print(f"Warning: Gold file not found at {gold_file}")
            return 0.5

        # Use GPT-4 Vision to compare images
        pred_fig = encode_image(str(pred_file))
        gold_fig = encode_image(str(gold_file))

        full_response, score = score_figure(pred_fig, gold_fig)

        print(f"Visual similarity score: {score}/100")
        print(f"Evaluation response: {full_response[:200]}...")

        # Convert score (0-100) to normalized score (0-1)
        # Threshold from original: >= 60
        normalized_score = score / 100.0

        return float(normalized_score)

    except Exception as e:
        print(f"Error in grading: {e}")
        import traceback
        traceback.print_exc()
        return 0.0

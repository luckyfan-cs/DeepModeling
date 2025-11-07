
"""
Grading logic for ScienceBench task 63 (biosignals interval analysis).
"""

from __future__ import annotations

import pandas as pd

from benchmarks.sciencebench.image_eval import grade_visual_rows

EXPECTED_FILES = ("bio_ecg_plot.png", "bio_rsp_plot.png")
THRESHOLD = 60.0


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

    selected_rows = []
    missing = []
    for filename in EXPECTED_FILES:
        match = merged[merged["file_name"] == filename]
        if match.empty:
            missing.append(filename)
            continue
        row = match.iloc[0]
        selected_rows.append(
            {
                "image_base64_pred": row["image_base64_pred"],
                "image_base64_gold": row["image_base64_gold"],
            }
        )

    if missing:
        print("Missing expected visualization(s): " + ", ".join(missing))
        return 0.0

    return grade_visual_rows(selected_rows, threshold_score=THRESHOLD)


"""
Grading function for sciencebench 075 topic modeling lda visualization task.

Mirrors the original ScienceAgentBench evaluation that compares the generated
PNG against the gold reference with a GPT-4 based judge (threshold 60). When
that optional dependency is unavailable we fall back to a deterministic pixel
similarity proxy.
"""

import pandas as pd

from benchmarks.sciencebench.image_eval import grade_visual_rows

EXPECTED_FILENAME = "topic_modeling_pred.png"
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

    filtered_rows = [
        row for row in merged.to_dict("records") if row.get("file_name") == EXPECTED_FILENAME
    ]
    if not filtered_rows:
        print(f"Expected visualization '{EXPECTED_FILENAME}' not found in submission.")
        return 0.0

    return grade_visual_rows(filtered_rows, threshold_score=THRESHOLD)

import pandas as pd
import re


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    """
    Grade the mathmodeling DABench submission.

    The submission format is: @mean_fare[value]
    We need to extract the value and compare with the ground truth.
    """
    try:
        if len(submission) != 1 or len(answers) != 1:
            return 0.0

        submission_str = str(submission.iloc[0]["answer"]).strip()
        answer_str = str(answers.iloc[0]["answer"]).strip()

        submission_pattern = r"@mean_fare\[([\d.]+)\]"
        answer_pattern = r"@mean_fare\[([\d.]+)\]"

        submission_match = re.search(submission_pattern, submission_str)
        answer_match = re.search(answer_pattern, answer_str)

        if not submission_match or not answer_match:
            return 0.0

        submission_value = float(submission_match.group(1))
        answer_value = float(answer_match.group(1))

        if abs(submission_value - answer_value) < 0.01:
            return 1.0
        return 0.0
    except Exception:
        return 0.0

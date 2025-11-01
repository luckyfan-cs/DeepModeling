import pandas as pd
import re


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    """
    Grade the DABench submission.

    The submission format is: @mean_fare[value]
    We need to extract the value and compare with the ground truth.

    Args:
        submission: DataFrame with columns ['id', 'answer']
        answers: DataFrame with columns ['id', 'answer']

    Returns:
        float: 1.0 if exact match, 0.0 otherwise
    """
    try:
        # Both should have exactly one row (id=0)
        if len(submission) != 1 or len(answers) != 1:
            return 0.0

        # Get the submission and answer strings
        submission_str = str(submission.iloc[0]['answer']).strip()
        answer_str = str(answers.iloc[0]['answer']).strip()

        # Parse the submission format: @mean_fare[value]
        submission_pattern = r'@mean_fare\[([\d.]+)\]'
        answer_pattern = r'@mean_fare\[([\d.]+)\]'

        submission_match = re.search(submission_pattern, submission_str)
        answer_match = re.search(answer_pattern, answer_str)

        if not submission_match or not answer_match:
            print(f"Failed to parse: submission='{submission_str}', answer='{answer_str}'")
            return 0.0

        # Extract values
        submission_value = float(submission_match.group(1))
        answer_value = float(answer_match.group(1))

        # Check if they match (allowing for small floating point differences)
        if abs(submission_value - answer_value) < 0.01:
            return 1.0
        else:
            print(f"Value mismatch: submission={submission_value}, answer={answer_value}")
            return 0.0

    except Exception as e:
        print(f"Error in grading: {e}")
        return 0.0

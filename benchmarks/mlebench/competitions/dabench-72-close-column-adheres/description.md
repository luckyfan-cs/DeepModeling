# DABench Task 72 - Check if the "Close" column adheres to a normal distribution.

## Task Description

Check if the "Close" column adheres to a normal distribution.

## Concepts

Distribution Analysis

## Data Description

Dataset file: `microsoft.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

Use the Shapiro-Wilk test to assess the normality of the "Close" column. If the p-value is less than 0.05, consider the data to be non-normally distributed. Otherwise, consider it to be normally distributed.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@normality_test_result[normality_test_result]\nwhere "normality_test_result" a string that is either "Normal" or "Non-normal" based on the p-value from the Shapiro-Wilk test.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Easy

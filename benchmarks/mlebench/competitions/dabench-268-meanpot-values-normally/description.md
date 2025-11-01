# DABench Task 268 - Are the MEANPOT values normally distributed in the dataset?

## Task Description

Are the MEANPOT values normally distributed in the dataset?

## Concepts

Distribution Analysis

## Data Description

Dataset file: `3901.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

Determine the normality of the values in the MEANPOT column using the Shapiro-Wilk test for normality. Consider the values to be normally distributed if the p-value is greater than 0.05. Report your findings as "Normal" if the p-value is greater than 0.05 and "Not Normal" otherwise. Report the p-value as well.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@normality_test_result[A string that should be either "Normal" or "Not Normal"] @p_value[The Shapiro-Wilk test p-value, rounded to three decimal places]

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Easy

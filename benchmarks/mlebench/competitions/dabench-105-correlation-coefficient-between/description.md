# DABench Task 105 - Calculate the correlation coefficient between ApplicantIncome and LoanAmount.

## Task Description

Calculate the correlation coefficient between ApplicantIncome and LoanAmount.

## Concepts

Correlation Analysis

## Data Description

Dataset file: `test_Y3wMUE5_7gLdaTN.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

Calculate the Pearson correlation coefficient to assess the strength and direction of linear relationship between ApplicantIncome and LoanAmount. Ignore the rows with missing values for either of the two columns. Round the correlation coefficient to two decimal places.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@correlation_coefficient[corr_coeff] where "corr_coeff" is a number between -1 and 1, rounded to two decimal places and represents the Pearson correlation coefficient between ApplicantIncome and LoanAmount.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Medium

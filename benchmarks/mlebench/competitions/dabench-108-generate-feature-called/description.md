# DABench Task 108 - Generate a new feature called "TotalIncome" by adding the ApplicantIncome and CoapplicantIncome columns. Calculate the mean and standard deviation of the TotalIncome column.

## Task Description

Generate a new feature called "TotalIncome" by adding the ApplicantIncome and CoapplicantIncome columns. Calculate the mean and standard deviation of the TotalIncome column.

## Concepts

Feature Engineering, Summary Statistics

## Data Description

Dataset file: `test_Y3wMUE5_7gLdaTN.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

Calculate the mean and standard deviation using the Panda's DataFrame mean() and std() functions distinctively. Round the results to two decimal places.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@mean_total_income[mean] @std_dev_total_income[std_dev] where "mean" is a float number that represents the mean value of the TotalIncome column rounded to two decimal places, and "std_dev" is a float number that represents the standard deviation of the TotalIncome column also rounded to two decimal places.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Medium

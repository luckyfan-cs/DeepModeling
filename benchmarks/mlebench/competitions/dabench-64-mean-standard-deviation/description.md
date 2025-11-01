# DABench Task 64 - Calculate the mean and standard deviation of the wage column.

## Task Description

Calculate the mean and standard deviation of the wage column.

## Concepts

Summary Statistics

## Data Description

Dataset file: `beauty and the labor market.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

The mean and standard deviation of the wage should be calculated using pandas' `mean()` and `std()` methods respectively. Do not apply any transformations, filtering or alteration to the wage data.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@mean_wage[mean_value] @std_wage[std_value] where "mean_value" and "std_value" are numbers with up to two decimal places.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Easy

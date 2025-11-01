# DABench Task 216 - Calculate the mean and standard deviation of the abs_diffsel column.

## Task Description

Calculate the mean and standard deviation of the abs_diffsel column.

## Concepts

Summary Statistics

## Data Description

Dataset file: `ferret-Pitt-2-preinf-lib2-100_sitediffsel.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

{
The mean and standard deviation should be calculated directly from the 'abs_diffsel' column.
Do not remove any outliers or modify the data prior to calculation.
The mean and standard deviation should be computed directly from all available data points.
}

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

{
@mean[mean_value]
@std_dev[std_dev_value]
where "mean_value" is a positive float number, rounded to two decimal places.
where "std_dev_value" is a positive float number, rounded to two decimal places.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Easy

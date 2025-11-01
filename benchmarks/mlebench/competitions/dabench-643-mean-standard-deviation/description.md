# DABench Task 643 - Calculate the mean, standard deviation, minimum, and maximum values of the "Volume" column.

## Task Description

Calculate the mean, standard deviation, minimum, and maximum values of the "Volume" column.

## Concepts

Summary Statistics

## Data Description

Dataset file: `random_stock_data.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

Use Python's built-in statistical functions to calculate these values. Round these numbers to two decimal places.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@mean_volume[mean value]
@std_volume[standard deviation value]
@min_volume[minimum value]
@max_volume[maximum value]
where "mean value", "standard deviation value", "minimum value", and "maximum value" are numbers rounded to two decimal places.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Easy

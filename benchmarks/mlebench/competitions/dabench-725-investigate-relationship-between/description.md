# DABench Task 725 - 1. Investigate the relationship between 'displacement' and 'mpg' by analyzing the distribution of 'mpg' for each unique value of 'displacement'. Calculate the mean and median 'mpg' for each of the three most common unique values of 'displacement'.

## Task Description

1. Investigate the relationship between 'displacement' and 'mpg' by analyzing the distribution of 'mpg' for each unique value of 'displacement'. Calculate the mean and median 'mpg' for each of the three most common unique values of 'displacement'.

## Concepts

Distribution Analysis, Correlation Analysis

## Data Description

Dataset file: `auto-mpg.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

{
- Only consider the three unique 'displacement' values that occur most frequently in the dataset.
- The 'mpg' means and medians must be calculated for each of these three values separately, with 'mpg' values only from rows with the corresponding 'displacement' value.
- Results must be rounded to two decimal places.
}

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

{
@mean1[mean1], @median1[median1]
@mean2[mean2], @median2[median2]
@mean3[mean3], @median3[median3]
where "mean1", "median1", "mean2", "median2", "mean3", "median3" are corresponding mean and median 'mpg' values for each of the top three 'displacement' values, respectively. Each value should be a float, rounded to two decimal places.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Hard

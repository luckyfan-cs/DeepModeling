# DABench Task 175 - Identify if there are any outliers in the age of the passengers on the Titanic using the Z-score method. Use a threshold of 3 for outlier detection.

## Task Description

Identify if there are any outliers in the age of the passengers on the Titanic using the Z-score method. Use a threshold of 3 for outlier detection.

## Concepts

Outlier Detection

## Data Description

Dataset file: `titanic.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

Use Z-score method for outlier detection. Any data point that has a Z-score greater than 3 or less than -3 should be considered an outlier. The python library scipy's zscore() function should be used. Ignore the null values during calculation.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@outliers_count[outliers_count] 
where "outliers_count" is the number of outliers detected in the age of passengers. This should be an integer number.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Medium

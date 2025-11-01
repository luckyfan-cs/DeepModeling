# DABench Task 27 - Identify the outliers in the charges incurred by individuals using the Z-score method.

## Task Description

Identify the outliers in the charges incurred by individuals using the Z-score method.

## Concepts

Outlier Detection

## Data Description

Dataset file: `insurance.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

Apply the Z-score method for outlier detection using the 1.5xIQR rule. Consider any value that falls below Q1 - 1.5 * IQR or above Q3 + 1.5 * IQR as an outlier. Report the total number of outliers, and the mean and median charges of these identified outliers.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@total_outliers[total_outliers] 
@mean_charges_outliers[mean_charges_outliers] 
@median_charges_outliers[median_charges_outliers] 
where "total_outliers" is an integer, "mean_charges_outliers" and "median_charges_outliers" are floating-point numbers rounded to two decimal places.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Medium

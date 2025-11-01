# DABench Task 669 - Identify and remove any outliers in the MedInc column of the provided dataset using the IQR method. Then calculate the mean and standard deviation of the cleaned MedInc column.

## Task Description

Identify and remove any outliers in the MedInc column of the provided dataset using the IQR method. Then calculate the mean and standard deviation of the cleaned MedInc column.

## Concepts

Outlier Detection, Summary Statistics

## Data Description

Dataset file: `my_test_01.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

Identify an outlier as any value that falls below Q1 - 1.5 * IQR or above Q3 + 1.5 * IQR, where Q1 and Q3 are the first and third quartiles, respectively, and IQR is the interquartile range (Q3 - Q1). Calculate the mean and standard deviation to two decimal places.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@mean[mean_value] where "mean_value" is a float rounded to two decimal places. @standard_deviation[standard_deviation_value] where "standard_deviation_value" is a float rounded to two decimal places.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Hard

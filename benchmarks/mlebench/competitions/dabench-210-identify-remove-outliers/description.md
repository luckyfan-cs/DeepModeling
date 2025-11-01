# DABench Task 210 - 1. Identify and remove any outliers in the "neg" sentiment score column using the Z-score method, where Z is defined as (value - mean) / standard deviation. Assume a data point to be an outlier if its Z-score is greater than 3 or less than -3. After removing outliers, calculate the new mean and standard deviation for the "neg" sentiment score column.

## Task Description

1. Identify and remove any outliers in the "neg" sentiment score column using the Z-score method, where Z is defined as (value - mean) / standard deviation. Assume a data point to be an outlier if its Z-score is greater than 3 or less than -3. After removing outliers, calculate the new mean and standard deviation for the "neg" sentiment score column.

## Concepts

Outlier Detection, Summary Statistics

## Data Description

Dataset file: `fb_articles_20180822_20180829_df.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

Z-score is calculated with its general mathematical formula (value - mean) / standard deviation. Consider a data point as an outlier if its Z-score is greater than 3 or less than -3. Do this for the "neg" sentiment score column only.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@mean_neg[mean]\n@std_dev_neg[std_dev] where "mean" and "std_dev" are floating-point numbers rounded to two decimal places. Additionally, "mean" and "std_dev" should be greater than 0 and less than 1 as they mimic sentiment scores.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Hard

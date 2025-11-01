# DABench Task 411 - Are there any outliers in the fare paid by the passengers? If so, how many outliers are there and what is their range?

## Task Description

Are there any outliers in the fare paid by the passengers? If so, how many outliers are there and what is their range?

## Concepts

Outlier Detection

## Data Description

Dataset file: `titanic_train.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

An outlier is identified based on the IQR method. An outlier is defined as a point that falls outside 1.5 times the IQR above the third quartile or below the first quartile.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@outlier_count[answer1] @outlier_range_low[answer2] @outlier_range_high[answer3] where "answer1" is the number of outliers, "answer2" is the lowest value among outliers and "answer3" is the highest value among outliers. All results should be rounded to 2 decimal places.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Medium

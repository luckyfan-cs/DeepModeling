# DABench Task 528 - Are there any outliers in the fare paid by the passengers? If so, how many are there and can you identify them?

## Task Description

Are there any outliers in the fare paid by the passengers? If so, how many are there and can you identify them?

## Concepts

Outlier Detection, Comprehensive Data Preprocessing

## Data Description

Dataset file: `titanic_test.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

Identify outliers using the IQR method where a fare is considered an outlier if it is 1.5 times the IQR above the third quartile or below the first quartile. Use all fare values for this analysis and do not consider the outlier if it's missing.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@outlier_count[count], @outlier_ids[id1, id2, ...]. The "count" is an integer. "id1, id2, ..." are the "PassengerId"s of the outliers, separated by commas and sorted in ascending order.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Medium

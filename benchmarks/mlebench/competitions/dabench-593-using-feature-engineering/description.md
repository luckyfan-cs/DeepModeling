# DABench Task 593 - Using feature engineering techniques, create a new feature that represents the waiting time for callers before being answered by an agent as a percentage of the average abandonment time. Then, explore the distribution of this new feature and determine if it adheres to a normal distribution.

## Task Description

Using feature engineering techniques, create a new feature that represents the waiting time for callers before being answered by an agent as a percentage of the average abandonment time. Then, explore the distribution of this new feature and determine if it adheres to a normal distribution.

## Concepts

Feature Engineering, Distribution Analysis

## Data Description

Dataset file: `20170413_000000_group_statistics.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

Create a new feature 'waiting_ratio' that is defined as the ratio of average waiting time to the average abandonment time, represented as a percentage. Convert the waiting and abandonment time from format HH:MM:SS to seconds before the calculation. After creating the feature, calculate the skewness of this new feature. Use the skewness to determine whether the data is normally distributed. For normally distributed data, skewness should be about 0.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@waiting_ratio_skewness[skewness_value]
@is_normal[is_normal]
where "skewness_value" is the skewness of the 'waiting_ratio' feature rounded to two decimal places.
where "is_normal" is a boolean value that should be "True" if the absolute value of skewness is less than 0.5 and "False" otherwise.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Hard

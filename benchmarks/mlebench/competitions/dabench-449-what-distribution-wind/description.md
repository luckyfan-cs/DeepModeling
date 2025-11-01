# DABench Task 449 - 1. What is the distribution of wind speeds (WINDSPEED) in the dataset? Is it normally distributed?

## Task Description

1. What is the distribution of wind speeds (WINDSPEED) in the dataset? Is it normally distributed?

## Concepts

Distribution Analysis

## Data Description

Dataset file: `baro_2015.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

Use the Shapiro-Wilk test to determine if the distribution is normal. Accept the null hypothesis that the data is normally distributed if the p-value is greater than 0.05, and reject it otherwise.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@shapiro_wilk_pvalue[p_value] @normal_distribution[yes/no] where "p_value" is a number between 0 and 1, rounded to four decimal places and "normal_distribution" is a string that can either be "yes" if p_value > 0.05 or "no" if p_value <= 0.05

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Easy

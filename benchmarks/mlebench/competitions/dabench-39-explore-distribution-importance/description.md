# DABench Task 39 - Explore the distribution of the "importance.score" column and determine if it follows a normal distribution by conducting a Shapiro-Wilk test. If the p-value is less than 0.05, apply a log transformation to make the distribution closer to normal. Calculate the mean and standard deviation of the transformed "importance.score" column.

## Task Description

Explore the distribution of the "importance.score" column and determine if it follows a normal distribution by conducting a Shapiro-Wilk test. If the p-value is less than 0.05, apply a log transformation to make the distribution closer to normal. Calculate the mean and standard deviation of the transformed "importance.score" column.

## Concepts

Distribution Analysis, Feature Engineering

## Data Description

Dataset file: `imp.score.ldlr.metabolome.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

1. Use the Shapiro-Wilk test to determine the normality of the data in the "importance.score" column. The null hypothesis for this test is that the data was drawn from a normal distribution.
2. Use a significance level of 0.05 for the Shapiro-Wilk test.
3. If the p-value from the Shapiro-Wilk test is less than 0.05, apply a natural log transformation to the "importance.score" column.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@is_normal[p_value]
@transformed_importance_score_mean[mean]
@transformed_importance_score_std[std]

where "p_value" is a number between 0 and 1, rounded to four decimal places.
where "mean" is the mean of the transformed "importance.score" column, rounded to two decimal places.
where "std" is the standard deviation of the transformed "importance.score" column, rounded to two decimal places.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Hard

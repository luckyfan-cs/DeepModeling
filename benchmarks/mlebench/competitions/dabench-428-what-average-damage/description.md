# DABench Task 428 - 1. What is the average damage in USD caused by storms in each year from 2000 to 2010? Are there any significant differences in the average damage between years?

## Task Description

1. What is the average damage in USD caused by storms in each year from 2000 to 2010? Are there any significant differences in the average damage between years?

## Concepts

Summary Statistics, Distribution Analysis

## Data Description

Dataset file: `cost_data_with_errors.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

{
Calculate the mean damage in USD for each year.
Perform a one-way Analysis of Variance (ANOVA) to test whether there are significant differences in the average damage between years.
The significance level (alpha) for the ANOVA test should be 0.05.
Report the p-value associated with the ANOVA test.
If the p-value is less than 0.05, infer that there are significant differences.
If the p-value is greater than or equal to 0.05, infer that there are no significant differences.
}

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

{
@average_damage[average_damage_from_2000, average_damage_from_2001, ..., average_damage_from_2010]
@p_value[p_value]
@difference_type[difference_type]
where "average_damage_from_year" is the mean damage in USD for the corresponding year, rounded to 2 decimal places.
where "p_value" is a number between 0 and 1, rounded to 4 decimal places.
where "difference_type" is a string that can either be "significant" or "none" based on the conditions specified in the constraints.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Hard

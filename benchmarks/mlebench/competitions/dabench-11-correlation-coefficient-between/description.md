# DABench Task 11 - Calculate the correlation coefficient between the "High Price" column and the "Low Price" column.

## Task Description

Calculate the correlation coefficient between the "High Price" column and the "Low Price" column.

## Concepts

Correlation Analysis

## Data Description

Dataset file: `GODREJIND.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

Calculate the Pearson correlation coefficient (r) to assess the strength and direction of the linear relationship between "High Price" and "Low Price". Assess the significance of the correlation using a two-tailed test with a significance level (alpha) of 0.05. Report the p-value associated with the correlation test. Consider the relationship to be linear if the p-value is less than 0.05 and the absolute value of r is greater than or equal to 0.5. Consider the relationship to be nonlinear if the p-value is less than 0.05 and the absolute value of r is less than 0.5. If the p-value is greater than or equal to 0.05, report that there is no significant correlation.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@correlation_coefficient[r_value] @p_value[p_value] @relationship_type[relationship_type], where "r_value" is a number between -1 and 1, rounded to two decimal places. "p_value" is a number between 0 and 1, rounded to four decimal places. "relationship_type" is a string that can either be "linear", "nonlinear", or "none" based on the conditions specified in the constraints.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Medium

# DABench Task 136 - Perform distribution analysis on the fare paid by passengers for each passenger class separately. Use the Shapiro-Wilk Test for normality. For each passenger class, the null hypothesis is that the fare follows a normal distribution.

## Task Description

Perform distribution analysis on the fare paid by passengers for each passenger class separately. Use the Shapiro-Wilk Test for normality. For each passenger class, the null hypothesis is that the fare follows a normal distribution.

## Concepts

Distribution Analysis, Summary Statistics

## Data Description

Dataset file: `titanic.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

The Shapiro-Wilk Test should be conducted separately for each passenger class. Use a significance level (alpha) of 0.05. If the p-value is less than 0.05, reject the null hypothesis.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@p_value_class_1[p_value_1], @p_value_class_2[p_value_2], @p_value_class_3[p_value_3] where 'p_value_1', 'p_value_2', and 'p_value_3' are the p-values of the Shapiro-Wilk Test for the 1st, 2nd and 3rd class passengers respectively, rounded to four decimal places.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Medium

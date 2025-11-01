# DABench Task 117 - Which variable has the strongest correlation with the happiness scores among countries? Is this correlation positive or negative?

## Task Description

Which variable has the strongest correlation with the happiness scores among countries? Is this correlation positive or negative?

## Concepts

Correlation Analysis

## Data Description

Dataset file: `2015.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

Calculate the Pearson correlation coefficient (r) between the happiness score and all other numerical variables in the dataset. The variable which has the highest magnitude of r (ignoring the sign) is the one with the strongest correlation.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@strongest_correlation_variable[variable_name] where "variable_name": the column name of the variable with the strongest correlation. @correlation_type[positive/negative] where "positive/negative": if the correlation is positive or negative based on the sign of the correlation coefficient.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Medium

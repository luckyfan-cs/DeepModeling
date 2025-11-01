# DABench Task 310 - Perform a correlation analysis on the numerical variables (age, fare, SibSp, Parch) to identify any significant relationships. Calculate the Pearson correlation coefficients between all pairs of these variables and identify the pair with the strongest positive correlation.

## Task Description

Perform a correlation analysis on the numerical variables (age, fare, SibSp, Parch) to identify any significant relationships. Calculate the Pearson correlation coefficients between all pairs of these variables and identify the pair with the strongest positive correlation.

## Concepts

Correlation Analysis

## Data Description

Dataset file: `titanic.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

Use Python's pandas library for correlation analysis. Calculate the Pearson correlation coefficients using the 'pandas.DataFrame.corr()' function with the default method (Pearson). The pair should not compare a variable with itself.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@strongest_correlation_pair[pair]
@strongest_correlation_coefficient[coefficient]
where "pair" is a list of two strings representing variables names,
"coefficient" is a float between -1 and 1, rounded to two decimal places.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Hard

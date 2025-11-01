# DABench Task 730 - Is there a correlation between population and GDP per capita for the recorded years and countries in the dataset?

## Task Description

Is there a correlation between population and GDP per capita for the recorded years and countries in the dataset?

## Concepts

Correlation Analysis

## Data Description

Dataset file: `gapminder_cleaned.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

Calculate the Pearson correlation coefficient (pearson’s r) between "Pop" and "Gdppercap" columns. Use the scipy library's pearsonr() function and consider the correlation to be significant if p-value is less than 0.05.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@correlation_coefficient[r_value]
@p_value[p_value]
where "r_value" is a number between -1 and 1, rounded to two decimal places.
where "p_value" is a number between 0 and 1, rounded to four decimal places.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Medium

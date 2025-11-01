# DABench Task 118 - Is there a linear relationship between the GDP per capita and the life expectancy score in the dataset? Conduct linear regression and use the resulting coefficient of determination (R-squared) to evaluate the model's goodness of fit.

## Task Description

Is there a linear relationship between the GDP per capita and the life expectancy score in the dataset? Conduct linear regression and use the resulting coefficient of determination (R-squared) to evaluate the model's goodness of fit.

## Concepts

Correlation Analysis, Machine Learning

## Data Description

Dataset file: `2015.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

Calculate the coefficient of determination (R-squared) for the given relationship. If R-squared is equal to or greater than 0.7, consider the model a good fit. Else, consider it a poor fit.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@coefficient_determination[R_square], @model_fit[model_fit], where "R_square" is the value of the coefficient of determination rounded to two decimal places and "model_fit" is a string that is either "good fit" or "poor fit" based on the calculated R-squared value.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Hard

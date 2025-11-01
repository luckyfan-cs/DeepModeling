# DABench Task 355 - Perform a linear regression analysis to predict fare based on age and passenger class.

## Task Description

Perform a linear regression analysis to predict fare based on age and passenger class.

## Concepts

Correlation Analysis, Machine Learning

## Data Description

Dataset file: `test_x.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

{
Use the simple linear regression model where Fare is the dependent variable and Age and Pclass are the independent variables.
Consider the relationship to be significant if the p-value is less than 0.05 for both variables (Age and Pclass).
If the p-value is greater than or equal to 0.05 for either variable, report that there is no significant relationship.
}

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

{
@coef_age[coef_age]
@coef_pclass[coef_pclass]
@relationship_age[relationship_age]
@relationship_pclass[relationship_pclass]
where "coef_age" and "coef_pclass" are the regression coefficients for the variables Age and Pclass respectively, rounded to two decimal places.
where "relationship_age" and "relationship_pclass" are strings that can either be "significant" or "not significant" based on the conditions specified in the constraints.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Hard

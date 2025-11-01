# DABench Task 423 - 2. Perform feature engineering on the given dataset to create a new feature 'Volatility' that is calculated using the formula: Volatility = (High Price - Low Price) / Open Price. What is the Pearson correlation coefficient between Volatility and trading volume? Interpret the result.

## Task Description

2. Perform feature engineering on the given dataset to create a new feature 'Volatility' that is calculated using the formula: Volatility = (High Price - Low Price) / Open Price. What is the Pearson correlation coefficient between Volatility and trading volume? Interpret the result.

## Concepts

Feature Engineering, Correlation Analysis

## Data Description

Dataset file: `bitconnect_price.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

Calculate the Pearson correlation coefficient (r) to assess the strength and direction of the linear relationship between the new feature 'Volatility' and trading volume. Consider the relationship to be positive if the r value is greater than or equal to 0.5. Consider the relationship to be negative if the r value is less than or equal to -0.5. Otherwise, report that there is no significant correlation.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@correlation_coefficient[correlation_coefficient], @relationship_type[type] where "correlation_coefficient" is a number between -1 and 1, rounded to two decimal places. "type" is a string that can be "positive", "negative", or "none" based on the conditions specified in the constraints.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Hard

# DABench Task 360 - Determine the correlation coefficient between temperature and humidity in the weather dataset.

## Task Description

Determine the correlation coefficient between temperature and humidity in the weather dataset.

## Concepts

Correlation Analysis

## Data Description

Dataset file: `weather_train.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

For missing values in either the "temperature" or "humidity" columns, use the 'dropna' method to remove these datapoints before calculations.
Calculate the Pearson correlation coefficient (r) to assess the strength and direction of the linear relationship between temperature and humidity.
Consider a correlation to be strong if the absolute value of r is greater than or equal to 0.7, moderate if it is between 0.3 and 0.7, and weak if it is less than 0.3.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@correlation_coefficient[r_value]
@correlation_strength[strength_value]
where "r_value" is a float number between -1 and 1, rounded to 2 decimal places.
where "strength_value" is a string that can be either "strong", "moderate", or "weak" based on the conditions specified in the constraints.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Medium

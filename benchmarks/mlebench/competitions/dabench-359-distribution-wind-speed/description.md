# DABench Task 359 - Check if the distribution of wind speed in the weather dataset is skewed.

## Task Description

Check if the distribution of wind speed in the weather dataset is skewed.

## Concepts

Distribution Analysis

## Data Description

Dataset file: `weather_train.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

For missing values in the "wind speed" column, use the 'dropna' method to remove these data points before calculations.
Determine the skewness using Pearson's First Coefficient of Skewness. 
Report whether the distribution is positively skewed, negatively skewed, or symmetric based on the obtained skewness value. 
Assume the distribution to be positively skewed if skewness value is > 0, negatively skewed if skewness is < 0, and symmetric if skewness is 0.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@skewness_value[skew_value]
@skewness_type[type_value]
where "skew_value" is a float number rounded to 2 decimal places.
where "type_value" is a string that can be either "positive", "negative", or "symmetric" based on the conditions specified in the constraints.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Easy

# DABench Task 647 - Create a new feature called "Price Range" by calculating the difference between the "High" and "Low" values for each entry. Then, determine if the "Price Range" follows a normal distribution.

## Task Description

Create a new feature called "Price Range" by calculating the difference between the "High" and "Low" values for each entry. Then, determine if the "Price Range" follows a normal distribution.

## Concepts

Feature Engineering, Distribution Analysis

## Data Description

Dataset file: `random_stock_data.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

Calculate "Price Range" for each row by subtracting the "Low" value from the "High" value. Test the normality of the resulting column using the Shapiro-Wilk test. Consider the data to follow a normal distribution if the p-value is greater than 0.05.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@price_range_mean[mean_value] @price_range_stddev[stddev_value] @price_range_p_value[p_value] @is_normal[str], where "mean_value" and "stddev_value" are the mean and standard deviation of "Price Range", rounded to two decimal places, "p_value" is a number between 0 and 1, rounded to four decimal places, and "is_normal" is a string that can be either "yes" or "no" based on the Shapiro-Wilk test result.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Hard

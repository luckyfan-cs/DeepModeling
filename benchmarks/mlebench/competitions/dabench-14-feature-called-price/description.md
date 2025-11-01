# DABench Task 14 - Create a new feature called "Price Range" which represents the difference between the "High Price" and "Low Price" for each row. Calculate the mean, median, and standard deviation of this new feature.

## Task Description

Create a new feature called "Price Range" which represents the difference between the "High Price" and "Low Price" for each row. Calculate the mean, median, and standard deviation of this new feature.

## Concepts

Feature Engineering, Summary Statistics

## Data Description

Dataset file: `GODREJIND.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

Make sure to use the correct columns for calculating the "Price Range". All calculations should be performed up to two decimal places.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@price_range_mean[mean]: The mean should be a single real number rounded to two decimal places. @price_range_median[median]: The median should be a single real number rounded to two decimal places. @price_range_std_dev[std_dev]: The standard deviation should be a single real number rounded to two decimal places.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Medium

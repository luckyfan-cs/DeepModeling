# DABench Task 6 - Create a new column called "AgeGroup" that categorizes the passengers into four age groups: 'Child' (0-12 years old), 'Teenager' (13-19 years old), 'Adult' (20-59 years old), and 'Elderly' (60 years old and above). Then, calculate the mean fare for each age group.

## Task Description

Create a new column called "AgeGroup" that categorizes the passengers into four age groups: 'Child' (0-12 years old), 'Teenager' (13-19 years old), 'Adult' (20-59 years old), and 'Elderly' (60 years old and above). Then, calculate the mean fare for each age group.

## Concepts

Feature Engineering, Summary Statistics

## Data Description

Dataset file: `test_ave.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

Make sure to round the mean fare of each group to 2 decimal places.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@mean_fare_child[mean_fare], @mean_fare_teenager[mean_fare], @mean_fare_adult[mean_fare], @mean_fare_elderly[mean_fare], where "mean_fare" is a float number rounded to 2 decimal places.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Medium

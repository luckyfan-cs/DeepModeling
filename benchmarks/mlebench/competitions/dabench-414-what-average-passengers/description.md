# DABench Task 414 - What is the average age of passengers in each ticket class (Pclass)?

## Task Description

What is the average age of passengers in each ticket class (Pclass)?

## Concepts

Summary Statistics, Comprehensive Data Preprocessing

## Data Description

Dataset file: `titanic_train.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

Calculate the average (mean) age of the passengers in each class separately (Pclass = 1, Pclass = 2, Pclass = 3).
Ignore the rows with missing age.
Round the average age to two decimal places.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@first_class_average_age[average_age_1]
@second_class_average_age[average_age_2]
@third_class_average_age[average_age_3]
where "average_age_1" is the average age of the first-class passengers, rounded to two decimal places.
where "average_age_2" is the average age of the second-class passengers, rounded to two decimal places.
where "average_age_3" is the average age of the third-class passengers, rounded to two decimal places.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Medium

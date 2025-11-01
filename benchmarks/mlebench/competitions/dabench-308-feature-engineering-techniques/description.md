# DABench Task 308 - Use feature engineering techniques to create a new variable "Title" by extracting the title from the Name column (e.g., "Mr.", "Mrs.", "Miss"). Only consider the following titles: 'Mr.', 'Mrs.', 'Miss.' and 'Master.' (titles followed by a dot). Then, calculate the average fare for each unique title to two decimal places.

## Task Description

Use feature engineering techniques to create a new variable "Title" by extracting the title from the Name column (e.g., "Mr.", "Mrs.", "Miss"). Only consider the following titles: 'Mr.', 'Mrs.', 'Miss.' and 'Master.' (titles followed by a dot). Then, calculate the average fare for each unique title to two decimal places.

## Concepts

Feature Engineering, Summary Statistics

## Data Description

Dataset file: `titanic.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

Only the titles 'Mr.', 'Mrs.', 'Miss.' and 'Master.' should be considered. Titles that do not fall within these four categories should be eliminated.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@average_fare_Mr[value1], @average_fare_Mrs[value2], @average_fare_Miss[value3], @average_fare_Master[value4], where value1, value2, value3, and value4 represent the average fares for 'Mr.', 'Mrs.', 'Miss.', and 'Master.', respectively. All values should be rounded to two decimal places.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Hard

# DABench Task 0 - Calculate Mean Fare

## Task Description

Calculate the mean fare paid by the passengers in the Titanic dataset.

## Concepts

- Summary Statistics

## Data Description

The dataset contains passenger information from the Titanic, including:
- `PassengerId`: Unique identifier for each passenger
- `Survived`: Survival status (0 = No, 1 = Yes)
- `Pclass`: Passenger class (1 = 1st, 2 = 2nd, 3 = 3rd)
- `Name`: Passenger name
- `Sex`: Gender
- `Age`: Age in years
- `SibSp`: Number of siblings/spouses aboard
- `Parch`: Number of parents/children aboard
- `Ticket`: Ticket number
- `Fare`: Passenger fare
- `Cabin`: Cabin number
- `Embarked`: Port of embarkation (C = Cherbourg, Q = Queenstown, S = Southampton)
- `AgeBand`: Age group category

## Files

- `train.csv` - The training data containing all passenger information
- `sample_submission.csv` - A sample submission file in the correct format

## Constraints

- Calculate the mean fare using Python's built-in statistics module or appropriate statistical method in pandas
- Round off the answer to two decimal places

## Submission Format

Your submission must follow this exact format:

```
@mean_fare[mean_fare_value]
```

where `mean_fare_value` is a floating-point number rounded to two decimal places.

### Example

```
@mean_fare[34.65]
```

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer.

## Goal

Calculate the correct mean fare value rounded to two decimal places.

## Difficulty Level

Easy

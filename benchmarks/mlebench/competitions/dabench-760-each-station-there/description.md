# DABench Task 760 - 6. For each station, are there any missing values in the observation values (obs_value)? If yes, which station has the most missing values and how many missing values does it have?

## Task Description

6. For each station, are there any missing values in the observation values (obs_value)? If yes, which station has the most missing values and how many missing values does it have?

## Concepts

Comprehensive Data Preprocessing

## Data Description

Dataset file: `weather_data_1864.csv`

The data is available in the `train.csv` file in the public directory.

## Constraints

In your analysis:
- Assume that missing values are represented as "NaN".
- Calculate the number of missing values for each station.

## Files

- `train.csv` - The training data
- `sample_submission.csv` - A sample submission file in the correct format

## Submission Format

@most_missing_station_name["station_name"]
@most_missing_station_count[num_missing_obs]

where "station_name" is a string representing the name of the station with the most missing observation value.
where "num_missing_obs" is a number greater than or equal to 0, representing the number of missing observation values for the station with the most missing values.

## Evaluation

Submissions are evaluated on **exact match** with the ground truth answer (with tolerance of 0.01 for floating-point values).

## Goal

Provide the correct answer in the specified format.

## Difficulty Level

Medium

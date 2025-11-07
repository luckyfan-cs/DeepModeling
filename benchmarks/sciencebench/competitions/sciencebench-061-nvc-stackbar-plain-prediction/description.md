# ScienceBench Task 61

## Overview

- Domain: Psychology and Cognitive science
- Subtask Categories: Computational Analysis, Data Visualization
- Source: nriesterer/syllogistic-nvc
- Output Type: Image

## Task

Create a stacked bar plot that summarises model errors derived from the plain-prediction data. Save the figure as `pred_results/stackedbar_plain_prediction.png`.

## Dataset

[START Dataset Preview: nvc]
|-- Ragni2016.csv
|-- accuracies_data_for_plot.csv
|-- ind_data_for_plot.csv
|-- valid_syllogisms.csv
[END Dataset Preview]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader decodes your base64 image, compares it against the reference stacked-bar plot, and marks the submission correct when the similarity score meets the 60-point threshold.

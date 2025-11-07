# ScienceBench Task 62

## Overview

- Domain: Psychology and Cognitive science
- Subtask Categories: Computational Analysis, Data Visualization
- Source: nriesterer/syllogistic-nvc
- Output Type: Image

## Task

Visualise the syllogistic model accuracies as a stacked bar chart highlighting plain predictions versus truth labels. Save the rendered figure to `pred_results/stackedbar_prediction.png`.

## Dataset

[START Dataset Preview: nvc]
|-- Ragni2016.csv
|-- accuracies_data_for_plot.csv
|-- ind_data_for_plot.csv
|-- valid_syllogisms.csv
[END Dataset Preview]

## Submission Format

Create `sample_submission.csv` with the columns `file_name` and `image_base64`. Include a single row for `stackedbar_prediction.png` and leave the encoded value blank.

## Evaluation

The grader decodes the submitted PNG, compares it with the reference visualization, and awards full credit when the similarity score reaches at least 60.

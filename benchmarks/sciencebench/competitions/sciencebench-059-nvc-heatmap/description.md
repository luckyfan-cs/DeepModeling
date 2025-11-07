# ScienceBench Task 59

## Overview

- Domain: Psychology and Cognitive science
- Subtask Categories: Computational Analysis, Data Visualization
- Source: nriesterer/syllogistic-nvc
- Output Type: Image

## Task

Create a heatmap that contrasts model predictions and most-frequent answers for the syllogistic NVC data. Save the visualization to `pred_results/nvc_heatmap.png`.

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

The grader decodes your base64 image, compares it with the reference heatmap, and accepts the submission once the similarity score reaches 60 or higher.

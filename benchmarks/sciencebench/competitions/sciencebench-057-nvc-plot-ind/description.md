# ScienceBench Task 57

## Overview

- Domain: Psychology and Cognitive science
- Subtask Categories: Data Visualization
- Source: nriesterer/syllogistic-nvc
- Output Type: Image

## Task

Use the provided syllogistic reasoning results to summarise model–rule frequencies and render the participant counts as a heatmap saved to `pred_results/indiv_table.png`.

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

The grader decodes your base64 image, compares it with the reference visualization, and accepts submissions meeting the 60-point similarity threshold.

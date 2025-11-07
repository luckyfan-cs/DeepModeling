# ScienceBench Task 68

## Overview

- Domain: Psychology and Cognitive science
- Subtask Categories: Computational Analysis, Data Visualization
- Source: brand-d/cogsci-jnmf
- Output Type: Image

## Task

Visualise the high-conscientiousness, low-openness pattern comparison and save the figure to `pred_results/CogSci_pattern_high_com_low_plot_data_pred.png`.

## Dataset

[START Dataset Preview: CogSci_pattern_high_com_low_plot_data]
|-- fit_result_conscientiousness_W_high.npy
|-- fit_result_conscientiousness_W_low.npy
[END Dataset Preview]

## Submission Format

Create `sample_submission.csv` with columns `file_name` and `image_base64`. Provide a single row for `CogSci_pattern_high_com_low_plot_data_pred.png`.

## Evaluation

The grader decodes the submitted visualization, compares it with the gold image, and passes the task when the similarity score reaches 60.

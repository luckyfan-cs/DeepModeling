# ScienceBench Task 66

## Overview

- Domain: Psychology and Cognitive science
- Subtask Categories: Computational Analysis, Data Visualization
- Source: brand-d/cogsci-jnmf
- Output Type: Image

## Task

Plot the high-similarity pattern overlays for the cognitive models and save the figure to `pred_results/CogSci_pattern_high_sim_plot_pred.png`.

## Dataset

[START Dataset Preview: CogSci_pattern_high_sim_plot_data]
|-- CogSci_pattern_high_sim_plot.csv
[END Dataset Preview]

## Submission Format

Create `sample_submission.csv` with columns `file_name` and `image_base64` and include a single row for `CogSci_pattern_high_sim_plot_pred.png`.

## Evaluation

The grader decodes your plot, compares it with the reference visualization, and accepts the submission once the similarity score reaches 60.

# ScienceBench Task 68

## Overview

- Domain: Psychology and Cognitive science
- Subtask Categories: Data Visualization
- Source: brand-d/cogsci-jnmf
- Expected Output: CogSci_pattern_high_com_low_plot_data_pred.png
- Output Type: Image

## Task

Visualize conscientiousness patterns in syllogistic reasoning using heatmaps. Process pre-computed weight matrices for high and low conscientiousness groups. Extract and compute a common pattern from these matrices. Generate a figure with three subplots: one each for high conscientiousness, low conscientiousness, and the common pattern.

## Dataset

N/A

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader decodes your base64 image, rescales it to the reference size, and computes a similarity score between 0 and 1.

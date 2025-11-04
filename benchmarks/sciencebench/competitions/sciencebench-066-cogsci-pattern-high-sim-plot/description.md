# ScienceBench Task 66

## Overview

- Domain: Psychology and Cognitive science
- Subtask Categories: Data Visualization
- Source: brand-d/cogsci-jnmf
- Expected Output: CogSci_pattern_high_sim_plot_pred.png
- Output Type: Image

## Task

Generate radar plots comparing cognitive models' similarities to consciousness and openness. Create two polar subplots, one for each personality trait, displaying the similarity scores for seven cognitive models.

## Dataset

[START Preview of CogSci_pattern_high_sim_plot.csv]
,conscientiousness,openness
Atmosphere,0.5228600310231368,0.11279155456167668
Conversion,0.14922967199624335,0.7325706642914023
Matching,0.6698714340521911,0.053331157214874234
…
[End Preview of CogSci_pattern_high_sim_plot.csv]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader decodes your base64 image, rescales it to the reference size, and computes a similarity score between 0 and 1.

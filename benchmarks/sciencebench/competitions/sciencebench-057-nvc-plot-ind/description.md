# ScienceBench Task 57

## Overview

- Domain: Psychology and Cognitive science
- Subtask Categories: Data Visualization
- Source: nriesterer/syllogistic-nvc
- Expected Output: indiv_table.png
- Output Type: Image

## Task

Generate a heatmap to visualize the number of persons associated with each model and rule using the data from ind_data_for_plot.csv.

## Dataset

[START Preview of nvc/ind_data_for_plot.csv]
Model;Rule;Num persons
PSYCOP;PartNeg;41
PSYCOP;EmptyStart;43
PSYCOP;FiguralRule;24
...
[END Preview of nvc/ind_data_for_plot.csv]

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode your final image as base64 (UTF-8 string) and associate it with the expected file name.

## Evaluation

The grader decodes your base64 image, rescales it to the reference size, and computes a similarity score between 0 and 1.

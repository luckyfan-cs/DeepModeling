# ScienceBench Task 9

## Overview

- Domain: Computational Chemistry
- Subtask Categories: Statistical Analysis, Data Visualization
- Source: deepchem/deepchem
- Output Type: Image

## Task

Load the FACTORS dataset, compute the Pearson correlation coefficient between each task and every other task, and visualize the distribution of correlation values as a histogram. 

## Dataset

Molecule,D_00001,D_00002,D_00003,D_00004,D_00005, ...
M_0164851,0,0,0,0,0, ...
M_0164852,0,0,0,0,0, ...
...

## Submission Format

Submit `sample_submission.csv` with the columns `file_name` and `image_base64`. Encode the PNG saved at `pred_results/Factors_correlations.png` as base64 (UTF-8 string) and place it in the row for that filename.

## Evaluation

The grader decodes your base64 image, writes it to disk, and compares it against the gold histogram using the original GPT-4 visual judge with a 60/100 threshold (falling back to pixel similarity if unavailable).

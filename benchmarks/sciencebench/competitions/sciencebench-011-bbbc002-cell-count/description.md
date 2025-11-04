# ScienceBench Task 11

## Overview

- Domain: Bioinformatics
- Subtask Categories: Deep Learning
- Source: deepchem/deepchem
- Expected Output: cell-count_pred.csv
- Output Type: Tabular

## Task

Train a cell counting model on the BBBC002 datasets containing Drosophila KC167 cells. Save the test set predictions as a single column "count" to "output file".

## Dataset

[START Preview of train/BBBC002_v1_counts.txt]
file name        human counter 1 (Robert Lindquist)        human counter #2 (Joohan Chang)
CPvalid1_48_40x_Tiles_p1394DAPI        18        20
CPvalid1_340_40x_Tiles_p1175DAPI        15        19
CPvalid1_Anillin_40x_Tiles_p1069DAPI        32        42
...
[END Preview of train/BBBC002_v1_counts.txt]

## Submission Format

Submit `sample_submission.csv` with the same header and column order as the template. Ensure numeric columns retain their dtype and identifiers remain aligned.

## Evaluation

Classification accuracy (higher is better).

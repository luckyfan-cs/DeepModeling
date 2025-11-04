# ScienceBench Task 26

## Overview

- Domain: Computational Chemistry
- Subtask Categories: Computational Analysis
- Source: chemosim-lab/ProLIF
- Expected Output: ligand_fingerprint_pred.csv
- Output Type: Tabular

## Task

Generate the interaction fingerprints between a selected ligand and protein for the first 10 trajectory frames.

## Dataset

N/A

## Submission Format

Submit `sample_submission.csv` with the same header and column order as the template. Ensure numeric columns retain their dtype and identifiers remain aligned.

## Evaluation

Negative root mean squared error (closer to zero is better).

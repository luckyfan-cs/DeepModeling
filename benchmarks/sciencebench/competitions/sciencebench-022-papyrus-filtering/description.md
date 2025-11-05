# ScienceBench Task 22

## Overview

- Domain: Bioinformatics
- Subtask Categories: Data Filtering, Cheminformatics
- Source: Papyrus
- Output Type: Tabular (pickle)

## Task

Filter the Papyrus dataset according to the companion notebook's criteria and produce a pickled pandas DataFrame of the surviving compounds. Retain the column schema from the provided gold reference and ensure rows are sorted deterministically.

## Dataset

The `papyrus/` directory contains:

- `papyrus_unfiltered.pkl` – base dataset to filter.
- `papyrus_protein_set.pkl` – protein metadata referenced by filtering rules.

## Evaluation

Your submission must save a pickled DataFrame at `pred_results/papyrus_filtered.pkl`. The grader normalizes both DataFrames (sorting, rounding numeric columns) and checks for an exact row-by-row match with the gold reference.
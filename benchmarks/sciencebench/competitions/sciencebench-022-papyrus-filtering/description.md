# ScienceBench Task 22

## Overview

- Domain: Computational Chemistry
- Subtask Categories: Data Selection
- Source: OlivierBeq/Papyrus-scripts
- Output Type: Binary (Pickle)

## Task

Filter the Papyrus dataset according to four criteria: keep only entries with quality ≥ "medium", restrict targets to ligand-gated ion channels or SLC solute carriers, keep only Ki/KD activity types, and retain human or rat proteins. Use `papyrus_protein_set.pkl` for protein metadata if needed. Save the filtered table (same columns as the original) to `pred_results/papyrus_filtered.pkl`.

## Dataset

The `papyrus/` directory contains:

- `papyrus_unfiltered.pkl` – full Papyrus activity table.
- `papyrus_protein_set.pkl` – protein metadata to support filtering.

## Submission Format

Write the filtered DataFrame to `pred_results/papyrus_filtered.pkl` using pandas pickle serialization.

## Evaluation

Submissions are accepted when the sorted, rounded table matches the gold reference pickle exactly (row-by-row equality after sorting by `Activity_ID`).

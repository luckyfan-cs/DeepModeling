# ScienceBench Task 94

## Overview

- Domain: Computational Chemistry
- Subtask Categories: Molecule Visualization
- Source: deepchem/deepchem
- Expected Output: `polyverse_visualize_molecules_pred.png`
- Output Type: Image

## Task

Visualise the molecule stored in `molecule_ZINC001754572633.pkl` (an RDKit `Mol`) as a graph. Colour carbon atoms orange, oxygen atoms magenta, and nitrogen atoms cyan. Lay out the graph with NetworkX spring layout (seed=10), set node size to 800, and label each atom.

## Dataset

[START Dataset Preview: polyverse_viz]
|-- molecule_ZINC001754572633.pkl
[END Dataset Preview]

## Submission Format

Encode the rendered figure as base64 and save it to `pred_results/polyverse_visualize_molecules_pred.png`. Submit `sample_submission.csv` with columns `file_name` and `image_base64` referencing that PNG.

## Evaluation

The grader compares the decoded image with the gold reference via a GPT-based judge (threshold 60) and falls back to a deterministic similarity check when the judge is unavailable.

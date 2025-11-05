# ScienceBench Task 52

## Overview

- Domain: Computational Chemistry
- Subtask Categories: Feature Engineering, Deep Learning, Molecule Visualization
- Source: deepchem/deepchem
- Output Type: Image

## Task

Train an aquatic toxicity model on the Papyrus Tetrahymena pyriformis dataset, compute atomic contribution scores for the provided test compound, and render a visualization highlighting per-atom effects. Save the visualization to the required PNG output path.

## Dataset

The `aquatic_toxicity/` folder contains:

- `Tetrahymena_pyriformis_OCHEM.sdf` – training molecules with toxicity endpoints.
- `Tetrahymena_pyriformis_OCHEM_test_ex.sdf` – the test molecule for visualization.

## Submission Format

Generate `pred_results/aquatic_toxicity_qsar_vis.png`. If the workflow uses base64 internally, ensure the final image is written to disk with the expected filename.

## Evaluation

Submissions are accepted when the generated visualization achieves at least the reference similarity score (60/100) against the gold figure.

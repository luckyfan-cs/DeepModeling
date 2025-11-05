# ScienceBench Task 102: refractive_index_prediction

## Overview

- **Domain**: Computational Chemistry
- **Subtask Categories**: Deep Learning
- **Source**: ppdebreuck/modnet
- **Output File**: ref_index_predictions_pred.csv
- **Output Type**: Tabular (CSV with predictions)

## Task

Train a MODNet model for predicting the refractive index for materials using the provided training data, then predict refractive index for materials in the test dataset.

## Input/Output

**Input Files**:
- `md_ref_index_train`: Training data in MODData format
- `MP_2018.6`: Test data in MODData format (Materials Project 2018.6 dataset)

**Output Format**:
- Submit predictions as a CSV file
- Required column: `refractive_index`
- Values should be numeric predictions of the refractive index

## Model Requirements

The task expects use of MODNet (Materials Optimal Descriptor Network) with specific architecture:
- 300 input features
- Layer structure: [128, 64, 32, []]
- Activation function: 'elu'

## Submission Format

Submit `sample_submission.csv` with structure:

```csv
id,refractive_index
0,1.523
1,2.145
...
```

## Evaluation

**Metric**: Mean Absolute Error (MAE)
- Lower is better
- Threshold for good performance: MAE < 0.78
- Score normalized where 0 MAE = perfect score

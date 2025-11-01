# ILI Time Series Forecasting

## Task Description

You are solving a machine learning task of time series forecasting using the ILI (Influenza-Like Illness) dataset.

The dataset presented here comprises real-world time series data tracking influenza-like illness statistics. We have split the dataset into train, validation, and test parts.

## Data Description

- **Input**: A sequence of past observations (INPUT_SEQ_LEN=36, INPUT_DIM=7)
- **Output**: Predict the next future sequence (PRED_SEQ_LEN=24, PRED_DIM=7)
- **Evaluation Metrics**: Mean Squared Error (MSE) and Mean Absolute Error (MAE)

The dataset contains 7 features from the CDC's influenza surveillance system:
1. % WEIGHTED ILI
2. % UNWEIGHTED ILI
3. AGE 0-4
4. AGE 5-24
5. ILITOTAL
6. NUM. OF PROVIDERS
7. OT (Other)

## Files

- `train_input.npy` - Training input features (shape: [N_train, 36, 7])
- `train_target.npy` - Training target values (shape: [N_train, 24, 7])
- `test_input.npy` - Test input features (shape: [N_test, 36, 7])
- `sample_submission.npy` - Sample submission in numpy format (shape: [N_test, 24, 7])

## Data Loading

You can load the data using numpy:

```python
import numpy as np

# Load training data
X_train = np.load('train_input.npy')
y_train = np.load('train_target.npy')

# Load test data
X_test = np.load('test_input.npy')

print(f"X_train shape: {X_train.shape}")  # (N_train, 36, 7)
print(f"y_train shape: {y_train.shape}")  # (N_train, 24, 7)
print(f"X_test shape: {X_test.shape}")    # (N_test, 36, 7)
```

## Submission Format

The submission should be a CSV file with the following format:
- Column `id`: Integer index for each test sample (0 to N_test-1)
- Columns `pred_0` to `pred_167`: Flattened predictions (24 timesteps × 7 features = 168 values per sample)

Example CSV structure:
```
id,pred_0,pred_1,pred_2,...,pred_166,pred_167
0,0.5,0.3,0.7,...,0.2,0.4
1,0.6,0.4,0.8,...,0.3,0.5
...
```

Example code to create submission:
```python
import numpy as np
import pandas as pd

# predictions should have shape (N_test, 24, 7)
# Flatten to (N_test, 168)
predictions_flat = predictions.reshape(len(predictions), -1)

# Create DataFrame
submission = pd.DataFrame(predictions_flat,
                         columns=[f'pred_{i}' for i in range(24 * 7)])
submission.insert(0, 'id', range(len(predictions)))

# Save as CSV
submission.to_csv('submission.csv', index=False)
```

## Evaluation

Your predictions will be evaluated using two metrics:
1. **MSE (Mean Squared Error)**: Lower is better
2. **MAE (Mean Absolute Error)**: Lower is better

The primary ranking metric is MSE.

## Goal

Train a time series forecasting model to accurately predict future ILI statistics based on historical observations.

## Notes

- This is a multivariate time series forecasting problem
- Each input sequence covers 36 weeks of data
- You need to predict the next 24 weeks
- All 7 features need to be predicted simultaneously
- The data has been preprocessed and standardized


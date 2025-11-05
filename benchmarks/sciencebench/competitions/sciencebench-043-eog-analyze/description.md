# ScienceBench Task 43: EOG_analyze

## Overview

- **Domain**: Psychology and Cognitive Science
- **Subtask Categories**: Computational Analysis, Data Visualization
- **Source**: neuropsychology/NeuroKit
- **Output File**: EOG_analyze_pred.png
- **Output Type**: Image (PNG)

## Task

Analyze Electrooculography (EOG) signal data to detect and visualize eye blinks.

The analysis involves:
1. Filter the EOG signal to remove noise and trends
2. Run a peak detection algorithm to detect eye blink locations
3. Create epochs around detected blinks
4. Visualize the aligned eye blink patterns

## Input/Output

**Input Files**:
- `eog_100hz.csv`: EOG signal data sampled at 100 Hz

**Output Format**:
- Save the visualization as: `pred_results/EOG_analyze_pred.png`
- Format: PNG image
- Should show aligned eye blink signals with median overlay

## Task Details

Use NeuroKit2 library for biosignal processing:
- `nk.eog_clean()`: Filter the signal to remove noise and trends
- `nk.eog_findpeaks()`: Detect peak locations (eye blinks)
- Create epochs around blinks and visualize patterns

## Submission Format

Submit the generated plot as an image file. The visualization should show:
- Individual eye blink traces (semi-transparent lines)
- Median/average blink pattern (bold line)
- Time-aligned signals showing consistent blink morphology

## Evaluation

**Metric**: Visual Similarity Score (using GPT-4 Vision)
- Compares generated plot with gold standard reference
- Evaluates signal processing accuracy and visualization quality
- Threshold: >= 60/100 for passing

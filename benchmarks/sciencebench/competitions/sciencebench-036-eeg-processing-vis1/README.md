# ScienceBench-036: EEG Processing and Visualization

## Task Overview

**Domain**: Psychology and Cognitive Science  
**Task Type**: Computational Analysis, Data Visualization  
**Output Type**: Image (PNG)  
**Difficulty**: Medium

## Description

Process electroencephalogram (EEG) data and generate a visualization showing the 20-point moving average of EEG frequency band power across four functionally distinct frequency bands.

## Dataset

- **Input**: `eeg_muse_example.csv` - EEG measurements from a Muse headband
- **Size**: ~889 KB
- **Columns**: timestamps, TP9, AF7, AF8, TP10, Right AUX
- **Rows**: ~23,000 measurements

## Task Requirements

1. Load EEG data from CSV
2. Calculate frequency band power for:
   - Delta (0.5-4 Hz): Deep sleep
   - Theta (4-8 Hz): Drowsiness and meditation
   - Alpha (8-13 Hz): Relaxed wakefulness
   - Beta (13-30 Hz): Active thinking and focus
3. Compute 20-point moving average for each band
4. Generate line chart showing all bands over time
5. Save as PNG image

## Evaluation

- **Metric**: Visual Similarity Score
- **Threshold**: >= 60/100
- **Method**: Image comparison using PSNR and correlation

## Tools

- **BioPsyKit**: Python package for biopsychological data analysis
- **NumPy/Pandas**: Data processing
- **Matplotlib/Seaborn**: Visualization

## File Structure

```
注册端 (Registry):
/home/aiops/liufan/projects/DeepModeling/benchmarks/sciencebench/competitions/sciencebench-036-eeg-processing-vis1/
├── config.yaml           # Competition configuration
├── description.md        # Task description
├── grade.py             # Grading function (visual similarity)
├── prepare.py           # Data preparation script
├── leaderboard.csv      # Placeholder leaderboard
├── checksums.yaml       # Data checksums
└── README.md           # This file

数据端 (Data):
/home/aiops/liufan/projects/ScienceAgent-bench/competitions/sciencebench-036-eeg-processing-vis1/
└── prepared/
    ├── public/          # Data visible to agent
    │   ├── eeg_muse_example.csv      # EEG measurements (889KB)
    │   └── sample_submission.png      # Placeholder submission
    └── private/         # Data for grading only
        └── biopsykit_eeg_processing_vis1_gold.png  # Gold standard (114KB)
```

## Usage

```bash
cd /home/aiops/liufan/projects/DeepModeling

python main.py \
  --workflow scientific \
  --benchmark sciencebench \
  --data-dir /home/aiops/liufan/projects/ScienceAgent-bench/competitions \
  --task sciencebench-036-eeg-processing-vis1 \
  --llm-model deepseek-chat
```

## Notes

- This is an **image-based task** (different from CSV-based tasks like Clintox)
- Evaluation uses visual similarity instead of numeric metrics
- Agent must have access to plotting libraries
- BioPsyKit may need to be installed in agent environment

## Status

✅ Competition created  
✅ Data prepared  
✅ Grading function tested  
⏳ Pending agent test run

---

**Created**: 2025-11-06  
**Instance ID**: 36  
**Source**: ScienceAgent-bench

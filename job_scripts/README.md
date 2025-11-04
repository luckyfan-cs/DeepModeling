# Job Scripts - Usage Examples

This directory contains example scripts demonstrating various use cases of the DeepModeling framework.

## 📋 Script Overview

| Script | Description | Use Case |
|--------|-------------|----------|
| `01_mathmodeling_single_task.sh` | Single mathematical modeling problem | Quick test, debugging |
| `02_mathmodeling_batch.sh` | Batch evaluation of math problems | Benchmark evaluation |
| `03_data_science_single_task.sh` | Single Kaggle competition | Data science task |
| `04_data_science_batch.sh` | Multiple ML competitions | Multi-modal evaluation |
| `05_external_storage.sh` | External data storage | Large datasets |
| `06_multi_modal_cv.sh` | Computer vision tasks | Image data |
| `07_multi_modal_timeseries.sh` | Time series forecasting | Temporal data |
| `08_advanced_options.sh` | Advanced configurations | Model comparison |

## 🚀 Quick Start

### Make scripts executable
```bash
chmod +x job_scripts/*.sh
```

### Run an example
```bash
# Mathematical modeling
./job_scripts/01_mathmodeling_single_task.sh

# Data science
./job_scripts/03_data_science_single_task.sh

# Computer vision
./job_scripts/06_multi_modal_cv.sh
```

## 📊 Example 1: Mathematical Modeling (Single Task)

**Script:** `01_mathmodeling_single_task.sh`

Demonstrates solving a single optimization problem from the BWOR dataset.

```bash
./job_scripts/01_mathmodeling_single_task.sh
```

**What it does:**
- Loads a candy factory production optimization problem
- Applies scientific method workflow
- Generates optimal solution using linear programming
- Evaluates against ground truth

## 📈 Example 2: Mathematical Modeling (Batch)

**Script:** `02_mathmodeling_batch.sh`

Runs multiple mathematical modeling problems in batch mode.

```bash
./job_scripts/02_mathmodeling_batch.sh
```

**What it does:**
- Reads task list from `config.yaml`
- Processes multiple problems sequentially
- Aggregates results and metrics
- Generates comprehensive evaluation report

## 🤖 Example 3: Data Science (Single Task)

**Script:** `03_data_science_single_task.sh`

Solves a Kaggle-style competition (Spaceship Titanic).

```bash
./job_scripts/03_data_science_single_task.sh
```

**What it does:**
- Loads tabular competition data
- Performs EDA and feature engineering
- Trains machine learning model
- Generates predictions and submission file

## 🌐 Example 4: Data Science (Batch - Multi-Modal)

**Script:** `04_data_science_batch.sh`

Evaluates multiple competitions across different data modalities.

```bash
./job_scripts/04_data_science_batch.sh
```

**Covered modalities:**
- **Tabular**: Classification, regression
- **Time Series**: Forecasting
- **Computer Vision**: Image classification
- **NLP**: Text classification

## 💾 Example 5: External Data Storage

**Script:** `05_external_storage.sh`

Demonstrates using external storage for large datasets.

```bash
# Set your external storage path
export EXTERNAL_DATA_DIR="/mnt/external_drive/mathmodeling-data"

./job_scripts/05_external_storage.sh
```

**Benefits:**
- Registry (small) stays in project
- Data (large) on external storage
- Shared data across projects
- Cost-optimized storage

## 🖼️ Example 6: Computer Vision

**Script:** `06_multi_modal_cv.sh`

Handles image classification tasks.

```bash
./job_scripts/06_multi_modal_cv.sh
```

**What it does:**
- Automatically loads images (PNG/JPG/TIFF)
- Designs CNN architecture
- Trains image classifier
- Generates predictions

## 📊 Example 7: Time Series Forecasting

**Script:** `07_multi_modal_timeseries.sh`

Processes time series data for forecasting.

```bash
./job_scripts/07_multi_modal_timeseries.sh
```

**What it does:**
- Loads temporal data (CSV/Parquet/HDF5)
- Extracts temporal features
- Handles seasonality and trends
- Generates multi-step forecasts

## ⚙️ Example 8: Advanced Options

**Script:** `08_advanced_options.sh`

Demonstrates advanced configurations and model comparisons.

```bash
./job_scripts/08_advanced_options.sh
```

**Features:**
- Multiple LLM model comparison
- Custom API endpoints
- Environment variables
- Logging and debugging options

## 🔧 Customization

### Modify API Keys

Edit your `.env` file:
```bash
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### Change Data Directory

Edit the script or set environment variable:
```bash
export DATA_DIR="/path/to/your/data"
./job_scripts/01_mathmodeling_single_task.sh
```

### Select Different Tasks

Modify the `TASK` variable in the script:
```bash
# In the script
TASK="your-task-id-here"
```

Or specify via config.yaml for batch processing:
```yaml
mathmodeling_competitions:
  - task-1
  - task-2
  - task-3
```

## 📝 Configuration Files

### config.yaml

Configure tasks for batch processing:

```yaml
# Mathematical Modeling
mathmodeling_competitions:
  - bwor-0
  - industry-5
  - mamo-easy-10-resource-allocation

# Data Science (MLE-Bench)
mle_competitions:
  - spaceship-titanic
  - house-prices-advanced-regression-techniques
  - digit-recognizer
  - nlp-getting-started
```

### .env

Set API keys and endpoints:

```bash
# LLM Provider API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Optional: Custom API endpoints
OPENAI_API_BASE=https://api.openai.com/v1
```

## 📊 Results

All results are saved in `runs/` directory:

```
runs/
├── benchmark_results/
│   └── scientific_on_mathmodeling/
│       ├── summary.json
│       └── detailed_results.csv
│
└── modeling_run_<task>_<id>/
    ├── submission.csv
    ├── logs/
    └── artifacts/
```

## 🎯 Best Practices

1. **Start Small**: Use single task scripts (`01`, `03`) for testing
2. **Test Locally**: Verify with small datasets before large runs
3. **Monitor Costs**: Use `gpt-4o-mini` for development, `gpt-4o` for production
4. **External Storage**: Use for datasets > 1GB
5. **Batch Processing**: Configure in `config.yaml` for multiple tasks
6. **Check Logs**: Review `runs/` for detailed execution traces

## 🔍 Troubleshooting

### Script fails with "Permission denied"
```bash
chmod +x job_scripts/*.sh
```

### "Data directory not found"
```bash
# Check data directory exists
ls -la data/mathmodeling-bench/competitions/

# Or use external storage
export EXTERNAL_DATA_DIR="/path/to/data"
```

### API key errors
```bash
# Verify .env file exists
cat .env

# Ensure keys are set
echo $OPENAI_API_KEY
```

### Task not found
```bash
# List available tasks
python -c "from benchmarks.mathmodelingbench.registry import Registry; r = Registry(); print(r.list_competition_ids())"
```

## 📚 Additional Resources

- [Main README](../README.md) - Framework overview
- [Quick Start Guide](../QUICK_START_SCIENTIFIC.md) - Getting started
- [Documentation](../docs/) - Detailed implementation docs

## 🤝 Contributing

To add new example scripts:

1. Create a new script in `job_scripts/`
2. Follow the naming convention: `XX_description.sh`
3. Add clear comments and echo statements
4. Update this README with the new example
5. Test the script before committing

## 📬 Support

For issues or questions:
- Check [GitHub Issues](https://github.com/your-org/DeepModeling/issues)
- Review [Documentation](../docs/)
- Contact: your-email@example.com

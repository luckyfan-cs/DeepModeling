# Job Scripts - Quick Start Examples

This directory contains example scripts for running different benchmarks in the DeepModeling framework.

## 📋 Available Scripts

| Script | Benchmark | Description | Example Task |
|--------|-----------|-------------|--------------|
| `sciencebench.sh` | ScienceBench | 102 scientific computing tasks | Drug toxicity prediction |
| `mathmodeling.sh` | Mathematical Modeling | 1,291 optimization problems | Linear programming, ODEs |
| `engineeringbench.sh` | Engineering | 102 industrial problems | Process optimization |
| `mlebench.sh` | MLE-Bench | 349 ML competitions | Kaggle-style challenges |

## 🚀 Quick Start

### 1. Make scripts executable
```bash
chmod +x job_scripts/*.sh
```

### 2. Run a benchmark

```bash
# Scientific computing (requires external data)
./job_scripts/sciencebench.sh

# Mathematical modeling
./job_scripts/mathmodeling.sh

# Engineering problems
./job_scripts/engineeringbench.sh

# Machine learning competitions
./job_scripts/mlebench.sh
```

## 📊 Benchmark Details

### 🔬 ScienceBench

**Script:** `sciencebench.sh`

**Domains:**
- Computational Chemistry (20 tasks)
- Geographical Information Science (27 tasks)
- Bioinformatics (27 tasks)
- Psychology and Cognitive Science (28 tasks)

**Usage:**
```bash
python main.py \
  --workflow scientific \
  --benchmark sciencebench \
  --data-dir /path/to/ScienceAgent-bench/competitions \
  --task sciencebench-001-clintox-nn
```

**Requirements:**
- External data directory with prepared datasets
- Metadata file at: `<data-dir>/../benchmark/ScienceAgentBench.csv`

**Example tasks:**
- `sciencebench-001-clintox-nn` - Drug toxicity prediction
- `sciencebench-002-mat-feature-select` - Materials property prediction
- `sciencebench-003-predict-bulk-modulus` - Bulk modulus prediction

---

### 📐 Mathematical Modeling

**Script:** `mathmodeling.sh`

**Categories:**
- BWOR: Basic word optimization problems (82 tasks)
- MAMO-Easy: Elementary math modeling (652 tasks)
- MAMO-Complex: Advanced optimization (211 tasks)
- MAMO-ODE: Differential equations (346 tasks)

**Usage:**
```bash
python main.py \
  --workflow scientific \
  --benchmark mathmodeling \
  --data-dir ./data/mathmodeling-bench \
  --task mamo-complex-105
```

**Example tasks:**
- `bwor-0` - Candy factory production optimization
- `mamo-easy-0` - Resource allocation
- `mamo-complex-105` - Multi-objective optimization
- `mamo-ode-0` - Population dynamics modeling

---

### ⚙️ Engineering Bench

**Script:** `engineeringbench.sh`

**Focus Areas:**
- Industrial operations research
- Process design and optimization
- Systems engineering

**Usage:**
```bash
python main.py \
  --workflow scientific \
  --benchmark engineeringbench \
  --data-dir ./benchmarks/engineeringbench/competitions \
  --task industry-0
```

**Example tasks:**
- `industry-0` to `industry-99` - Various industrial problems

---

### 🤖 MLE-Bench (Machine Learning)

**Script:** `mlebench.sh`

**Modalities:**
- Tabular data (classification, regression)
- Computer vision (image classification)
- Natural language processing (text classification)
- Time series (forecasting)

**Usage:**
```bash
python main.py \
  --workflow scientific \
  --benchmark mle \
  --data-dir ./benchmarks/mlebench/competitions \
  --task 3d-object-detection-for-autonomous-vehicles
```

**Example competitions:**
- `spaceship-titanic` - Tabular classification
- `digit-recognizer` - Image classification
- `nlp-getting-started` - Text classification

---

## 🔧 Customization

### Change the Data Directory

Edit the script or provide command-line argument:

```bash
# Option 1: Edit the script
vim job_scripts/sciencebench.sh
# Change: --data-dir /path/to/your/data

# Option 2: Run with custom path
python main.py \
  --workflow scientific \
  --benchmark sciencebench \
  --data-dir /custom/path/to/competitions \
  --task your-task-id
```

### Run Different Tasks

Modify the `--task` parameter:

```bash
python main.py \
  --workflow scientific \
  --benchmark mathmodeling \
  --data-dir ./data/mathmodeling-bench \
  --task bwor-10  # Change this
```

### Run Multiple Tasks

Pass multiple task IDs:

```bash
python main.py \
  --workflow scientific \
  --benchmark mathmodeling \
  --data-dir ./data/mathmodeling-bench \
  --task bwor-0 bwor-1 bwor-2
```

### Change LLM Model

Use `--llm-model` parameter:

```bash
python main.py \
  --workflow scientific \
  --benchmark sciencebench \
  --data-dir /path/to/data \
  --task sciencebench-001-clintox-nn \
  --llm-model gpt-4o  # or claude-3-5-sonnet-20241022
```

## 📝 Configuration

### Environment Variables (.env)

Set API keys:

```bash
# .env file
LLM_MODEL=gpt-4o-mini
LLM_TEMPERATURE=0.7
API_KEY=your-api-key-here
API_BASE=https://api.openai.com/v1
```

### Batch Processing (config.yaml)

Configure multiple tasks:

```yaml
mathmodeling_competitions:
  - bwor-0
  - bwor-1
  - mamo-easy-0
  - mamo-complex-105

engineering_competitions:
  - industry-0
  - industry-1
  - industry-10
```

## 📊 Results

All results are saved in the `runs/` directory:

```
runs/
├── benchmark_results/
│   └── scientific_on_sciencebench/
│       ├── results.csv           # Per-competition scores
│       └── summary.json          # Aggregated metrics
│
└── modeling_run_<task>_<uuid>/
    ├── submission.csv            # Model predictions
    ├── workspace/                # Working directory
    ├── logs/                     # Execution logs
    └── metadata.json             # Run metadata
```

## ⚠️ Important Notes

### ScienceBench Data Requirements

**The `sciencebench.sh` script requires:**

1. **External data directory** with prepared datasets
2. **Metadata file** at: `<data-dir>/../benchmark/ScienceAgentBench.csv`

**Example structure:**
```
/path/to/ScienceAgent-bench/
├── benchmark/
│   └── ScienceAgentBench.csv          # Required metadata
└── competitions/                       # Pass this as --data-dir
    ├── sciencebench-001-clintox-nn/
    │   └── prepared/
    │       ├── public/                # Input data
    │       └── private/               # Ground truth
    ├── sciencebench-002-mat-feature-select/
    └── ...
```

**Usage:**
```bash
python main.py \
  --workflow scientific \
  --benchmark sciencebench \
  --data-dir /path/to/ScienceAgent-bench/competitions \
  --task sciencebench-001-clintox-nn
```

## 🔍 Troubleshooting

### "Permission denied"
```bash
chmod +x job_scripts/*.sh
```

### "data_dir is required"
```bash
# Provide --data-dir argument
python main.py --workflow scientific --benchmark sciencebench \
  --data-dir /path/to/data --task your-task
```

### "Metadata file not found"

For ScienceBench, ensure metadata exists at:
```bash
ls <data-dir>/../benchmark/ScienceAgentBench.csv
```

### API key errors
```bash
# Check .env file
cat .env

# Verify environment variables
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('API_KEY'))"
```

## 🎯 Best Practices

1. **Start with single tasks** - Test with one task before batch processing
2. **Check data paths** - Ensure `--data-dir` points to the correct directory
3. **Monitor costs** - Use `gpt-4o-mini` for testing, upgrade for production
4. **Review logs** - Check `runs/` directory for detailed execution traces
5. **Use absolute paths** - Prefer absolute paths for `--data-dir` to avoid confusion

## 📚 Additional Resources

- [Main README](../README.md) - Framework overview
- [Quick Start Guide](../QUICK_START_SCIENTIFIC.md) - Detailed getting started
- [Documentation](../docs/) - Implementation details

## 📬 Support

For issues or questions, please check the main repository documentation.

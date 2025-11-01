# DeepModeling - A Unified LLM Agent Framework for Scientific Discovery Tasks

A comprehensive LLM Agent framework designed to tackle scientific discovery tasks, with a focus on data science, engineering, and mathematical modeling challenges.

## Overview

This framework integrates various components to facilitate the use of Large Language Models (LLMs) in solving complex scientific problems. It provides a structured approach to define tasks, manage datasets, and evaluate model performance.
## Quick Start

### 1. Setup Environment

```bash
git clone <repository_url>
cd DeepModeling
python -m venv deepmodeling-env
source deepmodeling-env/bin/activate  # On Windows: deepmodeling-env\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

Create a `.env` file with your API credentials:

```bash
cp .env.example .env
# Edit .env and add your API keys
```

### 4. Run Benchmark

Run a single task:

```bash
python main.py --workflow scientific --benchmark mathmodeling \
  --data-dir ./data/mathmodeling-bench \
  --task mathmodeling-1-feed-optimization
```

Run all configured tasks:

```bash
python main.py --workflow scientific --benchmark mathmodeling \
  --data-dir ./data/mathmodeling-bench
```

## Dataset Statistics

The framework includes **1,394 mathematical modeling competitions** from 5 major datasets:

| Dataset | Competitions | Description |
|---------|--------------|-------------|
| **BWOR** | 82 | Business and Operations Research problems |
| **IndustryOR** | 100 | Industrial Operations Research tasks |
| **MaMo Easy LP** | 652 | Easy linear programming problems |
| **MaMo Complex LP** | 211 | Complex linear programming tasks |
| **MaMo ODE** | 346 | Ordinary Differential Equation problems |
| **Original** | 3 | Hand-crafted benchmark tasks |
| **Total** | **1,394** | |

## Directory Structure

```
DeepModeling/
├── benchmarks/                 # All benchmark data
│   ├── mathmodelingbench/      # Registry (metadata)
│   │   └── competitions/
│   │       ├── bwor-0-*/       # BWOR dataset competitions
│   │       ├── industry-0-*/   # IndustryOR competitions
│   │       ├── mamo-easy-*/    # Easy LP competitions
│   │       ├── mamo-complex-*/ # Complex LP competitions
│   │       ├── mamo-ode-*/     # ODE competitions
│   │       └── mathmodeling-*/ # Original competitions
│   │
│   └── mathmodeling-bench/     # Data directory
│       └── competitions/
│           └── [competition-id]/
│               ├── raw/
│               │   └── problem.json           # Original problem with answer
│               └── prepared/
│                   ├── public/
│                   │   ├── problem.json       # Problem WITHOUT answer (for LLM)
│                   │   └── sample_submission.csv
│                   └── private/
│                       └── answer.csv         # Ground truth
│
├── modeling/                   # Core framework
├── examples/                   # Examples and tools
│   └── mathmodleing-to-mlebech/
│       ├── convert_mathmodeling.py   # Conversion script
│       └── README.md
│
├── docs/                       # Detailed documentation
│   ├── README.md               # Documentation index
│   ├── SCIENTIFIC_WORKFLOW_*.md
│   └── IMPLEMENTATION_*.md
│
├── batch_convert_datasets.py  # Batch processing tool
├── config.yaml                 # Competition configuration
├── main.py                     # Entry point
└── QUICK_START_SCIENTIFIC.md  # Quick start guide
```

### Data Storage Architecture

The framework uses a **registry-data separation** design to support flexible data storage:

**Registry (Small, ~20KB per competition)**
- Location: `benchmarks/mathmodelingbench/competitions/` (in project)
- Contains: config.yaml, grade.py, prepare.py, description.md
- Purpose: Metadata and evaluation logic
- Size: Can stay in project repository (~30MB total for 1,394 competitions)

**Data (Large, can be GB+)**
- Location: User-specified via `--data-dir` parameter
- Contains: raw/, prepared/public/, prepared/private/ directories
- Purpose: Actual problem data and ground truth
- Size: Can be stored on external storage if needed

**Usage Examples:**
```bash
# Data in project directory (default)
python main.py --workflow scientific --benchmark mathmodeling \
  --data-dir ./data/mathmodeling-bench \
  --task bwor-11-noindent-textbf-4

# Data on external storage (for large datasets)
python main.py --workflow scientific --benchmark mathmodeling \
  --data-dir /mnt/large_storage/mathmodeling-data \
  --task bwor-11-noindent-textbf-4
```

## Key Features

### 🔒 Ground Truth Protection
- **Public data** (given to LLM): Problem statement WITHOUT answers
- **Private data** (for grading): Ground truth answers
- **Raw data**: Complete original problem for reference

### 🎯 Automatic Tag Detection
The framework automatically detects submission tags based on problem content:
- `@profit[value]` - For profit maximization problems
- `@cost[value]` - For cost minimization problems
- `@value[value]` - For general numeric solutions

### ✅ Standardized Evaluation
- Exact match checker with tolerance (±1e-2)
- Consistent grading across all competitions
- CSV-based submission format

## Adding New Datasets

Use the batch conversion tool to add new datasets:

```bash
python batch_convert_datasets.py --dataset <dataset_file>
```

Or convert manually:

```bash
python examples/mathmodleing-to-mlebech/convert_mathmodeling.py \
  --dataset-file /path/to/dataset.json \
  --registry-root ./benchmarks/mathmodelingbench/competitions \
  --data-root ./data/mathmodeling-bench/competitions \
  --competition-prefix my-dataset \
  --default-tag value \
  --start-index 0
```

## Configuration

Edit `config.yaml` to select which competitions to run:

```yaml
mathmodeling_competitions:
  - bwor-0-candy-factory
  - industry-5-production-scheduling
  - mamo-easy-10-resource-allocation
  # ... add more competitions
```

## Examples

See detailed examples in:
- [QUICK_START_SCIENTIFIC.md](QUICK_START_SCIENTIFIC.md) - Scientific workflow quick start
- [examples/mathmodleing-to-mlebech/README.md](examples/mathmodleing-to-mlebech/README.md) - Dataset conversion guide

## Documentation

Detailed implementation documentation and design decisions:
- [docs/](docs/) - Implementation guides, bug fixes, and refactoring documentation
- [docs/SCIENTIFIC_WORKFLOW_IMPLEMENTATION.md](docs/SCIENTIFIC_WORKFLOW_IMPLEMENTATION.md) - Scientific workflow details
- [docs/ADAPTIVE_ITERATIONS_IMPLEMENTATION.md](docs/ADAPTIVE_ITERATIONS_IMPLEMENTATION.md) - Adaptive iterations guide

## Citation

If you use this framework in your research, please cite:

```bibtex
@software{deepmodeling2025,
  title={DeepModeling: Mathematical Modeling Benchmark Framework},
  author={Your Team},
  year={2025},
  url={https://github.com/your-repo/DeepModeling}
}
```

## License

[Add your license here]

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation in `/docs`

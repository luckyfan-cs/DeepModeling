<a name="readme-top"></a>

<div align="center">
  <h1 align="center">DeepModeling: Agentic LLM for Autonomous Data Science & Scientific Discovery</h1>
</div>

<div align="center">
  <a href="#"><img src="https://img.shields.io/badge/Python-3.11+-blue.svg?logo=python&logoColor=white" alt="Python"></a>
  <a href="#"><img src="https://img.shields.io/badge/Framework-Agentic%20LLM-orange.svg" alt="Framework"></a>
  <a href="#"><img src="https://img.shields.io/badge/Benchmarks-1,394%2B%20Problems-green.svg" alt="Benchmark"></a>
  <a href="#quick-start"><img src="https://img.shields.io/badge/Get%20Started-Quick%20Start-red.svg" alt="Quick Start"></a>
</div>

---

**DeepModeling** is an agentic LLM framework for **autonomous data science, scientific discovery, and mathematical modeling**. It autonomously solves complex problems across multiple domains:

- 🎯 **Full Autonomy**: Complete end-to-end automation from problem analysis to solution
- 🔄 **Iterative Discovery**: Self-correcting workflow from hypothesis to validated conclusions
- 🧠 **Scientific Reasoning**: Structured XML-tag-based reasoning following scientific method
- 📊 **Comprehensive Benchmarks**: 1,394+ problems across data science, mathematical modeling, and operations research
- 🎨 **Multi-Modal Support**: Handles any data modality (images, time series, tabular, text) and format (CSV, JSON, Parquet, HDF5, etc.)
- 🚀 **Production Ready**: Flexible data storage, external storage support, extensible architecture

<span id='table-of-contents'/>

## 📑 Table of Contents

* <a href='#news'>🔥 News</a>
* <a href='#key-features'>✨ Key Features</a>
* <a href='#architecture'>🏗️ Architecture</a>
* <a href='#quick-start'>⚡ Quick Start</a>
  * <a href='#installation'>Installation</a>
  * <a href='#running-benchmarks'>Running Benchmarks</a>
* <a href='#benchmarks'>📊 Benchmarks</a>
* <a href='#data-storage'>💾 Data Storage Architecture</a>
* <a href='#workflow'>🔬 Scientific Workflow</a>
* <a href='#documentation'>📖 Documentation</a>
* <a href='#citation'>🌟 Citation</a>

<span id='news'/>

## 🔥 News

<div class="scrollable">
  <ul>
    <li><strong>[2025.11]</strong>: 🎨 <b>Multi-Modal Data Support</b> - Full support for any data modality (images, time series, tabular, text) and format (CSV, JSON, Parquet, HDF5, images, etc.)!</li>
    <li><strong>[2025.11]</strong>: 🎊 <b>MLE-Bench Integration</b> - Full support for Kaggle-style data science competitions and machine learning tasks!</li>
    <li><strong>[2025.11]</strong>: 🎉 <b>Registry-Data Separation Architecture</b> - Supports external data storage for large-scale datasets!</li>
    <li><strong>[2025.11]</strong>: 📊 <b>1,394 Mathematical Modeling Problems</b> - Comprehensive benchmark suite across 5 major domains!</li>
    <li><strong>[2025.11]</strong>: 🔬 <b>Scientific Workflow</b> - Autonomous scientific discovery using XML-structured reasoning!</li>
    <li><strong>[2025.11]</strong>: 🚀 <b>DeepModeling Framework Release</b> - Complete framework spanning data science, scientific discovery, and mathematical modeling!</li>
  </ul>
</div>

<span id='key-features'/>

## ✨ Key Features

### 🔬 Scientific Method Workflow

The framework implements a complete scientific method cycle with structured XML-based reasoning:

```
Phenomenon → Hypothesis → Model → Experiment → Observation → Inference → Conclusion
     ↑                                                              ↓
     └──────────────────────────────────────────────────────────────┘
                        (Iterates until solved)
```

**Core Capabilities:**
- 📚 **Phenomenon Analysis**: Systematically analyzes problem statements and data
- 💡 **Hypothesis Generation**: Formulates testable hypotheses based on observations
- 🧪 **Model Development**: Designs and implements mathematical/computational models
- 🔬 **Experimentation**: Executes code and collects empirical results
- 📊 **Observation Processing**: Interprets outputs and identifies patterns
- 🎯 **Inference & Conclusion**: Draws conclusions and validates against ground truth

### 🔒 Ground Truth Protection

- **Public Data** (given to LLM): Problem statement WITHOUT answers
- **Private Data** (for grading): Ground truth answers stored separately
- **Raw Data**: Complete original problem for reference
- **Answer Sanitization**: Automatic removal of answers from public problem statements

### 🎨 Multi-Modal Data Support

The framework handles **any data modality** and **any file format**:

**Supported Data Modalities:**
- 📊 **Tabular Data**: Structured data with rows and columns (CSV, Excel, Parquet, Feather, HDF5)
- 📈 **Time Series**: Sequential temporal data (stock prices, sensor readings, weather data)
- 🖼️ **Images**: Computer vision tasks (PNG, JPG, TIFF, medical imaging formats)
- 📝 **Text**: Natural language processing (TXT, JSON, XML, Markdown)
- 🎵 **Audio**: Sound and speech data (WAV, MP3, FLAC)
- 🎥 **Video**: Sequential visual data (MP4, AVI)
- 🔢 **Numeric Arrays**: Multi-dimensional data (NumPy arrays, tensors)

**Supported File Formats:**
- **Data Formats**: CSV, JSON, Parquet, Feather, HDF5, Pickle, Excel (XLSX, XLS)
- **Image Formats**: PNG, JPG, JPEG, TIFF, BMP, GIF, SVG
- **Scientific Formats**: NetCDF, MATLAB (.mat), R data (.rds)
- **Database Formats**: SQLite, PostgreSQL dumps, MongoDB exports
- **Compressed Formats**: ZIP, TAR, GZ, BZ2

**Automatic Format Detection:**
The framework automatically detects and handles different data formats, preprocessing pipelines, and modality-specific operations without manual configuration.

### 📊 Comprehensive Benchmark Suite

**Mathematical Modeling Benchmarks (1,394 problems):**

| Dataset | Problems | Description |
|---------|----------|-------------|
| **BWOR** | 82 | Business and Operations Research problems |
| **IndustryOR** | 100 | Industrial Operations Research tasks |
| **MaMo Easy LP** | 652 | Easy linear programming problems |
| **MaMo Complex LP** | 211 | Complex linear programming tasks |
| **MaMo ODE** | 346 | Ordinary Differential Equation problems |
| **Original** | 3 | Hand-crafted benchmark tasks |
| **Subtotal** | **1,394** | Comprehensive mathematical modeling suite |

**Data Science Benchmarks (MLE-Bench):**

| Category | Description | Tasks | Data Modalities |
|----------|-------------|-------|-----------------|
| **Kaggle Competitions** | Real-world machine learning challenges | Classification, Regression, Time Series | Tabular, Images, Text, Time Series |
| **Data Analysis** | Exploratory data analysis and visualization | Statistical analysis, Feature engineering | All modalities supported |
| **Model Development** | End-to-end ML pipeline creation | Training, Validation, Prediction | Multi-modal pipelines |
| **Computer Vision** | Image and video processing | Object detection, Segmentation, Classification | Images, Video |
| **Natural Language** | Text understanding and generation | Text classification, Sentiment, NER | Text, Documents |
| **Time Series** | Temporal pattern recognition | Forecasting, Anomaly detection | Sequential data |
| **Evaluation** | Automated scoring against ground truth | Accuracy, F1, RMSE, AUC, IoU, BLEU | Modality-specific metrics |

### 🎯 Automatic Evaluation

The framework automatically detects submission tags and evaluates solutions:
- `@profit[value]` - For profit maximization problems
- `@cost[value]` - For cost minimization problems
- `@value[value]` - For general numeric solutions

**Evaluation Features:**
- Exact match checker with tolerance (±1e-2)
- Consistent grading across all competitions
- CSV-based submission format
- Automated metrics and reporting

<span id='architecture'/>

## 🏗️ Architecture

```
DeepModeling/
├── benchmarks/                 # Registry (metadata, ~30MB)
│   ├── mathmodelingbench/      # Mathematical Modeling (1,394 competitions)
│   │   └── competitions/
│   │       ├── bwor-*/         # BWOR (82 competitions)
│   │       ├── industry-*/     # IndustryOR (100 competitions)
│   │       ├── mamo-easy-*/    # Easy LP (652 competitions)
│   │       ├── mamo-complex-*/ # Complex LP (211 competitions)
│   │       └── mamo-ode-*/     # ODE (346 competitions)
│   │
│   └── mlebench/               # Data Science Competitions
│       └── competitions/
│           ├── [competition-id]/
│           │   ├── description.md        # Problem statement
│           │   ├── prepare.py           # Data preparation
│           │   ├── grade.py             # Scoring function
│           │   └── metadata.json        # Competition config
│
├── data/                       # Actual data (can be external)
│   ├── mathmodeling-bench/     # Mathematical modeling data
│   │   └── competitions/
│   │       └── [competition-id]/
│   │           ├── raw/
│   │           │   └── problem.json           # Original with answer
│   │           └── prepared/
│   │               ├── public/
│   │               │   ├── problem.json       # WITHOUT answer (for LLM)
│   │               │   └── sample_submission.csv
│   │               └── private/
│   │                   └── answer.csv         # Ground truth
│   │
│   └── mlebench/               # Data science competition data
│       └── competitions/
│           └── [competition-id]/
│               ├── raw/                # Original Kaggle data
│               └── prepared/
│                   ├── public/         # Train/test data for LLM
│                   │   ├── train.csv
│                   │   ├── test.csv
│                   │   └── sample_submission.csv
│                   └── private/        # Ground truth labels
│                       └── solution.csv
│
├── modeling/                   # Core framework
│   ├── workflows/              # Scientific workflow
│   ├── services/               # LLM, Sandbox, Workspace
│   ├── operators/              # Code generation, execution
│   └── benchmark/              # Benchmark integration
│       ├── mathmodeling.py    # Mathematical modeling benchmark
│       └── mle.py             # MLE-Bench integration
│
├── examples/                   # Tools and examples
├── docs/                       # Documentation (14 files)
├── main.py                     # Entry point
└── config.yaml                 # Competition configuration
```

<span id='quick-start'/>

## ⚡ Quick Start

<span id='installation'/>

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/DeepModeling.git
cd DeepModeling

# Create and activate virtual environment
python -m venv deepmodeling-env
source deepmodeling-env/bin/activate  # On Windows: deepmodeling-env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### API Keys Setup

Create a `.env` file with your API credentials:

```bash
cp .env.example .env
# Edit .env and add your API keys
```

Example `.env` configuration:

```bash
# LLM Provider Configuration
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Optional: Custom API endpoints
OPENAI_API_BASE=https://api.openai.com/v1
```

<span id='running-benchmarks'/>

### Running Benchmarks

**Mathematical Modeling Tasks:**

```bash
# Single task (Quick Test)
python main.py --workflow scientific --benchmark mathmodeling \
  --data-dir ./data/mathmodeling-bench \
  --llm-model gpt-4o-mini \
  --task bwor-0-a-candy-factory-uses-raw-materials-a-b-and-c-to-produce-three-different-b

# Multiple tasks (Batch Evaluation)
python main.py --workflow scientific --benchmark mathmodeling \
  --data-dir ./data/mathmodeling-bench \
  --llm-model gpt-4o-mini
```

**Data Science Tasks (MLE-Bench):**

```bash
# Single Kaggle-style competition
python main.py --workflow scientific --benchmark mle \
  --data-dir ./data/mlebench \
  --llm-model gpt-4o-mini \
  --task spaceship-titanic

# Multiple data science tasks
python main.py --workflow scientific --benchmark mle \
  --data-dir ./data/mlebench \
  --llm-model gpt-4o-mini
```

**External Data Storage (for large datasets):**

```bash
# Mathematical modeling on external storage
python main.py --workflow scientific --benchmark mathmodeling \
  --data-dir /mnt/external_drive/mathmodeling-data \
  --llm-model gpt-4o-mini \
  --task bwor-11-noindent-textbf-4

# Data science on external storage
python main.py --workflow scientific --benchmark mle \
  --data-dir /mnt/external_drive/mlebench-data \
  --llm-model gpt-4o-mini \
  --task house-prices-advanced-regression-techniques
```

<span id='benchmarks'/>

## 📊 Benchmarks

### Dataset Statistics

The framework provides comprehensive benchmarks across **two major domains**:

**1. Mathematical Modeling (1,394 problems)**

Covering optimization, operations research, and differential equations:

- **Linear Programming**: Resource allocation, production optimization, blending problems
- **Operations Research**: Scheduling, assignment, transportation problems
- **Differential Equations**: Dynamic systems, population models, physics simulations
- **Business Analytics**: Profit maximization, cost minimization, supply chain

**2. Data Science (MLE-Bench)**

Kaggle-style machine learning competitions across **all data modalities**:

- **Supervised Learning**: Classification, regression, ranking tasks (tabular, images, text)
- **Time Series**: Forecasting, sequence prediction, anomaly detection (sensor data, stock prices, weather)
- **Computer Vision**: Image classification, object detection, segmentation (PNG, JPG, DICOM)
- **Natural Language Processing**: Text classification, sentiment analysis, named entity recognition
- **Multi-Modal Learning**: Combined image-text, audio-visual tasks
- **Feature Engineering**: Automatic preprocessing for any data format
- **Model Selection**: Hyperparameter tuning, ensemble methods across modalities

### Problem Format

**Mathematical Modeling Problems:**

```json
{
  "id": "competition-id",
  "en_question": "English problem statement...",
  "cn_question": "中文问题描述...",
  "difficulty": "Medium"
}
```

**Submission Format:**
```csv
id,answer
0,@profit[5450]
```

**Data Science Problems (MLE-Bench):**

Each competition provides task-specific data in appropriate formats:

**Tabular Data Tasks:**
- **train.csv**: Training data with features and labels
- **test.csv**: Test data with features only
- **sample_submission.csv**: Expected submission format
- **description.md**: Problem statement and evaluation metric

**Computer Vision Tasks:**
- **train/**: Directory with training images (PNG, JPG, etc.)
- **test/**: Directory with test images
- **train_labels.csv**: Image IDs and labels
- **sample_submission.csv**: Expected prediction format

**Time Series Tasks:**
- **train.csv** or **train.parquet**: Historical time series data
- **test.csv**: Future timestamps to predict
- **sample_submission.csv**: Forecast submission format

**NLP Tasks:**
- **train.json** or **train.csv**: Text data with labels
- **test.json**: Text samples for prediction
- **sample_submission.csv**: Text classification results

**Multi-Modal Tasks:**
- **images/**: Image directory
- **text_data.csv**: Associated text features
- **metadata.json**: Additional context
- **sample_submission.csv**: Multi-modal predictions

**Submission Format (varies by modality):**
```csv
# Tabular/Classification
id,prediction
1,0.85
2,0.32

# Computer Vision (multi-class)
image_id,class_0,class_1,class_2
img_001,0.1,0.7,0.2

# Time Series (forecast)
timestamp,value
2024-01-01,123.45
2024-01-02,124.67
```

### Adding Custom Datasets

Use the batch conversion tool:

```bash
python batch_convert_datasets.py \
  --dataset-file /path/to/your/dataset.json \
  --registry-root ./benchmarks/mathmodelingbench/competitions \
  --data-root ./data/mathmodeling-bench/competitions \
  --competition-prefix my-dataset
```

<span id='data-storage'/>

## 💾 Data Storage Architecture

The framework uses a **registry-data separation** design for flexible storage:

### Registry (Small, ~20KB per competition)
- **Location**: `benchmarks/mathmodelingbench/competitions/` (in project)
- **Contents**: config.yaml, grade.py, prepare.py, description.md
- **Purpose**: Metadata and evaluation logic
- **Size**: ~30MB total (can stay in Git repository)

### Data (Large, can be GB+)
- **Location**: User-specified via `--data-dir` parameter
- **Contents**: raw/, prepared/public/, prepared/private/ directories
- **Purpose**: Actual problem data and ground truth
- **Size**: Can be stored on external storage (network drives, cloud storage, etc.)

### Benefits

✅ **Flexible Storage**: Data can be anywhere (local, external, network, cloud)
✅ **Lightweight Repository**: Git repo only contains ~30MB of registry files
✅ **Shared Data**: Multiple projects can share the same data directory
✅ **CI/CD Friendly**: No need to download large datasets for testing
✅ **Cost Optimization**: Large data on cheaper storage, registry on SSD

<span id='workflow'/>

## 🔬 Scientific Workflow

The framework implements a rigorous scientific method with XML-structured reasoning across **both mathematical modeling and data science tasks**:

### Example 1: Mathematical Modeling

1. **📚 Phenomenon Analysis**
   ```xml
   <Phenomenon>
   Analyzing the candy production optimization problem...
   - Three raw materials: A, B, C
   - Three candy brands: X, Y, Z
   - Constraints: composition ratios, monthly limits
   - Objective: Maximize profit
   </Phenomenon>
   ```

2. **💡 Hypothesis Formulation**
   ```xml
   <Hypothesis>
   This is a linear programming problem. We can formulate:
   - Decision variables: kg of each candy brand
   - Objective function: Revenue - Cost
   - Constraints: Material limits, composition requirements
   </Hypothesis>
   ```

3. **🧪 Model Development**
   ```xml
   <Model>
   Mathematical formulation:
   max: 3.40*X + 2.85*Y + 2.25*Z - (material costs)
   s.t.: composition constraints, material limits
   </Model>
   ```

4. **🔬 Experimentation**
   ```xml
   <Experiment>
   Implementing solution using PuLP/SciPy...
   [Code generation and execution]
   </Experiment>
   ```

5. **📊 Observation & Analysis**
   ```xml
   <Observation>
   Solution found: X=2000kg, Y=1500kg, Z=800kg
   Profit: $5,450
   All constraints satisfied
   </Observation>
   ```

6. **🎯 Conclusion**
   ```xml
   <Conclusion>
   Optimal solution achieved. Submitting answer: @profit[5450]
   </Conclusion>
   ```

### Example 2: Data Science (Kaggle Competition)

1. **📚 Phenomenon Analysis**
   ```xml
   <Phenomenon>
   Analyzing the Titanic survival prediction task...
   - Training data: 891 passengers with features and survival labels
   - Test data: 418 passengers, need to predict survival
   - Features: Age, Sex, Passenger Class, Fare, etc.
   - Objective: Maximize prediction accuracy
   </Phenomenon>
   ```

2. **💡 Hypothesis Formulation**
   ```xml
   <Hypothesis>
   This is a binary classification problem. Key insights:
   - Survival likely correlated with passenger class and gender
   - Age and fare may indicate socioeconomic status
   - Missing values in Age need imputation
   - Can use ensemble methods (Random Forest, XGBoost)
   </Hypothesis>
   ```

3. **🧪 Model Development**
   ```xml
   <Model>
   Pipeline design:
   1. Data preprocessing: handle missing values, encode categoricals
   2. Feature engineering: create family_size, title from name
   3. Model: Random Forest Classifier with cross-validation
   4. Hyperparameter tuning: GridSearchCV
   </Model>
   ```

4. **🔬 Experimentation**
   ```xml
   <Experiment>
   Implementing ML pipeline using scikit-learn...
   - Preprocessing: SimpleImputer, OneHotEncoder
   - Model: RandomForestClassifier(n_estimators=100)
   - Validation: 5-fold cross-validation
   [Code generation and execution]
   </Experiment>
   ```

5. **📊 Observation & Analysis**
   ```xml
   <Observation>
   Cross-validation accuracy: 82.3%
   Feature importance: Sex (0.31), Pclass (0.24), Fare (0.18)
   Predictions generated for 418 test samples
   Submission file created successfully
   </Observation>
   ```

6. **🎯 Conclusion**
   ```xml
   <Conclusion>
   Model achieved good validation performance.
   Submitting predictions to competition.
   </Conclusion>
   ```

### Adaptive Iterations

The workflow automatically iterates based on:
- ❌ **Code Errors**: Fixes syntax, logic, or runtime errors
- ⚠️ **Failed Tests**: Adjusts model based on test failures
- 📉 **Poor Results**: Refines approach if solution is suboptimal
- ✅ **Success**: Terminates when valid solution is found

<span id='documentation'/>

## 📖 Documentation

Detailed documentation is available in the [`docs/`](docs/) directory:

- **[QUICK_START_SCIENTIFIC.md](QUICK_START_SCIENTIFIC.md)** - Scientific workflow quick start
- **[docs/SCIENTIFIC_WORKFLOW_IMPLEMENTATION.md](docs/SCIENTIFIC_WORKFLOW_IMPLEMENTATION.md)** - Implementation details
- **[docs/ADAPTIVE_ITERATIONS_IMPLEMENTATION.md](docs/ADAPTIVE_ITERATIONS_IMPLEMENTATION.md)** - Adaptive iterations guide
- **[docs/README.md](docs/README.md)** - Documentation index

### Configuration Guide

Edit `config.yaml` to configure benchmarks:

```yaml
# Mathematical Modeling Benchmarks
mathmodeling_competitions:
  - bwor-0-a-candy-factory-uses-raw-materials-a-b-and-c-to-produce-three-different-b
  - industry-5-production-scheduling
  - mamo-easy-10-resource-allocation
  # Add more competitions...

# Data Science Benchmarks (MLE-Bench)
mle_competitions:
  - spaceship-titanic
  - house-prices-advanced-regression-techniques
  - digit-recognizer
  - nlp-getting-started
  # Add more Kaggle competitions...
```

### Advanced Usage

```python
from modeling.config import ModelingConfig, LLMConfig, WorkflowConfig
from modeling.workflows.factory import ScientificWorkflowFactory

# Configure workflow
config = ModelingConfig(
    llm=LLMConfig(provider='openai', model='gpt-4o-mini'),
    workflow=WorkflowConfig(name='scientific'),
    # ... other config
)

# Create workflow
factory = ScientificWorkflowFactory()
workflow = factory.create_workflow(config)

# Execute
result = await workflow.solve(task)
```

## 🤝 Contributing

We welcome contributions! Areas for improvement:

- 📊 **New Benchmarks**: Add more domains (data science, chemistry, physics, biology)
- 🎨 **Multi-Modal Datasets**: Add benchmarks with images, time series, audio, video data
- 🔬 **Workflow Extensions**: Implement new discovery methods and ML techniques
- 🛠️ **Tools Integration**: Connect external tools (MATLAB, Mathematica, scikit-learn extensions)
- 📝 **Documentation**: Improve guides and examples
- 🐛 **Bug Fixes**: Report and fix issues
- 🏆 **Kaggle Datasets**: Convert more Kaggle competitions to MLE-Bench format (especially multi-modal ones)

**How to Contribute:**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

<span id='citation'/>

## 🌟 Citation

If you use DeepModeling in your research, please cite:

```bibtex
@software{deepmodeling2025,
  title={DeepModeling: Agentic LLM for Autonomous Data Science, Scientific Discovery, and Mathematical Modeling},
  author={DeepModeling Team},
  year={2025},
  url={https://github.com/your-org/DeepModeling}
}
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- **Training Frameworks**: Integration with various LLM providers
- **Benchmark Sources**: BWOR, IndustryOR, MaMo datasets
- **Community**: Contributors and users providing feedback

## 📬 Contact

For questions and support:
- 📧 Email: your-email@example.com
- 💬 Issues: [GitHub Issues](https://github.com/your-org/DeepModeling/issues)
- 📖 Docs: [Documentation](docs/)

---

<div align="center">
  <p>Made with ❤️ by the DeepModeling Team</p>
  <p>⭐ Star us on GitHub if you find this project helpful!</p>
</div>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

# Scientific Discovery Workflow - Quick Start

## 🎯 What is it?

A workflow that applies the **scientific method** using **strict XML tag format** to solve problems in:
- Data Science
- Scientific Discovery
- Mathematical Modeling
- Engineering

## 🔄 How it works

```
Phenomenon → Hypothesis → Model → Experiment → Observation → Inference → Conclusion
     ↑                                                              ↓
     └──────────────────────────────────────────────────────────────┘
                        (Iterates until solved)
```

**Key Feature**: All reasoning is structured in XML tags like `<Phenomenon>`, `<Hypothesis>`, etc.

## 🚀 Quick Start


### 1. Use via main.py

```bash
python main.py --workflow scientific --benchmark mle \
    --llm-model gpt-4o-mini \
    --data-dir /path/to/data \
    --task detecting-insults-in-social-commentary

# MathModeling benchmark example
python main.py --workflow scientific --benchmark mathmodeling \
    --llm-model gpt-4o-mini \
    --data-dir /path/to/mathmodeling-bench \
    --task mathmodeling-0

python main.py --workflow scientific --benchmark mathmodeling \
    --llm-model gpt-4o-mini \
    --data-dir /path/to/mathmodeling-bench \
    --task mathmodeling-1
```

**💡 Tip: External Data Storage**

If your dataset is large, you can store it on external storage:

```bash
# Data on external drive/network storage
python main.py --workflow scientific --benchmark mathmodeling \
    --llm-model gpt-4o-mini \
    --data-dir /mnt/external_drive/mathmodeling-data \
    --task bwor-11

# Registry (small metadata files) stays in project
# Data (large files) can be anywhere you specify via --data-dir
```

### 3. Use programmatically

```python
import asyncio
from pathlib import Path
from modeling.config import ModelingConfig, LLMConfig, WorkflowConfig
from modeling.workflows.factory import ScientificWorkflowFactory

async def main():
    # Configure
    config = ModelingConfig(
        llm=LLMConfig(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key="your-api-key"
        ),
        workflow=WorkflowConfig(name="scientific")
    )
    config.agent.search.max_iterations = 3  # Number of scientific cycles

    # Create workflow
    factory = ScientificWorkflowFactory()
    workflow = factory.create_workflow(config)

    # Define problem
    instruction = """
    Analyze customer churn and build a predictive model.
    Dataset: customer_data.csv with features (age, tenure, monthly_charges)
    Task: Predict churn (yes/no) and identify key drivers
    """

    io_instructions = """
    Output: Save model metrics and insights to output.txt
    """

    # Run
    await workflow.solve(
        description=instruction,
        io_instructions=io_instructions,
        data_dir=Path("./data"),
        output_path=Path("./output.txt")
    )

asyncio.run(main())
```

## 📊 XML Tag Format

All scientific reasoning uses strict XML tags:

```xml
<Phenomenon>
Customer churn shows patterns in engagement metrics
</Phenomenon>

<Hypothesis>
Low engagement frequency predicts churn within 30 days
</Hypothesis>

<Model>
Logistic regression: P(churn) = σ(β₀ + β₁·engagement + β₂·tenure)
</Model>

<Experiment>
import pandas as pd
from sklearn.linear_model import LogisticRegression
# Pure Python code only - no markdown
data = pd.read_csv('customers.csv')
model = LogisticRegression()
model.fit(X_train, y_train)
print(f"Accuracy: {model.score(X_test, y_test)}")
</Experiment>

<Observation>
Accuracy: 0.85
Precision: 0.78
Recall: 0.62
Low recall indicates missed churners
</Observation>

<Inference>
Model works but recall too low. Need additional features beyond engagement.
</Inference>

<Conclusion>
Final model achieves 88% accuracy with balanced metrics.
Key finding: engagement × tenure interaction is critical predictor.
</Conclusion>
```

## 📁 Output Files

After running, you'll find:

```
runs/modeling_run_YYYYMMDD_HHMMSS/artifacts/
├── summary.json           # Standard chat format (see below)
└── summary_readable.txt   # Human-readable version
```

**summary.json** (conversation format):
```json
[
  {
    "role": "user",
    "content": "Task description\n\nI/O Requirements:\n..."
  },
  {
    "role": "assistant",
    "content": "<Phenomenon>\n...\n</Phenomenon>\n<Hypothesis>\n...\n</Hypothesis>\n<Model>\n...\n</Model>\n<Experiment>\ncode\n</Experiment>\n<Observation>\nresults\n</Observation>\n<Inference>\n...\n</Inference>\n...\n<Conclusion>\n...\n</Conclusion>"
  }
]
```

## 🎓 Scientific Stages Explained

1. **Phenomenon**: Understand the problem from user input
2. **Hypothesis**: Formulate testable hypothesis ("I think X causes Y")
3. **Model**: Create formal model (equations, algorithms)
4. **Experiment**: Write Python code to test (code only, no markdown!)
5. **Observation**: Record execution results (auto-generated)
6. **Inference**: Decide if hypothesis is supported or refine it
7. **Conclusion**: Synthesize all findings (final stage)

## 🔧 Configuration

```python
# Adjust number of iterations
config.agent.search.max_iterations = 5  # Default: 3

# Each iteration runs the complete scientific cycle
# More iterations = more refinement
```

## 💡 Tips

1. **Start with 2-3 iterations** for testing
2. **Clear instructions** help formulate better hypotheses
3. **Specify output format** in io_instructions
4. **Check summary.json** for complete conversation
5. **`<Experiment>` contains pure Python code** - no markdown or comments explaining the approach


## 🐛 Troubleshooting

**Import errors**:
```bash
cd /home/aiops/liufan/projects/DeepModeling
python -c "import modeling; print('✓ OK')"
```

**No API key**:
```python
import os
config.llm.api_key = os.getenv("OPENAI_API_KEY")
```

**Timeout errors**:
```python
config.sandbox.timeout = 600  # Increase to 10 minutes
```

## 📚 More Information

- **Full documentation**: [SCIENTIFIC_WORKFLOW_README.md](SCIENTIFIC_WORKFLOW_README.md)
- **Implementation details**: [SCIENTIFIC_WORKFLOW_IMPLEMENTATION.md](SCIENTIFIC_WORKFLOW_IMPLEMENTATION.md)
- **Main project**: [README.md](README.md)

## 🎯 Success Indicators

After running `test_scientific_workflow.py`, you should see:

✅ Console logs showing:
- `<Phenomenon>` analysis
- `<Hypothesis>` formulation
- `<Model>` description
- `<Experiment>` code execution
- `<Observation>` results
- `<Inference>` analysis
- `<Conclusion>` synthesis

✅ Files created:
- `runs/test_scientific_xml/artifacts/summary.json`
- `runs/test_scientific_xml/artifacts/summary_readable.txt`
- `runs/test_scientific_xml/output.txt`

---

**Ready to discover!** 🔬

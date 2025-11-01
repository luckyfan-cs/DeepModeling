# Scientific Discovery Workflow

## Overview

The Scientific Discovery Workflow implements a complete scientific method cycle using **strict XML tag format** for solving problems in:
- **Data Science**
- **Scientific Discovery**
- **Mathematical Modeling**
- **Engineering Solutions**

## Scientific Method Cycle

The workflow follows these stages in each iteration:

```
┌─────────────────────────────────────────────────────────┐
│  Phenomenon  →  Hypothesis  →  Model  →  Experiment     │
│       ↑                                      ↓           │
│  Conclusion ← Inference  ←  Observation  ←──┘           │
└─────────────────────────────────────────────────────────┘
```

### XML Tag Format

All scientific reasoning is structured using XML tags:

```xml
<Phenomenon>
Problem analysis and understanding
</Phenomenon>

<Hypothesis>
Testable hypothesis
</Hypothesis>

<Model>
Formal model (equations, algorithms)
</Model>

<Experiment>
# Pure Python code only
import numpy as np
...
</Experiment>

<Observation>
Execution results (automatically inserted)
</Observation>

<Inference>
Analysis of observations and next steps
</Inference>

<Conclusion>
Final synthesis (after all iterations)
</Conclusion>
```

### Stages

1. **Phenomenon** - Analyze and understand the problem
2. **Hypothesis** - Formulate testable hypotheses
3. **Model** - Create formal models (equations, algorithms)
4. **Experiment** - Write Python code to test (code only, no markdown)
5. **Observation** - Record experimental results (auto-generated from execution)
6. **Inference** - Draw conclusions from observations
7. **Conclusion** - Final synthesis (after iterations)

## Usage

### Command Line

```bash
python main.py --workflow scientific --benchmark mle [options]
```

### Programmatic Usage

```python
from modeling.config import ModelingConfig, LLMConfig, WorkflowConfig
from modeling.workflows.factory import ScientificWorkflowFactory

# Configure
config = ModelingConfig(
    llm=LLMConfig(
        model="gpt-4o-mini",
        temperature=0.7,
    ),
    workflow=WorkflowConfig(name="scientific"),
)

# Create workflow
factory = ScientificWorkflowFactory()
workflow = factory.create_workflow(config)

# Run
await workflow.solve(
    description="Your problem description",
    io_instructions="Output requirements",
    data_dir=Path("./data"),
    output_path=Path("./output.txt")
)
```

## Example: Data Science Problem

```python
instruction = """
Analyze customer churn prediction:
1. Load customer data
2. Identify key features
3. Build predictive model
4. Evaluate performance
"""

io_instructions = """
Output: Save model metrics and insights to output.txt
"""
```

The workflow will:
- **Iteration 1**: Initial hypothesis and simple model
- **Iteration 2**: Refine based on observations
- **Iteration 3**: Optimize and finalize
- **Conclusion**: Synthesize findings

## Configuration

Adjust iterations in config:

```python
config.agent.search.max_iterations = 5  # Default: 3
```

## Output Artifacts

The workflow saves conversations in standard chat format:

**summary.json** - Complete conversation in JSON format:
```json
[
  {
    "role": "user",
    "content": "Task description\n\nI/O Requirements:\n..."
  },
  {
    "role": "assistant",
    "content": "<Phenomenon>\n...\n</Phenomenon>\n<Hypothesis>\n...\n</Hypothesis>\n...\n<Conclusion>\n...\n</Conclusion>"
  }
]
```

**summary_readable.txt** - Human-readable conversation format

All files saved to: `runs/modeling_run_*/artifacts/`

## Prompt Design

Prompts guide the model to:
- ✅ Use strict XML tag format for all scientific reasoning
- ✅ Generate pure Python code in `<Experiment>` tags
- ✅ Infer next steps from context (sees `<Hypothesis>`, generates `<Model>`)
- ✅ Be domain-agnostic (works for data science, physics, engineering, etc.)
- ✅ Build complete multi-turn reasoning in single assistant response

## Example Workflows

### Data Science (XML Format)
```xml
<Phenomenon>
Customer churn shows correlation with engagement metrics
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
# Load data, train model, evaluate
</Experiment>

<Observation>
Accuracy: 85%, Recall: 62%, Precision: 78%
Low recall indicates missed churners
</Observation>

<Inference>
Need additional features beyond engagement frequency
</Inference>

<Hypothesis>
Adding recency and monetary value improves prediction
</Hypothesis>
...
```

### Scientific Discovery
```xml
<Phenomenon>
Protein folding exhibits temperature-dependent stability changes
</Phenomenon>

<Hypothesis>
Critical temperature threshold exists for structural stability
</Hypothesis>

<Model>
ΔG = ΔH - TΔS (Gibbs free energy)
Stability lost when ΔG > 0
</Model>

<Experiment>
import numpy as np
# Molecular dynamics simulation code
</Experiment>

<Observation>
Unfolding begins at 37.2°C
ΔG crosses zero at this temperature
</Observation>

<Inference>
Hypothesis confirmed: critical threshold at physiological temperature
</Inference>
```

## Testing

Run the test script:

```bash
python test_scientific_workflow.py
```

This will run a simple data science problem through the complete workflow.

## Key Features

- ✅ **Strict XML Tag Format**: All reasoning structured in parseable tags
- ✅ **Iterative Refinement**: Multiple cycles to improve solutions
- ✅ **Grounded Validation**: Code execution validates hypotheses
- ✅ **Context-Aware Generation**: Model infers next step from previous tags
- ✅ **Conversation Format**: Standard chat format for easy integration
- ✅ **Domain Flexibility**: Works for multiple problem types
- ✅ **Scientific Rigor**: Follows proper scientific methodology

## Comparison with AIDE

| Feature | AIDE | Scientific |
|---------|------|------------|
| Focus | Solution optimization | Hypothesis testing |
| Format | Free-form code/text | Strict XML tags |
| Iterations | Draft → Debug → Improve | Phenomenon → ... → Conclusion |
| Output | Best solution code | Complete conversation with all cycles |
| Conversation | Not saved | Saved as standard chat format |
| Use Case | Kaggle competitions | Research, discovery, modeling |

## Future Enhancements

- [ ] Support for multi-experiment parallelization
- [ ] Statistical significance testing
- [ ] Automated hypothesis generation from data
- [ ] Integration with scientific databases
- [ ] Visualization of discovery process

## Citation

If you use this workflow in research, please cite:

```bibtex
@software{scientific_workflow_2024,
  title={Scientific Discovery Workflow},
  author={DeepModeling Team},
  year={2024},
  url={https://github.com/deepmodeling/modeling}
}
```

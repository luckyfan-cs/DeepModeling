# MathModeling Task 0 - Candy Production Mix

Determine the optimal production amounts for three candy brands (X, Y, Z) made from raw materials A, B, and C. Each brand must respect the material proportion constraints, monthly availability limits, and the processing and sales economics described below. The objective is to maximize monthly profit.

| Raw Material | Brand X | Brand Y | Brand Z | Cost ($/kg) | Monthly Limit (kg) |
|--------------|---------|---------|---------|-------------|--------------------|
| A | ≥ 60% | ≥ 30% | – | 2.00 | 2000 |
| B | – | – | – | 1.50 | 2500 |
| C | ≤ 20% | ≤ 50% | ≤ 60% | 1.00 | 1200 |

| | Brand X | Brand Y | Brand Z |
|--------------|---------|---------|---------|
| Processing Cost ($/kg) | 0.50 | 0.40 | 0.30 |
| Selling Price ($/kg) | 3.40 | 2.85 | 2.25 |

### Submission Format
- Provide a single row with `id` and `answer` columns.
- The answer must use the template `@profit[value]`, where `value` is the rounded optimal monthly profit.

### Evaluation
- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported profit.

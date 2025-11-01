# MathModeling Task 1 - Feed Selection Optimization

Determine the least-cost mix of five available feeds that satisfies the daily nutritional requirements for each animal. Every kilogram of feed contributes protein, minerals, and vitamins according to Table 1-22.

| Feed | Protein (g) | Minerals (g) | Vitamins (mg) | Price ($/kg) |
|------|-------------|--------------|---------------|--------------|
| 1 | 3 | 1.0 | 0.5 | 0.20 |
| 2 | 2 | 0.5 | 1.0 | 0.70 |
| 3 | 1 | 0.2 | 0.2 | 0.40 |
| 4 | 6 | 2.0 | 2.0 | 0.30 |
| 5 | 18 | 0.5 | 0.8 | 0.80 |

Nutritional requirements per animal per day:
- Protein ≥ 700 g
- Minerals ≥ 30 g
- Vitamins ≥ 100 mg

### Submission Format
- Provide a single row with `id` and `answer` columns.
- The answer must use the template `@cost[value]`, where `value` is the minimized daily feed cost (rounded to two decimals).

### Evaluation
- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported cost.

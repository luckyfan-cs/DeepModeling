# Mamo Easy 490 A Military Commander Needs To Allocate Resources Between Two Types

A military commander needs to allocate resources between two types of units, $X$ and $Y$, where the allocations must be whole numbers due to the nature of the units. The total number of units that can be supported is constrained by available resources: 10 units of X and 20 units of Y together cannot exceed 3000 due to logistical constraints. To achieve a strategic objective, the combined strength of 3 units of X and 5 units of Y must be at least 500. Furthermore, there should not be a difference in allocation exceeding 1000 between unit X and unit Y for maintaining balance in force deployment.\n\nEach unit of $X$ requires $\$10,000$ worth support points whereas each unit of $Y$ requires $\$20,000$. The commander aims to minimize the total support points allocated while adhering to these constraints. Calculate the minimum total cost required for this operation in dollars, rounded to the nearest dollar.

### Submission Format
- Provide a single row with `id` and `answer` columns.
- The answer must use the template `@cost[value]`, where `value` is the numeric solution rounded as appropriate.

### Evaluation
- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported value.

# Mamo Easy 594 A Transportation Company Is Planning To Distribute Its Fleet Of Ve

A transportation company is planning to distribute its fleet of vehicles across four different locations: $X1, X2, X3$, and $X4$. These locations could be various warehouses or distribution centers. The company has a cost associated with each location due to factors like distance, road conditions, and local regulations. The costs are 2, 3, 4, and 5 units for $X1, X2, X3$, and $X4$ respectively.\n\nThe allocation must adhere to the following constraints due to operational limitations:\n- The combined number of vehicles at locations $X1$ and $X2$ cannot exceed 500.\n- Similarly, the total number of vehicles at locations $X3$ and $X4$ is capped at 600.\n- To maintain a minimum level of service quality across all regions served by the company, there should be no fewer than 300 vehicles distributed between locations $X1$ and $X3$.\n- Similarly, a minimum total of 400 vehicles should be allocated between locations $X2$ and $X4$. \n\nAdditionally, each location has specific bounds on vehicle allocation:\n- Location $X1$: no more than 300 vehicles\n- Location $X2$: no more than 200 vehicles\n- Location $X3$: no more than 300 vehicles\n- Location $X4$: no more than 400 vehicles\n\nGiven these constraints along with the requirement that the allocations for each location must be whole numbers due to the indivisible nature of vehicle fleets,\nThe question is: What is the minimum total cost for optimal distribution of the fleet across these four locations within specified bounds? Provide your answer rounded to nearest whole number.

### Submission Format
- Provide a single row with `id` and `answer` columns.
- The answer must use the template `@cost[value]`, where `value` is the numeric solution rounded as appropriate.

### Evaluation
- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported value.

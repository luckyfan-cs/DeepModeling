# Mamo Easy 617 A Construction Company Is Planning To Allocate Resources To Four D

A construction company is planning to allocate resources to four different projects: x1, x2, x3, and x4. These projects could involve building residential houses, commercial buildings, public infrastructures, and renovation works respectively. The objective is to minimize the total cost associated with these projects where costs are 200, 300, 150 and 400 units for each unit of resource allocated to project x1, x2, x3 and x4 respectively.\n\nThe allocation must adhere to the following constraints due to budget limitations and manpower availability:\n- The combined resource allocation for project x1 and project x2 cannot exceed 1000 units.\n- Twice the allocation for project x2 added with the allocation for project x3 cannot exceed 1200 units.\n- Three times the allocation for project x1 minus half of the allocation for project x3 must be at least equal to 500 units.\n- Allocation for project X4 should not be less than that of Project X1.\n\nGiven that all allocations must be whole numbers due to nature of resources being indivisible. Furthermore each project has specific bounds on resource allocations between zero (inclusive) and certain maximum values determined by various factors like regulatory compliance or strategic importance: \nWhat is the minimum total cost for the company given an optimal resource distribution across all four projects within their respective specified bounds? Provide your answer rounded off to nearest whole number.

### Submission Format
- Provide a single row with `id` and `answer` columns.
- The answer must use the template `@cost[value]`, where `value` is the numeric solution rounded as appropriate.

### Evaluation
- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported value.

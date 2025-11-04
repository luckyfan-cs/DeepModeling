# Mamo Easy 624 In A Supply Chain Optimization Scenario A Company Needs To Allocat

In a supply chain optimization scenario, a company needs to allocate resources across four different areas: $x1, x2, x3$, and $x4$. These could represent investments in raw materials procurement, production facilities, logistics infrastructure, and sales and marketing efforts respectively. The objective is to minimize the total cost associated with these allocations. The costs per unit of allocation are 1.5 for $x1$, 2 for $x2$, 3 for $x3$, and 4 for $x4$.\n\nThe resource allocation must adhere to the following constraints:\n- The combined resource allocation for areas $x1$ and $x2$ cannot exceed 1000 units due to limited available budget or resources.\n- Similarly, the combined resource allocation for areas $x3$ and $x4$ cannot exceed 1200 units.\n- Additionally, the difference between 70% of the resources allocated to area $x1$ and 80% of those allocated to area $x2$ should be at least 200 units. This might reflect strategic considerations about balancing investment in raw materials procurement versus production facilities.\n- Lastly, the resources allocated to area $x4$ should exceed those allocated to area$x3$ by at least 300 units. This might be due to greater emphasis on sales and marketing efforts compared with logistics infrastructure.\n\nGiven these conditions (and considering that all allocations are integers due to indivisibility of certain resources), what is the minimum total cost required? Provide your answer rounded down to the nearest whole number.

### Submission Format
- Provide a single row with `id` and `answer` columns.
- The answer must use the template `@cost[value]`, where `value` is the numeric solution rounded as appropriate.

### Evaluation
- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported value.

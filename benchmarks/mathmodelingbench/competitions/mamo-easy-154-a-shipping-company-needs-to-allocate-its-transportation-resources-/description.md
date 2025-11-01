# Mamo Easy 154 A Shipping Company Needs To Allocate Its Transportation Resources 

A shipping company needs to allocate its transportation resources between two of its major routes: Route $X$ and Route $Y$. The total number of shipments on both routes cannot exceed 1000 due to capacity constraints. To meet the demand, at least 1500 units (calculated as twice the number of shipments on route X plus thrice the number of shipments on route Y) must be transported. Additionally, to maintain service quality, the number of shipments on route X should be at least 200 more than that on route Y. The cost associated with each shipment is $\$50$ for Route $X$ and $\$70$ for Route $Y$. Given these conditions, and taking into account that the number of shipments must be whole numbers due to their indivisible nature, calculate the minimum total cost in dollars that would allow the company to meet all these requirements while staying within the given bounds for each route.

### Submission Format
- Provide a single row with `id` and `answer` columns.
- The answer must use the template `@cost[value]`, where `value` is the numeric solution rounded as appropriate.

### Evaluation
- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported value.

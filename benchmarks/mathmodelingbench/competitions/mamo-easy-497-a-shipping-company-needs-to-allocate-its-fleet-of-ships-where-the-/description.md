# Mamo Easy 497 A Shipping Company Needs To Allocate Its Fleet Of Ships Where The 

A shipping company needs to allocate its fleet of ships (where the allocations must be whole numbers due to the nature of the ships) between two routes: Route X and Route Y. The total number of ships that can be deployed is limited to 100 due to logistical constraints. To meet customer demand, the combined capacity of twice the number of ships on route X and those on route Y must be at least 60. Furthermore, the difference in the number of ships between route X and route Y should not exceed 30 to maintain operational balance.\n\nEach ship operating on Route X and Route Y incurs costs related to fuel, crew salaries, maintenance, etc., which amount to 10 and 20 units respectively. The company aims to minimize these total costs while adhering to these constraints. Also note that there are specific bounds on ship allocation for each route: no more than 70 for Route X and no more than 50 for Route Y.\n\nWhat is the minimum total cost required for this operation? Provide your answer rounded off to nearest whole number.

### Submission Format
- Provide a single row with `id` and `answer` columns.
- The answer must use the template `@cost[value]`, where `value` is the numeric solution rounded as appropriate.

### Evaluation
- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported value.

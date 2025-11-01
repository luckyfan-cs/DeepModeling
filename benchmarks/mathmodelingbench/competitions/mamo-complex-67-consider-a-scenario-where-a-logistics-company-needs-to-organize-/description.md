# Mamo Complex 67 Consider A Scenario Where A Logistics Company Needs To Organize 

Consider a scenario where a logistics company needs to organize a delivery route across five warehouses. These warehouses are located in different cities labeled as A, B, C, D, and E. A delivery truck has to start from any one of these warehouses, deliver goods at each of the remaining four exactly once, and finally return to the starting warehouse. The challenge here is to plan the route in a way that minimizes the total travel cost. The cost could be based on various factors like distance, fuel usage, or time spent.

Here are the details of the travel costs between the warehouses:

The cost to travel from Warehouse A to B is 15 units, to C is 88 units, to D is 54 units, and to E is 92 units.

From Warehouse B, the cost to reach A is 15 units, to C is 29 units, to D is 98 units, and to E is 33 units.

For Warehouse C, the cost to get to A is 88 units, to B is 29 units, to D is 96 units, and to E is 96 units.

Moving from Warehouse D, it costs 54 units to reach A, 98 units to get to B, 96 units to C, and 63 units to E.

Lastly, from Warehouse E, the cost to go to A is 92 units, to B is 33 units, to C is 96 units, and to D is 63 units.

How can the logistics company plan the route so that the total travel cost is minimized for the delivery truck to visit each warehouse exactly once and return to the starting warehouse?

### Submission Format
- Provide a single row with `id` and `answer` columns.
- The answer must use the template `@cost[value]`, where `value` is the numeric solution rounded as appropriate.

### Evaluation
- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported value.

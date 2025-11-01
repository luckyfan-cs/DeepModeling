# Mamo Complex 62 Imagine A Logistics Manager Tasked With Planning A Delivery Rout

Imagine a logistics manager tasked with planning a delivery route for a truck that needs to visit four different cities to distribute goods. The cities are identified numerically as 1, 2, 3, and 4. The truck can start its journey from any of these cities but must travel to each city exactly once and then return to the starting point. The objective is to arrange this route in such a way that the total travel cost is minimized. The costs associated with traveling between the cities are as follows:
- The cost to travel from City 1 to City 2 is 52 units, to City 3 is 89 units, and to City 4 is 11 units.
- From City 2, it costs 52 units to reach City 1, 14 units to get to City 3, and 13 units to City 4.
- Traveling from City 3, the costs are 89 units to City 1, 14 units to City 2, and 87 units to City 4.
- Lastly, from City 4, it costs 11 units to go to City 1, 13 units to City 2, and 87 units to City 3.

What is the minimum total travel cost for the truck to visit each city exactly once and return to the starting city?

### Submission Format
- Provide a single row with `id` and `answer` columns.
- The answer must use the template `@cost[value]`, where `value` is the numeric solution rounded as appropriate.

### Evaluation
- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported value.

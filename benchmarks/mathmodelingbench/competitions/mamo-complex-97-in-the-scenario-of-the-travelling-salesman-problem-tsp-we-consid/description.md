# Mamo Complex 97 In The Scenario Of The Travelling Salesman Problem Tsp We Consid

In the scenario of the Travelling Salesman Problem (TSP), we consider four distinct cities labeled as City 1, City 2, City 3, and City 4. A salesperson must visit each of these cities starting from any one of them, travel to each of the other cities exactly once, and then return to the starting city. The primary objective for the salesperson is to minimize the total travel cost during this circuit.

Here's a detailed look at the travel costs between each pair of cities:
- The cost to travel from City 1 to City 2 is 76 units, to City 3 is 17 units, and to City 4 is 24 units.
- From City 2, the travel costs are 76 units to City 1, 84 units to City 3, and just 11 units to City 4.
- For journeys from City 3, it costs 17 units to reach City 1, a steep 84 units to get to City 2, and 90 units to go to City 4.
- Lastly, from City 4, the costs involved are 24 units to City 1, 11 units to City 2, and 90 units to City 3.

Given these conditions, what is the minimum total travel cost for the salesperson to complete their route of visiting each city exactly once and returning to the starting point?

### Submission Format
- Provide a single row with `id` and `answer` columns.
- The answer must use the template `@cost[value]`, where `value` is the numeric solution rounded as appropriate.

### Evaluation
- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported value.

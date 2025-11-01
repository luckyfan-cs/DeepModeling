# Mamo Complex 77 Imagine A Scenario Where A Salesperson Must Visit Four Distinct 

Imagine a scenario where a salesperson must visit four distinct cities to conduct business meetings. Let's label these cities as City 1, City 2, City 3, and City 4. The salesperson can start their trip from any city, but they must visit each city exactly once and then return to the starting point. The main objective is to minimize the total cost of traveling between these cities.

Here’s a detailed breakdown of the travel costs:
- From City 1, the travel cost is 27 units to City 2, 48 units to City 3, and 76 units to City 4.
- From City 2, it costs 27 units to return to City 1, 82 units to reach City 3, and 88 units to go to City 4.
- From City 3, traveling back to City 1 costs 48 units, moving to City 2 costs 82 units, and it is 97 units to journey to City 4.
- Lastly, from City 4, it costs 76 units to go back to City 1, 88 units to travel to City 2, and 97 units to move to City 3.

What is the minimum total travel cost for the salesperson to visit each of these cities exactly once and return to the starting city?

### Submission Format
- Provide a single row with `id` and `answer` columns.
- The answer must use the template `@cost[value]`, where `value` is the numeric solution rounded as appropriate.

### Evaluation
- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported value.

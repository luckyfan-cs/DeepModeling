# Mamo Easy 313 In A Military Operation The Commander Needs To Allocate Resources 

In a military operation, the commander needs to allocate resources among three types of units: Tanks, Aircrafts, and Submarines. The number of each type of unit must be an integer due to the nature of the units. The total resource points that can be allocated are limited to 1000, with each Tank requiring 5 resource points, each Aircraft requiring 3 resource points, and each Submarine requiring 2 resource points. To achieve a strategic objective, the combined strength of twice the number of Tanks plus four times the number of Aircrafts plus Submarines must be at least 200. Moreover, there is an additional constraint that requires the difference between Tanks and Aircrafts plus Submarines to exactly equal 50.\n\nEach unit type has different operational costs: for every Tank it is $30$, for every Aircraft it is $20$, and for every Submarine it is $10$. The goal is to minimize these costs while adhering to all constraints. What would be this minimum cost in dollars?

### Submission Format
- Provide a single row with `id` and `answer` columns.
- The answer must use the template `@cost[value]`, where `value` is the numeric solution rounded as appropriate.

### Evaluation
- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported value.

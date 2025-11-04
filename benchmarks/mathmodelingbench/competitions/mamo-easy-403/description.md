# Mamo Easy 403 In A Military Logistics Operation A Commander Needs To Allocate Re

In a military logistics operation, a commander needs to allocate resources between four types of units: Tanks, Aircrafts, Ships, and Drones. The allocations must be whole numbers due to the nature of the units. The total number of Tank and Aircraft units that can be supported is limited to 1000 due to logistical constraints, while the total number of Ship and Drone units cannot exceed 600. Additionally, there should always be at least 200 more Tanks than Ships and no more than 50 difference in quantity between Aircrafts and Drones.\n\nEach unit type requires different support points as follows: each Tank requires 4 support points, each Aircraft requires 3 support points, each Ship requires 5 support points and each Drone requires 2 support points. Also note that the maximum allowable quantity for each unit type are as follows: Tanks - 700 units; Aircrafts - 400 units; Ships -300 units; Drones -250 units.\n\nThe commander aims to minimize the total support points allocated while adhering to these constraints. Calculate the minimum total support points required for this operation.

### Submission Format
- Provide a single row with `id` and `answer` columns.
- The answer must use the template `@cost[value]`, where `value` is the numeric solution rounded as appropriate.

### Evaluation
- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported value.

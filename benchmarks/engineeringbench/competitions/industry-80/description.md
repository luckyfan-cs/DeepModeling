# Industry 80 On Danzig Street Vehicles Can Park On Both Sides Of The Street

On Danzig Street, vehicles can park on both sides of the street. Mr. Edmonds, who lives at No. 1, is organizing a party with about 30 participants, and they will arrive in 15 cars. The length of the i-th car is λ_i, in meters, as follows:

| i  | 1  | 2   | 3  | 4   | 5   | 6   | 7   | 8   | 9   | 10  | 11  | 12  | 13  | 14  | 15  |
|----|----|-----|----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| λ_i | 4  | 4.5 | 5  | 4.1 | 2.4 | 5.2 | 3.7 | 3.5 | 3.2 | 4.5 | 2.3 | 3.3 | 3.8 | 4.6 | 3   |

In order to avoid disturbing the neighbors, Mr. Edmonds wants to arrange parking on both sides of the street so that the total length of the street occupied by his friends' vehicles is minimized. Please provide a mathematical programming formulation and solve this problem using AMPL.
How does the program change if the cars on one side of the street cannot occupy more than 30 meters?

### Submission Format
- Provide a single row with `id` and `answer` columns.
- The answer must use the template `@cost[value]`, where `value` is the numeric solution rounded as appropriate.

### Evaluation
- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported value.

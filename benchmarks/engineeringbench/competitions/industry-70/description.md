# Industry 70 Consider Assigning N 2 Factories To N Locations

Consider assigning $n=2$ factories to $n$ locations. The transportation volume between factory $i$ and factory $j$ is $d_{ij}$, and the unit transportation cost from location $p$ to location $q$ is $c_{pq}$. The specific values are shown in the following table: Table 1.1

|        | Transportation volume to Location 1 | Transportation volume to Location 2 | Transportation cost to Location 1 | Transportation cost to Location 2 |
| :----: | :---------------------------------: | :---------------------------------: | :-------------------------------: | :-------------------------------: |
| Factory 1 | 10 | 20 | 5 | 8 |
| Factory 2 | 30 | 40 | 6 | 7 |

In order to minimize the total transportation cost, formulate this problem as an integer model.

### Submission Format
- Provide a single row with `id` and `answer` columns.
- The answer must use the template `@cost[value]`, where `value` is the numeric solution rounded as appropriate.

### Evaluation
- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported value.

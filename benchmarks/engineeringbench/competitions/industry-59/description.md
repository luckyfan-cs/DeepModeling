# Industry 59 A Traveling Salesman Must Visit 7 Customers At 7 Different Locations

A traveling salesman must visit 7 customers at 7 different locations, with the (symmetric) distance matrix as follows:

|  | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | - | 86 | 49 | 57 | 31 | 69 | 50 |
| 2 |  | - | 68 | 79 | 93 | 24 | 5 |
| 3 |  |  | - | 16 | 7 | 72 | 67 |
| 4 |  |  |  | - | 90 | 69 | 1 |
| 5 |  |  |  |  | - | 86 | 59 |
| 6 |  |  |  |  |  | - | 81 |

Formulate a mathematical program to determine the visiting order starting and ending at location 1 to minimize the travel distance, and solve it using COPTPY.

### Submission Format
- Provide a single row with `id` and `answer` columns.
- The answer must use the template `@cost[value]`, where `value` is the numeric solution rounded as appropriate.

### Evaluation
- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported value.

# Industry 26 A Factory Produces Three Types Of Products I Ii And Iii

A factory produces three types of products: I, II, and III. Each product needs to go through two processing procedures, A and B. The factory has two pieces of equipment that can complete process A, denoted as A1 and A2; it has three pieces of equipment that complete process B, denoted as B1, B2, and B3. Product I can be processed on any equipment for A and B; Product II can be processed on any A equipment but only on B1 for process B; Product III can only be processed on A2 and B2. Given the unit processing time on various machines, raw material costs, product sale prices, effective machine hours, and the costs of operating the machines at full capacity as shown in Table 1-4, the task is to arrange the optimal production plan to maximize the factory's profit.

Table 1-4
| Equipment  | Product I | Product II | Product III | Effective Machine Hours | Operating Costs at Full Capacity (Yuan) |
|------------|-----------|------------|-------------|--------------------------|------------------------------------------|
| A1         | 5         | 10         |             | 6000                     | 300                                      |
| A2         | 7         | 9          | 12          | 10000                    | 321                                      |
| B1         | 6         | 8          |             | 4000                     | 250                                      |
| B2         | 4         |            | 11          | 7000                     | 783                                      |
| B3         | 7         |            |             | 4000                     | 200                                      |
| Raw Material Cost (Yuan/Unit) | 0.25 | 0.35       | 0.50       |                          |                                          |
| Unit Price (Yuan/Unit)        | 1.25 | 2.00       | 2.80       |                          |                                          |

### Submission Format
- Provide a single row with `id` and `answer` columns.
- The answer must use the template `@profit[value]`, where `value` is the numeric solution rounded as appropriate.

### Evaluation
- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported value.

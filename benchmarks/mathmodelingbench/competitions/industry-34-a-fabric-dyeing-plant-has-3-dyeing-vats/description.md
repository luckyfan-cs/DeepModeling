# Industry 34 A Fabric Dyeing Plant Has 3 Dyeing Vats

A fabric dyeing plant has 3 dyeing vats. Each batch of fabric must be dyed in sequence in each vat: first, the second, and third vats. The plant must color five batches of fabric of different sizes. The time required in hours to dye batch $i$ in vat $j$ is given in the following matrix:

$$
\left(\begin{array}{ccc}
3 & 1 & 1 \\
2 & 1.5 & 1 \\
3 & 1.2 & 1.3 \\
2 & 2 & 2 \\
2.1 & 2 & 3
\end{array}\right)
$$

Schedule the dyeing operations in the vats to minimize the completion time of the last batch.

### Submission Format
- Provide a single row with `id` and `answer` columns.
- The answer must use the template `@cost[value]`, where `value` is the numeric solution rounded as appropriate.

### Evaluation
- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported value.

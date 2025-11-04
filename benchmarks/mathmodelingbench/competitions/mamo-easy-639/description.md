# Mamo Easy 639 In The Field Of Education A University Is Planning To Allocate Its

In the field of education, a university is planning to allocate its budget across four different departments: $x1$, $x2$, $x3$, and $x4$. These could represent departments like Science, Arts, Engineering, and Humanities respectively. The objective is to minimize the total cost associated with these departments, with costs being $\$200$, $\$300$, $\$500$, and $\$1000$ for each unit allocated to $x1$, $x2$, $x3$, and $x4$ respectively.\n\nThe allocation must adhere to the following constraints due to budget limitations and departmental requirements:\n- The total resource allocation for all departments cannot exceed 100 units.\n- To ensure adequate funding for research activities, the sum of ten times the allocation for department $x1$ and twenty times that for department $x2$ should be at least 50 units.\n- Due to certain strategic objectives, three times the allocation for department $x3$ should not exceed forty times that of department $x4$ by more than 10 units.\n- Furthermore, considering faculty salaries and operating expenses, fifteen point five times the allocation for department $x2$ minus half of that for department $x3$, after subtracting the allocation for department x1 , must not exceed 70 units.\n\nGiven these conditions along with the fact that allocations must be in whole numbers due to practicalities of budget distribution (and each department has specific bounds on resource allocation, the upper bounds of x1, x2, x3, x4 are 20, 30, 40, 50, respectively), what would be the minimum total cost in dollars rounded to nearest whole number?

### Submission Format
- Provide a single row with `id` and `answer` columns.
- The answer must use the template `@cost[value]`, where `value` is the numeric solution rounded as appropriate.

### Evaluation
- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported value.

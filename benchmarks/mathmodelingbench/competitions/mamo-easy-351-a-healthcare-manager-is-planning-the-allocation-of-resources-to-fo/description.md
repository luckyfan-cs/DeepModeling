# Mamo Easy 351 A Healthcare Manager Is Planning The Allocation Of Resources To Fo

A healthcare manager is planning the allocation of resources to four different departments: x1, x2, x3, and x4. These departments could involve general medicine, surgery, diagnostics, and research respectively. The objective is to minimize the total cost associated with these departments, with costs being 100, 50, 30, and 200 units for x1, x2, x3 and x4 respectively.\n\nThe allocation must adhere to the following constraints due to budgetary limitations:- The combined resource allocation for general medicine (x1) and surgery (x2) must be at least 10 units.- The combined resource allocation for diagnostics (x3) and research (x4) must be at least 20 units.- Five times the allocation for general medicine minus twice the allocation for surgery cannot exceed zero units - this represents a balance in funding between these two critical areas.- Three times the resources allocated to diagnostics minus those allocated to research must be at least zero - reflecting a priority on diagnostic services.\n\nGiven that all department allocations are integers due to financial policies and each department has specific bounds on resource allocation:What is the minimum total cost for the healthcare organization given optimal resource distribution within specified limits? Provide your answer rounded to nearest whole number.

### Submission Format
- Provide a single row with `id` and `answer` columns.
- The answer must use the template `@cost[value]`, where `value` is the numeric solution rounded as appropriate.

### Evaluation
- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported value.

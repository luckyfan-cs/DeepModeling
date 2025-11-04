# Mamo Easy 251 A Manager Needs To Schedule The Working Hours For Three Employees 

A manager needs to schedule the working hours for three employees (X, Y, and Z) in a day. The total working hours across all three employees cannot exceed 24 due to labor laws. Employee X must work at least 2 hours more than employee Y due to their role requirements. The combined working hours of employee Y and Z cannot exceed 16 as they share a common workspace with limited availability. Each hour of work for employees X, Y, and Z incurs different costs to the company: $8, $6, and $5 respectively.\n\nGiven these constraints and that the number of working hours for each employee must be an integer due to scheduling practicalities (with bounds on individual working hours being between 0-10 for X, 0-8 for Y, and 0-6 for Z), what is the minimum total cost for this scheduling scenario? Provide your answer rounded to the nearest whole dollar.

### Submission Format
- Provide a single row with `id` and `answer` columns.
- The answer must use the template `@cost[value]`, where `value` is the numeric solution rounded as appropriate.

### Evaluation
- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported value.

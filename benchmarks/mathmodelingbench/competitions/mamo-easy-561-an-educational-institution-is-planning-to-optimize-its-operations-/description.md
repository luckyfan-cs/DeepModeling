# Mamo Easy 561 An Educational Institution Is Planning To Optimize Its Operations 

An educational institution is planning to optimize its operations by allocating resources efficiently across three main areas: teachers, staff, and classrooms. Each teacher costs the institution \$5000, each staff member costs \$3000, and each classroom costs \$200. The institution aims to minimize the total cost while meeting certain constraints:\n\n- For every classroom, there should be at least one teacher available. This ensures that all classes have a dedicated teacher.\n- Similarly, for every classroom, there should be at least two staff members available for administrative and maintenance tasks.\n- The total number of teachers and staff combined cannot exceed 100 due to budgetary limitations.\n\nMoreover, the institution must ensure that they employ at least 5 teachers and 2 staff members due to operational requirements. Also, it must maintain at least one classroom open for teaching purposes. All these values are integers due to the indivisible nature of the resources being allocated (i.e., you can't hire half a teacher or use half a classroom).\n\nGiven these conditions, what is the minimum total cost for the educational institution under optimal resource allocation? Provide your answer rounded to the nearest dollar.

### Submission Format
- Provide a single row with `id` and `answer` columns.
- The answer must use the template `@cost[value]`, where `value` is the numeric solution rounded as appropriate.

### Evaluation
- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported value.

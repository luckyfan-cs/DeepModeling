# Mamo Easy 370 A Manager Is Planning A Schedule For Four Tasks T1 T2 T3 And T4

A manager is planning a schedule for four tasks: t1, t2, t3, and t4. Each task has a different workload, with workloads being 1 unit for t1, 2 units for t2, 3 units for t3, and 4 units for t4 respectively. The objective is to minimize the total workload associated with these tasks.\n\nThe scheduling must adhere to the following constraints due to time limitations and dependencies between tasks:- Task t1 must start at least at hour 5.- The difference in start times between task t2 and task t1 cannot exceed 8 hours.- The difference in start times between task t3 and task t2 must be at least 10 hours.- The difference in start times between task t4 and task t3 cannot exceed 15 hours.\n\nGiven the constraints and the objective function, along with the requirement that the starting times for tasks (t1, t2, t3, and t4) must be whole numbers because we can only schedule tasks on an hourly basis:What is the minimum total workload for these four tasks within a single day (24 hours), given the optimal scheduling of their starting times? Provide your answer rounded to the nearest whole number.

### Submission Format
- Provide a single row with `id` and `answer` columns.
- The answer must use the template `@cost[value]`, where `value` is the numeric solution rounded as appropriate.

### Evaluation
- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported value.

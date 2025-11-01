# Mamo Easy 618 A Scheduling Manager Is Tasked With Allocating Work Hours Among Fo

A scheduling manager is tasked with allocating work hours among four teams: Team X1, Team X2, Team X3, and Team X4. The objective is to minimize the total fatigue score that associates with each hour of work are 2 for team X1, 3 for team X2, 4 for team X3, and 5 for team X4.\n\nThe allocation must adhere to the following constraints due to manpower availability and project requirements:\n- The combined working hours of Teams X1 and X2 cannot exceed 8 hours.\n- The sum of twice the working hours of Team X2 and the working hours of Team X3 must be at least 10 hours, reflecting specific project demands.\n- The difference between the working hours allocated to Team X3 and three times that allocated to Team X4 should not exceed 15 hours to ensure workload balance.\n- The difference between the number of working hours assigned to Teams x4 and x1 must exactly be equal to five because a certain task requires this coordination between these two teams.\n\nEach team's work allocation is bound within specific limits due to their skill set or other operational considerations. Given these conditions along with the requirement that all allocations should be in whole numbers due to practicalities related to scheduling:\nWhat would be the minimum total fatigue score under optimal scheduling? Provide your answer rounded off to the nearest whole number.

### Submission Format
- Provide a single row with `id` and `answer` columns.
- The answer must use the template `@cost[value]`, where `value` is the numeric solution rounded as appropriate.

### Evaluation
- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported value.

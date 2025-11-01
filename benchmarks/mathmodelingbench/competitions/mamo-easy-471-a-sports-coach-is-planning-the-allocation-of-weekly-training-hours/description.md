# Mamo Easy 471 A Sports Coach Is Planning The Allocation Of Weekly Training Hours

A sports coach is planning the allocation of weekly training hours for two groups within the team: group $X$ focuses on strength conditioning, and group $Y$ on skill development. The objective is to optimize the team's performance by minimizing the total fatigue score, which is affected by the training intensity and duration for each group. The fatigue scores associated with each hour of training are 10 for group $X$, and 20 for group $Y$.\n\nThe team has the following constraints for their weekly training schedule:\n- The combined hours of three times strength conditioning (group $X$) and twice the skill development (group $Y$) cannot exceed 60 hours, considering the available facilities and trainers.\n- To achieve a balanced training program, at least 12 hours in total must be allocated to both groups.\n- Additionally, there should not be more than an eight-hour difference between skill development (group Y) and strength conditioning (group X).\n\nGiven these conditions and aiming for whole numbers of training hours due to scheduling practicalities, what would be the minimum total fatigue score given optimal allocation of weekly training hours among these two groups?

### Submission Format
- Provide a single row with `id` and `answer` columns.
- The answer must use the template `@cost[value]`, where `value` is the numeric solution rounded as appropriate.

### Evaluation
- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported value.

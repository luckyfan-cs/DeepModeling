# Mamo Easy 210 In A Healthcare Scenario A Hospital Needs To Allocate Personnel Ac

In a healthcare scenario, a hospital needs to allocate personnel across three roles: Doctor, Nurse, and Technician. These roles could represent different shifts or departments within the hospital. The total number of staff allocated cannot be less than 100 due to patient demand. The difference in numbers between Doctors and Nurses must not exceed 10 for maintaining balanced care levels, while the difference between Technicians and Nurses should not be less than -5 for ensuring operational efficiency.\n\nEach role incurs different costs per unit person based on salary and other associated expenses: Doctors cost 50 units, Nurses cost 30 units, and Technicians cost 20 units. The hospital aims to minimize the total staffing cost while adhering to these constraints and ensuring that all allocations are in whole numbers due to each individual representing a single person.\n\nCalculate the minimum total staffing cost required for this scenario, rounded to the nearest whole number.

### Submission Format
- Provide a single row with `id` and `answer` columns.
- The answer must use the template `@cost[value]`, where `value` is the numeric solution rounded as appropriate.

### Evaluation
- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported value.

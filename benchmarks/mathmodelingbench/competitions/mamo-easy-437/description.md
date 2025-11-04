# Mamo Easy 437 In A Healthcare Setting A Hospital Manager Needs To Schedule Hours

In a healthcare setting, a hospital manager needs to schedule hours for doctors and nurses over the course of a week. The aim is to minimize total staffing costs while meeting certain requirements related to patient care and staff availability. Each hour worked by a doctor costs 10 units, while each hour worked by a nurse costs 20 units.\n\nThe following constraints apply:\n- To ensure adequate patient care, the combined effort of twice the doctor hours plus the nurse hours must be at least 50.\n- To prevent overworking the staff, the sum of doctor hours and three times the nurse hours cannot exceed 150.\n- For operational reasons, there must be at least 10 more doctor hours than nurse hours in any given week.\n\nGiven that both doctors' and nurses' working hours are integers due to practical scheduling considerations and each role has specific bounds on weekly workhours:\nWhat is the minimum total staffing cost for this scenario (in units), rounded to the nearest whole number?

### Submission Format
- Provide a single row with `id` and `answer` columns.
- The answer must use the template `@cost[value]`, where `value` is the numeric solution rounded as appropriate.

### Evaluation
- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported value.

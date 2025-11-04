# Mamo Complex 59 Consider A Courier Company That Needs To Deliver Packages To Fiv

Consider a courier company that needs to deliver packages to five distinct cities, denoted as E, F, G, H, and I. The courier can start from any city, but they must visit each city only once and then return to the starting point. The aim is to find a route that would minimize the total delivery cost. The cost might include factors like distance, fuel expenses, or traffic conditions. Here's an outline of the delivery cost between these cities:
The cost to deliver from City E to F is 50 units, to G is 48 units, to H is 99 units, and to I is 91 units.
From City F, it costs 50 units to deliver to E, 57 units to deliver to G, 84 units to H, and 72 units to I.
For City G, the delivery costs are 48 units to E, 57 units to F, 46 units to H, and 86 units to I.
If the package starts from City H, it costs 99 units to deliver to E, 84 units to F, 46 units to G, and 29 units to I.
Lastly, from City I, it costs 91 units to deliver to E, 72 units to F, 86 units to G, and 29 units to H.
What is the least total delivery cost for the courier to visit each city exactly once and then return to the starting point?

### Submission Format
- Provide a single row with `id` and `answer` columns.
- The answer must use the template `@cost[value]`, where `value` is the numeric solution rounded as appropriate.

### Evaluation
- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported value.

# Mamo Complex 61 Consider Four Cities E F G And H

Consider four cities: E, F, G, and H. A delivery driver is tasked with delivering packages to each of these cities. The driver can start their route from any one of these cities. However, the driver must ensure that they visit each city exactly once and then return back to the city they started from. The ultimate goal is to minimize the total travel cost, which might include expenses such as fuel, toll fees, or time spent on the road.

Here's a detailed breakdown of the travel costs between these cities:

To travel from City E to F costs 17 units, to G costs 52 units, and to H costs 79 units.
From City F, the cost is 17 units to go to E, 15 units to reach G, and 71 units to go to H.
If the driver starts from City G, it costs 52 units to reach E, 15 units to go to F, and 54 units to reach H.
Lastly, if the journey begins from City H, it costs 79 units to go to E, 71 units to go to F, and 54 units to reach G.

Now the question is: What is the minimum total travel cost for the driver to deliver packages in each city exactly once and then return to the starting city?

### Submission Format
- Provide a single row with `id` and `answer` columns.
- The answer must use the template `@cost[value]`, where `value` is the numeric solution rounded as appropriate.

### Evaluation
- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported value.

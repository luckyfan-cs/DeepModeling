# Industry 33 The Current Problem Faced By The Company Is How To Use The Fewest Nu

The current problem faced by the company is how to use the fewest number of containers to pack the currently needed goods for transportation, while considering the weight of the goods, specific packaging requirements, and inventory limitations. Professional modeling and analysis are needed for a batch of goods’ transportation strategy to ensure maximum utilization of the limited container space.

The company currently has a batch to be transported, with each container able to hold a maximum of 60 tons of goods and each container used must load at least 18 tons of goods. The goods to be loaded include five types: A, B, C, D, and E, with quantities of 120, 90, 300, 90, and 120 respectively. The weights are 0.5 tons for A, 1 ton for B, 0.4 tons for C, 0.6 tons for D, and 0.65 tons for E. Additionally, to meet specific usage requirements, every time A goods are loaded, at least 1 unit of C must also be loaded, but loading C alone does not require simultaneously loading A; and considering the demand limitation for D goods, each container must load at least 12 units of D.

Establish an operations research model so that the company can use the fewest number of containers to pack this batch of goods.

### Submission Format
- Provide a single row with `id` and `answer` columns.
- The answer must use the template `@value[value]`, where `value` is the numeric solution rounded as appropriate.

### Evaluation
- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported value.

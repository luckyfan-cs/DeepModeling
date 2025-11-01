# Mamo Easy 598 A Financial Advisor Is Planning To Allocate Investment Across Four

A financial advisor is planning to allocate investment across four categories: Stocks, Bonds, Mutual Funds, and Derivatives. The aim is to minimize the total risk score associated with the portfolio. The risk scores associated with each unit of investment are 3 for Stocks, 4 for Bonds, 2 for Mutual Funds, and 5 for Derivatives.\n\nThe allocation must adhere to the following constraints due to client preferences and regulatory requirements:\n- The combined investment in Stocks and Bonds must be at least \$1000K.\n- The difference between the investments in Mutual Funds and Derivatives should not exceed \$500K.\n- Investment in Stocks should exceed that in Mutual Funds by at least \$200K.\n- The sum of investments in Bonds and Derivatives should equal exactly \$1500K.\n\nGiven these conditions and considering that all investments are made in whole numbers due to transactional practicalities (in thousand dollars), what is the minimum total risk score for this portfolio given optimal allocations among these four categories? Provide your answer rounded to the nearest whole number.

### Submission Format
- Provide a single row with `id` and `answer` columns.
- The answer must use the template `@cost[value]`, where `value` is the numeric solution rounded as appropriate.

### Evaluation
- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported value.

# Bwor 0 A Candy Factory Uses Raw Materials A B And C To Produce Three Different B

A candy factory uses raw materials A, B, and C to produce three different brands of candy: Brand X, Brand Y, and Brand Z. The content proportions of A, B, and C in each brand, the costs of the raw materials, the monthly usage limits for each raw material, as well as the unit processing cost and selling price of each candy brand are shown in Table 1-17.The question is: How many kilograms of each brand of candy should the factory produce each month in order to maximize its profit?Please formulate a linear programming mathematical model for this problem.
\begin{table}[h]
    \centering
    \caption{Raw Materials and Candy Production Data}
    \renewcommand{\arraystretch}{1.2}
    \begin{tabular}{c|ccc|c|c}
        \toprule
        Raw Materials & X & Y & Z & Raw Material Cost(dollar/kg) & Monthly Usage Limit(kg) \\
        \midrule
        A & $\geq 60\%$ & $\geq 30\%$ & & 2.00 & 2000 \\
        B & & & & 1.50 & 2500 \\
        C & $\leq 20\%$ & $\leq 50\%$ & $\leq 60\%$ & 1.00 & 1200 \\
        \midrule
        Processing Cost(dollar/kg) & 0.50 & 0.40 & 0.30 & & \\
        Selling Price(dollar/kg) & 3.40 & 2.85 & 2.25 & & \\
        \bottomrule
    \end{tabular}
\end{table}

### Submission Format
- Provide a single row with `id` and `answer` columns.
- The answer must use the template `@profit[value]`, where `value` is the numeric solution rounded as appropriate.

### Evaluation
- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported value.

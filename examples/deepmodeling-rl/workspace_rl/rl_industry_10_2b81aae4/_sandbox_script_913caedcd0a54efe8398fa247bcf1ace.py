To test the hypothesis, we will use Python's `scipy.optimize.linprog` function to solve the linear programming problem. We will formulate the constraints and the objective function accordingly.
from scipy.optimize import linprog

# Coefficients of the objective function (negative because we are minimizing the negative of the profit)
c = [-650, -725]

# Coefficients of the inequality constraints
A = [
    [20, 0],
    [5, 7],
    [3, 6]
]

# Right-hand side of the inequality constraints
b = [120, 80, 40]

# Bounds for the variables (x_A and x_B)
x_bounds = (5, None)  # x_A must be at least 5

# Solve the linear programming problem
result = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, (0, None)], method='highs')

# Extract the optimal solution
x_A_opt = result.x[0]
x_B_opt = result.x[1]
profit = -result.fun  # Convert back to positive profit

# Since the model is linear and we want to minimize idle time, we can check the utilization of each process
utilization = [120 / (20 * x_A_opt), 80 / (5 * x_A_opt + 7 * x_B_opt), 40 / (3 * x_A_opt + 6 * x_B_opt)]

# Output the results
print(f"Optimal number of type A motorcycles: {x_A_opt}")
print(f"Optimal number of type B motorcycles: {x_B_opt}")
print(f"Total profit: {profit}")
print(f"Utilization of manufacturing: {utilization[0]:.2f}")
print(f"Utilization of assembly: {utilization[1]:.2f}")
print(f"Utilization of inspection: {utilization[2]:.2f}")
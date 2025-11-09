import pulp

# Define the problem
prob = pulp.LpProblem("MaximizeProtein", pulp.LpMaximize)

# Variables
x1 = pulp.LpVariable('Chicken', lowBound=0)  # weight of chicken in grams
x2 = pulp.LpVariable('Salmon', lowBound=0)   # weight of salmon in grams
x3 = pulp.LpVariable('Tofu', lowBound=0)     # weight of tofu in grams
x4 = pulp.LpVariable('Broccoli', lowBound=0) # number of 100g packs of broccoli
x5 = pulp.LpVariable('Carrots', lowBound=0)  # number of 100g packs of carrots
x6 = pulp.LpVariable('Spinach', lowBound=0)  # number of 100g packs of spinach
x7 = pulp.LpVariable('BellPepper', lowBound=0) # number of 100g packs of bell pepper
x8 = pulp.LpVariable('Mushrooms', lowBound=0) # number of 100g packs of mushrooms

# Objective function
prob += 23*x1 + 20*x2 + 8*x3 + 2.8*x4 + 0.9*x5 + 2.9*x6 + 1.0*x7 + 3.1*x8

# Constraints
prob += 3*x1 + 5*x2 + 1.5*x3 + 1.2*x4 + 0.8*x5 + 1.5*x6 + 1.0*x7 + 2*x8 <= 20
prob += x1 + x2 + x3 + 100*(x4 + x5 + x6 + x7 + x8) <= 800
prob += x4 + x5 + x6 + x7 + x8 >= 3

# Solve the problem
prob.solve()

# Output the solution
print(f"Total Protein: {pulp.value(prob.objective)}")
print(f"Chicken: {pulp.value(x1)} grams")
print(f"Salmon: {pulp.value(x2)} grams")
print(f"Tofu: {pulp.value(x3)} grams")
print(f"Broccoli: {pulp.value(x4)} packs")
print(f"Carrots: {pulp.value(x5)} packs")
print(f"Spinach: {pulp.value(x6)} packs")
print(f"Bell Pepper: {pulp.value(x7)} packs")
print(f"Mushrooms: {pulp.value(x8)} packs")
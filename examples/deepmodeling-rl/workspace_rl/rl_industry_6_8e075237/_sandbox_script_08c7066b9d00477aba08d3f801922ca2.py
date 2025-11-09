Here is the updated Python code for the experiment, which includes the installation of the `gurobipy` library:
import os
import pandas as pd
import gurobipy as gp
from gurobipy import GRB

# Check if gurobipy is installed
if 'gurobipy' not in os.sys.modules:
    import subprocess
    subprocess.check_call([os.sys.executable, '-m', 'pip', 'install', 'gurobipy'])

# Define the problem data
warehouses = ['Verona', 'Perugia', 'Rome', 'Pescara', 'Taranto', 'Lamezia']
ports = ['Genoa', 'Venice', 'Ancona', 'Naples', 'Bari']

# Supply and demand
supply = pd.Series([10, 12, 20, 24, 18, 40], index=warehouses)
demand = pd.Series([20, 15, 25, 33, 21], index=ports)

# Distances
distance = pd.DataFrame(
    [[290, 115, 355, 715, 810],
     [380, 340, 165, 380, 610],
     [505, 530, 285, 220, 450],
     [655, 450, 155, 240, 315],
     [1010, 840, 550, 305, 95],
     [1072, 1097, 747, 372, 333]],
    index=warehouses, columns=ports
)

# Cost per container per km
cost_per_km = 30

# Create a model
m = gp.Model("container_transport")

# Decision variables
x = m.addVars(warehouses, ports, vtype=GRB.INTEGER, name="x")

# Objective: Minimize total cost
m.setObjective(gp.quicksum(distance.loc[i, j] * cost_per_km * x[i, j] for i in warehouses for j in ports), GRB.MINIMIZE)

# Supply constraints
m.addConstrs((x.sum(i, '*') <= supply[i] for i in warehouses), name="supply")

# Demand constraints
m.addConstrs((x.sum('*', j) == demand[j] for j in ports), name="demand")

# Capacity constraints (each truck can carry up to 2 containers)
m.addConstrs((x[i, j] <= 2 for i in warehouses for j in ports), name="capacity")

# Solve the model
m.optimize()

# Extract the solution
solution = pd.DataFrame(index=warehouses, columns=ports)
for i in warehouses:
    for j in ports:
        if x[i, j].x > 0:
            solution.loc[i, j] = x[i, j].x

# Calculate the total cost
total_cost = m.objVal

# Print the solution
print(solution)
print(f"Total Cost: {total_cost}")
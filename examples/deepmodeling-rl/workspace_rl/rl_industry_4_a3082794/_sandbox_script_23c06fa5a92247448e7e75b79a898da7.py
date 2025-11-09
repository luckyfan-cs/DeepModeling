import pandas as pd

# Define the fiber content and cost per 100 grams for each food item
fiber_content = {'okra': 3.2, 'carrots': 2.7, 'celery': 1.6, 'cabbage': 2.0}
cost_per_100g = {'salmon': 4.0, 'beef': 3.6, 'pork': 1.8, 'okra': 2.6, 'carrots': 1.2, 'celery': 1.6, 'cabbage': 2.3}

# Calculate the cost per gram for each food item
cost_per_gram = {food: cost / 100 for food, cost in cost_per_100g.items()}

# Calculate the fiber content per gram for each food item
fiber_per_gram = {food: fiber / 100 for food, fiber in fiber_content.items()}

# Define the total food intake and budget
total_food_intake = 600
budget = 15

# Define the protein sources and their cost per gram
protein_sources = {'salmon': cost_per_gram['salmon'], 'beef': cost_per_gram['beef'], 'pork': cost_per_gram['pork']}

# Find the protein source with the lowest cost per gram
optimal_protein = min(protein_sources, key=protein_sources.get)

# Calculate the maximum possible fiber intake with the optimal protein source
max_fiber_with_protein = (total_food_intake - 100) * fiber_per_gram[optimal_protein] + 100 * fiber_per_gram['okra']  # Assuming 100 grams of okra for the protein source

# Calculate the remaining budget after buying the protein source
remaining_budget = budget - 100 * cost_per_gram[optimal_protein]

# Calculate the maximum possible fiber intake with the remaining budget
max_fiber_with_remaining_budget = (remaining_budget / total_food_intake) * (total_food_intake - 100) * max(fiber_per_gram['okra'], fiber_per_gram['carrots'], fiber_per_gram['celery'], fiber_per_gram['cabbage'])

# Calculate the total fiber intake
total_fiber_intake = max_fiber_with_protein + max_fiber_with_remaining_budget

# Calculate the grams of each vegetable to buy
grams_of_vegetables = (remaining_budget / total_food_intake) * (total_food_intake - 100) * max(fiber_per_gram['okra'], fiber_per_gram['carrots'], fiber_per_gram['celery'], fiber_per_gram['cabbage']) / max(fiber_per_gram['okra'], fiber_per_gram['carrots'], fiber_per_gram['celery'], fiber_per_gram['cabbage'])

# Calculate the grams of the protein source to buy
grams_of_protein = 100

# Create a DataFrame to store the results
results = pd.DataFrame({
    'id': [0],
    'answer': [total_fiber_intake]
})

# Save the results to a CSV file
results.to_csv('submission.csv', index=False)
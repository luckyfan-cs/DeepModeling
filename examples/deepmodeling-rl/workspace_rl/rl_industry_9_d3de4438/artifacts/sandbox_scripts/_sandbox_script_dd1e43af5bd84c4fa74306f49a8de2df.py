import pandas as pd

# Load the data
data = {
    'Area Code': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L'],
    'Residential Areas within 800 m Radius': [
        ['A', 'C', 'E', 'G', 'H', 'I'],
        ['B', 'H', 'I'],
        ['A', 'C', 'G', 'H', 'I'],
        ['D', 'J'],
        ['A', 'E', 'G'],
        ['F', 'J', 'K'],
        ['A', 'C', 'E', 'G'],
        ['A', 'B', 'C', 'H', 'I'],
        ['A', 'B', 'C', 'H', 'I'],
        ['D', 'F', 'J', 'K', 'L'],
        ['F', 'J', 'K', 'L'],
        ['J', 'K', 'L']
    ]
}

df = pd.DataFrame(data)

# Convert the list of residential areas into sets for easier manipulation
df['Residential Areas within 800 m Radius'] = df['Residential Areas within 800 m Radius'].apply(lambda x: set(x))

# Function to find the minimum number of chain stores
def find_min_chain_stores(residential_areas):
    remaining_areas = set.union(*residential_areas)
    chain_stores = []
    while remaining_areas:
        max_coverage = -1
        best_store = None
        for area in residential_areas:
            coverage = remaining_areas.intersection(area)
            if len(coverage) > max_coverage:
                max_coverage = len(coverage)
                best_store = area
        remaining_areas -= best_store
        chain_stores.append(best_store)
    return len(chain_stores)

min_chain_stores = find_min_chain_stores(df['Residential Areas within 800 m Radius'])
min_chain_stores
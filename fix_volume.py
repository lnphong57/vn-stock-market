import json

# Load the JSON file
with open('data/processed/price_history_processed.json', 'r') as f:
    data = json.load(f)

# Process each item in the array
for item in data:
    if 'transaction_value' in item:
        # Remove quotes by converting to int
        item['transaction_value'] = float(item['transaction_value'])

# Save back to the file
with open('data/processed/price_history_processed.json', 'w') as f:
    json.dump(data, f, indent=4)
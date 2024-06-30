import json

# Open and read the JSON file
with open('output.json', 'r') as f:
    data = json.load(f)

# Extract the data from the file
# items = data['items']

# Find the length of the total data
total_length = len(data)

print(total_length)

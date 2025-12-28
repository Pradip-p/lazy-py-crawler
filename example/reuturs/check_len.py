import json

# Load JSON data from file
with open('all.json', 'r') as f:
    data = json.load(f)

# Remove duplicates by converting to set and back to list
data = list(json.dumps(item, sort_keys=True) for item in data)
print(len(data))
# Convert back to original format
# data = [json.loads(item) for item in data]

# # Write new data to file
# with open('output_file.json', 'w') as f:
#     json.dump(data, f, indent=4)

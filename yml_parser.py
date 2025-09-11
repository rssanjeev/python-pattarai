from ruamel.yaml import YAML
import sys

# Load YAML from file
input_file = "input.yml"
yaml = YAML()
with open(input_file, "r") as f:
    data = yaml.load(f)

# Update column names to uppercase
for model in data.get('models', []):
    for column in model.get('columns', []):
        if 'name' in column:
            column['name'] = column['name'].upper()

# Output to console
yaml.dump(data, sys.stdout)

# Optional: Save to file
# with open("updated.yml", "w") as f:
#     yaml.dump(data, f)
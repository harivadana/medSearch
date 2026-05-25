import json

with open("data/processed/inverted_index.json", "r") as f:

    index = json.load(f)

print(index["asthma"])
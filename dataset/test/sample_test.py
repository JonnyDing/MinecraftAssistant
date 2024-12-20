import json
import random

# File paths
uploaded_file_path = "../train/lora/jsonl/minecraft_plus.jsonl"
output_file_path = "./test.jsonl"

# Load the JSONL data
data = []
with open(uploaded_file_path, "r", encoding="utf-8") as infile:
    for line in infile:
        data.append(json.loads(line.strip()))

# Randomly select 200 samples
random_samples = random.sample(data, min(200, len(data)))

# Save the random samples to a new JSONL file
with open(output_file_path, "w", encoding="utf-8") as outfile:
    for sample in random_samples:
        json.dump(sample, outfile, ensure_ascii=False)
        outfile.write("\n")


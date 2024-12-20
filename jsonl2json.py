import json
new_input_file_path = "dataset/train/lora/jsonl/minecraft_plus.jsonl"
new_output_file_path = "dataset/train/lora/minecraft_plus.json"

# Reading the newly uploaded JSONL file
new_converted_data = []
with open(new_input_file_path, "r", encoding="utf-8") as infile:
    for line in infile:
        item = json.loads(line.strip())
        new_converted_item = {
            "instruction": item.get("input", ""),
            "input": "",
            "output": item.get("target", ""),
        }
        new_converted_data.append(new_converted_item)

# Writing the converted data to a JSON file
with open(new_output_file_path, "w", encoding="utf-8") as json_file:
    json.dump(new_converted_data, json_file, ensure_ascii=False, indent=4)



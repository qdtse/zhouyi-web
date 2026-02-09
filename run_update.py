
import json
import os
import sys

# Add current directory to sys.path
sys.path.append(os.getcwd())

try:
    from update_zhuge_data import en_data_1
    from zhuge_en_part2 import en_data_2
except ImportError as e:
    print(f"Import Error: {e}")
    # Fallback: Read files and eval? No, too risky.
    # Check if files exist
    print(os.listdir())
    sys.exit(1)

full_en_data = {**en_data_1, **en_data_2}

json_path = "zhuge_data.json"
if not os.path.exists(json_path):
    print("zhuge_data.json not found")
    sys.exit(1)

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

count = 0
for item in data:
    idx = item["index"]
    if idx in full_en_data:
        item["poem_en"] = full_en_data[idx]["poem"]
        item["explain_en"] = full_en_data[idx]["explain"]
        count += 1

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Update Complete. Updated {count} entries.")

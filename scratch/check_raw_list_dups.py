import json
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

with open('data/raw_parsed_new_list.json', 'r', encoding='utf-8') as f:
    raw_list = json.load(f)

descs = [it['desc'].strip() for it in raw_list]
counts = Counter(descs)
dups_in_raw = {k: v for k, v in counts.items() if v > 1}

print(f"Total entries in raw list: {len(raw_list)}")
print(f"Unique descriptions in raw list: {len(counts)}")
print(f"Duplicate descriptions in raw list: {len(dups_in_raw)}")
for k, v in dups_in_raw.items():
    print(f"   '{k}': appears {v} times")

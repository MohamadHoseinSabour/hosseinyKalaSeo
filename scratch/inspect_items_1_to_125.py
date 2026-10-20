import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_candidates_harvested.json', encoding='utf-8') as f:
    items = json.load(f)

for i in range(0, 125):
    it = items[i]
    sheet = it.get('sheet_folder', '')
    brand = it.get('brand', '')
    parent = it.get('parent_name', '')
    name = it.get('name', '')
    cands = it.get('candidates', [])
    print(f"[{i+1}] ({sheet}) [{brand}] {parent} - {name}")
    for c_idx, c in enumerate(cands):
        print(f"     Cand {c_idx+1}: {c.get('matched_title')}")

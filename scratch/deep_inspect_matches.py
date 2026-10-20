import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_candidates_harvested.json', encoding='utf-8') as f:
    items = json.load(f)

print(f"Total items: {len(items)}\n")

for i, it in enumerate(items):
    name = it.get('name', '')
    parent = it.get('parent_name', '')
    brand = it.get('brand', '')
    cands = it.get('candidates', [])
    sheet = it.get('sheet_folder', '')
    
    # Check if any candidate has brand or significant word in title
    matching_cands = []
    for c in cands:
        t = c.get('matched_title', '')
        matching_cands.append(t)
        
    print(f"[{i+1}] ({sheet}) [{brand}] {parent} - {name}")
    for idx, t in enumerate(matching_cands):
        print(f"     Cand {idx+1}: {t}")

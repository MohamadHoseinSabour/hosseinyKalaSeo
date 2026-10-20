import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_candidates_harvested.json', encoding='utf-8') as f:
    items = json.load(f)

for i in range(0, 16):
    it = items[i]
    b = it.get('brand')
    p = it.get('parent_name')
    n = it.get('name')
    print(f"[{i+1}] [{b}] {p} -> {n}")
    for c_i, c in enumerate(it.get('candidates', [])):
        print(f"     Cand {c_i+1}: {c.get('matched_title')}")

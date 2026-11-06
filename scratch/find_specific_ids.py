import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/id_mappings.json', 'r', encoding='utf-8') as f:
    mappings = json.load(f)

for k, v in mappings.items():
    if isinstance(v, dict) and 'slug' in v:
        slug = v['slug']
        if any(x in slug for x in ['pro-omega-t7', 'dn-275', 'dn-950']):
            print(f"{slug} -> Real ID: {k}")

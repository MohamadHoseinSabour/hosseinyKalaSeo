import sys
import os
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_candidates_harvested.json', 'r', encoding='utf-8') as f:
    harv = json.load(f)

print(f"Total harvested items: {len(harv)}")
for i, item in enumerate(harv[:10]):
    print(f"Item {i+1}:")
    print(f"  Row: {item.get('row')}")
    print(f"  Name: {item.get('name')}")
    print(f"  Parent: {item.get('parent_name')}")
    print(f"  Brand: {item.get('brand')}")
    print(f"  Sheet: {item.get('sheet') or item.get('sheet_folder')}")
    print(f"  Candidates count: {len(item.get('candidates', []))}")
    if item.get('candidates'):
        print(f"  First candidate: {item['candidates'][0]}")

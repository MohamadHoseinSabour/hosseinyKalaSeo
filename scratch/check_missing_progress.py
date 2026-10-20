import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_61_products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

with open('scratch/creation_progress.json', 'r', encoding='utf-8') as f:
    progress = json.load(f)

print(f"Total products planned: {len(products)}")
print(f"Total completed in progress: {len(progress)}")

missing = []
for p in products:
    name = p['name']
    if name not in progress or not progress[name].get('live_verified'):
        missing.append(p)

print(f"Missing products count: {len(missing)}")
for m in missing:
    print(f"  - [{m['sheet']}] Row {m['row']}: {m['name']} ({m['type']})")

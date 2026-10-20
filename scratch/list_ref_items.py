import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/missing_products.json', encoding='utf-8') as f:
    missing = json.load(f)

with open('scratch/missing_products.json', encoding='utf-8') as f:
    missing = json.load(f)

sheets = {}
for m in missing:
    s = m.get('sheet', '')
    sheets.setdefault(s, []).append(m)

for s, items in sheets.items():
    print(f"\nSheet [{s}]: {len(items)} items")
    for idx, r in enumerate(items[:5]):
        p = r.get('parent_name')
        n = r.get('name')
        full = f"{p} -> {n}" if p else n
        print(f"  {idx+1}. Row {r.get('row')}: [{r.get('brand')}] {full}")

import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_candidates_harvested.json', encoding='utf-8') as f:
    items = json.load(f)

# Group by sheet/category
sheets = {}
for it in items:
    s = it.get('sheet_folder', 'other')
    sheets.setdefault(s, []).append(it)

print(f"Total items in harvested: {len(items)}")
for s, lst in sheets.items():
    print(f"\nCategory [{s}]: {len(lst)} items")
    for it in lst:
        p = it.get('parent_name')
        n = it.get('name')
        b = it.get('brand')
        full = f"{p} -> {n}" if p else n
        cands_count = len(it.get('candidates', []))
        print(f"  Row {it.get('row')}: [{b}] {full} ({cands_count} candidates)")

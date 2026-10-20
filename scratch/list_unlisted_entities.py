import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/catalog_current_rows.json', encoding='utf-8') as f:
    rows = json.load(f)

entities = []
curr = None
for r in rows:
    if not r['is_variation']:
        curr = {
            'sheet': r['sheet'],
            'folder': r['folder'],
            'parent_row': r['row'],
            'name': r['name'],
            'brand': r['brand'],
            'ptype': r['ptype'],
            'status': r['status'],
            'variations': []
        }
        entities.append(curr)
    else:
        if curr:
            curr['variations'].append(r)

unlisted = [p for p in entities if p['status'] == 'در سایت تعریف نشده']
print(f"Total Unlisted Entities: {len(unlisted)}")

for i, p in enumerate(unlisted, 1):
    vc = len(p['variations'])
    v_info = f"({vc} vars)" if vc > 0 else "single"
    sheet = p['sheet']
    prow = p['parent_row']
    brand = p['brand']
    pname = p['name']
    print(f"{i:2d}. [{sheet} | Row {prow}] [{brand}] {pname} {v_info}")

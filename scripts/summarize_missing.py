import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/missing_products.json', encoding='utf-8') as f:
    data = json.load(f)

parents = [p for p in data if not p.get('is_variation')]
variations = [p for p in data if p.get('is_variation')]

print(f"Total missing records: {len(data)}")
print(f"Parent products: {len(parents)}")
print(f"Variations: {len(variations)}")

by_sheet = {}
for p in parents:
    by_sheet.setdefault(p['sheet'], []).append(p)

for s, prods in by_sheet.items():
    print(f"\n==========================================")
    print(f"Sheet: {s} ({len(prods)} parent products)")
    print(f"==========================================")
    for p in prods:
        # find its variations if any
        vars_for_p = [v for v in variations if v.get('parent_name') == p['name'] and v['sheet'] == s]
        var_str = f" ({len(vars_for_p)} variations: " + ", ".join([v['name'] for v in vars_for_p]) + ")" if vars_for_p else ""
        print(f"• [Row {p['row']:2d}] [{p.get('brand')}] {p['name']}{var_str}")

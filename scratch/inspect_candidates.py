import sys
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/inventory_audit_summary.json', 'r', encoding='utf-8') as f:
    d = json.load(f)['new_products']

print(f"=== NEW PRODUCTS CANDIDATES ({len(d)}) ===")
by_cat = {}
for it in d:
    cat = it.get('suggested_cat', 'نامشخص')
    by_cat.setdefault(cat, []).append(it)

for cat, items in by_cat.items():
    print(f"\n--- {cat} ({len(items)} items) ---")
    for it in items:
        print(f"  [#{it['index']}] {it['raw_title']} (برند: {it['detected_brand']}, موجودی: {it['qty']})")

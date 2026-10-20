import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/missing_products.json', encoding='utf-8') as f:
    missing = json.load(f)

for sheet_name in ['یخچال و فریزر', 'شستشو و نظافت']:
    items = [m for m in missing if m.get('sheet') == sheet_name]
    print(f"\n==========================================")
    print(f"Sheet: {sheet_name} ({len(items)} items)")
    print(f"==========================================")
    for idx, r in enumerate(items):
        p = r.get('parent_name')
        n = r.get('name')
        b = r.get('brand')
        full = f"{p} -> {n}" if p else n
        print(f"{idx+1}. Row {r.get('row')}: [{b}] {full} | Type: {r.get('type')}")

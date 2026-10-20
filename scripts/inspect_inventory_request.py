import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

print(f"Total products in products.json: {len(products)}")

clover_prods = [p for p in products if 'کلور' in p.get('name', '') or 'clover' in p.get('slug', '').lower()]
for p in clover_prods:
    v_count = len(p.get('variations', []))
    print(f"ID: {p.get('id')}, Name: {p.get('name')}, Type: {p.get('type')}, Variations: {v_count}")
    if p.get('variations'):
        for v in p['variations']:
            print(f"   Var ID: {v.get('id')}, Name: {v.get('name')}, Attrs: {v.get('attributes')}")

print("\n--- Checking Pans / Frying pans (مایتابه / تابه) ---")
pan_prods = [p for p in products if any(w in p.get('name', '') for w in ['تابه', 'ماهیتابه', 'مایتابه'])]
for p in pan_prods:
    print(f"ID: {p.get('id')}, Name: {p.get('name')}, Type: {p.get('type')}")
    if p.get('variations'):
        for v in p['variations']:
            print(f"   Var ID: {v.get('id')}, Name: {v.get('name')}")

import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/current_catalog_reference.json', 'r', encoding='utf-8') as f:
    ref = json.load(f)

print("=== LIVE PRODUCTS: قابلمه OR تابه ===")
for p in ref['live_products']:
    name = p['name']
    if any(k in name for k in ['قابلمه', 'تابه', 'ماهیتابه', 'مایتابه']):
        print(f"ID: {p['id']}, Name: {name}, Type: {p.get('type')}")
        for v in p.get('variations', []):
            print(f"   Var: {v.get('variation_id')}, Attr: {v.get('attributes')}")

print("\n=== OLD EXCEL ITEMS: قابلمه OR تابه ===")
for it in ref['excel_items']:
    name = it.get('name', '')
    if any(k in name for k in ['قابلمه', 'تابه', 'ماهیتابه', 'مایتابه']):
        print(f"Name: {name} | PID: {it.get('product_id')} | VID: {it.get('variation_id')} | Cat: {it.get('main_cat')} | Sub: {it.get('subcat')}")

print("\n=== INVENTORY RAW CSV ITEMS: تابه OR مایتابه ===")
with open('data/inventory_incoming_raw.csv', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if any(k in line for k in ['تابه', 'مایتابه', 'ماهیتابه']):
            print(f"CSV Line: {line}")

import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

print("=== ALL REFRIGERATOR PRODUCTS IN PRODUCTS.JSON ===")
ref_prods = []
for p in products:
    name = p.get('name', '')
    cats = [c if isinstance(c, str) else c.get('name', '') for c in p.get('categories', [])]
    if any('یخچال' in c or 'فریزر' in c for c in cats) or any(k in name for k in ['یخچال', 'فریزر']):
        ref_prods.append(p)

print(f"Total refrigerator products: {len(ref_prods)}")
for p in ref_prods:
    print(f"\nID: {p['id']} | Type: {p.get('type')} | Name: {p['name']}")
    if p.get('variations'):
        for v in p['variations']:
            print(f"   Var ID: {v.get('id')} | Name: {v.get('name')} | Attrs: {v.get('attributes')} | Stock: {v.get('in_stock')} | Price: {v.get('regular_price')}")
    else:
        print(f"   Simple | Stock: {p.get('in_stock')} | Price: {p.get('regular_price')}")

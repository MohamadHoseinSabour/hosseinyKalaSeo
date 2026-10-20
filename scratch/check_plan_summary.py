import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_61_products.json', 'r', encoding='utf-8') as f:
    prods = json.load(f)

v_prods = [p for p in prods if p['type'] == 'variable']
s_prods = [p for p in prods if p['type'] == 'simple']
print(f"Total: {len(prods)}, Variable: {len(v_prods)}, Simple: {len(s_prods)}")

print("\n--- VARIABLE PRODUCTS ---")
for v in v_prods:
    var_names = [x['variant_attr'] or x['name'] for x in v['variations']]
    print(f"Parent: {v['name']} | Row {v['row']} | Vars ({len(v['variations'])}): {var_names}")

print("\n--- SAMPLE SIMPLE PRODUCTS (FIRST 5) ---")
for s in s_prods[:5]:
    print(f"Simple: {s['name']} | Row {s['row']} | Price: {s['price_rial']} | Slug: {s['slug']}")

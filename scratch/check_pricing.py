import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_61_products.json', 'r', encoding='utf-8') as f:
    prods = json.load(f)

priced = []
unpriced = []
for p in prods:
    has_price = False
    if p['price_rial']:
        has_price = True
    for v in p['variations']:
        if v['price_rial']:
            has_price = True
    if has_price:
        priced.append(p)
    else:
        unpriced.append(p)

print(f"Products with price: {len(priced)}")
print(f"Products without price: {len(unpriced)}")
for p in priced:
    print(f"  Priced: {p['name']} -> {p['price_rial']} (Vars: {[v['price_rial'] for v in p['variations']]})")

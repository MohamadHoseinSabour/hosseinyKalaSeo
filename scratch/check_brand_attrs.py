import sys
import json

sys.stdout.reconfigure(encoding='utf-8')
with open('data/products.json', encoding='utf-8') as f:
    products = json.load(f)

for p in products:
    attrs = p.get('attributes', [])
    for a in attrs:
        if a.get('name') == 'برند':
            opts = a.get('options', [])
            print(f"{p['id']}: {p['name'][:40]} -> {opts}")

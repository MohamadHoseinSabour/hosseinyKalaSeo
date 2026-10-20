import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

av_prods = [p for p in products if p.get('id') in [3516, 3534]]
for p in av_prods:
    print(f"ID: {p['id']}")
    print(f"Name: {p.get('name')}")
    print(f"Slug: {p.get('slug')}")
    print(f"SKU: {p.get('sku')}")
    print(f"Categories: {[c.get('name') if isinstance(c, dict) else c for c in p.get('categories', [])]}")
    print(f"Attributes: {p.get('attributes')}")
    print("---")

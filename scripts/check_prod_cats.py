import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

for p in products:
    cats = p.get('categories', [])
    cat_names = [c if isinstance(c, str) else c.get('name', '') for c in cats]
    print(f"ID {p['id']}: {p['name'][:40]} | Cats: {cat_names}")

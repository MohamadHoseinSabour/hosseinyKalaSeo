import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

for p in products:
    name = p.get('name', '')
    if 'تلویزیون' in name or 'اینچ' in name:
        print(f"ID: {p['id']} | Name: {name} | Slug: {p.get('slug')}")

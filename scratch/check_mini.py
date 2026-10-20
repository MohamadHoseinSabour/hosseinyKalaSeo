import json
import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

with open('data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

for p in products:
    name = p.get('name', '')
    if 'مینی' in name or 'کلور' in name:
        if 'مینی' in name:
            print(f"{p.get('id')}: {name}")
            for v in p.get('variations', []):
                print(f"   var: {v.get('attributes')}")

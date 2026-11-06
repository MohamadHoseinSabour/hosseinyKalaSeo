import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

for p in products:
    if p.get('id') == 2885 or 'bost-bvc' in str(p.get('slug', '')):
        print("ID:", p.get('id'))
        print("Name:", p.get('name'))
        print("Price:", p.get('price'))
        print("Regular Price:", p.get('regular_price'))
        print("Images:", [img.get('src') for img in p.get('images', [])][:2])
        print("Desc snippet:", str(p.get('description', ''))[:300])
        print("Attributes:", p.get('attributes'))
        break

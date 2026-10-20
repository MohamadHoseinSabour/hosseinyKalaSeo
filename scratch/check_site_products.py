import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data/products.json', encoding='utf-8') as f:
    products = json.load(f)

print(f"Total products on site: {len(products)}")

brands = ['کلور', 'هیمالیا', 'دوو', 'پاکشوما', 'دیپوینت', 'نیکسان', 'آلتون', 'دونالکس']
for b in brands:
    matched = [p for p in products if b in p.get('name', '')]
    print(f"\nBrand [{b}] on site: {len(matched)}")
    for p in matched:
        print(f"  - ID: {p.get('id')} | Name: {p.get('name')} | Slug: {p.get('slug')}")

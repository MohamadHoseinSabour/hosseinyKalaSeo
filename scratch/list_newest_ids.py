import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('data/products.json', 'r', encoding='utf-8') as f:
    site_products = json.load(f)

newest = [p for p in site_products if p.get('status') == 'publish']
newest.sort(key=lambda x: x['id'], reverse=True)

print('Top 40 newest products:')
for i, p in enumerate(newest[:40], 1):
    print(f"{i}. ID {p['id']}: {p['name']} | price: {p.get('price')} | slug: {p['slug']}")

import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('data/products.json', 'r', encoding='utf-8') as f:
    prods = json.load(f)

p_4100 = [p for p in prods if 4000 <= p.get('id', 0) < 4235 and p.get('status') == 'publish']
print(f"Products between 4000 and 4234: {len(p_4100)}")
for p in p_4100:
    print(f"ID {p['id']}: {p['name']} | slug: {p['slug']}")

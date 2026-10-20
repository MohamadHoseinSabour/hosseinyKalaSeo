import sys, json
sys.stdout.reconfigure(encoding='utf-8')

with open('data/products_raw.json', encoding='utf-8') as f:
    raw = json.load(f)

for p in raw:
    if p.get('variations'):
        print(f"Product ID {p['id']}: {p['name']}")
        for v in p['variations']:
            print(f"   vid={v['variation_id']}, attrs={v.get('attributes')}")

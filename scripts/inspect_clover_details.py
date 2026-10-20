import sys, json
sys.stdout.reconfigure(encoding='utf-8')

with open('data/products_raw.json', encoding='utf-8') as f:
    raw = json.load(f)

for pid in [2457, 2471, 2484, 2497]:
    p = next((x for x in raw if x['id'] == pid), None)
    if p:
        print(f"ID: {p['id']}, Name: {p['name']}, Type: {p['type']}")
        for v in p.get('variations', []):
            print(f"   Variation ID: {v['variation_id']}, Attrs: {v['attributes']}")

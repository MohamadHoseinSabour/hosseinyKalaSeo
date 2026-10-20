import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/live_products_check.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

with open('data/categories.json', 'r', encoding='utf-8') as f:
    cats = json.load(f)

cat_map = {c['id']: c for c in cats}

print("=== Checking all 96 products by category ===")
by_cat = {}
for p in products:
    p_cats = p.get('product_cat', [])
    for cid in p_cats:
        cname = cat_map.get(cid, {}).get('name', str(cid))
        by_cat.setdefault(f"{cid}: {cname}", []).append((p['id'], p['title']['rendered']))

for cname, prods in sorted(by_cat.items()):
    print(f"\n📂 {cname} ({len(prods)} products):")
    for pid, title in prods:
        print(f"   - [{pid}] {title}")

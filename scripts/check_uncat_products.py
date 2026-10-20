import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/live_products_check.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

with open('data/categories.json', 'r', encoding='utf-8') as f:
    cats = json.load(f)

cat_map = {c['id']: c for c in cats}

print("=== Checking for Uncategorized or Empty Categories ===")
uncat_products = []
for p in products:
    p_cats = p.get('product_cat', [])
    if not p_cats or any(cid in [1, 15] for cid in p_cats):
        uncat_products.append(p)

print(f"Uncategorized products: {len(uncat_products)}")
for p in uncat_products:
    print(f"  ID: {p['id']} | Title: {p['title']['rendered']} | Cats: {p.get('product_cat')}")

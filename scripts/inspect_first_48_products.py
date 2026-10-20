import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/live_products_check.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

with open('data/categories.json', 'r', encoding='utf-8') as f:
    cats = json.load(f)

cat_map = {c['id']: c['name'] for c in cats}

for i, p in enumerate(sorted(products, key=lambda x: x['id'])[:48], 1):
    pid = p['id']
    title = p['title']['rendered']
    p_cats = p.get('product_cat', [])
    cat_names = [f"{cid}:{cat_map.get(cid, str(cid))}" for cid in p_cats]
    print(f"#{i:<2} | ID: {pid:<5} | Cats: {', '.join(cat_names):<40} | Title: {title}")

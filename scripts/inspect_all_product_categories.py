import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# 1. Fetch all categories to have ID -> Name map
r_cats = requests.get('https://hosseinykala.ir/wp-json/wp/v2/product_cat?per_page=100', auth=AUTH, headers=HEADERS, timeout=30)
cats = r_cats.json()
cat_map = {c['id']: c for c in cats}

# 2. Fetch all products
all_products = []
page = 1
while True:
    r_prods = requests.get(f'https://hosseinykala.ir/wp-json/wp/v2/product?per_page=100&page={page}', auth=AUTH, headers=HEADERS, timeout=30)
    if r_prods.status_code == 200:
        batch = r_prods.json()
        if not batch:
            break
        all_products.extend(batch)
        page += 1
    else:
        break

print(f"Total products fetched: {len(all_products)}")

# Save products to scratch/live_products_check.json
with open('data/live_products_check.json', 'w', encoding='utf-8') as f:
    json.dump(all_products, f, ensure_ascii=False, indent=2)

# Inspect products in vacuum cleaner (category 21) or any subcategory of 21
vacuum_cat_ids = {21, 160, 161, 162}
print("\n=== Products in Vacuum Cleaner Categories (IDs: 21, 160, 161, 162) ===")
for p in all_products:
    prod_cat_ids = set(p.get('product_cat', []))
    if prod_cat_ids.intersection(vacuum_cat_ids):
        cat_names = [cat_map.get(cid, {}).get('name', str(cid)) for cid in prod_cat_ids]
        print(f"ID: {p['id']:<5} | Title: {p['title']['rendered'][:45]:<45} | Cats: {cat_names}")

print("\n=== Full List of All Products and their Assigned Categories ===")
for p in sorted(all_products, key=lambda x: x['id']):
    prod_cat_ids = p.get('product_cat', [])
    cat_names = [cat_map.get(cid, {}).get('name', str(cid)) for cid in prod_cat_ids]
    title = p.get('title', {}).get('rendered', '')
    print(f"ID: {p['id']:<5} | Title: {title:<50} | Cats: {cat_names}")

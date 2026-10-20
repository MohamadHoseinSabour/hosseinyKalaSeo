import json
import os
import sys
import requests

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

PROJECT_DIR = r"c:\Users\mmhhs\OneDrive\Documents\GitHub\hosseinyKalaSeo"
DATA_DIR = os.path.join(PROJECT_DIR, 'data')

# 1. Load categories
with open(os.path.join(DATA_DIR, 'categories.json'), 'r', encoding='utf-8') as f:
    cats = json.load(f)
cat_map = {c['id']: c['name'] for c in cats}

# 2. Fetch live product categories from site for all 96 products
print("Fetching live product terms from site...")
all_live_products = []
page = 1
while True:
    r = requests.get(f"https://hosseinykala.ir/wp-json/wp/v2/product?per_page=100&page={page}", auth=AUTH, headers=HEADERS, timeout=30)
    if r.status_code == 200:
        batch = r.json()
        if not batch:
            break
        all_live_products.extend(batch)
        page += 1
    else:
        break

print(f"Fetched {len(all_live_products)} products from live site.")
live_cat_by_id = {p['id']: p.get('product_cat', []) for p in all_live_products}

# 3. Update products_raw.json
raw_file = os.path.join(DATA_DIR, 'products_raw.json')
with open(raw_file, 'r', encoding='utf-8') as f:
    products_raw = json.load(f)

updated_count = 0
for p in products_raw:
    pid = p['product_id']
    if pid in live_cat_by_id:
        live_cids = live_cat_by_id[pid]
        live_cnames = [cat_map.get(cid, str(cid)) for cid in live_cids]
        if set(p.get('category_ids', [])) != set(live_cids):
            print(f"Updating products_raw.json for #{pid} '{p['name'][:30]}': {p.get('categories')} -> {live_cnames}")
            p['category_ids'] = live_cids
            p['categories'] = live_cnames
            updated_count += 1
        else:
            # ensure names are synced
            p['categories'] = live_cnames

with open(raw_file, 'w', encoding='utf-8') as f:
    json.dump(products_raw, f, ensure_ascii=False, indent=2)
print(f"\nSaved updated products_raw.json ({updated_count} products updated).")

# 4. Update products.json
prod_file = os.path.join(DATA_DIR, 'products.json')
with open(prod_file, 'r', encoding='utf-8') as f:
    products_json = json.load(f)

for p in products_json:
    pid = p.get('product_id') or p.get('id')
    if pid in live_cat_by_id:
        live_cids = live_cat_by_id[pid]
        live_cnames = [cat_map.get(cid, str(cid)) for cid in live_cids]
        p['categories'] = live_cnames
        p['category'] = live_cnames[0] if live_cnames else ""

with open(prod_file, 'w', encoding='utf-8') as f:
    json.dump(products_json, f, ensure_ascii=False, indent=2)
print(f"Saved updated products.json.")

# 5. Regenerate Excel files
print("\nRegenerating Excel catalogs...")
import subprocess
result = subprocess.run([sys.executable, os.path.join(PROJECT_DIR, 'scripts', 'update_full_catalog_excel.py')], capture_output=True, text=True, encoding='utf-8')
print("Excel update output:\n", result.stdout)
if result.stderr:
    print("Excel update errors:\n", result.stderr)

print("=== Done! ===")

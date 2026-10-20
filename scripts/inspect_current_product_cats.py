import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# 1. Fetch all product_cat
page = 1
all_cats = []
while True:
    try:
        r = requests.get(f'https://hosseinykala.ir/wp-json/wp/v2/product_cat?per_page=100&page={page}', auth=AUTH, headers=headers, timeout=25)
        if r.status_code == 200:
            batch = r.json()
            if not batch:
                break
            all_cats.extend(batch)
            page += 1
        else:
            break
    except Exception as e:
        print(f"Error fetching page {page}: {e}")
        break

print(f"Total product_cat items in WooCommerce: {len(all_cats)}")

# Check if 238 exists
c238 = next((c for c in all_cats if c['id'] == 238), None)
if c238:
    print(f"Found test cat 238: {c238['name']}. Deleting it...")
    try:
        rd = requests.delete('https://hosseinykala.ir/wp-json/wp/v2/product_cat/238?force=true', auth=AUTH, headers=headers, timeout=25)
        print(f"Delete result: {rd.status_code}")
        all_cats = [c for c in all_cats if c['id'] != 238]
    except Exception as e:
        print(f"Delete error: {e}")

# Save to scratch/categories_live.json
with open('data/categories_live.json', 'w', encoding='utf-8') as f:
    json.dump(all_cats, f, ensure_ascii=False, indent=2)

roots = [c for c in all_cats if c.get('parent', 0) == 0]
children = [c for c in all_cats if c.get('parent', 0) != 0]

print(f"\n--- Root Categories (Parent = 0): {len(roots)} ---")
for c in sorted(roots, key=lambda x: x['name']):
    print(f"ID: {c['id']:<4} | Count: {c.get('count', 0):<3} | Name: {c['name']:<25} | Slug: {c['slug']}")

print(f"\n--- Subcategories (Parent != 0): {len(children)} ---")
for c in sorted(children, key=lambda x: (x.get('parent', 0), x['name'])):
    p = next((x for x in all_cats if x['id'] == c.get('parent')), None)
    pname = p['name'] if p else str(c.get('parent'))
    print(f"ID: {c['id']:<4} | Parent: {c.get('parent'):<4} ({pname:<18}) | Count: {c.get('count', 0):<3} | Name: {c['name']:<25} | Slug: {c['slug']}")

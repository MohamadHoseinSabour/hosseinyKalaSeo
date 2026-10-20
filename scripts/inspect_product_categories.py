import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

r = requests.get('https://hosseinykala.ir/wp-json/wp/v2/product_cat?per_page=100', auth=AUTH, headers=headers)
if r.status_code == 200:
    cats = r.json()
    print(f"Total product_cat items in WooCommerce: {len(cats)}\n")
    
    roots = [c for c in cats if c.get('parent', 0) == 0]
    children = [c for c in cats if c.get('parent', 0) != 0]
    
    print(f"--- Root Categories (Parent = 0): {len(roots)} ---")
    for c in sorted(roots, key=lambda x: x['name']):
        print(f"ID: {c['id']:<4} | Count: {c.get('count', 0):<3} | Name: {c['name']:<25} | Slug: {c['slug']}")
        
    print(f"\n--- Subcategories (Parent != 0): {len(children)} ---")
    for c in sorted(children, key=lambda x: (x.get('parent', 0), x['name'])):
        parent_cat = next((p for p in cats if p['id'] == c.get('parent')), None)
        pname = parent_cat['name'] if parent_cat else str(c.get('parent'))
        print(f"ID: {c['id']:<4} | Parent: {c.get('parent'):<4} ({pname:<18}) | Count: {c.get('count', 0):<3} | Name: {c['name']:<25} | Slug: {c['slug']}")
else:
    print(f"Failed to fetch product_cat: {r.status_code}")

import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')
AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

r = requests.get('https://hosseinykala.ir/wp-json/wp/v2/product_cat?per_page=100', auth=AUTH, headers=headers, timeout=15)
if r.status_code == 200:
    cats = r.json()
    print(f"Total cats: {len(cats)}")
    roots = [c for c in cats if c.get('parent', 0) == 0]
    print(f"Roots count: {len(roots)}")
    for rc in roots:
        print(f"  Root: {rc['id']} - {rc['name']} ({rc['slug']})")

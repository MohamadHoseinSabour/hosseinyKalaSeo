import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'User-Agent': 'Mozilla/5.0'}

r = requests.get('https://hosseinykala.ir/wp-json/wp/v2/product_cat?per_page=100', auth=AUTH, headers=headers, timeout=25)
if r.status_code == 200:
    cats = r.json()
    clean_cats = []
    for c in cats:
        clean_cats.append({
            'id': c['id'],
            'name': c['name'],
            'slug': c['slug'],
            'url': c['link'],
            'parent': c.get('parent', 0),
            'count': c.get('count', 0),
            'description': c.get('description', '')
        })
    clean_cats = sorted(clean_cats, key=lambda x: x['id'])
    with open('data/categories.json', 'w', encoding='utf-8') as f:
        json.dump(clean_cats, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(clean_cats)} categories to data/categories.json.")
    
    roots = [c for c in clean_cats if c['parent'] == 0]
    print(f"Root categories ({len(roots)}):")
    for rc in roots:
        print(f"  [{rc['id']}] {rc['name']} ({rc['url']})")

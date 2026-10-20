import sys
import json
import requests

sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {'User-Agent': 'Mozilla/5.0'}
WC_URL = 'https://hosseinykala.ir/wp-json/wc/v3/products'

for pid in [3546, 3534, 3516, 2637, 2408]:
    r = requests.get(f'{WC_URL}/{pid}', auth=AUTH, headers=HEADERS, timeout=20)
    if r.status_code == 200:
        data = r.json()
        cats = [c.get('name') for c in data.get('categories', [])]
        print(f"ID {pid}: Name='{data.get('name')}' | Slug='{data.get('slug')}' | Cats={cats}")
        for a in data.get('attributes', []):
            if a.get('name') == 'برند':
                print(f"   Brand Attribute: {a.get('options')}")

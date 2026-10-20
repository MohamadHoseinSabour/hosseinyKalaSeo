import requests
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'User-Agent': 'Mozilla/5.0'}

for pid in [2680, 3453, 2972, 3395, 3266]:
    try:
        r = requests.get(f'https://hosseinykala.ir/wp-json/wp/v2/product/{pid}', auth=AUTH, headers=headers, timeout=10)
        print(f"Product {pid}: HTTP {r.status_code}")
        if r.status_code == 200:
            d = r.json()
            title = d.get('title', {}).get('rendered', '')
            slug = d.get('slug', '')
            link = d.get('link', '')
            status = d.get('status', '')
            print(f"   Title: {title}")
            print(f"   Slug: {slug}")
            print(f"   Link: {link}")
            print(f"   Status: {status}")
    except Exception as e:
        print(f"Product {pid}: Error {e}")

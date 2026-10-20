import requests
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {'User-Agent': 'Mozilla/5.0'}

pids = [3626, 4095, 3494, 3709, 4068]
for pid in pids:
    r = requests.get(f'https://hosseinykala.ir/wp-json/wc/v3/products/{pid}', auth=AUTH, headers=HEADERS, timeout=15)
    if r.status_code == 200:
        p = r.json()
        print(f"ID {pid}: {p.get('name')}")
        print(f"  slug: {p.get('slug')}")
        print(f"  stock: {p.get('stock_status')}")
        print(f"  price: {p.get('price')} | reg: {p.get('regular_price')} | sale: {p.get('sale_price')}")
        print(f"  categories: {[c.get('name') for c in p.get('categories', [])]}")

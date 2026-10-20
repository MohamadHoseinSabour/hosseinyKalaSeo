import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')
AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

r = requests.get('https://hosseinykala.ir/wp-json/wp/v2/product?product_cat=21&per_page=100', auth=AUTH, headers=headers, timeout=30)
if r.status_code == 200:
    prods = r.json()
    print(f"Total products in category 21 (جاروبرقی): {len(prods)}")
    for p in prods:
        print(f"  ID: {p['id']} | Title: {p['title']['rendered']}")

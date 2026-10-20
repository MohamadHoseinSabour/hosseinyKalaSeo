import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

r = requests.get('https://hosseinykala.ir/wp-json/wp/v2/product/2972', auth=AUTH, headers=headers, timeout=20)
if r.status_code == 200:
    p = r.json()
    print("Keys in wp/v2/product:", list(p.keys()))
    print("Price fields:", {k: v for k, v in p.items() if 'price' in k.lower() or 'stock' in k.lower()})
    print("product_cat:", p.get('product_cat'))
    print("meta:", p.get('meta'))

import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')
AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

r = requests.get('https://hosseinykala.ir/wp-json/wp/v2/product/2972', auth=AUTH, headers=headers, timeout=30)
if r.status_code == 200:
    p = r.json()
    print("Product 2972 categories on site now:", p.get('product_cat'))
else:
    print("Error:", r.status_code)

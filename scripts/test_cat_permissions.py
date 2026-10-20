import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')
AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

r = requests.options('https://hosseinykala.ir/wp-json/wp/v2/product_cat', auth=AUTH, headers=headers)
print(f"OPTIONS product_cat: {r.status_code}, Allow: {r.headers.get('Allow')}")

r2 = requests.options('https://hosseinykala.ir/wp-json/wp/v2/product_cat/92', auth=AUTH, headers=headers)
print(f"OPTIONS product_cat/92: {r2.status_code}, Allow: {r2.headers.get('Allow')}")

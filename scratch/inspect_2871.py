import requests
from requests.auth import HTTPBasicAuth

headers = {'User-Agent': 'Mozilla/5.0'}
resp = requests.get('https://hosseinykala.ir/wp-json/wp/v2/product/2871?context=edit', auth=HTTPBasicAuth('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto'), headers=headers, timeout=30)
if resp.status_code == 200:
    data = resp.json()
    print("Name:", data.get('title', {}).get('raw'))
    print("Slug:", data.get('slug'))
    print("Categories:", data.get('product_cat'))
    print("Excerpt:", data.get('excerpt', {}).get('raw'))
    print("Description raw:", data.get('content', {}).get('raw')[:400])

import requests
from requests.auth import HTTPBasicAuth

headers = {'User-Agent': 'Mozilla/5.0'}
resp = requests.get('https://hosseinykala.ir/wp-json/wp/v2/product/3546', auth=HTTPBasicAuth('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto'), headers=headers, timeout=30)
print("Status:", resp.status_code)
if resp.status_code == 200:
    data = resp.json()
    print("Name:", data.get('title', {}).get('raw') or data.get('title', {}).get('rendered'))
    print("Slug:", data.get('slug'))
    print("Link:", data.get('link'))
    print("Categories:", data.get('product_cat') or data.get('categories'))
    print("Content rendered length:", len(data.get('content', {}).get('rendered', '')))
    print("Content raw:", data.get('content', {}).get('raw'))
    print("Excerpt:", data.get('excerpt', {}).get('rendered'))
else:
    print("Error:", resp.text[:300])

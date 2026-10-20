import requests
from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'User-Agent': 'Mozilla/5.0'}
resp = requests.get('https://hosseinykala.ir/wp-json/wp/v2/product/3840?context=edit', auth=auth, headers=headers, timeout=30)
if resp.status_code == 200:
    data = resp.json()
    print("Name:", data.get('title', {}).get('raw'))
    print("Slug:", data.get('slug'))
    print("Categories:", data.get('product_cat'))
    print("Content:", data.get('content', {}).get('raw')[:400])
    print("Status:", data.get('status'))
else:
    print("Error:", resp.status_code, resp.text[:200])

import requests
from requests.auth import HTTPBasicAuth
import json

headers = {'User-Agent': 'Mozilla/5.0'}
resp = requests.get('https://hosseinykala.ir/wp-json/wp/v2/product/3546?context=edit', auth=HTTPBasicAuth('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto'), headers=headers, timeout=30)
data = resp.json()
print("Content raw:")
print(data.get('content', {}).get('raw'))

with open('data/categories.json', 'r', encoding='utf-8') as f:
    cats = json.load(f)

for c in cats:
    c_name = c.get('name', '')
    if 'ظرفشویی' in c_name or 'کلور' in c_name:
        print(f"Cat ID: {c.get('id')}, Name: {c_name}, Slug: {c.get('slug')}, URL: {c.get('url')}")

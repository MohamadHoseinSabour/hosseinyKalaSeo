import json
import requests
from requests.auth import HTTPBasicAuth

with open('data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

p3546 = next((p for p in products if p.get('id') == 3546), None)
print("From products.json:")
if p3546:
    print(f"Name: {p3546.get('name')}")
    print(f"Slug: {p3546.get('slug')}")
    print(f"Categories: {p3546.get('categories')}")
    print(f"Attributes: {p3546.get('attributes')}")
    print(f"Description excerpt: {p3546.get('description', '')[:300]}")
    print(f"Short description: {p3546.get('short_description', '')}")

# Check live from site
resp = requests.get('https://hosseinykala.ir/wp-json/wc/v3/products/3546', auth=HTTPBasicAuth('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto'), timeout=30)
if resp.status_code == 200:
    data = resp.json()
    print("\nLive from WooCommerce API:")
    print(f"Name: {data.get('name')}")
    print(f"Slug: {data.get('slug')}")
    print(f"Permalink: {data.get('permalink')}")
    print(f"Categories: {data.get('categories')}")
    print(f"Attributes: {data.get('attributes')}")
    print(f"Description excerpt: {data.get('description', '')[:400]}")

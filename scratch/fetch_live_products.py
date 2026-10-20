import requests
from requests.auth import HTTPBasicAuth
import json

auth = HTTPBasicAuth('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'User-Agent': 'Mozilla/5.0'}

all_products = []
page = 1
while True:
    print(f"Fetching page {page}...")
    resp = requests.get(
        f'https://hosseinykala.ir/wp-json/wp/v2/product?per_page=100&page={page}&context=edit',
        auth=auth,
        headers=headers,
        timeout=60
    )
    if resp.status_code != 200:
        print(f"Finished or error at page {page}: {resp.status_code}")
        break
    data = resp.json()
    if not data:
        break
    all_products.extend(data)
    print(f"Got {len(data)} products (total: {len(all_products)})")
    if len(data) < 100:
        break
    page += 1

print(f"Total products fetched from site: {len(all_products)}")
with open('scratch/live_wp_products.json', 'w', encoding='utf-8') as f:
    json.dump(all_products, f, ensure_ascii=False, indent=2)

print("Saved to scratch/live_wp_products.json")

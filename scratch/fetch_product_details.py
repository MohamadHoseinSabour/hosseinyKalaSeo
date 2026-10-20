import requests
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

def get_product(pid):
    url = f'https://hosseinykala.ir/wp-json/wc/v3/products/{pid}'
    res = requests.get(url, auth=AUTH, headers=HEADERS, timeout=15)
    if res.status_code == 200:
        return res.json()
    return None

# Let's inspect IDs 3626, 4095, 3494, 4068, 3709
for pid in [3626, 4095, 3494, 4068, 3709]:
    p = get_product(pid)
    if p:
        print(f"=== Product ID {pid} ===")
        print(f"Name: {p.get('name')}")
        print(f"Slug: {p.get('slug')}")
        print(f"Type: {p.get('type')}")
        print(f"Status: {p.get('status')}")
        print(f"Stock: {p.get('stock_status')}")
        print(f"Price: {p.get('price')} | Reg: {p.get('regular_price')} | Sale: {p.get('sale_price')}")
        print(f"Categories: {p.get('categories')}")
        print(f"Images: {[img.get('src') for img in p.get('images', [])]}")
        print(f"Short Desc: {p.get('short_description', '')[:100]}")
        print(f"Desc snippet: {p.get('description', '')[:150]}")
        print(f"Attributes: {p.get('attributes')}")
        print()

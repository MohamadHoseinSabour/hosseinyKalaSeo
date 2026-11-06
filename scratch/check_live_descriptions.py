import sys
import json
import requests
from requests.auth import HTTPBasicAuth

sys.stdout.reconfigure(encoding='utf-8')

AUTH = HTTPBasicAuth('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
BASE_URL = 'https://hosseinykala.ir/wp-json/wc/v3/products/'

# Let's inspect some of the 44 products:
with open('scratch/published_44_products_result.json', 'r', encoding='utf-8') as f:
    p44 = json.load(f)

print(f"Total in published_44_results: {len(p44)}")

sample_44 = list(p44.values())[:5]
for item in sample_44:
    pid = item['product_id']
    res = requests.get(f"{BASE_URL}{pid}", auth=AUTH, timeout=15)
    if res.status_code == 200:
        d = res.json()
        desc = d.get('description', '')
        s_desc = d.get('short_description', '')
        print(f"PID {pid} ({d.get('name')[:30]}):")
        print(f"  - description length: {len(desc)} characters")
        print(f"  - short_description length: {len(s_desc)} characters")

print("\n--- Checking the 2 new products (Candy, Olive) ---")
for pid in [4492, 4494]:
    res = requests.get(f"{BASE_URL}{pid}", auth=AUTH, timeout=15)
    if res.status_code == 200:
        d = res.json()
        desc = d.get('description', '')
        s_desc = d.get('short_description', '')
        print(f"PID {pid} ({d.get('name')[:30]}):")
        print(f"  - description length: {len(desc)} characters")
        print(f"  - short_description length: {len(s_desc)} characters")

print("\n--- Checking the 5 TVs ---")
for pid in [4497, 4499, 4501, 4503, 4505]:
    res = requests.get(f"{BASE_URL}{pid}", auth=AUTH, timeout=15)
    if res.status_code == 200:
        d = res.json()
        desc = d.get('description', '')
        s_desc = d.get('short_description', '')
        print(f"PID {pid} ({d.get('name')[:30]}):")
        print(f"  - description length: {len(desc)} characters")
        print(f"  - short_description length: {len(s_desc)} characters")

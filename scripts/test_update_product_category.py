import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Content-Type': 'application/json'
}

# Update product 2972
payload = {
    'product_cat': [92, 153]
}
r = requests.post('https://hosseinykala.ir/wp-json/wp/v2/product/2972', auth=AUTH, headers=headers, json=payload, timeout=25)
print(f"Update 2972 status: {r.status_code}")
if r.status_code == 200:
    p = r.json()
    print("New categories:", p.get('product_cat'))
else:
    print("Error:", r.text[:300])

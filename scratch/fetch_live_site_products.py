import sys
import requests
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
BASE_URL = 'https://hosseinykala.ir'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

# Fetch all products (page 1 to end)
page = 1
all_products = []
while True:
    url = f"{BASE_URL}/wp-json/wc/v3/products?per_page=50&page={page}"
    resp = requests.get(url, auth=AUTH, headers=HEADERS, timeout=30)
    if resp.status_code != 200:
        break
    items = resp.json()
    if not items:
        break
    all_products.extend(items)
    print(f"Page {page}: fetched {len(items)} products (total so far: {len(all_products)})")
    page += 1

print(f"Total products fetched: {len(all_products)}")

# Check variable products and fetch their variations
all_variations = {}
for p in all_products:
    if p.get('type') == 'variable':
        parent_id = p['id']
        var_url = f"{BASE_URL}/wp-json/wc/v3/products/{parent_id}/variations?per_page=50"
        var_resp = requests.get(var_url, auth=AUTH, headers=HEADERS, timeout=30)
        if var_resp.status_code == 200:
            vars_list = var_resp.json()
            all_variations[parent_id] = vars_list
            print(f"Parent ID {parent_id} ({p['name'][:30]}): {len(vars_list)} variations")

total_vars = sum(len(v) for v in all_variations.values())
print(f"Total variations fetched: {total_vars}")

# Save snapshot to scratch/site_products_live.json
snapshot = {
    'products': all_products,
    'variations': all_variations
}
with open('scratch/site_products_live.json', 'w', encoding='utf-8') as f:
    json.dump(snapshot, f, ensure_ascii=False, indent=2)

print("Saved snapshot to scratch/site_products_live.json")

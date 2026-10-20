import os
import sys
import time
import requests

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.sync_excel_prices_to_website import load_catalog_prices, BASE_URL, AUTH, HEADERS, commit_catalog_prices, CATALOG_PATH

simple_products, _, _ = load_catalog_prices()

# The first 50 simple products that timed out in the 50-item batch
batch_1 = simple_products[:50]
print(f"Retrying {len(batch_1)} simple products in smaller chunks of 15...")

chunk_size = 15
total_updated = 0

for i in range(0, len(batch_1), chunk_size):
    chunk = batch_1[i:i + chunk_size]
    payload = {
        'update': [
            {
                'id': p['id'],
                'regular_price': p['regular_price'],
                'sale_price': p['sale_price'],
                'stock_status': p.get('stock_status', 'instock')
            }
            for p in chunk
        ]
    }

    url = f"{BASE_URL}/wp-json/wc/v3/products/batch"
    resp = requests.post(url, auth=AUTH, headers=HEADERS, json=payload, timeout=60)
    if resp.status_code == 200:
        data = resp.json()
        updated_list = data.get('update', [])
        total_updated += len(updated_list)
        print(f"   Chunk {i // chunk_size + 1}: Successfully updated {len(updated_list)} simple products.")
    else:
        print(f"   [ERROR] Chunk {i // chunk_size + 1} failed: {resp.status_code} - {resp.text[:200]}")
    time.sleep(1)

print(f"\nTotal retried simple products updated: {total_updated} of {len(batch_1)}")

# Commit to catalog
u = commit_catalog_prices(CATALOG_PATH)
print(f"Committed {u} items in catalog.")

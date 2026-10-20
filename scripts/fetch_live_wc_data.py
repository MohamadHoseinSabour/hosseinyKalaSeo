import os
import sys
import json
import time
import requests
import openpyxl
from requests.adapters import HTTPAdapter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class SourceAddressAdapter(HTTPAdapter):
    def __init__(self, source_address, **kwargs):
        self.source_address = source_address
        super().__init__(**kwargs)
    def init_poolmanager(self, *args, **kwargs):
        kwargs['source_address'] = (self.source_address, 0)
        return super().init_poolmanager(*args, **kwargs)

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.xlsx')
AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {'User-Agent': 'Mozilla/5.0'}

s = requests.Session()
s.mount('https://', SourceAddressAdapter('10.102.29.1'))

print("=== Fetching all variable products and their variations from WooCommerce ===")
# Fetch variable products
all_products = []
for p in range(1, 3):
    r = s.get(f'https://hosseinykala.ir/wp-json/wc/v3/products?per_page=100&page={p}', auth=AUTH, headers=HEADERS, timeout=20)
    if r.status_code == 200:
        all_products.extend(r.json())

variable_parents = {p['id']: p for p in all_products if p.get('type') == 'variable'}
print(f"Total variable parents on site: {len(variable_parents)}")

# Fetch variations for each parent
site_variations_by_parent = {}
for pid in variable_parents:
    r = s.get(f'https://hosseinykala.ir/wp-json/wc/v3/products/{pid}/variations?per_page=100', auth=AUTH, headers=HEADERS, timeout=20)
    if r.status_code == 200:
        site_variations_by_parent[pid] = r.json()
    time.sleep(0.1)

print(f"Fetched variations for {len(site_variations_by_parent)} parents.")
total_site_vars = sum(len(v) for v in site_variations_by_parent.values())
print(f"Total site variations: {total_site_vars}")

# Save snapshot to scratch for quick reference
os.makedirs(os.path.join(PROJECT_DIR, 'scratch'), exist_ok=True)
with open(os.path.join(PROJECT_DIR, 'scratch', 'wc_live_dump.json'), 'w', encoding='utf-8') as f:
    json.dump({
        'products': all_products,
        'variations': site_variations_by_parent
    }, f, ensure_ascii=False, indent=2)

print("Saved scratch/wc_live_dump.json")

import os
import sys
import json
import requests
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
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {'User-Agent': 'Mozilla/5.0'}

s = requests.Session()
s.mount('https://', SourceAddressAdapter('10.102.29.1'))

print("Fetching products from WooCommerce API...")
all_wc_products = []
for page in range(1, 3):
    r = s.get(f'https://hosseinykala.ir/wp-json/wc/v3/products?per_page=100&page={page}', auth=AUTH, headers=HEADERS, timeout=25)
    if r.status_code == 200:
        all_wc_products.extend(r.json())
        print(f"Page {page}: {len(r.json())} products.")

print(f"Total WC products fetched: {len(all_wc_products)}")

# Update products.json
products_path = os.path.join(DATA_DIR, 'products.json')
existing_prods_by_id = {}
if os.path.exists(products_path):
    with open(products_path, 'r', encoding='utf-8') as f:
        existing = json.load(f)
        for p in existing:
            existing_prods_by_id[p['id']] = p

updated_products_list = []
for p in all_wc_products:
    pid = p['id']
    old_p = existing_prods_by_id.get(pid, {})
    
    prod_obj = {
        'id': pid,
        'url': p.get('permalink', f"https://hosseinykala.ir/product/{p.get('slug')}/"),
        'slug': p.get('slug', ''),
        'name': p.get('name', ''),
        'type': p.get('type', 'simple'),
        'status': p.get('status', 'publish'),
        'price': p.get('price', ''),
        'regular_price': p.get('regular_price', ''),
        'sale_price': p.get('sale_price', ''),
        'currency': 'IRT',
        'in_stock': p.get('stock_status') == 'instock',
        'stock_status': p.get('stock_status', 'instock'),
        'categories': p.get('categories', old_p.get('categories', [])),
        'featured_image': p.get('images', [{}])[0].get('src', '') if p.get('images') else old_p.get('featured_image', ''),
        'short_description': p.get('short_description', old_p.get('short_description', '')),
        'description': p.get('description', old_p.get('description', '')),
        'date': p.get('date_created', old_p.get('date', '')),
        'modified': p.get('date_modified', old_p.get('modified', ''))
    }
    updated_products_list.append(prod_obj)

with open(products_path, 'w', encoding='utf-8') as f:
    json.dump(updated_products_list, f, ensure_ascii=False, indent=2)
print(f"✓ Saved data/products.json with {len(updated_products_list)} items.")

# Update id_mappings.json products section
id_mappings_path = os.path.join(DATA_DIR, 'id_mappings.json')
if os.path.exists(id_mappings_path):
    with open(id_mappings_path, 'r', encoding='utf-8') as f:
        id_maps = json.load(f)
    
    id_maps['products'] = [
        {
            'id': item['id'],
            'name': item['name'],
            'slug': item['slug'],
            'shortlink': f"https://hosseinykala.ir/?p={item['id']}"
        }
        for item in sorted(updated_products_list, key=lambda x: x['id'], reverse=True)
    ]
    with open(id_mappings_path, 'w', encoding='utf-8') as f:
        json.dump(id_maps, f, ensure_ascii=False, indent=2)
    print(f"✓ Updated data/id_mappings.json products.")

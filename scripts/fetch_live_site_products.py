import os
import sys
import json
import time
import socket
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

def get_session():
    # Candidates for local interface IP (non-VPN)
    candidates = ['10.234.170.38']
    
    # Also discover all local IPv4s
    try:
        hostname = socket.gethostname()
        for ip in socket.gethostbyname_ex(hostname)[2]:
            if ip not in candidates:
                candidates.append(ip)
    except Exception:
        pass

    auth = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
    headers = {'User-Agent': 'Mozilla/5.0'}

    for ip in candidates:
        try:
            s = requests.Session()
            s.mount('https://', SourceAddressAdapter(ip))
            r = s.get('https://hosseinykala.ir/wp-json/wc/v3/products?per_page=1', auth=auth, headers=headers, timeout=5)
            if r.status_code == 200:
                print(f"✓ Connected to WooCommerce API via IP {ip}")
                return s, auth, headers
        except Exception:
            continue

    # Fallback to default session
    try:
        s = requests.Session()
        r = s.get('https://hosseinykala.ir/wp-json/wc/v3/products?per_page=1', auth=auth, headers=headers, timeout=5)
        if r.status_code == 200:
            print("✓ Connected to WooCommerce API via default routing")
            return s, auth, headers
    except Exception:
        pass

    raise ConnectionError("Could not connect to WooCommerce API on any interface.")

def fetch_all():
    s, auth, headers = get_session()
    
    print("\n[1/3] Fetching all products from WooCommerce...")
    all_products = []
    page = 1
    while True:
        url = f'https://hosseinykala.ir/wp-json/wc/v3/products?per_page=100&page={page}'
        print(f"  - Fetching page {page}...")
        r = s.get(url, auth=auth, headers=headers, timeout=30)
        if r.status_code != 200:
            print(f"  Warning: status {r.status_code} on page {page}")
            break
        items = r.json()
        if not items:
            break
        all_products.extend(items)
        total_pages = int(r.headers.get('x-wp-totalpages', 1))
        print(f"    Page {page}/{total_pages}: {len(items)} products fetched.")
        if page >= total_pages:
            break
        page += 1

    print(f"\n✓ Total products fetched: {len(all_products)}")

    variable_products = [p for p in all_products if p.get('type') == 'variable']
    print(f"[2/3] Fetching variations for {len(variable_products)} variable products...")
    
    variations_by_parent = {}
    total_variations = 0

    for idx, parent in enumerate(variable_products, 1):
        pid = parent['id']
        pname = parent.get('name', '')
        url = f'https://hosseinykala.ir/wp-json/wc/v3/products/{pid}/variations?per_page=100'
        rv = s.get(url, auth=auth, headers=headers, timeout=30)
        if rv.status_code == 200:
            v_list = rv.json()
            variations_by_parent[str(pid)] = v_list
            total_variations += len(v_list)
            print(f"  [{idx}/{len(variable_products)}] Product {pid} ({pname[:40]}...): {len(v_list)} variations")
        else:
            print(f"  [{idx}/{len(variable_products)}] ERROR fetching variations for {pid}: status {rv.status_code}")
        time.sleep(0.05)

    print(f"\n✓ Total variations fetched: {total_variations}")

    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scratch')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'site_products_live.json')

    data = {
        'products': all_products,
        'variations': variations_by_parent,
        'fetched_at': time.strftime('%Y-%m-%d %H:%M:%S'),
        'total_products': len(all_products),
        'total_variations': total_variations
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n[3/3] ✓ Successfully saved snapshot to: {output_file}")
    return data

if __name__ == '__main__':
    fetch_all()

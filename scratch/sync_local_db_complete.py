import os, sys, requests, json
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
from urllib3.util import Retry

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_DIR, 'data')

class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
SESSION = requests.Session()
retries = Retry(total=4, backoff_factor=2, status_forcelist=[500, 502, 503, 504])
adapter = TLSAdapter(max_retries=retries)
SESSION.mount('https://', adapter)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

def main():
    print("=== FETCHING ALL WOOCOMMERCE PRODUCTS FOR LOCAL DB SYNC ===")
    
    # 1. Load categories mapping
    cats_path = os.path.join(DATA_DIR, 'categories.json')
    cat_map = {}
    if os.path.exists(cats_path):
        with open(cats_path, 'r', encoding='utf-8') as f:
            cat_list = json.load(f)
            cat_map = {c['id']: c['name'] for c in cat_list}
            
    all_products = []
    page = 1
    while True:
        url = f"https://hosseinykala.ir/wp-json/wc/v3/products?per_page=100&page={page}"
        print(f"Fetching products page {page}...")
        r = SESSION.get(url, auth=AUTH, headers=HEADERS, timeout=60)
        if r.status_code != 200:
            print(f"Error fetching page {page}: {r.status_code} - {r.text[:200]}")
            break
        items = r.json()
        if not items:
            break
        all_products.extend(items)
        total_pages = int(r.headers.get('X-WP-TotalPages', 1))
        print(f"  Got {len(items)} items. (Page {page}/{total_pages})")
        if page >= total_pages:
            break
        page += 1

    print(f"\nTotal products fetched from site: {len(all_products)}")

    # 2. Build complete products.json and id_mappings.json
    id_mappings = {}
    products_json_list = []

    for p in all_products:
        pid = p['id']
        pname = p.get('name', '')
        pslug = p.get('slug', '')
        ptype = p.get('type', 'simple')
        pprice = p.get('price', '')
        preg_price = p.get('regular_price', '')
        psale_price = p.get('sale_price', '')
        pstock = p.get('stock_status', 'instock')
        purl = p.get('permalink', f"https://hosseinykala.ir/product/{pslug}/")
        
        # categories
        cat_names = [c.get('name', '') for c in p.get('categories', [])]
        main_cat = cat_names[0] if cat_names else ''
        
        # images
        img_src = p['images'][0]['src'] if p.get('images') else ''

        prod_entry = {
            'product_id': pid,
            'id': pid,
            'name': pname,
            'slug': pslug,
            'url': purl,
            'shortlink': f"https://hosseinykala.ir/?p={pid}",
            'type': ptype,
            'price': pprice,
            'price_regular': preg_price,
            'price_sale': psale_price,
            'in_stock': (pstock == 'instock'),
            'stock_status': pstock,
            'category': " > ".join(cat_names),
            'categories': cat_names,
            'sku': p.get('sku', ''),
            'image': img_src,
            'variations_count': len(p.get('variations', [])),
            'variations': p.get('variations', []),
            'attributes': p.get('attributes', []),
            'regular_price': preg_price,
            'sale_price': psale_price
        }
        products_json_list.append(prod_entry)

        id_mappings[str(pid)] = {
            'name': pname,
            'slug': pslug,
            'type': ptype,
            'url': f"https://hosseinykala.ir/?p={pid}",
            'price': int(pprice) if pprice and pprice.isdigit() else 0
        }

        # If variable, fetch variations to include in id_mappings
        if ptype == 'variable' and p.get('variations'):
            var_url = f"https://hosseinykala.ir/wp-json/wc/v3/products/{pid}/variations?per_page=100"
            try:
                r_var = SESSION.get(var_url, auth=AUTH, headers=HEADERS, timeout=40)
                if r_var.status_code == 200:
                    var_items = r_var.json()
                    for v in var_items:
                        vid = v['id']
                        v_attr = ", ".join([f"{a.get('name')}: {a.get('option')}" for a in v.get('attributes', [])])
                        v_name = f"{pname} - {v_attr}" if v_attr else pname
                        v_price = v.get('price', '')
                        id_mappings[str(vid)] = {
                            'name': v_name,
                            'parent_id': pid,
                            'type': 'variation',
                            'url': f"https://hosseinykala.ir/?p={vid}",
                            'price': int(v_price) if v_price and v_price.isdigit() else 0
                        }
            except Exception as e:
                print(f"  Warning: failed to fetch variations for #{pid}: {e}")

    # 3. Save files
    products_file = os.path.join(DATA_DIR, 'products.json')
    with open(products_file, 'w', encoding='utf-8') as f:
        json.dump(products_json_list, f, ensure_ascii=False, indent=2)
    print(f"✓ Saved {len(products_json_list)} products to {products_file}")

    id_mappings_file = os.path.join(DATA_DIR, 'id_mappings.json')
    with open(id_mappings_file, 'w', encoding='utf-8') as f:
        json.dump(id_mappings, f, ensure_ascii=False, indent=2)
    print(f"✓ Saved {len(id_mappings)} entries to {id_mappings_file}")

    print("\n=== Local DB Synchronization Completed Successfully! ===")

if __name__ == '__main__':
    main()

import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

# Test creating a draft product on wc/v3
test_payload = {
    'name': 'Test Permission Check Product',
    'type': 'simple',
    'status': 'draft',
    'regular_price': '100000',
    'stock_status': 'outofstock'
}

print("Testing POST /wp-json/wc/v3/products...")
r_wc = requests.post('https://hosseinykala.ir/wp-json/wc/v3/products', auth=AUTH, headers=HEADERS, json=test_payload)
print('WC v3 POST status:', r_wc.status_code)
if r_wc.status_code in [200, 201]:
    prod = r_wc.json()
    test_id = prod.get('id')
    print(f"Success! Created test product ID: {test_id}")
    # Delete test product
    r_del = requests.delete(f'https://hosseinykala.ir/wp-json/wc/v3/products/{test_id}?force=true', auth=AUTH, headers=HEADERS)
    print("Deleted test product status:", r_del.status_code)
else:
    print('WC v3 POST error:', r_wc.text[:200])

    print("\nTesting POST /wp-json/wp/v2/product...")
    test_wp_payload = {
        'title': 'Test Permission Check Product WP',
        'status': 'draft'
    }
    r_wp = requests.post('https://hosseinykala.ir/wp-json/wp/v2/product', auth=AUTH, headers=HEADERS, json=test_wp_payload)
    print('WP v2 POST status:', r_wp.status_code)
    if r_wp.status_code in [200, 201]:
        prod_wp = r_wp.json()
        wp_id = prod_wp.get('id')
        print(f"Success WP! Created test product ID: {wp_id}")
        r_del = requests.delete(f'https://hosseinykala.ir/wp-json/wp/v2/product/{wp_id}?force=true', auth=AUTH, headers=HEADERS)
        print("Deleted WP test product status:", r_del.status_code)
    else:
        print('WP v2 POST error:', r_wp.text[:200])

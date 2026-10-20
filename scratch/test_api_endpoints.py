import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

print("Testing WP v2 with custom User-Agent...")
r = requests.get('https://hosseinykala.ir/wp-json/wp/v2/product/2972', auth=AUTH, headers=HEADERS)
print('WP v2 status:', r.status_code)
if r.status_code == 200:
    data = r.json()
    print('Title:', data.get('title'))
    print('Slug:', data.get('slug'))
    print('Featured media:', data.get('featured_media'))
    print('Product cat:', data.get('product_cat'))
else:
    print('Error text:', r.text[:200])

print("\nTesting WC v3 with custom User-Agent...")
r_wc = requests.get('https://hosseinykala.ir/wp-json/wc/v3/products/2972', auth=AUTH, headers=HEADERS)
print('WC v3 status:', r_wc.status_code)
if r_wc.status_code == 200:
    data_wc = r_wc.json()
    print('WC Title:', data_wc.get('name'))
else:
    print('WC Error text:', r_wc.text[:200])

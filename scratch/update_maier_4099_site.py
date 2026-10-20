import sys
import json
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

with open('data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

target_p = None
for p in products:
    if p.get('id') == 4249:
        target_p = p
        break

if not target_p:
    print('Product 4249 not found in data/products.json!')
    sys.exit(1)

old_desc = target_p.get('description', '')
new_desc = old_desc.replace('MR-4155', 'MR-4099').replace('۴۱۵۵', '۴۰۹۹')
new_short_desc = target_p.get('short_description', '').replace('MR-4155', 'MR-4099').replace('۴۱۵۵', '۴۰۹۹')
new_name = 'آسیاب قهوه مایر مدل MR-4099'
new_slug = 'maier-mr4099-digital-conical-burr-coffee-grinder'

print('Target Name:', new_name)
print('Target Slug:', new_slug)

s = requests.Session()
s.mount('https://', TLSAdapter())

# Method 1: WC batch endpoint
print('\n--- Attempting Method 1: WC Batch Update ---')
batch_payload = {
    'update': [
        {
            'id': 4249,
            'name': new_name,
            'slug': new_slug,
            'description': new_desc,
            'short_description': new_short_desc
        }
    ]
}

wc_batch_url = 'https://hosseinykala.ir/wp-json/wc/v3/products/batch'
success = False
try:
    r = s.post(wc_batch_url, auth=AUTH, headers=HEADERS, json=batch_payload, timeout=45)
    print('WC batch status:', r.status_code)
    if r.status_code == 200:
        res = r.json()
        print('WC batch response update count:', len(res.get('update', [])))
        if res.get('update'):
            up_item = res['update'][0]
            print('Updated Name:', up_item.get('name'))
            print('Updated Slug:', up_item.get('slug'))
            print('Updated Permalink:', up_item.get('permalink'))
            success = True
    else:
        print('WC batch error:', r.text[:300])
except Exception as e:
    print('WC batch exception:', type(e).__name__, e)

if not success:
    print('\n--- Attempting Method 2: WP v2 Direct Update ---')
    wp_v2_url = 'https://hosseinykala.ir/wp-json/wp/v2/product/4249'
    wp_payload = {
        'title': new_name,
        'slug': new_slug,
        'content': new_desc,
        'excerpt': new_short_desc
    }
    try:
        r2 = s.post(wp_v2_url, auth=AUTH, headers=HEADERS, json=wp_payload, timeout=45)
        print('WP v2 status:', r2.status_code)
        if r2.status_code == 200:
            res2 = r2.json()
            print('WP Title:', res2.get('title', {}).get('rendered'))
            print('WP Slug:', res2.get('slug'))
            print('WP Link:', res2.get('link'))
            success = True
        else:
            print('WP v2 error:', r2.text[:300])
    except Exception as e:
        print('WP v2 exception:', type(e).__name__, e)

if not success:
    print('\n--- Attempting Method 3: WC v3 PUT Single ---')
    wc_single_url = 'https://hosseinykala.ir/wp-json/wc/v3/products/4249'
    wc_payload = {
        'name': new_name,
        'slug': new_slug,
        'description': new_desc,
        'short_description': new_short_desc
    }
    try:
        r3 = s.put(wc_single_url, auth=AUTH, headers=HEADERS, json=wc_payload, timeout=45)
        print('WC single status:', r3.status_code)
        if r3.status_code == 200:
            res3 = r3.json()
            print('WC single Name:', res3.get('name'))
            print('WC single Slug:', res3.get('slug'))
            success = True
        else:
            print('WC single error:', r3.text[:300])
    except Exception as e:
        print('WC single exception:', type(e).__name__, e)

res_str = 'SUCCESS' if success else 'FAILED'
print(f'\nFinal Website Update Result: {res_str}')

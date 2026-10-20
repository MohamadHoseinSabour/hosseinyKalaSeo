import sys, requests
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

s = requests.Session()
s.mount('https://', TLSAdapter())

r = s.get('https://hosseinykala.ir/wp-json/wc/v3/products?per_page=1', auth=AUTH, headers=HEADERS, timeout=15)
print("WC API Products Status:", r.status_code)
if r.status_code == 200:
    prod = r.json()[0]
    print(f"Product ID: {prod['id']} | Name: {prod['name']} | Status: {prod['status']} | Stock: {prod['stock_status']}")

r_media = s.get('https://hosseinykala.ir/wp-json/wp/v2/media?per_page=1', auth=AUTH, headers=HEADERS, timeout=15)
print("WP Media API Status:", r_media.status_code)
if r_media.status_code == 200:
    med = r_media.json()[0]
    print(f"Media ID: {med['id']} | Title: {med['title']['rendered']}")

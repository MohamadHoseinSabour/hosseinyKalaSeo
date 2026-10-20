import sys, requests, json
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
s = requests.Session()
s.mount('https://', TLSAdapter())
HEADERS = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}

r = s.get('https://hosseinykala.ir/wp-json/wc/v3/products/3664', auth=AUTH, headers=HEADERS, timeout=15)
p = r.json()
print('Product 3664 Name:', p.get('name'))
print('Type:', p.get('type'))
print('Attributes:', json.dumps(p.get('attributes'), ensure_ascii=False))
print('Variations:', p.get('variations'))

# Also get current variations
r_var = s.get('https://hosseinykala.ir/wp-json/wc/v3/products/3664/variations', auth=AUTH, headers=HEADERS, timeout=15)
print('Variations list:')
for v in r_var.json():
    print(f"  ID: {v['id']} | Attrs: {v['attributes']} | Price: {v['price']} | Stock: {v['stock_status']}")

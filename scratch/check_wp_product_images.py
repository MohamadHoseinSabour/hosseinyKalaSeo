import requests, json, sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
from requests.adapters import HTTPAdapter

class SourceAddressAdapter(HTTPAdapter):
    def __init__(self, source_address, **kwargs):
        self.source_address = source_address
        super().__init__(**kwargs)
    def init_poolmanager(self, *args, **kwargs):
        kwargs['source_address'] = (self.source_address, 0)
        return super().init_poolmanager(*args, **kwargs)

s = requests.Session()
s.mount('https://', SourceAddressAdapter('10.102.29.1'))
auth = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

test_ids = [4302, 4297, 4286, 4284, 4282, 4280, 4270, 4257]
for pid in test_ids:
    r = s.get(f'https://hosseinykala.ir/wp-json/wp/v2/product/{pid}', auth=auth, headers=headers, timeout=15)
    if r.status_code == 200:
        d = r.json()
        feat_id = d.get('featured_media')
        print(f"{pid}: {d.get('title', {}).get('rendered')} -> featured_media: {feat_id}")
        if feat_id:
            mr = s.get(f'https://hosseinykala.ir/wp-json/wp/v2/media/{feat_id}', auth=auth, headers=headers, timeout=10)
            if mr.status_code == 200:
                print(f"    Media URL: {mr.json().get('source_url')}")
    else:
        print(f"{pid}: error {r.status_code}")

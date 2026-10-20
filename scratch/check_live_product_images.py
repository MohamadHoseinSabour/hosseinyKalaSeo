import requests, json, sys
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

test_ids = [4302, 4297, 4286, 4284, 4282, 4280, 4270, 4257]
for pid in test_ids:
    r = s.get(f'https://hosseinykala.ir/wp-json/wc/v3/products/{pid}', auth=auth, timeout=15)
    if r.status_code == 200:
        d = r.json()
        imgs = d.get('images', [])
        print(f"{pid}: {d.get('name')} -> images count: {len(imgs)}")
        for im in imgs:
            print(f"    src: {im.get('src')}")
    else:
        print(f"{pid}: error {r.status_code}")

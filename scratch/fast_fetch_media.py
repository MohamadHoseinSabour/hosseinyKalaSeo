import requests, json, sys, os
from concurrent.futures import ThreadPoolExecutor, as_completed
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

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

def get_session():
    s = requests.Session()
    s.mount('https://', SourceAddressAdapter('10.102.29.1'))
    return s

new_ids = [
    4302, 4297, 4294, 4292, 4290, 4288, 4286, 4284, 4282, 4280,
    4278, 4276, 4274, 4272, 4270, 4268, 4266, 4264, 4262, 4258,
    4257, 4255, 4253, 4251, 4249, 4245, 4241, 4239, 4237, 4235
]

def fetch_single_product(pid):
    s = get_session()
    try:
        r = s.get(f'https://hosseinykala.ir/wp-json/wp/v2/product/{pid}', auth=AUTH, headers=HEADERS, timeout=8)
        if r.status_code == 200:
            d = r.json()
            title = d.get('title', {}).get('rendered', '')
            slug = d.get('slug', '')
            feat_id = d.get('featured_media')
            img_url = None
            if feat_id:
                mr = s.get(f'https://hosseinykala.ir/wp-json/wp/v2/media/{feat_id}', auth=AUTH, headers=HEADERS, timeout=8)
                if mr.status_code == 200:
                    img_url = mr.json().get('source_url')
            return {
                'id': pid,
                'title': title,
                'slug': slug,
                'featured_media_id': feat_id,
                'img_url': img_url,
                'status': 'success'
            }
        else:
            return {'id': pid, 'status': f'http_{r.status_code}'}
    except Exception as e:
        return {'id': pid, 'status': f'error_{str(e)}'}

print("Starting parallel fetch for 30 products...", flush=True)
results = {}
with ThreadPoolExecutor(max_workers=8) as executor:
    future_to_pid = {executor.submit(fetch_single_product, pid): pid for pid in new_ids}
    for future in as_completed(future_to_pid):
        data = future.result()
        pid = data['id']
        results[pid] = data
        title = data.get('title', '')[:30]
        img = data.get('img_url', 'No image')
        print(f"✓ ID {pid}: {title} -> {img}", flush=True)

with open('scratch/fast_fetched_media.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nFinished! Total products fetched: {len(results)}", flush=True)

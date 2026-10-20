import requests, json, sys, os
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

new_ids = [
    4302, 4297, 4294, 4292, 4290, 4288, 4286, 4284, 4282, 4280,
    4278, 4276, 4274, 4272, 4270, 4268, 4266, 4264, 4262, 4258,
    4257, 4255, 4253, 4251, 4249, 4245, 4241, 4239, 4237, 4235
]

results = []
print(f"Fetching media and details for {len(new_ids)} products...")

for idx, pid in enumerate(new_ids, 1):
    try:
        r = s.get(f'https://hosseinykala.ir/wp-json/wp/v2/product/{pid}', auth=auth, headers=headers, timeout=20)
        if r.status_code == 200:
            d = r.json()
            title = d.get('title', {}).get('rendered', '')
            slug = d.get('slug', '')
            feat_id = d.get('featured_media')
            img_urls = []
            
            if feat_id:
                mr = s.get(f'https://hosseinykala.ir/wp-json/wp/v2/media/{feat_id}', auth=auth, headers=headers, timeout=15)
                if mr.status_code == 200:
                    src = mr.json().get('source_url')
                    if src:
                        img_urls.append(src)
            
            results.append({
                'id': pid,
                'title': title,
                'slug': slug,
                'featured_media_id': feat_id,
                'images': img_urls
            })
            print(f"[{idx}/{len(new_ids)}] ID {pid}: {title[:35]} -> images: {len(img_urls)}")
        else:
            print(f"[{idx}/{len(new_ids)}] ID {pid}: Error {r.status_code}")
    except Exception as e:
        print(f"[{idx}/{len(new_ids)}] ID {pid}: Exception {e}")

with open('scratch/fetched_products_media.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\nSaved to scratch/fetched_products_media.json")

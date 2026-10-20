import os
import sys
import json
import requests

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
REF_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scratch', 'product_refs')
os.makedirs(REF_DIR, exist_ok=True)

with open(os.path.join(DATA_DIR, 'products.json'), 'r', encoding='utf-8') as f:
    products = json.load(f)

check_ids = [2766, 2745, 2594, 3026, 3016, 3013, 3065, 3056, 2538, 2445]
downloaded = {}

headers = {'User-Agent': 'Mozilla/5.0'}

for p in products:
    if p['id'] in check_ids:
        img_url = p.get('featured_image')
        print(f"Product {p['id']} ({p['name']}): {img_url}")
        if img_url:
            ext = img_url.split('.')[-1].split('?')[0]
            if len(ext) > 4:
                ext = 'jpg'
            local_filename = f"prod_{p['id']}.{ext}"
            local_path = os.path.join(REF_DIR, local_filename)
            try:
                r = requests.get(img_url, headers=headers, timeout=15)
                if r.status_code == 200:
                    with open(local_path, 'wb') as f_out:
                        f_out.write(r.content)
                    print(f"  -> Downloaded: {local_path} ({len(r.content)/1024:.1f} KB)")
                    downloaded[p['id']] = local_path
            except Exception as e:
                print(f"  -> Error downloading {img_url}: {e}")

print("\nDownloaded references map:")
for k, v in downloaded.items():
    print(f"ID {k}: {v}")

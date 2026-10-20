import requests
import sys
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {'User-Agent': 'Mozilla/5.0'}

for pid in [3626, 4095, 3494, 3709, 4068]:
    try:
        r = requests.get(f'https://hosseinykala.ir/wp-json/wc/v3/products/{pid}', auth=AUTH, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            p = r.json()
            print(f"=== PID {pid}: {p.get('name')} ===")
            print("Categories:", [(c.get('id'), c.get('name')) for c in p.get('categories', [])])
            print("Images:", [img.get('src') for img in p.get('images', [])])
            print("Short Desc:\n", p.get('short_description', ''))
            print("Description snippet:\n", p.get('description', '')[:500])
            print("-" * 50)
    except Exception as e:
        print(f"Error fetching {pid}: {e}")

import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

r = requests.get('https://hosseinykala.ir/wp-json/wp/v2/menu-items?menus=16&per_page=100', auth=AUTH, headers=headers)
if r.status_code == 200:
    items = r.json()
    print(f"Total items in menu 16: {len(items)}")
    for it in sorted(items, key=lambda x: x.get('menu_order', 0))[:15]:
        title = it.get('title', {}).get('rendered', '')
        itype = it.get('type')
        obj = it.get('object')
        obj_id = it.get('object_id')
        url = it.get('url')
        print(f"ID: {it['id']:<5} | Title: {title:<20} | Type: {itype:<10} | Obj: {obj} ({obj_id}) | URL: {url}")

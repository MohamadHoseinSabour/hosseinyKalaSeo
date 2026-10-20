import requests
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = 'https://hosseinykala.ir/wp-json/wp/v2'
AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')

search_terms = ['الکترواستیل', 'وگاترونیکس', 'توستر', 'فر', '290', '۲۹۰', 'دونالکس', 'هواپز', 'سرخکن', 'سرخ کن', 'اپولاتور', 'اپیلاتور', 'شیور', 'پتوشور', 'پاکیزان']

for term in search_terms:
    try:
        res = requests.get(f'{BASE_URL}/product', auth=AUTH, params={'search': term, 'per_page': 50})
        if res.status_code == 200:
            items = res.json()
            print(f"=== Search: '{term}' -> {len(items)} items ===")
            for it in items:
                print(f"  ID: {it['id']} | Title: {it['title']['rendered']} | Slug: {it['slug']}")
        else:
            print(f"Search '{term}' returned status: {res.status_code}")
    except Exception as e:
        print(f"Error on '{term}': {e}")

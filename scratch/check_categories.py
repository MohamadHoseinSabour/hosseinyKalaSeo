import requests
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {'User-Agent': 'Mozilla/5.0'}

r = requests.get('https://hosseinykala.ir/wp-json/wc/v3/products/categories?per_page=100', auth=AUTH, headers=HEADERS, timeout=15)
if r.status_code == 200:
    for c in r.json():
        name = c.get('name', '')
        if any(k in name for k in ['آبمیوه', 'نوشیدنی', 'گوشت', 'سرخ', 'اصلاح', 'زیبایی', 'شستشو', 'لباسشویی', 'دونالکس']):
            print(f"ID: {c.get('id')} | Name: {name} | Slug: {c.get('slug')} | Parent: {c.get('parent')}")

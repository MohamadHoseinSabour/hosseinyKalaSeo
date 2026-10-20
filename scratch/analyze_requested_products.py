import os
import sys
import json
import requests
import openpyxl

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

def search_wc(term):
    url = f'https://hosseinykala.ir/wp-json/wc/v3/products?search={term}&per_page=20'
    res = requests.get(url, auth=AUTH, headers=HEADERS, timeout=15)
    if res.status_code == 200:
        return res.json()
    return []

print("=== 1. Searching WC for 'الکترواستیل' / 'فر' / 'وگاترونیکس' ===")
for t in ['الکترواستیل', 'فر برقی', 'وگاترونیکس', 'آون']:
    items = search_wc(t)
    print(f"Term '{t}': {len(items)} found")
    for it in items:
        print(f"  ID: {it['id']} | Name: {it['name']} | Slug: {it['slug']} | Categories: {[c['name'] for c in it.get('categories', [])]}")

print("\n=== 2. Searching WC for '290' / 'دونالکس' / 'غذاساز' / 'آبمیوه' ===")
for t in ['290', 'دونالکس']:
    items = search_wc(t)
    print(f"Term '{t}': {len(items)} found")
    for it in items:
        if '290' in it['name'] or 'غذاساز' in it['name'] or 'آبمیوه' in it['name']:
            print(f"  ID: {it['id']} | Name: {it['name']} | Slug: {it['slug']}")

print("\n=== 3. Searching WC for 'هواپز' / 'سرخکن' / 'سرخ کن' ===")
for t in ['هواپز', 'سرخکن', 'سرخ کن']:
    items = search_wc(t)
    print(f"Term '{t}': {len(items)} found")
    for it in items:
        print(f"  ID: {it['id']} | Name: {it['name']} | Slug: {it['slug']}")

print("\n=== 4. Searching WC for 'اپولاتور' / 'اپیلاتور' / 'شیور' ===")
for t in ['اپولاتور', 'اپیلاتور', 'شیور']:
    items = search_wc(t)
    print(f"Term '{t}': {len(items)} found")
    for it in items:
        print(f"  ID: {it['id']} | Name: {it['name']} | Slug: {it['slug']}")

print("\n=== 5. Searching WC for 'پتوشور' / 'پاکیزان' ===")
for t in ['پتوشور', 'پاکیزان']:
    items = search_wc(t)
    print(f"Term '{t}': {len(items)} found")
    for it in items:
        print(f"  ID: {it['id']} | Name: {it['name']} | Slug: {it['slug']} | Status: {it['status']} | Stock: {it['stock_status']} | Price: {it['price']} | RegPrice: {it['regular_price']} | SalePrice: {it['sale_price']}")

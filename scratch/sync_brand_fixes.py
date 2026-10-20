import sys
import json
import requests

sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Content-Type': 'application/json'
}
WC_URL = 'https://hosseinykala.ir/wp-json/wc/v3/products'

# 1. Update titles and slugs
title_slug_updates = [
    {
        'id': 3534,
        'name': 'تلویزیون ال ای دی ۸۵ اینچ هوشمند 4K هاورسن مدل Ultra HD',
        'slug': 'haverson-85-inch-4k-smart-tv'
    },
    {
        'id': 3516,
        'name': 'تلویزیون ال ای دی ۳۲ اینچ هاورسن مدل HD',
        'slug': 'haverson-32-inch-hd-led-tv'
    },
    {
        'id': 2637,
        'name': 'یخچال و فریزر دوقلو 36 فوت کلور مدل RNT101-FNT101',
        'slug': 'clover-rnt101-fnt101-twin-refrigerator-36ft'
    },
    {
        'id': 2408,
        'name': 'یخچال و فریزر 27 فوت کلور مدل FRNT101',
        'slug': 'clover-frnt101-refrigerator-27ft'
    }
]

for item in title_slug_updates:
    pid = item['id']
    payload = {'name': item['name'], 'slug': item['slug']}
    r = requests.put(f"{WC_URL}/{pid}", auth=AUTH, headers=HEADERS, json=payload, timeout=20)
    if r.status_code == 200:
        print(f"✓ Updated product {pid}: {item['name']} | {item['slug']}")
    else:
        print(f"✗ Failed {pid}: {r.status_code} - {r.text[:100]}")

# 2. Fix Brand Attributes
brand_fixes = {
    3457: 'دونالکس',
    3354: 'دستی لوکس',
    3312: 'نیکایی',
    3285: 'پرو امگا',
    3065: 'پرو امگا',
    3056: 'پرو امگا',
    3049: 'پرو امگا',
    3546: 'کلور',
    3534: 'هاورسن',
    3516: 'هاورسن'
}

for pid, brand in brand_fixes.items():
    # fetch product first to get current attributes
    r_get = requests.get(f"{WC_URL}/{pid}", auth=AUTH, headers=HEADERS, timeout=20)
    if r_get.status_code != 200:
        print(f"✗ Could not fetch attributes for {pid}: {r_get.status_code}")
        continue
    prod = r_get.json()
    attrs = prod.get('attributes', [])
    found = False
    for a in attrs:
        if a.get('name') == 'برند':
            a['options'] = [brand]
            found = True
            break
    if not found:
        attrs.append({
            'name': 'برند',
            'visible': True,
            'variation': False,
            'options': [brand]
        })
    r_put = requests.put(f"{WC_URL}/{pid}", auth=AUTH, headers=HEADERS, json={'attributes': attrs}, timeout=20)
    if r_put.status_code == 200:
        print(f"✓ Updated brand attribute for {pid} to: {brand}")
    else:
        print(f"✗ Failed attribute update for {pid}: {r_put.status_code} - {r_put.text[:100]}")

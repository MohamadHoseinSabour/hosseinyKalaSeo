import sys
import requests
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

POST_TARGETS = {
    3000: 'portable-cellulose-air-cooler-guide',
    3098: 'mini-hotel-refrigerator-buying-guide',
    3099: '15-place-dishwasher-buying-guide',
    3100: 'combi-vs-twin-refrigerator-guide',
    3101: 'clover-brand-review',
    3102: 'economical-dowry-checklist-guide'
}

PRODUCT_TARGETS = {
    3453: 'electrosteel-future-twin-refrigerator-21ft',
    2972: 'clover-glory-plus-54ft-twin-refrigerator',
    3395: 'himalia-alpha-twin-refrigerator-28ft',
    3266: 'pakshoma-18000-split-air-conditioner'
}

def update_item(endpoint, item_id, slug):
    url = f"https://hosseinykala.ir/wp-json/wp/v2/{endpoint}/{item_id}"
    payload = {'slug': slug}
    for attempt in range(3):
        try:
            r = requests.post(url, json=payload, auth=AUTH, headers=HEADERS, timeout=20)
            if r.status_code == 200:
                d = r.json()
                print(f"[OK] {endpoint}/{item_id} -> Slug: {d.get('slug')} | Link: {d.get('link')}", flush=True)
                return True
            else:
                print(f"[FAIL] {endpoint}/{item_id} (attempt {attempt+1}): HTTP {r.status_code} - {r.text[:100]}", flush=True)
        except Exception as e:
            print(f"[RETRY] {endpoint}/{item_id} (attempt {attempt+1}): {e}", flush=True)
    return False

print("=== Updating Post Slugs ===", flush=True)
for pid, slug in POST_TARGETS.items():
    update_item('posts', pid, slug)

print("\n=== Updating Product Slugs ===", flush=True)
for pid, slug in PRODUCT_TARGETS.items():
    update_item('product', pid, slug)

print("\n=== Slug Updates Completed ===", flush=True)

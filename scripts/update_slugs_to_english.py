import os
import sys
import json
import requests

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

auth = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

POST_SLUG_MAP = {
    2932: 'washing-machine-8kg-vs-9kg-guide',
    2926: 'twin-refrigerator-buying-guide'
}

PRODUCT_SLUG_MAP = {
    3065: 'pro-omega-t7-hair-clipper',
    3056: 'pro-omega-t5-hair-clipper',
    3049: 'pro-omega-8806-hair-dryer',
    3035: 'donallex-dn-205-blender',
    3032: 'donallex-dn-275-hand-blender',
    3026: 'donallex-dn-950-air-fryer-8l',
    3019: 'donallex-dn-120-juicer-1000w',
    3016: 'donallex-dn475-espresso-maker',
    3013: 'donallex-dn480-espresso-maker',
    3007: 'donallex-815-steam-iron-2500w',
    2885: 'bost-bvc-pc18b-vacuum-cleaner',
    2871: 'clover-cdw-h15v-dishwasher-15p',
    2766: 'soft-water-ir-06-purifier',
    2745: 'depoint-max-du-twin-refrigerator-34ft',
    2704: 'eastcool-2835-refrigerator-5ft',
    2691: 'eastcool-2919-hotel-refrigerator-9ft',
    2680: 'electrosteel-future-twin-refrigerator-21ft',
    2661: 'panasonic-mc-cg715-vacuum-cleaner',
    2637: 'clover-rnt101-fnt101-twin-refrigerator-36ft',
    2594: 'depoint-boss-pro-refrigerator-30ft',
    2585: 'depoint-t7-refrigerator-28ft',
    2579: 'daewoo-lm-9170-washing-machine-9kg',
    2559: 'reyton-vento-7000-air-cooler',
    2538: 'reyton-vento-16000-portable-air-cooler',
    2519: 'hitachi-cv-950f-vacuum-cleaner',
    2510: 'clover-bmw-t3-washing-machine-8kg',
    2505: 'clover-bmw-t2-washing-machine-9kg',
    2497: 'clover-frnt-70-glory-plus',
    2484: 'clover-rosso-homebar-refrigerator-27ft',
    2471: 'clover-glory-w60-twin-refrigerator-40ft',
    2464: 'clover-glory-plus-lm70-twin-refrigerator',
    2457: 'clover-rosso-plus-w60-twin-refrigerator-40ft',
    2431: 'clover-mini-refrigerator-10ft',
    2408: 'clover-frnt101-refrigerator-27ft'
}

def update_slugs():
    success_count = 0
    fail_count = 0

    print("=== Updating Article Slugs ===")
    for post_id, new_slug in POST_SLUG_MAP.items():
        url = f"https://hosseinykala.ir/wp-json/wp/v2/posts/{post_id}"
        payload = {'slug': new_slug}
        res = requests.post(url, json=payload, auth=auth, headers=headers, timeout=15)
        if res.status_code == 200:
            data = res.json()
            print(f"[OK] Post {post_id} -> {data.get('slug')}")
            success_count += 1
        else:
            print(f"[FAIL] Post {post_id}: HTTP {res.status_code} - {res.text[:100]}")
            fail_count += 1

    print("\n=== Updating Product Slugs ===")
    for prod_id, new_slug in PRODUCT_SLUG_MAP.items():
        url = f"https://hosseinykala.ir/wp-json/wp/v2/product/{prod_id}"
        payload = {'slug': new_slug}
        res = requests.post(url, json=payload, auth=auth, headers=headers, timeout=15)
        if res.status_code == 200:
            data = res.json()
            print(f"[OK] Product {prod_id} -> {data.get('slug')}")
            success_count += 1
        else:
            print(f"[FAIL] Product {prod_id}: HTTP {res.status_code} - {res.text[:100]}")
            fail_count += 1

    print(f"\nCompleted slug updates. Success: {success_count}, Failed: {fail_count}")
    return fail_count == 0

if __name__ == '__main__':
    update_slugs()

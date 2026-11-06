import urllib.request
import base64
import json
import ssl
import sys

sys.stdout.reconfigure(encoding='utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

creds = base64.b64encode(b'agent:Mlwg pHHX NQ64 drrz 7ca2 IVto').decode('utf-8')

post_slugs = [
    'mellat-bank-200m-appliances-loan-guide',
    'bajet-tejarat-refah-300m-appliances',
    'refah-bank-beta-installment-guide',
    'washing-machine-8kg-vs-9kg-guide',
    'twin-refrigerator-buying-guide',
    'mini-hotel-refrigerator-buying-guide',
    'portable-cellulose-air-cooler-guide',
    'combi-vs-twin-refrigerator-guide',
    '15-place-dishwasher-buying-guide'
]

product_slugs = [
    'pro-omega-t5-hair-clipper',
    'bost-bvc-pc18b-vacuum-cleaner',
    'clover-bmw-t2-washing-machine-9kg',
    'clover-glory-plus-lm70-twin-refrigerator',
    'clover-fantasy-patterned-10ft-mini-refrigerator',
    'reyton-vento-16000-portable-air-cooler',
    'pro-omega-t7-hair-clipper',
    'donallex-dn-275-hand-blender',
    'delmonti-dn580-toaster-oven',
    'donallex-dn-950-air-fryer-8l',
    'clover-bmw-t3-washing-machine-8kg',
    'clover-cdw-h15v-dishwasher-15p'
]

print("--- POSTS ---")
for slug in post_slugs:
    url = f'https://hosseinykala.ir/wp-json/wp/v2/posts?slug={slug}'
    req = urllib.request.Request(url, headers={'Authorization': f'Basic {creds}', 'User-Agent': 'Mozilla/5.0'})
    try:
        data = json.loads(urllib.request.urlopen(req, context=ctx, timeout=10).read().decode('utf-8'))
        if data:
            p = data[0]
            print(f"Post: {slug} -> ID: {p['id']} | Title: {p['title']['rendered'][:50]}")
        else:
            print(f"Post NOT FOUND: {slug}")
    except Exception as e:
        print(f"Post err {slug}: {e}")

print("\n--- PRODUCTS ---")
for slug in product_slugs:
    url = f'https://hosseinykala.ir/wp-json/wp/v2/product?slug={slug}'
    req = urllib.request.Request(url, headers={'Authorization': f'Basic {creds}', 'User-Agent': 'Mozilla/5.0'})
    try:
        data = json.loads(urllib.request.urlopen(req, context=ctx, timeout=10).read().decode('utf-8'))
        if data:
            p = data[0]
            print(f"Product: {slug} -> ID: {p['id']} | Title: {p['title']['rendered'][:50]}")
        else:
            print(f"Product NOT FOUND: {slug}")
    except Exception as e:
        print(f"Product err {slug}: {e}")

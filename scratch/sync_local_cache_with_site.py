import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

brand_attr_map = {
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

for p in products:
    pid = p['id']
    if pid == 3534:
        p['name'] = 'تلویزیون ال ای دی ۸۵ اینچ هوشمند 4K هاورسن مدل Ultra HD'
        p['slug'] = 'haverson-85-inch-4k-smart-tv'
        p['url'] = f"https://hosseinykala.ir/product/{p['slug']}/"
    elif pid == 3516:
        p['name'] = 'تلویزیون ال ای دی ۳۲ اینچ هاورسن مدل HD'
        p['slug'] = 'haverson-32-inch-hd-led-tv'
        p['url'] = f"https://hosseinykala.ir/product/{p['slug']}/"
    elif pid == 2637:
        p['name'] = 'یخچال و فریزر دوقلو 36 فوت کلور مدل RNT101-FNT101'
        p['slug'] = 'clover-rnt101-fnt101-twin-refrigerator-36ft'
        p['url'] = f"https://hosseinykala.ir/product/{p['slug']}/"
    elif pid == 2408:
        p['name'] = 'یخچال و فریزر 27 فوت کلور مدل FRNT101'
        p['slug'] = 'clover-frnt101-refrigerator-27ft'
        p['url'] = f"https://hosseinykala.ir/product/{p['slug']}/"

    if pid in brand_attr_map:
        target_b = brand_attr_map[pid]
        attrs = p.get('attributes', [])
        found = False
        for a in attrs:
            if a.get('name') == 'برند':
                a['options'] = [target_b]
                found = True
                break
        if not found:
            attrs.append({
                'id': 0,
                'name': 'برند',
                'slug': 'برند',
                'position': 0,
                'visible': True,
                'variation': False,
                'options': [target_b]
            })
        p['attributes'] = attrs

with open('data/products.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

with open('data/id_mappings.json', 'r', encoding='utf-8') as f:
    mappings = json.load(f)

slug_updates = {
    3534: 'haverson-85-inch-4k-smart-tv',
    3516: 'haverson-32-inch-hd-led-tv',
    2637: 'clover-rnt101-fnt101-twin-refrigerator-36ft',
    2408: 'clover-frnt101-refrigerator-27ft'
}

for item in mappings.get('products', []):
    pid = item.get('id')
    if pid in slug_updates:
        item['slug'] = slug_updates[pid]
        item['url'] = f"https://hosseinykala.ir/product/{slug_updates[pid]}/"

with open('data/id_mappings.json', 'w', encoding='utf-8') as f:
    json.dump(mappings, f, ensure_ascii=False, indent=2)

print("✓ Synced data/products.json and data/id_mappings.json successfully!")

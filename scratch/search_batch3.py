import requests
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

targets = [
    ('washing_and_cleaning', 'feridolin-sw35-mini-wash', 'مینی واش فریدولین 3.5', 'مینی واش فریدولین SW35'),
    ('cooking_appliances', 'donalex-dn970-airfryer', 'سرخ کن دونالکس DN-970', 'سرخ کن دونالکس 970'),
    ('beverage_makers', 'donalex-dn380-espresso', 'اسپرسوساز دونالکس 380', 'اسپرسوساز دونالکس 380'),
    ('beverage_makers', 'donalex-dn375-espresso', 'اسپرسوساز دونالکس 375', 'اسپرسوساز دونالکس 375'),
    ('cooking_appliances', 'parskhazar-rc361-rice-cooker', 'پلوپز پارس خزر مدل 361', 'پلوپز پارس خزر 361'),
    ('washing_and_cleaning', 'saper-4025-iron', 'اتوبخار ساپر 4025', 'اتو بخار ساپر 4025'),
    ('beverage_makers', 'saper-1031-kettle', 'کتری برقی ساپر 1031', 'کتری برقی ساپر 1031'),
    ('cooking_appliances', 'alton-v303-oven', 'فر توکار آلتون V303', 'فر برقی آلتون V303')
]

found = []
for cat, slug, name, q in targets:
    try:
        r = requests.get('https://api.digikala.com/v1/search/', params={'q': q}, headers=headers, timeout=6)
        if r.status_code == 200:
            prods = r.json().get('data', {}).get('products', [])
            print(f"Target: {name} (q='{q}') -> {len(prods)} products")
            for p in prods[:2]:
                title = p.get('title_fa')
                imgs = p.get('images', {}).get('main', {}).get('url', [])
                img_url = imgs[0].split('?')[0] if imgs else ''
                print(f"   Cand: {title}")
                print(f"         {img_url}")
                found.append({
                    'category': cat,
                    'slug': slug,
                    'target_name': name,
                    'query': q,
                    'cand_title': title,
                    'image_url': img_url
                })
    except Exception as e:
        print(f"Error {q}: {e}")

with open('scratch/batch3_cands.json', 'w', encoding='utf-8') as f:
    json.dump(found, f, ensure_ascii=False, indent=2)

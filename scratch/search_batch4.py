import requests
import json
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

targets = [
    ('beauty_health', 'panasonic-hv11-hair-straightener', 'اتو مو پاناسونیک HV11', 'اتو مو پاناسونیک HV11'),
    ('beauty_health', 'promaron-706-shaver', 'ریش تراش چرخشی پرومارون 706', 'ریش تراش پرومارون 706'),
    ('beverage_makers', 'volga-f164-kettle', 'کتری برقی ولگا', 'کتری برقی ولگا 64'),
    ('beverage_makers', 'castello-470-grinder', 'آسیاب برقی کاستلو 470', 'آسیاب کاستلو 470'),
    ('beverage_makers', 'grenwic-as2520-espresso', 'اسپرسوساز گرنویک', 'اسپرسو ساز گرناویک 2520')
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

with open('scratch/batch4_cands.json', 'w', encoding='utf-8') as f:
    json.dump(found, f, ensure_ascii=False, indent=2)

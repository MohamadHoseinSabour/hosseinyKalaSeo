import requests
import json
import os
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

targets = [
    ('cooking_appliances', 'aviz-granite-pan-28cm', 'تابه گرانیتی اویز سایز 28', 'تابه گرانیتی اویز 28'),
    ('cooking_appliances', 'aviz-granite-pan-32cm', 'تابه گرانیتی اویز سایز 32', 'تابه گرانیتی اویز 32'),
    ('beverage_makers', 'sunny-sn007-kettle', 'کتری برقی سانی 1.5 لیتر', 'کتری برقی سانی SN-007'),
    ('cooling_heating', 'parskhazar-4060-fan', 'پنکه پایه بلند پارس خزر', 'پنکه پارس خزر 4060'),
    ('beverage_makers', 'tefal-ki150d-kettle', 'کتری برقی تفال 2 لیتر', 'کتری برقی تفال KI150D')
]

downloaded = []
for cat, slug, target_name, q in targets:
    try:
        r = requests.get('https://api.digikala.com/v1/search/', params={'q': q}, headers=headers, timeout=6)
        if r.status_code == 200:
            prods = r.json().get('data', {}).get('products', [])
            if prods:
                p = prods[0]
                title = p.get('title_fa')
                imgs = p.get('images', {}).get('main', {}).get('url', [])
                if imgs:
                    raw_url = imgs[0].split('?')[0]
                    dest_dir = os.path.join('scratch', 'batch_eval', cat)
                    os.makedirs(dest_dir, exist_ok=True)
                    dest_file = os.path.join(dest_dir, f"{slug}.jpg")
                    
                    r_img = requests.get(raw_url, timeout=10)
                    if r_img.status_code == 200:
                        with open(dest_file, 'wb') as f_img:
                            f_img.write(r_img.content)
                        im = Image.open(dest_file)
                        w, h = im.size
                        downloaded.append({
                            'category': cat,
                            'slug': slug,
                            'target_name': target_name,
                            'cand_title': title,
                            'file_path': os.path.abspath(dest_file),
                            'dimensions': f"{w}x{h}"
                        })
                        print(f"Downloaded: {slug} ({w}x{h}) - Matched: {title}")
    except Exception as e:
        print(f"Error {slug}: {e}")

with open('scratch/batch5_cands.json', 'w', encoding='utf-8') as f:
    json.dump(downloaded, f, ensure_ascii=False, indent=2)

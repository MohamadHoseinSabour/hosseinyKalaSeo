import requests
import json
import os
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

targets = [
    {
        'category': 'beverage_makers',
        'slug': 'donalex-dn355-hand-mixer',
        'target_name': 'همزن دستی دونالکس مدل 355',
        'query': 'همزن دستی دونالکس DN-355'
    },
    {
        'category': 'beverage_makers',
        'slug': 'donalex-dn380-espresso-maker',
        'target_name': 'اسپرسوساز دونالکس 380',
        'query': 'اسپرسوساز دونالکس DN-380'
    },
    {
        'category': 'beauty_health',
        'slug': 'promaron-rl706-shaver',
        'target_name': 'ریش تراش چرخشی پرومارون مدل 706',
        'query': 'ریش تراش پرومارون RL-706'
    },
    {
        'category': 'cooking_appliances',
        'slug': 'alton-h312-hood',
        'target_name': 'هود آشپزخانه آلتون مدل H312',
        'query': 'هود آلتون H312'
    },
    {
        'category': 'cooking_appliances',
        'slug': 'alton-h315b-hood',
        'target_name': 'هود آشپزخانه آلتون مدل H315B',
        'query': 'هود آلتون H315B'
    }
]

downloaded = []
for it in targets:
    q = it['query']
    cat = it['category']
    slug = it['slug']
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
                        it['cand_title'] = title
                        it['file_path'] = os.path.abspath(dest_file)
                        it['dimensions'] = f"{w}x{h}"
                        downloaded.append(it)
                        print(f"Downloaded: {slug} ({w}x{h}) - Matched: {title}")
    except Exception as e:
        print(f"Error {slug}: {e}")

with open('scratch/batch_b_cands.json', 'w', encoding='utf-8') as f:
    json.dump(downloaded, f, ensure_ascii=False, indent=2)

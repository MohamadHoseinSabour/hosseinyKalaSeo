import requests
import json
import os
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

targets = [
    {
        'category': 'washing_and_cleaning',
        'slug': 'daewoo-dwk-990s-washing-machine-silver',
        'target_name': 'ماشین لباسشویی 9 کیلوگرم اتوماتیک دوو سری سینیور DWK-990 رنگ: سیلور (990S)',
        'query': 'ماشین لباسشویی دوو LM-990S'
    },
    {
        'category': 'washing_and_cleaning',
        'slug': 'pakshoma-15kg-twin-tub-washer',
        'target_name': 'ماشین لباسشویی دوقلو نیمه اتوماتیک پاکشوما ظرفیت: 15 کیلوگرم',
        'query': 'لباسشویی دوقلو پاکشوما FA15'
    },
    {
        'category': 'washing_and_cleaning',
        'slug': 'pakshoma-21kg-twin-tub-washer',
        'target_name': 'ماشین لباسشویی دوقلو نیمه اتوماتیک پاکشوما ظرفیت: 21 کیلوگرم',
        'query': 'لباسشویی دوقلو پاکشوما FA21'
    },
    {
        'category': 'refrigerators',
        'slug': 'niksan-rf8410-combi-fridge-steel',
        'target_name': 'یخچال و فریزر کمبی نیکسان مدل RF84102E2 رنگ: استیل',
        'query': 'یخچال نیکسان 8410 استیل'
    },
    {
        'category': 'refrigerators',
        'slug': 'clover-mini-refrigerator-snopi',
        'target_name': 'مینی یخچال 10 فوت کلور مدل طرح دار فانتزی',
        'query': 'یخچال کلور Snopi'
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

with open('scratch/batch_a_cands.json', 'w', encoding='utf-8') as f:
    json.dump(downloaded, f, ensure_ascii=False, indent=2)

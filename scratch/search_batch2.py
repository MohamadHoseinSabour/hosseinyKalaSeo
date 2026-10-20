import requests
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

targets = [
    ('cooking_appliances', 'alton-sg518-gas-hob', 'گاز صفحه ای آلتون SG518', 'گاز صفحه ای آلتون 518'),
    ('cooking_appliances', 'alton-h312-hood', 'هود آشپزخانه آلتون H312', 'هود آلتون H312'),
    ('cooking_appliances', 'alton-h315b-hood', 'هود آشپزخانه آلتون H315B', 'هود آلتون H315'),
    ('cooking_appliances', 'alton-built-in-oven-v303', 'فر توکار آلتون 7303', 'فر توکار آلتون'),
    ('cooking_appliances', 'parskhazar-rc361-rice-cooker', 'پلوپز پارس خزر 361', 'پلوپز پارس خزر 361'),
    ('cooking_appliances', 'parskhazar-rc181-silver-rice-cooker', 'پلوپز پارس خزر 8 نفره نقره ای', 'پلوپز 8 نفره پارس خزر نقره ای'),
    ('refrigerators', 'niksan-rf8410-combi-fridge', 'یخچال کمبی نیکسان RF84102E2', 'یخچال نیکسان 8410'),
    ('washing_and_cleaning', 'clover-viva-9kg-washer', 'لباسشویی کلور ویوا 9 کیلو', 'لباسشویی کلور ویوا'),
    ('washing_and_cleaning', 'hitachi-cv950f-vacuum', 'جاروبرقی سطلی هیتاچی 1200', 'جاروبرقی سطلی هیتاچی 950'),
    ('washing_and_cleaning', 'panda-80l-vacuum', 'جاروبرقی صنعتی پاندا 80 لیتر', 'جاروبرقی صنعتی Panda 80')
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

with open('scratch/batch2_cands.json', 'w', encoding='utf-8') as f:
    json.dump(found, f, ensure_ascii=False, indent=2)

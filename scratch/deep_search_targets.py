import requests
import json
import os
import sys
import urllib.parse
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

targets = [
    {
        'category': 'cooking_appliances',
        'slug': 'parskhazar-rc361-rice-cooker',
        'queries': ['پلوپز 361 پارس خزر', 'پلوپز تیان پارس خزر RC-361', 'پلوپز 16 نفره پارس خزر']
    },
    {
        'category': 'cooking_appliances',
        'slug': 'alton-sg518-gas-hob',
        'queries': ['اجاق گاز صفحه ای آلتون مدل SG518', 'گاز صفحه ای استیل آلتون مدل SG518', 'گاز آلتون SG518']
    },
    {
        'category': 'cooking_appliances',
        'slug': 'alton-h312-hood',
        'queries': ['هود مخفی آلتون مدل H312', 'هود آلتون مدل H312', 'هود آلتون H312']
    },
    {
        'category': 'cooking_appliances',
        'slug': 'alton-h315b-hood',
        'queries': ['هود مخفی آلتون مدل H315B', 'هود آلتون مدل H315B', 'هود آلتون H315']
    },
    {
        'category': 'washing_and_cleaning',
        'slug': 'pakshoma-9kg-twin-tub-washer',
        'queries': ['لباسشویی دوقلو پاکشوما 9.5', 'ماشین لباسشویی دوقلو پاکشوما 9 کیلو', 'لباسشویی دوقلو پاکشوما PWT-9654']
    },
    {
        'category': 'washing_and_cleaning',
        'slug': 'simaran-ssi8002-iron',
        'queries': ['اتو بخار سیماران مدل 8002', 'اتوبخار سیماران 8002', 'اتوبخار سیماران SSI-8002']
    },
    {
        'category': 'beverage_makers',
        'slug': 'saper-seb1031-kettle',
        'queries': ['کتری برقی ساپر مدل 1031', 'کتری ساپر 1031', 'کتری برقی ساپر SEB-1031']
    },
    {
        'category': 'beverage_makers',
        'slug': 'saper-seb1011-kettle',
        'queries': ['کتری برقی ساپر 1011', 'کتری برقی ساپر SEB-1011', 'کتری ساپر 1011']
    },
    {
        'category': 'beverage_makers',
        'slug': 'simaran-ek750-kettle',
        'queries': ['کتری برقی سیماران مدل 750', 'کتری برقی سیماران EK-750', 'کتری سیماران 750']
    },
    {
        'category': 'beverage_makers',
        'slug': 'castello-cpg470-grinder',
        'queries': ['آسیاب برقی کاستلو مدل 470', 'آسیاب کاستلو CPG-470', 'آسیاب برقی کاستلو 470']
    },
    {
        'category': 'beauty_health',
        'slug': 'panasonic-eh-hv11-hair-straightener',
        'queries': ['اتو مو پاناسونیک مدل EH-HV11', 'اتو مو مسافرتی پاناسونیک HV11', 'اتو مو پاناسونیک HV11']
    },
    {
        'category': 'beauty_health',
        'slug': 'promaron-rl706-shaver',
        'queries': ['ریش تراش پرومارون مدل RL-706', 'ریش تراش چرخشی پرومارون 706', 'ماشین اصلاح پرومارون 706']
    }
]

os.makedirs('scratch/deep_candidates', exist_ok=True)
results = {}

for t in targets:
    slug = t['slug']
    cat = t['category']
    results[slug] = []
    print(f"\n==========================================")
    print(f"Target: {slug}")
    
    found_urls = set()
    
    for q in t['queries']:
        # 1. Torob
        try:
            t_url = f"https://api.torob.com/v4/base-product/search/?sort=popularity&page=0&size=4&query={urllib.parse.quote(q)}"
            r = requests.get(t_url, headers=headers, timeout=8)
            if r.status_code == 200:
                for item in r.json().get('results', []):
                    title = item.get('name1', '')
                    img_url = item.get('image_url', '')
                    prk = item.get('random_key', '')
                    if img_url and img_url not in found_urls:
                        found_urls.add(img_url)
                        results[slug].append({
                            'source': 'torob',
                            'title': title,
                            'img_url': img_url,
                            'id': prk
                        })
                        print(f"  [Torob] {title}")
        except Exception as e:
            pass

        # 2. Digikala
        try:
            r = requests.get('https://api.digikala.com/v1/search/', params={'q': q}, headers=headers, timeout=8)
            if r.status_code == 200:
                for item in r.json().get('data', {}).get('products', []):
                    title = item.get('title_fa', '')
                    imgs = item.get('images', {}).get('main', {}).get('url', [])
                    img_url = imgs[0].split('?')[0] if imgs else ''
                    pid = item.get('id')
                    if img_url and img_url not in found_urls:
                        found_urls.add(img_url)
                        results[slug].append({
                            'source': 'digikala',
                            'title': title,
                            'img_url': img_url,
                            'id': pid
                        })
                        print(f"  [Digikala] {title}")
        except Exception as e:
            pass

with open('scratch/deep_search_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\nDeep search complete! Saved to scratch/deep_search_results.json")

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
        'category': 'cooling_heating',
        'slug': 'panasonic-pedestal-fan',
        'query': 'پنکه پاناسونیک',
        'sig': 'پاناسونیک'
    },
    {
        'category': 'cooling_heating',
        'slug': 'onax-b35-water-cooler',
        'query': 'کولر آبی اوناکس B35',
        'sig': 'اوناکس'
    },
    {
        'category': 'cooling_heating',
        'slug': 'onax-h50-water-cooler',
        'query': 'کولر آبی اوناکس 50',
        'sig': 'اوناکس'
    },
    {
        'category': 'beauty_health',
        'slug': 'panasonic-hv11-straightener',
        'query': 'اتو مو پاناسونیک HV11',
        'sig': 'HV11'
    },
    {
        'category': 'beauty_health',
        'slug': 'promaron-rl706-shaver',
        'query': 'ریش تراش پرومارون 706',
        'sig': '706'
    },
    {
        'category': 'beauty_health',
        'slug': 'promaron-9909-curler',
        'query': 'فر کننده مو پرومارون 9909',
        'sig': '9909'
    },
    {
        'category': 'water_purifiers',
        'slug': 'hano-water-dispenser',
        'query': 'آبسردکن هانو',
        'sig': 'هانو'
    },
    {
        'category': 'water_purifiers',
        'slug': 'westwater-water-purifier',
        'query': 'تصفیه آب وست واتر',
        'sig': 'وست واتر'
    },
    {
        'category': 'beverage_makers',
        'slug': 'zamrooti-cream-kettle',
        'query': 'کتری برقی زامروتی کرم',
        'sig': 'زامروتی'
    },
    {
        'category': 'beverage_makers',
        'slug': 'zamrooti-tea-maker',
        'query': 'چای ساز زامروتی',
        'sig': 'زامروتی'
    },
    {
        'category': 'beverage_makers',
        'slug': 'volga-f164-kettle',
        'query': 'کتری برقی ولگا 64',
        'sig': 'ولگا'
    },
    {
        'category': 'beverage_makers',
        'slug': 'willez-2015-tea-maker',
        'query': 'چای ساز ویلز 2015',
        'sig': 'ویلز'
    },
    {
        'category': 'cooking_appliances',
        'slug': 'alton-mds-gas-cooker',
        'query': 'اجاق گاز فردار آلتون MDS',
        'sig': 'MDS'
    },
    {
        'category': 'cooking_appliances',
        'slug': 'willez-5062-airfryer',
        'query': 'سرخ کن ویلز 5062',
        'sig': '5062'
    }
]

os.makedirs('scratch/candidates_batch_e', exist_ok=True)
downloaded = []

for t in targets:
    q = t['query']
    slug = t['slug']
    cat = t['category']
    sig = t['sig']
    print(f"\nSearching: {q} (sig: {sig})")
    
    # Try DK
    try:
        r = requests.get('https://api.digikala.com/v1/search/', params={'q': q}, headers=headers, timeout=6)
        if r.status_code == 200:
            prods = r.json().get('data', {}).get('products', [])
            for p in prods[:3]:
                title = p.get('title_fa', '')
                if sig.lower() in title.lower():
                    imgs = p.get('images', {}).get('main', {}).get('url', [])
                    if imgs:
                        raw_url = imgs[0].split('?')[0]
                        dest = f"scratch/candidates_batch_e/{slug}_dk.jpg"
                        r_img = requests.get(raw_url, headers=headers, timeout=8)
                        if r_img.status_code == 200:
                            with open(dest, 'wb') as f:
                                f.write(r_img.content)
                            im = Image.open(dest)
                            print(f"  [DK Matched] {title} -> {im.size}")
                            downloaded.append({
                                'target': t,
                                'source': 'digikala',
                                'title': title,
                                'file': dest,
                                'dimensions': im.size,
                                'pid': p.get('id')
                            })
                            break
    except Exception as e:
        print(f"  DK Err: {e}")

    # Try Torob
    try:
        t_url = f"https://api.torob.com/v4/base-product/search/?sort=popularity&page=0&size=4&query={urllib.parse.quote(q)}"
        r = requests.get(t_url, headers=headers, timeout=6)
        if r.status_code == 200:
            for item in r.json().get('results', [])[:3]:
                title = item.get('name1', '')
                img_url = item.get('image_url', '')
                if img_url and sig.lower() in title.lower():
                    dest = f"scratch/candidates_batch_e/{slug}_torob.jpg"
                    r_img = requests.get(img_url, headers=headers, timeout=8)
                    if r_img.status_code == 200:
                        with open(dest, 'wb') as f:
                            f.write(r_img.content)
                        im = Image.open(dest)
                        print(f"  [Torob Matched] {title} -> {im.size}")
                        downloaded.append({
                            'target': t,
                            'source': 'torob',
                            'title': title,
                            'file': dest,
                            'dimensions': im.size,
                            'pid': item.get('random_key')
                        })
                        break
    except Exception as e:
        print(f"  Torob Err: {e}")

with open('scratch/batch_e_downloaded.json', 'w', encoding='utf-8') as f:
    json.dump(downloaded, f, ensure_ascii=False, indent=2)

print(f"\nBatch E complete: {len(downloaded)} candidates downloaded!")

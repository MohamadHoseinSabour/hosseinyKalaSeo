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
        'target_name': 'پلوپز پارس خزر مدل 361',
        'dk_query': 'پلوپز پارس خزر 361',
        'torob_query': 'پلوپز پارس خزر 361',
        'sig_code': '361'
    },
    {
        'category': 'cooking_appliances',
        'slug': 'alton-sg518-gas-hob',
        'target_name': 'گاز صفحه ای استیل آلتون مدل SG518',
        'dk_query': 'گاز صفحه ای آلتون SG518',
        'torob_query': 'گاز صفحه ای آلتون SG518',
        'sig_code': '518'
    },
    {
        'category': 'cooking_appliances',
        'slug': 'alton-h312-hood',
        'target_name': 'هود آشپزخانه آلتون مدل H312',
        'dk_query': 'هود مخفی آلتون H312',
        'torob_query': 'هود آلتون H312',
        'sig_code': '312'
    },
    {
        'category': 'cooking_appliances',
        'slug': 'alton-h315b-hood',
        'target_name': 'هود آشپزخانه آلتون مدل H315B',
        'dk_query': 'هود مخفی آلتون H315B',
        'torob_query': 'هود آلتون H315B',
        'sig_code': '315'
    },
    {
        'category': 'washing_and_cleaning',
        'slug': 'pakshoma-21kg-twin-tub-washer',
        'target_name': 'ماشین لباسشویی دوقلو نیمه اتوماتیک پاکشوما 21 کیلوگرم',
        'dk_query': 'لباسشویی دوقلو پاکشوما 21',
        'torob_query': 'لباسشویی دوقلو پاکشوما 21',
        'sig_code': '21'
    },
    {
        'category': 'washing_and_cleaning',
        'slug': 'pakshoma-9kg-twin-tub-washer',
        'target_name': 'ماشین لباسشویی دوقلو نیمه اتوماتیک پاکشوما 9 کیلوگرم',
        'dk_query': 'لباسشویی دوقلو پاکشوما 9',
        'torob_query': 'لباسشویی دوقلو پاکشوما 9',
        'sig_code': '9'
    },
    {
        'category': 'washing_and_cleaning',
        'slug': 'simaran-ssi8002-iron',
        'target_name': 'اتوبخار سیماران مدل 8002 زرد',
        'dk_query': 'اتوبخار سیماران 8002',
        'torob_query': 'اتو بخار سیماران 8002',
        'sig_code': '8002'
    },
    {
        'category': 'beverage_makers',
        'slug': 'saper-seb1031-kettle',
        'target_name': 'کتری برقی ساپر مدل 1031',
        'dk_query': 'کتری برقی ساپر 1031',
        'torob_query': 'کتری برقی ساپر 1031',
        'sig_code': '1031'
    },
    {
        'category': 'beverage_makers',
        'slug': 'kenwood-hm430-hand-mixer',
        'target_name': 'همزن برقی کنوود مدل HM430',
        'dk_query': 'همزن کنوود HM430',
        'torob_query': 'همزن کنوود HM430',
        'sig_code': '430'
    },
    {
        'category': 'beverage_makers',
        'slug': 'castello-cpg470-grinder',
        'target_name': 'آسیاب برقی کاستلو مدل 470',
        'dk_query': 'آسیاب کاستلو 470',
        'torob_query': 'آسیاب کاستلو 470',
        'sig_code': '470'
    }
]

os.makedirs('scratch/candidates_batch_c', exist_ok=True)
results = []

for item in targets:
    print(f"\n--- Searching: {item['target_name']} ---")
    candidates = []
    
    # 1. Try Digikala search
    try:
        r = requests.get('https://api.digikala.com/v1/search/', params={'q': item['dk_query']}, headers=headers, timeout=6)
        if r.status_code == 200:
            prods = r.json().get('data', {}).get('products', [])
            for p in prods[:4]:
                pid = p.get('id')
                title = p.get('title_fa', '')
                main_img = p.get('images', {}).get('main', {}).get('url', [])
                img_url = main_img[0].split('?')[0] if main_img else ''
                candidates.append({
                    'source': 'digikala',
                    'product_id': pid,
                    'title': title,
                    'image_url': img_url
                })
    except Exception as e:
        print(f"DK Search Error: {e}")

    # 2. Try Torob search
    try:
        t_url = f"https://api.torob.com/v4/base-product/search/?sort=popularity&page=0&size=4&query={urllib.parse.quote(item['torob_query'])}"
        r = requests.get(t_url, headers=headers, timeout=6)
        if r.status_code == 200:
            res = r.json().get('results', [])
            for p in res[:3]:
                title = p.get('name1', '')
                img_url = p.get('image_url', '')
                candidates.append({
                    'source': 'torob',
                    'product_id': p.get('random_key'),
                    'title': title,
                    'image_url': img_url
                })
    except Exception as e:
        print(f"Torob Search Error: {e}")

    # Download matching candidates
    matched_downloaded = []
    idx = 0
    for cand in candidates:
        title = cand.get('title', '')
        url = cand.get('image_url', '')
        src = cand.get('source')
        if not url:
            continue
            
        # check sig_code
        if item['sig_code'].lower() in title.lower():
            idx += 1
            filename = f"{item['slug']}_cand{idx}.jpg"
            filepath = os.path.join('scratch', 'candidates_batch_c', filename)
            try:
                # If DK product, try to get gallery unbadged images!
                if src == 'digikala' and cand.get('product_id'):
                    pid = cand.get('product_id')
                    r_detail = requests.get(f'https://api.digikala.com/v2/product/{pid}/', headers=headers, timeout=6)
                    if r_detail.status_code == 200:
                        p_data = r_detail.json().get('data', {}).get('product', {})
                        gallery = p_data.get('images', {}).get('list', [])
                        if gallery:
                            # Try candidate image from gallery
                            for g_idx, g_img in enumerate(gallery[:4]):
                                g_url = g_img.get('url', [None])[0]
                                if g_url:
                                    g_clean = g_url.split('?')[0]
                                    g_name = f"{item['slug']}_gallery{g_idx+1}.jpg"
                                    g_path = os.path.join('scratch', 'candidates_batch_c', g_name)
                                    r_g = requests.get(g_clean, timeout=10)
                                    if r_g.status_code == 200:
                                        with open(g_path, 'wb') as gf:
                                            gf.write(r_g.content)
                                        im = Image.open(g_path)
                                        matched_downloaded.append({
                                            'type': f'dk_gallery_{g_idx+1}',
                                            'title': title,
                                            'path': g_path,
                                            'dimensions': f"{im.width}x{im.height}",
                                            'url': g_clean
                                        })
                
                # Also save direct URL
                r_img = requests.get(url, timeout=10)
                if r_img.status_code == 200:
                    with open(filepath, 'wb') as f:
                        f.write(r_img.content)
                    im = Image.open(filepath)
                    matched_downloaded.append({
                        'type': f'{src}_main',
                        'title': title,
                        'path': filepath,
                        'dimensions': f"{im.width}x{im.height}",
                        'url': url
                    })
                    print(f"  [FOUND & DOWNLOADED] {title} -> {im.width}x{im.height}")
            except Exception as dl_err:
                print(f"  DL Error: {dl_err}")

    results.append({
        'target': item,
        'matched_count': len(matched_downloaded),
        'candidates': matched_downloaded
    })

with open('scratch/batch_c_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\nBatch C harvesting complete! Saved to scratch/batch_c_results.json")

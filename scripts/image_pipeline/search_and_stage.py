import os
import sys
import re
import json
import time
import requests
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}

def clean_title(title):
    t = re.sub(r'[📂◀↳]', '', title).strip()
    return t

def slugify(text):
    # convert persian/english to clean slug
    t = text.lower()
    t = re.sub(r'[^a-zA-Z0-9\s-]', '', t)
    t = re.sub(r'\s+', '-', t).strip('-')
    return t if t else 'product'

def search_candidates_for_product(prod_info, max_candidates=3):
    name = prod_info.get('name', '')
    brand = prod_info.get('brand', '')
    parent_name = prod_info.get('parent_name', '')
    
    # Formulate smart search queries
    clean_name = clean_title(name)
    queries = []
    
    if parent_name:
        queries.append(f"{brand} {clean_title(parent_name)} {clean_name}")
        queries.append(f"{brand} {clean_title(parent_name)}")
    else:
        queries.append(f"{brand} {clean_name}")
        queries.append(clean_name)
        
    candidates = []
    seen_urls = set()
    
    for q in queries:
        try:
            url = "https://api.digikala.com/v1/search/"
            resp = requests.get(url, params={'q': q}, headers=HEADERS, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                products = data.get('data', {}).get('products', [])
                for p in products:
                    main_img = p.get('images', {}).get('main', {}).get('url', [])
                    if main_img:
                        raw_img_url = main_img[0].split('?')[0]
                        if raw_img_url not in seen_urls:
                            seen_urls.add(raw_img_url)
                            candidates.append({
                                'source': 'digikala_search',
                                'query_used': q,
                                'matched_product_id': p.get('id'),
                                'matched_title': p.get('title_fa'),
                                'image_url': raw_img_url
                            })
                    if len(candidates) >= max_candidates:
                        break
        except Exception as e:
            print(f"Error querying '{q}': {e}")
            
        if len(candidates) >= max_candidates:
            break
            
    return candidates

def download_candidates_for_item(item, output_base_dir='scratch/candidates'):
    slug = item.get('slug', 'prod_' + str(item.get('row', '0')))
    sheet_dir = item.get('sheet_en', 'misc')
    target_dir = os.path.join(output_base_dir, sheet_dir, slug)
    os.makedirs(target_dir, exist_ok=True)
    
    candidates = search_candidates_for_product(item)
    downloaded = []
    
    for idx, c in enumerate(candidates, 1):
        ext = 'jpg'
        dest_filename = f"cand_{idx}.{ext}"
        dest_path = os.path.join(target_dir, dest_filename)
        
        try:
            r = requests.get(c['image_url'], headers=HEADERS, timeout=15)
            if r.status_code == 200 and len(r.content) > 5000:
                with open(dest_path, 'wb') as f:
                    f.write(r.content)
                img = Image.open(dest_path)
                w, h = img.size
                downloaded.append({
                    'candidate_index': idx,
                    'file_path': dest_path,
                    'relative_path': os.path.relpath(dest_path),
                    'matched_title': c['matched_title'],
                    'matched_id': c['matched_product_id'],
                    'query_used': c['query_used'],
                    'image_url': c['image_url'],
                    'width': w,
                    'height': h,
                    'size_bytes': len(r.content)
                })
        except Exception as err:
            print(f"Error downloading {c['image_url']}: {err}")
            
    return downloaded

if __name__ == '__main__':
    # Test on a specific item
    test_item = {
        'row': 22,
        'name': 'یخچال و فریزر دوقلو هیمالیا مدل آیس پول 60MW',
        'brand': 'هیمالیا',
        'sheet_en': 'refrigerators',
        'slug': 'himalia-ice-pool-60mw-twin'
    }
    res = download_candidates_for_item(test_item)
    print(json.dumps(res, ensure_ascii=False, indent=2))

import os
import sys
import json
import time
import requests
from PIL import Image
import io

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_NEW_PRODS = os.path.join(PROJECT_DIR, 'data', 'new_products')

MASTER_PATH = os.path.join(PROJECT_DIR, 'scratch', 'products_44_master_data.json')
with open(MASTER_PATH, 'r', encoding='utf-8') as f:
    products = json.load(f)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

def search_digikala(query):
    try:
        url = 'https://api.digikala.com/v1/search/'
        r = requests.get(url, params={'q': query}, headers=HEADERS, timeout=4)
        if r.status_code == 200:
            items = r.json().get('data', {}).get('products', [])
            if items:
                img_url = items[0].get('images', {}).get('main', {}).get('url', [''])[0]
                if img_url:
                    return {
                        'source': 'digikala',
                        'title': items[0].get('title_fa'),
                        'img_url': img_url.split('?')[0] # get full res original
                    }
    except Exception as e:
        pass
    return None

def download_and_optimize_image(img_url, out_path):
    try:
        r = requests.get(img_url, headers=HEADERS, timeout=8)
        if r.status_code == 200:
            img = Image.open(io.BytesIO(r.content))
            img = img.convert('RGB')
            
            # Target size: 1000x1000 with white padding if needed
            w, h = img.size
            max_dim = max(w, h)
            
            # Create white square canvas
            square_img = Image.new('RGB', (max_dim, max_dim), (255, 255, 255))
            paste_x = (max_dim - w) // 2
            paste_y = (max_dim - h) // 2
            square_img.paste(img, (paste_x, paste_y))
            
            # Resize to 1000x1000
            if max_dim != 1000:
                square_img = square_img.resize((1000, 1000), Image.Resampling.LANCZOS)
                
            # Save as WebP ~90-110 KB
            square_img.save(out_path, 'WEBP', quality=85, method=6)
            file_size_kb = os.path.getsize(out_path) / 1024
            return True, file_size_kb, img.size
    except Exception as e:
        return False, str(e), None
    return False, "Download failed", None

results = []

for idx, p in enumerate(products):
    slug = p['slug']
    folder = os.path.join(DATA_NEW_PRODS, slug, 'images')
    out_webp = os.path.join(folder, 'featured.webp')
    
    # Check if already downloaded
    if os.path.exists(out_webp) and os.path.getsize(out_webp) > 10000:
        print(f"[{idx+1}/{len(products)}] ALREADY EXISTS: {slug}")
        results.append({'slug': slug, 'status': 'existing', 'size_kb': os.path.getsize(out_webp)/1024})
        continue

    query = p.get('search_term') or p['name']
    print(f"[{idx+1}/{len(products)}] Searching for '{query}'...")
    
    found = search_digikala(query)
    # If not found with full query, try model and brand
    if not found:
        short_query = f"{p['brand_fa']} {p['model']}"
        found = search_digikala(short_query)
        
    if found:
        img_url = found['img_url']
        print(f"   ✓ Found on {found['source']}: {found['title'][:40]} -> {img_url}")
        success, size_kb, orig_size = download_and_optimize_image(img_url, out_webp)
        if success:
            print(f"   ✓ Saved {out_webp} ({size_kb:.1f} KB, orig: {orig_size})")
            results.append({'slug': slug, 'status': 'downloaded', 'size_kb': size_kb, 'source': found['source'], 'img_url': img_url})
            # Save metadata
            meta = {
                'source': found['source'],
                'source_title': found['title'],
                'original_url': img_url,
                'file_size_kb': size_kb,
                'dimensions': [1000, 1000]
            }
            with open(os.path.join(folder, 'image_info.json'), 'w', encoding='utf-8') as f_meta:
                json.dump(meta, f_meta, ensure_ascii=False, indent=2)
        else:
            print(f"   ✗ Download error: {size_kb}")
            results.append({'slug': slug, 'status': 'failed_download', 'error': size_kb})
    else:
        print(f"   ✗ Not found on Digikala: {query}")
        results.append({'slug': slug, 'status': 'not_found', 'query': query})
        
    time.sleep(0.3)

summary_path = os.path.join(PROJECT_DIR, 'scratch', 'image_search_summary_pass1.json')
with open(summary_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

downloaded_count = sum(1 for r in results if r['status'] in ['downloaded', 'existing'])
print(f"\n=======================================================")
print(f"Pass 1 Complete: {downloaded_count} / {len(products)} images secured.")
print(f"=======================================================")

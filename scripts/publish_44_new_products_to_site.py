import os
import sys
import json
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_NEW_PRODS = os.path.join(PROJECT_DIR, 'data', 'new_products')
OUT_RESULT = os.path.join(PROJECT_DIR, 'scratch', 'published_44_products_result.json')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

LOCK = threading.Lock()

def upload_image(slug, name, img_path):
    with open(img_path, 'rb') as f:
        img_bytes = f.read()

    upload_headers = {
        'User-Agent': 'Mozilla/5.0',
        'Content-Type': 'image/webp',
        'Content-Disposition': f'attachment; filename="{slug}.webp"'
    }

    url = 'https://hosseinykala.ir/wp-json/wp/v2/media'
    r = requests.post(url, auth=AUTH, headers=upload_headers, data=img_bytes, timeout=45)
    if r.status_code in [200, 201]:
        m_data = r.json()
        media_id = m_data.get('id')
        media_url = m_data.get('source_url')
        
        # Update Alt and Title
        try:
            requests.post(
                f'https://hosseinykala.ir/wp-json/wp/v2/media/{media_id}',
                auth=AUTH,
                headers=HEADERS,
                json={'alt_text': name, 'title': name},
                timeout=15
            )
        except Exception:
            pass
        return media_id, media_url
    else:
        raise Exception(f"Media upload failed ({r.status_code}): {r.text[:150]}")

def create_product(prod_data, media_id):
    slug = prod_data['slug']
    name = prod_data['name']
    
    # Format categories
    cat_objs = [{'id': cid} for cid in prod_data.get('wc_category_ids', [])]
    
    # Format attributes
    wc_attrs = []
    for idx, attr in enumerate(prod_data.get('attributes', [])):
        wc_attrs.append({
            'name': attr['name'],
            'position': idx,
            'visible': True,
            'variation': False,
            'options': attr['options']
        })

    payload = {
        'name': name,
        'slug': slug,
        'type': 'simple',
        'status': 'publish', # published on site
        'featured': False,
        'catalog_visibility': 'visible',
        'description': prod_data.get('description') or prod_data.get('long_description', ''),
        'short_description': prod_data.get('short_description', ''),
        'sku': f"HK-{slug.upper()}",
        'manage_stock': False,
        'stock_status': 'outofstock', # set to out of stock as explicitly requested
        'regular_price': '',
        'sale_price': '',
        'categories': cat_objs,
        'images': [{'id': media_id, 'alt': name}] if media_id else [],
        'attributes': wc_attrs,
        'meta_data': [
            {'key': '_yoast_wpseo_metadesc', 'value': prod_data.get('meta_description', '')},
            {'key': 'rank_math_description', 'value': prod_data.get('meta_description', '')},
            {'key': '_yoast_wpseo_focuskw', 'value': prod_data.get('focus_keyword', '')},
            {'key': 'rank_math_focus_keyword', 'value': prod_data.get('focus_keyword', '')},
            {'key': '_yoast_wpseo_title', 'value': f"{name} | فروشگاه لوازم خانگی حسینی"},
            {'key': 'rank_math_title', 'value': f"{name} | فروشگاه لوازم خانگی حسینی"}
        ]
    }

    url = 'https://hosseinykala.ir/wp-json/wc/v3/products'
    r = requests.post(url, auth=AUTH, headers=HEADERS, json=payload, timeout=45)
    if r.status_code in [200, 201]:
        res_data = r.json()
        return res_data.get('id'), res_data.get('permalink')
    else:
        raise Exception(f"Product creation failed ({r.status_code}): {r.text[:150]}")

def process_single_product(slug, published_results, total_count):
    info_path = os.path.join(DATA_NEW_PRODS, slug, 'info.json')
    img_path = os.path.join(DATA_NEW_PRODS, slug, 'images', 'featured.webp')
    
    if not os.path.exists(info_path):
        return False, f"Missing info.json for {slug}"
        
    with open(info_path, 'r', encoding='utf-8') as f:
        prod_info = json.load(f)
        
    # Upload Media
    media_id = None
    media_url = None
    if os.path.exists(img_path):
        try:
            media_id, media_url = upload_image(slug, prod_info['name'], img_path)
        except Exception as e:
            print(f"[{slug}] ⚠️ Media error: {e}", flush=True)
            
    # Create Product
    try:
        pid, permalink = create_product(prod_info, media_id)
        
        with LOCK:
            published_results[slug] = {
                'slug': slug,
                'name': prod_info['name'],
                'product_id': pid,
                'permalink': permalink,
                'media_id': media_id,
                'media_url': media_url,
                'status': 'publish',
                'stock_status': 'outofstock',
                'published_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            curr_done = len(published_results)
            print(f"[{curr_done}/{total_count}] ✓ منتشر شد (PID: {pid}): {prod_info['name'][:35]}", flush=True)
            with open(OUT_RESULT, 'w', encoding='utf-8') as f_out:
                json.dump(published_results, f_out, ensure_ascii=False, indent=2)
                
        return True, pid
    except Exception as e:
        print(f"[{slug}] ❌ Create error: {e}", flush=True)
        return False, str(e)

def main():
    folders = sorted([f for f in os.listdir(DATA_NEW_PRODS) if os.path.isdir(os.path.join(DATA_NEW_PRODS, f))])
    print(f"=== اجرای سریع هم‌روند انتشار {len(folders)} محصول جدید در سایت (۳ پردازش همزمان) ===", flush=True)
    
    published_results = {}
    if os.path.exists(OUT_RESULT):
        with open(OUT_RESULT, 'r', encoding='utf-8') as f:
            try:
                published_results = json.load(f)
            except Exception:
                published_results = {}
                
    remaining_slugs = [s for s in folders if s not in published_results or not published_results[s].get('product_id')]
    print(f"قبلاً منتشر شده: {len(published_results)} | باقی‌مانده جهت انتشار: {len(remaining_slugs)}", flush=True)
    
    if not remaining_slugs:
        print("✓ تمام محصولات قبلاً با موفقیت منتشر شده‌اند!", flush=True)
        return

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(process_single_product, slug, published_results, len(folders)): slug for slug in remaining_slugs}
        for future in as_completed(futures):
            slug = futures[future]
            try:
                ok, res = future.result()
            except Exception as e:
                print(f"[{slug}] Exception: {e}", flush=True)

    print(f"\n✓ فرآیند کامل شد! جمع کل کالاهای منتشر شده: {len(published_results)} از {len(folders)}", flush=True)

if __name__ == '__main__':
    main()

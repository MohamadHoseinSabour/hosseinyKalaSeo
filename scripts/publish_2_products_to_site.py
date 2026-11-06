import os
import sys
import json
import time
import requests
from requests.auth import HTTPBasicAuth

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEW_PRODS_DIR = os.path.join(PROJECT_DIR, 'data', 'new_products')
OUTPUT_RESULT = os.path.join(PROJECT_DIR, 'scratch', 'published_2_products_result.json')

AUTH = HTTPBasicAuth('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
WP_BASE = 'https://hosseinykala.ir'
MEDIA_API = f'{WP_BASE}/wp-json/wp/v2/media'
WC_PRODUCTS_API = f'{WP_BASE}/wp-json/wc/v3/products'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

SLUGS = [
    "candy-kcv-325-g-vacuum-cleaner",
    "olive-43-inch-ol-43fss30-smart-tv"
]

def upload_image(image_path, title, slug):
    print(f"در حال آپلود تصویر برای {slug}...")
    with open(image_path, 'rb') as img_f:
        img_bytes = img_f.read()

    media_headers = dict(HEADERS)
    media_headers.update({
        'Content-Disposition': f'attachment; filename="{slug}.webp"',
        'Content-Type': 'image/webp'
    })

    res = requests.post(MEDIA_API, data=img_bytes, headers=media_headers, auth=AUTH, timeout=40)
    if res.status_code in (200, 201):
        media_data = res.json()
        media_id = media_data.get('id')
        media_url = media_data.get('source_url', '')
        print(f"✓ تصویر با شناسه {media_id} آپلود شد.")
        return media_id, media_url
    else:
        raise Exception(f"خطای آپلود مدیا ({res.status_code}): {res.text[:200]}")

def publish_product(slug):
    p_dir = os.path.join(NEW_PRODS_DIR, slug)
    info_path = os.path.join(p_dir, 'info.json')
    with open(info_path, 'r', encoding='utf-8') as f:
        info = json.load(f)

    img_path = os.path.join(p_dir, 'images', 'featured.webp')
    media_id, media_url = upload_image(img_path, info['name'], slug)

    cat_list = [{'id': cid} for cid in info.get('wc_category_ids', [])]
    tag_list = [{'name': t} for t in info.get('tags', [])]
    
    sku = f"HK-{slug.upper()}"
    
    payload = {
        'name': info['name'],
        'slug': slug,
        'type': 'simple',
        'status': 'publish',
        'catalog_visibility': 'visible',
        'description': info['description'],
        'short_description': info['short_description'],
        'sku': sku,
        'price': '',
        'regular_price': '',
        'manage_stock': False,
        'stock_status': 'outofstock',
        'images': [{'id': media_id}],
        'categories': cat_list,
        'tags': tag_list,
        'attributes': info.get('attributes', []),
        'meta_data': [
            {'key': 'rank_math_focus_keyword', 'value': info.get('focus_keyword', '')},
            {'key': 'rank_math_description', 'value': info.get('meta_description', '')},
            {'key': '_yoast_wpseo_focuskw', 'value': info.get('focus_keyword', '')},
            {'key': '_yoast_wpseo_metadesc', 'value': info.get('meta_description', '')}
        ]
    }

    print(f"در حال ایجاد محصول در ووکامرس برای {slug}...")
    res = requests.post(WC_PRODUCTS_API, json=payload, headers=HEADERS, auth=AUTH, timeout=40)
    if res.status_code in (200, 201):
        prod_data = res.json()
        pid = prod_data.get('id')
        permalink = prod_data.get('permalink', f"{WP_BASE}/product/{slug}/")
        print(f"🎉 محصول با شناسه {pid} با موفقیت منتشر شد: {permalink}")
        return {
            'slug': slug,
            'name': info['name'],
            'product_id': pid,
            'permalink': permalink,
            'media_id': media_id,
            'media_url': media_url,
            'status': 'publish',
            'stock_status': 'outofstock',
            'sku': sku,
            'published_at': time.strftime("%Y-%m-%d %H:%M:%S")
        }
    else:
        raise Exception(f"خطای ایجاد محصول ({res.status_code}): {res.text[:300]}")

def main():
    print("=== انتشار ۲ محصول جدید در وب‌سایت ووکامرس حسینی کالا ===")
    results = {}
    for slug in SLUGS:
        res = publish_product(slug)
        results[slug] = res
        time.sleep(1)

    os.makedirs(os.path.dirname(OUTPUT_RESULT), exist_ok=True)
    with open(OUTPUT_RESULT, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n✅ نتایج در {os.path.basename(OUTPUT_RESULT)} ذخیره شد.")

if __name__ == '__main__':
    main()

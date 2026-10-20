import os
import sys
import json
import time
import requests
import urllib.parse
from html import unescape

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from requests.adapters import HTTPAdapter

class SourceAddressAdapter(HTTPAdapter):
    def __init__(self, source_address, **kwargs):
        self.source_address = source_address
        super().__init__(**kwargs)
    def init_poolmanager(self, *args, **kwargs):
        kwargs['source_address'] = (self.source_address, 0)
        return super().init_poolmanager(*args, **kwargs)

SESSION = requests.Session()
SESSION.mount('https://', SourceAddressAdapter('10.102.29.1'))
SESSION.mount('http://', SourceAddressAdapter('10.102.29.1'))

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'application/json'
}

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

def fetch_all_items(endpoint, params=None):
    if params is None:
        params = {}
    params['per_page'] = 100
    page = 1
    all_items = []
    
    while True:
        params['page'] = page
        url = f"https://hosseinykala.ir/wp-json/wp/v2/{endpoint}"
        success = False
        for attempt in range(5):
            try:
                res = SESSION.get(url, auth=AUTH, headers=HEADERS, params=params, timeout=30)
                if res.status_code != 200:
                    print(f"[{endpoint}] Page {page} status {res.status_code}: {res.text[:100]}")
                    break
                items = res.json()
                if not isinstance(items, list) or len(items) == 0:
                    success = True
                    break
                all_items.extend(items)
                
                total_pages = int(res.headers.get('X-WP-TotalPages', 1))
                print(f"[{endpoint}] Fetched page {page}/{total_pages} ({len(items)} items)")
                if page >= total_pages:
                    success = True
                    break
                page += 1
                success = True
                break
            except Exception as e:
                print(f"[{endpoint}] Attempt {attempt+1}/5 on page {page} failed: {e}")
                time.sleep(3)
                
        if not success or page > 20:
            break
            
    return all_items

def main():
    print("=== Starting Robust Full Data Sync from hosseinykala.ir ===")
    
    # 1. Fetch Product Categories
    print("\n1. Fetching Product Categories...")
    raw_pcats = fetch_all_items('product_cat')
    pcat_map = {c['id']: unescape(c['name']) for c in raw_pcats}
    product_categories = []
    for c in raw_pcats:
        p_obj = {
            'id': c['id'],
            'name': unescape(c['name']),
            'slug': c['slug'],
            'url': c['link'],
            'parent': c['parent'],
            'count': c['count'],
            'description': c.get('description', '')
        }
        product_categories.append(p_obj)
    
    # 2. Fetch Post Categories
    print("\n2. Fetching Post Categories (Blog)...")
    raw_cats = fetch_all_items('categories')
    cat_map = {c['id']: unescape(c['name']) for c in raw_cats}
    post_categories = []
    for c in raw_cats:
        c_obj = {
            'id': c['id'],
            'name': unescape(c['name']),
            'slug': c['slug'],
            'url': c['link'],
            'parent': c['parent'],
            'count': c['count'],
            'description': c.get('description', '')
        }
        post_categories.append(c_obj)

    # 3. Fetch Tags
    print("\n3. Fetching Tags...")
    raw_tags = fetch_all_items('tags')
    tag_map = {t['id']: unescape(t['name']) for t in raw_tags}
    tags_list = []
    for t in raw_tags:
        tags_list.append({
            'id': t['id'],
            'name': unescape(t['name']),
            'slug': t['slug'],
            'count': t['count']
        })

    # 4. Fetch Products
    print("\n4. Fetching Products...")
    raw_prods = fetch_all_items('product', {'status': 'any', '_embed': 'true'})
    products_list = []
    for p in raw_prods:
        feat_img = ''
        if '_embedded' in p and 'wp:featuredmedia' in p['_embedded']:
            medias = p['_embedded']['wp:featuredmedia']
            if medias and len(medias) > 0 and 'source_url' in medias[0]:
                feat_img = medias[0]['source_url']
        
        item_cats = []
        if '_embedded' in p and 'wp:term' in p['_embedded']:
            for term_group in p['_embedded']['wp:term']:
                for term in term_group:
                    if term.get('taxonomy') == 'product_cat':
                        item_cats.append({
                            'id': term.get('id'),
                            'name': unescape(term.get('name', '')),
                            'slug': term.get('slug', '')
                        })
        elif 'product_cat' in p:
            for cat_id in p['product_cat']:
                if cat_id in pcat_map:
                    item_cats.append({
                        'id': cat_id,
                        'name': pcat_map[cat_id]
                    })

        prod_obj = {
            'id': p['id'],
            'url': p.get('link', f"https://hosseinykala.ir/product/{p.get('slug')}/"),
            'slug': p.get('slug', ''),
            'name': unescape(p.get('title', {}).get('rendered', '')),
            'status': p.get('status', 'publish'),
            'price': p.get('price', None),
            'currency': 'IRT',
            'in_stock': p.get('status') == 'publish',
            'categories': item_cats,
            'featured_image': feat_img,
            'short_description': p.get('excerpt', {}).get('rendered', ''),
            'description': p.get('content', {}).get('rendered', ''),
            'date': p.get('date', ''),
            'modified': p.get('modified', '')
        }
        products_list.append(prod_obj)

    # 5. Fetch Posts / Articles
    print("\n5. Fetching Posts (Articles)...")
    raw_posts = fetch_all_items('posts', {'status': 'any', '_embed': 'true'})
    posts_list = []
    for p in raw_posts:
        feat_img = ''
        if '_embedded' in p and 'wp:featuredmedia' in p['_embedded']:
            medias = p['_embedded']['wp:featuredmedia']
            if medias and len(medias) > 0 and 'source_url' in medias[0]:
                feat_img = medias[0]['source_url']

        p_item_cats = []
        p_item_tags = []
        if '_embedded' in p and 'wp:term' in p['_embedded']:
            for term_group in p['_embedded']['wp:term']:
                for term in term_group:
                    tax = term.get('taxonomy')
                    if tax == 'category':
                        p_item_cats.append({
                            'id': term.get('id'),
                            'name': unescape(term.get('name', '')),
                            'slug': term.get('slug', '')
                        })
                    elif tax == 'post_tag':
                        p_item_tags.append({
                            'id': term.get('id'),
                            'name': unescape(term.get('name', '')),
                            'slug': term.get('slug', '')
                        })
        else:
            for cat_id in p.get('categories', []):
                if cat_id in cat_map:
                    p_item_cats.append({'id': cat_id, 'name': cat_map[cat_id]})
            for tag_id in p.get('tags', []):
                if tag_id in tag_map:
                    p_item_tags.append({'id': tag_id, 'name': tag_map[tag_id]})

        post_obj = {
            'id': p['id'],
            'url': p.get('link', f"https://hosseinykala.ir/{p.get('slug')}/"),
            'slug': p.get('slug', ''),
            'title': unescape(p.get('title', {}).get('rendered', '')),
            'status': p.get('status', 'publish'),
            'categories': p_item_cats,
            'tags': p_item_tags,
            'featured_image': feat_img,
            'excerpt': p.get('excerpt', {}).get('rendered', ''),
            'content': p.get('content', {}).get('rendered', ''),
            'date': p.get('date', ''),
            'modified': p.get('modified', '')
        }
        posts_list.append(post_obj)

    # Safety check: do not overwrite with empty lists if fetch failed
    if len(products_list) > 0:
        with open(os.path.join(DATA_DIR, 'products.json'), 'w', encoding='utf-8') as f:
            json.dump(products_list, f, ensure_ascii=False, indent=2)
        print(f"[SAVED] products.json ({len(products_list)} items)")

    if len(posts_list) > 0:
        with open(os.path.join(DATA_DIR, 'posts.json'), 'w', encoding='utf-8') as f:
            json.dump(posts_list, f, ensure_ascii=False, indent=2)
        print(f"[SAVED] posts.json ({len(posts_list)} items)")

    if len(product_categories) > 0:
        with open(os.path.join(DATA_DIR, 'categories.json'), 'w', encoding='utf-8') as f:
            json.dump(product_categories, f, ensure_ascii=False, indent=2)
        print(f"[SAVED] categories.json ({len(product_categories)} items)")

    if len(post_categories) > 0:
        with open(os.path.join(DATA_DIR, 'post_categories.json'), 'w', encoding='utf-8') as f:
            json.dump(post_categories, f, ensure_ascii=False, indent=2)
        print(f"[SAVED] post_categories.json ({len(post_categories)} items)")

    if len(tags_list) > 0:
        with open(os.path.join(DATA_DIR, 'tags.json'), 'w', encoding='utf-8') as f:
            json.dump(tags_list, f, ensure_ascii=False, indent=2)
        print(f"[SAVED] tags.json ({len(tags_list)} items)")

    # 6. Build ID Mappings
    if len(products_list) > 0 or len(posts_list) > 0:
        id_mappings = {
            'products': [
                {
                    'id': item['id'],
                    'name': item['name'],
                    'slug': item['slug'],
                    'shortlink': f"https://hosseinykala.ir/?p={item['id']}"
                }
                for item in sorted(products_list, key=lambda x: x['id'], reverse=True)
            ],
            'posts': [
                {
                    'id': item['id'],
                    'title': item['title'],
                    'slug': item['slug'],
                    'status': item['status'],
                    'shortlink': f"https://hosseinykala.ir/?p={item['id']}"
                }
                for item in sorted(posts_list, key=lambda x: x['id'], reverse=True)
            ],
            'product_categories': [
                {
                    'id': item['id'],
                    'name': item['name'],
                    'slug': item['slug'],
                    'url': item.get('url') or f"https://hosseinykala.ir/product-category/{item['slug']}/"
                }
                for item in sorted(product_categories, key=lambda x: x['name'])
            ],
            'post_categories': [
                {
                    'id': item['id'],
                    'name': item['name'],
                    'slug': item['slug'],
                    'shortlink': f"https://hosseinykala.ir/?cat={item['id']}"
                }
                for item in sorted(post_categories, key=lambda x: x['name'])
            ]
        }
        with open(os.path.join(DATA_DIR, 'id_mappings.json'), 'w', encoding='utf-8') as f:
            json.dump(id_mappings, f, ensure_ascii=False, indent=2)
        print(f"[SAVED] id_mappings.json ({len(id_mappings['products'])} products, {len(id_mappings['posts'])} posts)")

    print("\n=== Sync Completed Successfully! ===")

if __name__ == '__main__':
    main()

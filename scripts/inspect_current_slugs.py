import requests
import json
import urllib.parse

auth = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

posts_to_inspect = [3000, 3098, 3099, 3100, 3101, 3102]
products_to_inspect = [3453, 2972, 3395, 3266, 2680]

print("--- Inspecting Posts ---")
current_posts = {}
for pid in posts_to_inspect:
    r = requests.get(f'https://hosseinykala.ir/wp-json/wp/v2/posts/{pid}', auth=auth, headers=headers)
    if r.status_code == 200:
        data = r.json()
        current_posts[pid] = {
            'slug': data.get('slug'),
            'link': data.get('link'),
            'title': data.get('title', {}).get('rendered', '')
        }
        print(f"Post {pid}: slug='{data.get('slug')}', link='{data.get('link')}'")
    else:
        print(f"Post {pid}: HTTP {r.status_code} - {r.text[:100]}")

print("\n--- Inspecting Products ---")
current_products = {}
for pid in products_to_inspect:
    r = requests.get(f'https://hosseinykala.ir/wp-json/wp/v2/product/{pid}', auth=auth, headers=headers)
    if r.status_code == 200:
        data = r.json()
        current_products[pid] = {
            'slug': data.get('slug'),
            'link': data.get('link'),
            'title': data.get('title', {}).get('rendered', '')
        }
        print(f"Product {pid}: slug='{data.get('slug')}', link='{data.get('link')}'")
    else:
        print(f"Product {pid}: HTTP {r.status_code} - {r.text[:100]}")

with open('inspect_slugs_before.json', 'w', encoding='utf-8') as f:
    json.dump({'posts': current_posts, 'products': current_products}, f, ensure_ascii=False, indent=2)

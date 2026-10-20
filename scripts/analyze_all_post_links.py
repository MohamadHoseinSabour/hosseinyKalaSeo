import requests
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

r = requests.get('https://hosseinykala.ir/wp-json/wp/v2/posts?per_page=100&status=any', auth=AUTH, headers=HEADERS)
posts = r.json()
print(f"Total posts: {len(posts)}", flush=True)

all_site_links = {}

for p in posts:
    pid = p['id']
    title = p['title'].get('rendered', '')
    content = p.get('content', {}).get('raw') or p.get('content', {}).get('rendered', '')
    links = re.findall(r'href=["\'](https?://[^"\']+)["\']', content)
    for l in links:
        if 'hosseinykala.ir' in l:
            if l not in all_site_links:
                all_site_links[l] = []
            all_site_links[l].append((pid, title))

print(f"Total unique internal links across all posts: {len(all_site_links)}", flush=True)

cat_query_links = [l for l in all_site_links if 'product_cat=' in l]
prod_query_links = [l for l in all_site_links if re.search(r'\?p=\d+', l)]
canonical_cat_links = [l for l in all_site_links if '/product-category/' in l]
canonical_prod_links = [l for l in all_site_links if '/product/' in l]

print(f"\n--- Category Query Links (?product_cat=): {len(cat_query_links)} ---", flush=True)
for l in cat_query_links:
    posts_using = [str(x[0]) for x in all_site_links[l]]
    print(f"  {l} -> used in posts: {', '.join(posts_using)}", flush=True)

print(f"\n--- Product/Post Query Links (?p=ID): {len(prod_query_links)} ---", flush=True)
for l in prod_query_links:
    posts_using = [str(x[0]) for x in all_site_links[l]]
    print(f"  {l} -> used in posts: {', '.join(posts_using)}", flush=True)

print(f"\n--- Canonical Category Links: {len(canonical_cat_links)} ---", flush=True)
for l in canonical_cat_links:
    print(f"  {l}", flush=True)

print(f"\n--- Canonical Product Links: {len(canonical_prod_links)} ---", flush=True)
for l in canonical_prod_links:
    print(f"  {l}", flush=True)

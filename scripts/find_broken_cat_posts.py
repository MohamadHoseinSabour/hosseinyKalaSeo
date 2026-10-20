import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

r = requests.get('https://hosseinykala.ir/wp-json/wp/v2/posts?per_page=100&status=any', auth=AUTH, headers=HEADERS)
print(f"Status: {r.status_code}")
if r.status_code == 200:
    posts = r.json()
    print(f"Total posts fetched: {len(posts)}")
    bad_posts = []
    for p in posts:
        content = p.get('content', {}).get('raw') or p.get('content', {}).get('rendered', '')
        if 'product_cat=' in content or '?product_cat' in content:
            bad_posts.append((p['id'], p['title'].get('rendered', '')))
    print(f"Found {len(bad_posts)} posts containing ?product_cat=:")
    for pid, title in bad_posts:
        print(f" - [{pid}] {title}")
else:
    print(f"Error response: {r.text[:200]}")

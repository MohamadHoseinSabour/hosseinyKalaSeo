import re
import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

article_ids = [3851, 3853, 3855, 3857, 3859, 3861]

posts_data = {}

for pid in article_ids:
    r = requests.get(f'https://hosseinykala.ir/wp-json/wp/v2/posts/{pid}', auth=AUTH, headers=HEADERS)
    if r.status_code == 200:
        data = r.json()
        title = data.get('title', {}).get('rendered', '')
        content = data.get('content', {}).get('raw') or data.get('content', {}).get('rendered', '')
        status = data.get('status', '')
        slug = data.get('slug', '')
        links = re.findall(r'href=["\'](https?://[^"\']+)["\']', content)
        posts_data[pid] = {
            'title': title,
            'status': status,
            'slug': slug,
            'links': links
        }
        print(f"=== Post {pid}: {title} (status: {status}, slug: {slug}) ===")
        for l in links:
            print(f"   -> {l}")
    else:
        print(f"Error fetching post {pid}: {r.status_code}")

with open('data/current_article_links.json', 'w', encoding='utf-8') as f:
    json.dump(posts_data, f, ensure_ascii=False, indent=2)

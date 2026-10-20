import requests
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def fetch_posts():
    url = "https://hosseinykala.ir/wp-json/wp/v2/posts"
    params = {'per_page': 100, 'status': 'publish,future,draft'}
    r = requests.get(url, auth=AUTH, headers=HEADERS, params=params, timeout=20)
    if r.status_code != 200:
        print(f"Failed to fetch posts: {r.status_code}")
        # try without status or try publish only
        r = requests.get(url, auth=AUTH, headers=HEADERS, params={'per_page': 100}, timeout=20)
    
    posts = r.json()
    print(f"Fetched {len(posts)} posts.")
    summary = []
    for p in posts:
        summary.append({
            'id': p.get('id'),
            'title': p.get('title', {}).get('rendered'),
            'slug': p.get('slug'),
            'status': p.get('status'),
            'date': p.get('date'),
            'link': p.get('link'),
            'content_length': len(p.get('content', {}).get('raw') or p.get('content', {}).get('rendered', ''))
        })
    with open('data/all_posts_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print("Saved summary to data/all_posts_summary.json")

if __name__ == '__main__':
    fetch_posts()

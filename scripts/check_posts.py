import sys
import json
import requests
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Content-Type': 'application/json'
}

def check_posts():
    r = requests.get('https://hosseinykala.ir/wp-json/wp/v2/posts?status=any&per_page=100', auth=AUTH, headers=HEADERS)
    posts = r.json()
    print(f"Total posts on site: {len(posts)}")
    for p in sorted(posts, key=lambda x: x['date']):
        print(f"ID: {p['id']} | Status: {p['status']} | Date: {p['date']} | Slug: {p['slug']} | Title: {p['title']['rendered'][:45]}")

if __name__ == '__main__':
    check_posts()

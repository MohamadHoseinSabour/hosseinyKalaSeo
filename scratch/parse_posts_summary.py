import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/all_posts_summary.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

print('Total posts:', len(posts))
for p in posts:
    print(f"ID: {p.get('id')} | Slug: {p.get('slug')} | Title: {p.get('title')}")

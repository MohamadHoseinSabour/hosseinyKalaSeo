import sys
import json
import requests

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

with open('data/categories.json', encoding='utf-8') as f:
    cats = json.load(f)

print(f"Total categories: {len(cats)}")
main_cats = [c for c in cats if c.get('parent') == 0]
print(f"Main categories: {len(main_cats)}")

for c in main_cats:
    url = c.get('url')
    cid = c.get('id')
    name = c.get('name')
    slug = c.get('slug')
    try:
        r = requests.get(url, headers=HEADERS, timeout=12)
        print(f"ID: {cid} | Name: {name} | Status: {r.status_code} | URL: {url}")
    except Exception as e:
        print(f"ID: {cid} | Name: {name} | Error: {e}")

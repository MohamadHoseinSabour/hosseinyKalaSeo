import json
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/categories.json', encoding='utf-8') as f:
    cats = json.load(f)

print(f"Total categories in data/categories.json: {len(cats)}")
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for c in cats:
    url = c['url']
    try:
        r = requests.get(url, headers=headers, timeout=10)
        print(f"[{r.status_code}] ID: {c['id']:<4} | Name: {c['name']:<25} | URL: {url}")
    except Exception as e:
        print(f"[ERR] ID: {c['id']:<4} | Name: {c['name']:<25} | Error: {e}")

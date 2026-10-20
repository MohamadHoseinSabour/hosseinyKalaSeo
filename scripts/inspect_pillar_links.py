import requests
import json
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

r = requests.get('https://hosseinykala.ir/wp-json/wp/v2/posts/3851', auth=AUTH, headers=HEADERS)
data = r.json()
content = data.get('content', {}).get('raw') or data.get('content', {}).get('rendered', '')

links = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', content, re.DOTALL)
print(f"Total links in Post 3851: {len(links)}\n")
for href, anchor in links:
    clean_anchor = re.sub(r'<[^>]+>', '', anchor).strip()
    print(f"[{href}] ===> '{clean_anchor}'")

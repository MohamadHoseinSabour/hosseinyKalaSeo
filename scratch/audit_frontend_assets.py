import requests
from bs4 import BeautifulSoup
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'}
r = requests.get('https://hosseinykala.ir/', headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

print(f"HTML Size: {len(r.text) / 1024:.1f} KB")

css_tags = soup.find_all('link', rel='stylesheet')
print(f"\nCSS Files ({len(css_tags)} total):")
for c in css_tags:
    href = c.get('href', '')
    media = c.get('media', 'all')
    print(f"  [{media}] {href}")

js_tags = soup.find_all('script', src=True)
print(f"\nJS Files ({len(js_tags)} total):")
for s in js_tags:
    src = s.get('src', '')
    async_attr = 'async' if s.has_attr('async') else ''
    defer_attr = 'defer' if s.has_attr('defer') else ''
    flags = f"{async_attr} {defer_attr}".strip() or "blocking"
    print(f"  [{flags}] {src}")

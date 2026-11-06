import requests
from bs4 import BeautifulSoup
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}

r = requests.get('https://hosseinykala.ir/', headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

print("=== 1. Header & Hero Images ===")
imgs = soup.find_all('img')
print(f"Total img tags: {len(imgs)}")
for idx, img in enumerate(imgs[:10]):
    print(f"\nImage #{idx+1}:")
    print(f"  class: {img.get('class')}")
    print(f"  src: {img.get('src')[:80] if img.get('src') else 'None'}")
    print(f"  data-src: {img.get('data-src')[:80] if img.get('data-src') else 'None'}")
    print(f"  width: {img.get('width')}, height: {img.get('height')}")
    print(f"  loading: {img.get('loading')}")
    print(f"  fetchpriority: {img.get('fetchpriority')}")
    print(f"  data-lazyloaded: {img.get('data-lazyloaded')}")

print("\n=== 2. Preload Tags ===")
preloads = soup.find_all('link', rel='preload')
print(f"Total preloads: {len(preloads)}")
for p in preloads:
    print(f"  as={p.get('as')}, href={p.get('href')[:80]}")

print("\n=== 3. Font Declarations & font-display ===")
# Search in style tags or linked fonts
for s in soup.find_all('style'):
    if '@font-face' in s.text:
        print("Found @font-face in inline style:")
        for line in s.text.splitlines():
            if 'font-family' in line or 'font-display' in line or 'src:' in line:
                print("  ", line.strip()[:100])

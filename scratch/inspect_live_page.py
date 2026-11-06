import requests
import re
from bs4 import BeautifulSoup

url = "https://hosseinykala.ir/"
mobile_ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"

r = requests.get(url, headers={"User-Agent": mobile_ua}, timeout=30)
html = r.text

print(f"Status: {r.status_code}, HTML length: {len(html)} chars")

soup = BeautifulSoup(html, 'html.parser')

print("\n--- 1. Stylesheets (<link rel='stylesheet'>) ---")
stylesheets = soup.find_all('link', rel=lambda x: x and 'stylesheet' in x)
for s in stylesheets:
    href = s.get('href', '')
    media = s.get('media', 'all')
    print(f"CSS: href={href} | media={media}")

print("\n--- 2. Preloads (<link rel='preload'>) ---")
preloads = soup.find_all('link', rel=lambda x: x and 'preload' in x)
for p in preloads:
    href = p.get('href', '')
    as_type = p.get('as', '')
    fp = p.get('fetchpriority', '')
    print(f"PRELOAD: as={as_type} | fetchpriority={fp} | href={href}")

print("\n--- 3. Scripts (<script>) ---")
scripts = soup.find_all('script')
head_scripts = soup.head.find_all('script') if soup.head else []
print(f"Total scripts: {len(scripts)}, Head scripts: {len(head_scripts)}")
for sc in head_scripts:
    src = sc.get('src')
    defer = sc.get('defer') is not None
    async_attr = sc.get('async') is not None
    if src:
        print(f"HEAD JS: src={src} | defer={defer} | async={async_attr}")

print("\n--- 4. Specific Banner: clover-october-sale-square-banner.webp ---")
for img in soup.find_all('img'):
    src = img.get('src', '')
    data_src = img.get('data-src', '')
    srcset = img.get('srcset', '')
    if 'clover' in src or 'clover' in data_src or 'square-banner' in src or 'square-banner' in data_src:
        print(f"IMG FOUND:")
        print(f"  src: {src}")
        print(f"  data-src: {data_src}")
        print(f"  srcset: {srcset[:100]}..." if srcset else "  srcset: None")
        print(f"  sizes: {img.get('sizes')}")
        print(f"  width: {img.get('width')}, height: {img.get('height')}")
        print(f"  loading: {img.get('loading')}")
        print(f"  fetchpriority: {img.get('fetchpriority')}")
        print(f"  class: {img.get('class')}")
        print(f"  parent tag: {img.parent.name if img.parent else 'None'}, parent class: {img.parent.get('class') if img.parent else ''}")

print("\n--- 5. Fonts in CSS or Inline ---")
# Search for @font-face in inline styles
style_tags = soup.find_all('style')
for idx, st in enumerate(style_tags):
    text = st.get_text()
    if '@font-face' in text:
        print(f"\nStyle tag #{idx} has @font-face:")
        font_faces = re.findall(r'@font-face\s*\{[^}]+\}', text)
        for ff in font_faces:
            print("  " + " ".join(ff.split())[:120] + "...")

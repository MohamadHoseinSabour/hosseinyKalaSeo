import requests
from bs4 import BeautifulSoup
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'}
r = requests.get('https://hosseinykala.ir/', headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

body = soup.find('body')
# Find all images inside the main content area
main = soup.find('div', class_=lambda c: c and ('main-page-wrapper' in c or 'site-content' in c or 'elementor' in c))
if main:
    print("Main container:", main.get('class'))
    content_imgs = main.find_all('img')
    print(f"Total images in main: {len(content_imgs)}")
    for idx, img in enumerate(content_imgs[:10]):
        src = img.get('src') or ''
        data_src = img.get('data-src') or ''
        classes = img.get('class') or []
        parent = img.parent
        print(f"\n[Main Img #{idx+1}]:")
        print(f"  class: {classes}")
        print(f"  src: {src[:70]}")
        print(f"  data-src: {data_src[:70]}")
        print(f"  parent: {parent.name} | class: {parent.get('class')}")
        print(f"  width: {img.get('width')}, height: {img.get('height')}")
        print(f"  loading: {img.get('loading')}")
        print(f"  fetchpriority: {img.get('fetchpriority')}")

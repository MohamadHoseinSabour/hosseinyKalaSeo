import requests
from bs4 import BeautifulSoup
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'}
r = requests.get('https://hosseinykala.ir/', headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

print(f"HTTP Status: {r.status_code}")
print(f"Cache Header: {r.headers.get('x-hosseinykala-cache', 'NONE')}")

print("\n=== 1. PRELOADS in <head> ===")
preloads = soup.find_all('link', rel='preload')
print(f"Total Preloads: {len(preloads)}")
for p in preloads:
    print(f"  as={p.get('as')}, href={p.get('href')[:80]}, type={p.get('type')}")

print("\n=== 2. LAYOUT RESERVATION STYLE ===")
opt_style = soup.find('style', id='hk-lcp-cls-optimizer')
print(f"Optimization style present: {bool(opt_style)}")
if opt_style:
    print("Style preview:\n", opt_style.text[:300].strip())

print("\n=== 3. HERO BANNER IMG TAG ===")
hero_img = soup.find('img', src=lambda s: s and 'clover-home-appliances-october-sale-banner' in s)
if not hero_img:
    hero_img = soup.find('img', attrs={'data-xts-src': lambda s: s and 'clover-home-appliances-october-sale-banner' in s})

if hero_img:
    print("Hero Img found!")
    print(f"  src: {hero_img.get('src')[:80]}")
    print(f"  loading: {hero_img.get('loading')}")
    print(f"  fetchpriority: {hero_img.get('fetchpriority')}")
    print(f"  class: {hero_img.get('class')}")
    print(f"  w={hero_img.get('width')}, h={hero_img.get('height')}")
else:
    print("Hero img NOT found!")

print("\n=== 4. LOGO IMG TAG ===")
logo_img = soup.find('img', class_=lambda c: c and 'xts-logo-main' in c)
if logo_img:
    print("Logo Img found!")
    print(f"  src: {logo_img.get('src')[:80]}")
    print(f"  w={logo_img.get('width')}, h={logo_img.get('height')}")
    print(f"  fetchpriority: {logo_img.get('fetchpriority')}")

import requests
import re
from bs4 import BeautifulSoup

mobile_ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
headers = {'User-Agent': mobile_ua}

r = requests.get('https://hosseinykala.ir/', headers=headers, timeout=25)
print("Homepage fetch status:", r.status_code, "Length:", len(r.text))

soup = BeautifulSoup(r.text, 'html.parser')

print("\n--- Preload Tags in Head ---")
for l in soup.find_all('link', rel=lambda x: x and 'preload' in x):
    print(f"  as={l.get('as')} | media={l.get('media')} | href={l.get('href')}")

print("\n--- Script Tags in Head ---")
for s in (soup.head.find_all('script') if soup.head else []):
    if s.get('src'):
        print(f"  src={s.get('src')} | defer={s.get('defer')}")

print("\n--- Mobile Banner Image Tag ---")
m_img = soup.find('img', src=re.compile(r'clover-october-sale-square-banner'))
if m_img:
    print("Found mobile banner img:")
    print("  src:", m_img.get('src'))
    print("  class:", m_img.get('class'))
    print("  width:", m_img.get('width'), "height:", m_img.get('height'))
    print("  sizes:", m_img.get('sizes'))
    print("  loading:", m_img.get('loading'))
    print("  fetchpriority:", m_img.get('fetchpriority'))
else:
    # Search in raw text
    print("m_img not matched by BeautifulSoup. Searching raw regex...")
    m = re.search(r'(<img[^>]*clover-october-sale-square-banner[^>]*>)', r.text)
    if m:
        print("Raw tag:", m.group(1))
    else:
        print("Banner not found in HTML!")

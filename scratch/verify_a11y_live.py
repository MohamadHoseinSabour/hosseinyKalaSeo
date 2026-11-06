import requests
import re
from bs4 import BeautifulSoup

mobile_ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
r = requests.get('https://hosseinykala.ir/', headers={'User-Agent': mobile_ua}, timeout=20)
print("Fetch status:", r.status_code)

soup = BeautifulSoup(r.text, 'html.parser')

print("\n--- Viewport Meta ---")
vp = soup.find('meta', attrs={'name': 'viewport'})
print("Viewport content:", vp.get('content') if vp else "None")

print("\n--- Category Links aria-label ---")
cat_links = soup.find_all('a', class_=lambda c: c and 'xts-cat-link' in c)
print(f"Total .xts-cat-link found: {len(cat_links)}")
for l in cat_links[:3]:
    print("  Link href:", l.get('href'), "| aria-label:", l.get('aria-label'))

print("\n--- Contrast CSS in hk-core-stability-css ---")
style = soup.find('style', id='hk-core-stability-css')
if style and 'Accessibility (A11y)' in style.get_text():
    print("Contrast CSS found and present!")
else:
    print("Contrast CSS NOT found in style tag!")

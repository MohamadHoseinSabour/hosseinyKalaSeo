import urllib.request
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

req = urllib.request.Request('https://hosseinykala.ir/shop/', headers={'User-Agent': 'Mozilla/5.0 (iPhone)'})
with urllib.request.urlopen(req, timeout=15) as r:
    html = r.read().decode('utf-8', errors='ignore')

# find products in shop
products = re.findall(r'<div[^>]*class=[\'"][^\'"]*product[^\'"]*[\'"][^>]*>', html)
print('Total product divs:', len(products))
if products:
    print('Sample product div:', products[0])

# Search for any img tags in the main content
main_imgs = re.findall(r'<img[^>]+>', html)
print(f'Total imgs on shop: {len(main_imgs)}')
for i, img in enumerate(main_imgs[2:6]):
    print(f'[{i}] {img[:250]}')

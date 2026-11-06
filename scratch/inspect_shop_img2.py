import urllib.request
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

req = urllib.request.Request('https://hosseinykala.ir/shop/', headers={'User-Agent': 'Mozilla/5.0 (iPhone)'})
with urllib.request.urlopen(req, timeout=15) as r:
    html = r.read().decode('utf-8', errors='ignore')

# find products in shop
products = re.findall(r'<li[^>]*class=[\'"][^\'"]*product[^\'"]*[\'"][^>]*>.*?</li>', html, re.DOTALL)
print('Total products on shop page:', len(products))
if products:
    p1 = products[0]
    imgs = re.findall(r'<img[^>]+>', p1)
    print(f'First product has {len(imgs)} images:')
    for img in imgs:
        print(' ', img[:250])

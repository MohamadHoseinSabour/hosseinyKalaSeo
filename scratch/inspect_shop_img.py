import urllib.request
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

req = urllib.request.Request('https://hosseinykala.ir/shop/', headers={'User-Agent': 'Mozilla/5.0 (iPhone)'})
with urllib.request.urlopen(req, timeout=15) as r:
    html = r.read().decode('utf-8', errors='ignore')

matches = re.findall(r'<img[^>]*class=[\'"][^\'"]*attachment-woocommerce_thumbnail[^\'"]*[\'"][^>]*>', html)
print('Product card images on shop:', len(matches))
if matches:
    first_img = matches[0]
    print('First product card img:')
    print('  len:', len(first_img))
    print('  attrs:', first_img[:200])
    print('  is_lazy:', 'lazy' in first_img or 'data-src' in first_img, 'fetchpriority:', 'fetchpriority' in first_img)

import urllib.request
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

req = urllib.request.Request('https://hosseinykala.ir/shop/', headers={'User-Agent': 'Mozilla/5.0 (iPhone)'})
with urllib.request.urlopen(req, timeout=15) as r:
    html = r.read().decode('utf-8', errors='ignore')

# Search for images with /uploads/ in src
imgs = re.findall(r'<img[^>]+src=[\'"][^\'"]*/uploads/[^\'"]*[\'"][^>]*>', html)
print(f"Total uploads images on /shop/: {len(imgs)}")
for i, img in enumerate(imgs[:5]):
    print(f"[{i}] {img[:250]}")

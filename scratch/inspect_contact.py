import urllib.request
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

req = urllib.request.Request('https://hosseinykala.ir/contact/', headers={'User-Agent': 'Mozilla/5.0 (iPhone)'})
with urllib.request.urlopen(req, timeout=15) as r:
    html = r.read().decode('utf-8', errors='ignore')

# Look at images on contact page
imgs = re.findall(r'<img[^>]+>', html)
print(f"Total img tags on /contact/: {len(imgs)}")
for i, img in enumerate(imgs[:15]):
    src = re.search(r'(?:src|data-src)=[\'"]([^\'"]+)[\'"]', img)
    src_val = src.group(1) if src else "NO SRC"
    print(f"[{i}] {src_val}")

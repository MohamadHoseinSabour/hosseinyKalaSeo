import urllib.request
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

req = urllib.request.Request('https://hosseinykala.ir/', headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)'})
with urllib.request.urlopen(req, timeout=15) as resp:
    html = resp.read().decode('utf-8')

print("1. Meta viewport in live HTML:")
for m in re.finditer(r'<meta[^>]*viewport[^>]*>', html):
    print("  ", m.group(0))

print("\n2. Checking xts-cat-link in live HTML (sample 5):")
for m in list(re.finditer(r'<a[^>]*xts-cat-link[^>]*>', html))[:5]:
    print("  ", m.group(0))

print("\n3. Checking placeholder & search input:")
for m in re.finditer(r'<input[^>]*name=["\']s["\'][^>]*>', html):
    print("  ", m.group(0))

print("\n4. Checking hk-core-stability-css presence:")
print("  Present in HTML:", "hk-core-stability-css" in html)

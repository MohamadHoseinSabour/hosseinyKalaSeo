import urllib.request
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Mobile test
headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
}

req = urllib.request.Request('https://hosseinykala.ir/?t=' + str(int(__import__('time').time())), headers=headers)
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        headers_dict = dict(resp.getheaders())
except Exception as e:
    print("Error fetching:", e)
    sys.exit(1)

print("Status:", resp.status)
print("Cache headers:", {k: v for k, v in headers_dict.items() if 'cache' in k.lower() or 'x-' in k.lower()})

print("\n--- Preload tags in HEAD ---")
for p in re.findall(r'<link[^>]*rel=[\"\']preload[\"\'][^>]*>', html, re.I):
    print(" ", p)

print("\n--- jQuery script tags ---")
for s in re.findall(r'<script[^>]*jquery(?:\.min)?\.js[^>]*>', html, re.I):
    print(" ", s)

print("\n--- wp-i18n / hooks script tags ---")
for s in re.findall(r'<script[^>]*wp-includes/js/dist/(?:i18n|hooks)[^>]*>', html, re.I):
    print(" ", s)

print("\n--- Viewport meta tag ---")
for v in re.findall(r'<meta[^>]*viewport[^>]*>', html, re.I):
    print(" ", v)

print("\n--- Check empty links ---")
empty_links = []
for a in re.finditer(r'<a\s+([^>]*href=[\"\'][^\"\']+[\"\'][^>]*)>(.*?)</a>', html, re.DOTALL | re.I):
    tag_attrs = a.group(1)
    inner_text = re.sub(r'<[^>]+>', '', a.group(2)).strip()
    has_aria = 'aria-label' in tag_attrs or 'aria-labelledby' in tag_attrs
    has_title = 'title=' in tag_attrs
    has_img_alt = bool(re.search(r'<img[^>]+alt=[\"\'][^\"\']+[\"\']', a.group(2), re.I))
    if not inner_text and not has_aria and not has_title and not has_img_alt:
        empty_links.append(tag_attrs[:120])

print(f"Total empty/inaccessible links found: {len(empty_links)}")
for l in empty_links[:10]:
    print(" ", l)

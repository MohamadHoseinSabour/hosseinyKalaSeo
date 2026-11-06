import urllib.request
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

req = urllib.request.Request('https://hosseinykala.ir/', headers={
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)'
})
with urllib.request.urlopen(req, timeout=15) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

scripts = re.findall(r'<script([^>]*)>(.*?)</script>', html, re.DOTALL | re.I)
print(f"Total script tags: {len(scripts)}")

for i, (attrs, body) in enumerate(scripts):
    if 'wp' in attrs or 'wp' in body or 'i18n' in attrs or 'i18n' in body or 'jQuery' in body or 'elementor-common' in attrs:
        src = re.search(r'src=[\"\']([^\"\']+)[\"\']', attrs)
        src_val = src.group(1) if src else "INLINE"
        is_defer = 'defer' in attrs
        is_async = 'async' in attrs
        print(f"[{i}] src={src_val} (defer={is_defer}, async={is_async})")
        if not src:
            # show first 100 chars of inline script
            clean_body = body.strip().replace('\n', ' ')[:120]
            print(f"     Inline snippet: {clean_body}")

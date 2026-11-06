import urllib.request
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

test_urls = [
    ("Homepage", "https://hosseinykala.ir/"),
    ("Contact / Business Card", "https://hosseinykala.ir/contact"),
    ("Contact / Business Card (slash)", "https://hosseinykala.ir/contact/"),
    ("Shop", "https://hosseinykala.ir/shop/"),
    ("Contact Us", "https://hosseinykala.ir/contact-us/"),
    ("About Us", "https://hosseinykala.ir/about-us/")
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

print("=== PASS 1: Priming Cache (Generating Static HTML) ===")
for name, u in test_urls:
    req = urllib.request.Request(u, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as r:
        html = r.read().decode('utf-8', errors='ignore')
        title = re.search(r'<title>(.*?)</title>', html)
        h1 = re.search(r'<h[1-2][^>]*>(.*?)</h[1-2]>', html)
        body = re.search(r'<body[^>]*class=[\'"]([^\'"]+)[\'"]', html)
        cache_hdr = r.headers.get('X-HosseinyKala-Cache')
        page_id = [c for c in (body.group(1).split() if body else []) if 'page-id' in c or 'archive' in c]
        clean_title = title.group(1) if title else 'No Title'
        clean_h1 = re.sub(r'<[^>]+>', '', h1.group(1)).strip() if h1 else 'No H1'
        print(f"[{cache_hdr:<4}] {name:<25} | ID: {str(page_id):<22} | Title: {clean_title[:30]}")

print("\n=== PASS 2: Serving from Cache (Verifying Content Integrity) ===")
for name, u in test_urls:
    req = urllib.request.Request(u, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as r:
        html = r.read().decode('utf-8', errors='ignore')
        title = re.search(r'<title>(.*?)</title>', html)
        body = re.search(r'<body[^>]*class=[\'"]([^\'"]+)[\'"]', html)
        cache_hdr = r.headers.get('X-HosseinyKala-Cache')
        page_id = [c for c in (body.group(1).split() if body else []) if 'page-id' in c or 'archive' in c]
        clean_title = title.group(1) if title else 'No Title'
        print(f"[{cache_hdr:<4}] {name:<25} | ID: {str(page_id):<22} | Title: {clean_title[:30]}")

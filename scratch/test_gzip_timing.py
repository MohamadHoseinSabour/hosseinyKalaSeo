import urllib.request
import gzip
import time
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

urls = [
    ("Homepage", "https://hosseinykala.ir/"),
    ("Shop", "https://hosseinykala.ir/shop/"),
    ("Product", "https://hosseinykala.ir/product/depoint-decent-combi-refrigerator-freezer/"),
    ("Contact", "https://hosseinykala.ir/contact/"),
    ("Blog", "https://hosseinykala.ir/blog/")
]

headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)',
    'Accept-Encoding': 'gzip, deflate'
}

print(f"{'Page':<12} | {'Cache Header':<14} | {'Encoding':<12} | {'Transfer Size':<15} | {'Total Time':<12}")
print("-" * 75)

for name, url in urls:
    req = urllib.request.Request(url, headers=headers)
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=15) as r:
        raw_body = r.read()
        dt = time.time() - t0
        h = {k.lower(): v for k, v in r.getheaders()}
        cache_hdr = h.get('x-hosseinykala-cache', 'NONE')
        encoding = h.get('content-encoding', 'none')
        
    print(f"{name:<12} | {cache_hdr:<14} | {encoding:<12} | {len(raw_body):<8} bytes | {dt*1000:<6.0f} ms ({dt:.2f}s)")

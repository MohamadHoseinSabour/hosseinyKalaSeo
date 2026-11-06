import urllib.request
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
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15'
}

print(f"{'Page':<12} | {'Cache Header':<14} | {'Total Time':<12} | {'Content Size':<12}")
print("-" * 60)

for name, url in urls:
    times = []
    cache_hdr = 'NONE'
    size = 0
    for i in range(2):
        t0 = time.time()
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as r:
            body = r.read()
            dt = time.time() - t0
            times.append(dt)
            h = {k.lower(): v for k, v in r.getheaders()}
            cache_hdr = h.get('x-hosseinykala-cache', 'NONE')
            size = len(body)
            
    avg_t = min(times)
    print(f"{name:<12} | {cache_hdr:<14} | {avg_t*1000:<7.0f} ms ({avg_t:.2f}s) | {size:<12} bytes")

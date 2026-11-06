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
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15',
    'Accept-Encoding': 'gzip, deflate, br'
}

print(f"{'Page':<12} | {'Req 1 (Time)':<15} | {'Req 1 Cache':<12} | {'Req 2 (Time)':<15} | {'Req 2 Cache':<12} | {'Savings':<10}")
print("-" * 80)

for name, url in urls:
    # Request 1 (Miss / Priming)
    t0 = time.time()
    try:
        req1 = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req1, timeout=20) as r1:
            h1 = dict(r1.getheaders())
            body1 = r1.read()
            dt1 = time.time() - t0
            c1 = h1.get('x-hosseinykala-cache', 'NONE')
            
        # Request 2 (Hit test)
        t1 = time.time()
        req2 = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req2, timeout=20) as r2:
            h2 = dict(r2.getheaders())
            body2 = r2.read()
            dt2 = time.time() - t1
            c2 = h2.get('x-hosseinykala-cache', 'NONE')
            
        savings = f"{(dt1 - dt2) / dt1 * 100:.1f}%" if dt1 > dt2 else "0%"
        print(f"{name:<12} | {dt1*1000:<7.0f} ms ({dt1:.2f}s) | {c1:<12} | {dt2*1000:<7.0f} ms ({dt2:.2f}s) | {c2:<12} | {savings:<10}")
    except Exception as e:
        print(f"{name:<12} | Error: {e}")

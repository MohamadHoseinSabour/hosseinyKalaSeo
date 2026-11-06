import urllib.request
import time
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

urls = [
    ("Homepage", "https://hosseinykala.ir/"),
    ("Shop", "https://hosseinykala.ir/shop/"),
    ("Single Product", "https://hosseinykala.ir/product/depoint-decent-combi-refrigerator-freezer/"),
    ("Contact Us", "https://hosseinykala.ir/contact-us/"),
    ("Online Business Card", "https://hosseinykala.ir/contact/"),
    ("About Us", "https://hosseinykala.ir/about-us/"),
    ("Blog Archive", "https://hosseinykala.ir/blog/")
]

headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15',
    'Accept-Encoding': 'gzip, deflate'
}

print(f"{'Page':<22} | {'Req 1 (Gen)':<15} | {'Req 2 (HIT)':<15} | {'Encoding':<10} | {'Status':<6}")
print("-" * 75)

for name, u in urls:
    # Req 1
    t0 = time.time()
    try:
        req1 = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req1, timeout=20) as r1:
            body1 = r1.read()
            dt1 = time.time() - t0
            h1 = {k.lower(): v for k, v in r1.getheaders()}
            c1 = h1.get('x-hosseinykala-cache', 'NONE')
            
        # Req 2
        t1 = time.time()
        req2 = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req2, timeout=20) as r2:
            body2 = r2.read()
            dt2 = time.time() - t1
            h2 = {k.lower(): v for k, v in r2.getheaders()}
            c2 = h2.get('x-hosseinykala-cache', 'NONE')
            enc = h2.get('content-encoding', 'none')
            
        print(f"{name:<22} | {dt1*1000:<5.0f} ms ({c1:<4}) | {dt2*1000:<5.0f} ms ({c2:<4}) | {enc:<10} | {r2.status:<6}")
    except Exception as e:
        print(f"{name:<22} | Error: {e}")

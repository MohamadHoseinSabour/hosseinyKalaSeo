import urllib.request
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

urls = [
    ('Homepage', 'https://hosseinykala.ir/'),
    ('Shop', 'https://hosseinykala.ir/shop/'),
    ('Product', 'https://hosseinykala.ir/product/depoint-decent-combi-refrigerator-freezer/'),
    ('Contact (no slash)', 'https://hosseinykala.ir/contact'),
    ('Contact (with slash)', 'https://hosseinykala.ir/contact/'),
    ('Contact-Us', 'https://hosseinykala.ir/contact-us/'),
    ('About-Us', 'https://hosseinykala.ir/about-us/'),
    ('Blog', 'https://hosseinykala.ir/blog/')
]

headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15',
    'Accept-Encoding': 'gzip, deflate'
}

print(f"{'Page':<22} | {'Req 1 Cache':<12} | {'Req 2 Cache':<12} | {'Status':<6}")
print("-" * 65)

for name, u in urls:
    # 1. First request
    req1 = urllib.request.Request(u, headers=headers)
    try:
        with urllib.request.urlopen(req1, timeout=20) as r1:
            h1 = {k.lower(): v for k, v in r1.getheaders()}
            c1 = h1.get('x-hosseinykala-cache', 'NONE')
            status1 = r1.status
            
        # 2. Second request
        req2 = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req2, timeout=20) as r2:
            h2 = {k.lower(): v for k, v in r2.getheaders()}
            c2 = h2.get('x-hosseinykala-cache', 'NONE')
            status2 = r2.status
            
        print(f"{name:<22} | {c1:<12} | {c2:<12} | {status2:<6}")
    except urllib.error.HTTPError as e:
        print(f"{name:<22} | HTTP {e.code}")
    except Exception as e:
        print(f"{name:<22} | Error: {e}")

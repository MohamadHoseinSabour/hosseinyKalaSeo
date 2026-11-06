import urllib.request
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

urls = [
    'https://hosseinykala.ir/',
    'https://hosseinykala.ir/shop/',
    'https://hosseinykala.ir/product/depoint-decent-combi-refrigerator-freezer/',
    'https://hosseinykala.ir/contact/',
    'https://hosseinykala.ir/blog/'
]

for u in urls:
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 (iPhone)'})
    with urllib.request.urlopen(req) as r:
        headers = {k.lower(): v for k, v in r.getheaders()}
        cache_status = headers.get('x-hosseinykala-cache', 'NONE')
        print(f"{u:<60} | Cache: {cache_status:<6} | Status: {r.status}")

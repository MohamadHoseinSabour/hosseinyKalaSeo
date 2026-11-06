import urllib.request
import time
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)',
    'Accept-Encoding': 'gzip, deflate'
}

pages = ['/contact', '/contact-us/', '/about-us/']

for p in pages:
    url = 'https://hosseinykala.ir' + p
    # req 1
    t0 = time.time()
    req1 = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req1, timeout=15) as r1:
        dt1 = time.time() - t0
        h1 = {k.lower(): v for k, v in r1.getheaders()}
        c1 = h1.get('x-hosseinykala-cache', 'NONE')
        enc1 = h1.get('content-encoding', 'none')
        
    # req 2
    t1 = time.time()
    req2 = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req2, timeout=15) as r2:
        dt2 = time.time() - t1
        h2 = {k.lower(): v for k, v in r2.getheaders()}
        c2 = h2.get('x-hosseinykala-cache', 'NONE')
        enc2 = h2.get('content-encoding', 'none')
        
    print(f"{p:<15} | 1st: {dt1*1000:<5.0f} ms ({c1}) | 2nd: {dt2*1000:<5.0f} ms ({c2}, enc:{enc2})")

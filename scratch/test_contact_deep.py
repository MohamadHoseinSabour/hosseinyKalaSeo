import urllib.request
import time
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

url = 'https://hosseinykala.ir/contact'
t0 = time.time()
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=15) as r:
        final_url = r.geturl()
        code = r.status
        body = r.read()
        dt = time.time() - t0
        print(f"URL: {url} -> Final: {final_url}")
        print(f"Status: {code} | Size: {len(body)} | Time: {dt:.2f}s")
        for k, v in r.getheaders():
            print(f"  {k}: {v}")
except Exception as e:
    print("Error:", e)

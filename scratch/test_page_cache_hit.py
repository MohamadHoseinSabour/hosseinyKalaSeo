import requests
import time
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
s = requests.Session()
s.headers.update(headers)

print("--- Run 1 (Prime Cache) ---")
t0 = time.perf_counter()
r1 = s.get('https://hosseinykala.ir/', timeout=25)
t1 = (time.perf_counter() - t0) * 1000
cache1 = r1.headers.get('x-hosseinykala-cache', 'MISS')
print(f"Run 1: HTTP {r1.status_code} in {t1:.1f}ms | Cache: {cache1} | Size: {len(r1.content)/1024:.1f} KB")

time.sleep(1)

print("\n--- Run 2 (From Cache) ---")
t0 = time.perf_counter()
r2 = s.get('https://hosseinykala.ir/', timeout=10)
t2 = (time.perf_counter() - t0) * 1000
cache2 = r2.headers.get('x-hosseinykala-cache', 'MISS')
print(f"Run 2: HTTP {r2.status_code} in {t2:.1f}ms | Cache: {cache2} | Size: {len(r2.content)/1024:.1f} KB")

time.sleep(1)

print("\n--- Run 3 (Verification) ---")
t0 = time.perf_counter()
r3 = s.get('https://hosseinykala.ir/', timeout=10)
t3 = (time.perf_counter() - t0) * 1000
cache3 = r3.headers.get('x-hosseinykala-cache', 'MISS')
print(f"Run 3: HTTP {r3.status_code} in {t3:.1f}ms | Cache: {cache3} | Size: {len(r3.content)/1024:.1f} KB")

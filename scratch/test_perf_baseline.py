import requests
import time
import json
import re

url = "https://hosseinykala.ir/"
mobile_ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
desktop_ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

print("--- Testing Mobile Requests ---")
for i in range(5):
    t0 = time.time()
    try:
        r = requests.get(url, headers={"User-Agent": mobile_ua}, timeout=30)
        dur = time.time() - t0
        print(f"Req {i+1}: status={r.status_code}, total_time={dur:.3f}s")
        print(f"  Server: {r.headers.get('server')}")
        print(f"  X-LiteSpeed-Cache: {r.headers.get('x-litespeed-cache')}")
        print(f"  X-LiteSpeed-Tag: {r.headers.get('x-litespeed-tag')}")
        print(f"  Age: {r.headers.get('age')}")
        print(f"  Cache-Control: {r.headers.get('cache-control')}")
        print(f"  Vary: {r.headers.get('vary')}")
        print(f"  Content-Encoding: {r.headers.get('content-encoding')}")
        print(f"  Content-Length: {len(r.content)} bytes")
    except Exception as e:
        print(f"Req {i+1} failed: {e}")

print("\n--- Testing Desktop Requests ---")
for i in range(2):
    t0 = time.time()
    try:
        r = requests.get(url, headers={"User-Agent": desktop_ua}, timeout=30)
        dur = time.time() - t0
        print(f"Desktop Req {i+1}: status={r.status_code}, time={dur:.3f}s, ls_cache={r.headers.get('x-litespeed-cache')}")
    except Exception as e:
        print(f"Desktop Req {i+1} failed: {e}")

import time
import requests

test_urls = [
    ("Homepage cached", "https://hosseinykala.ir/"),
    ("Homepage uncached query", "https://hosseinykala.ir/?test_cache_bust=12345"),
    ("Category page", "https://hosseinykala.ir/product-category/refrigerator-freezer/"),
    ("Product page", "https://hosseinykala.ir/product/clever-glory-plus-refrigerator/"),
    ("Cart page", "https://hosseinykala.ir/cart/"),
    ("Shop/Search", "https://hosseinykala.ir/?s=یخچال&post_type=product")
]

for label, url in test_urls:
    t0 = time.time()
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)"}, timeout=30)
        dur = time.time() - t0
        cache_hdr = r.headers.get('x-hosseinykala-cache') or r.headers.get('x-litespeed-cache')
        print(f"{label:25} | Code: {r.status_code} | Time: {dur:5.2f}s | Cache: {cache_hdr} | Age: {r.headers.get('age')}")
    except Exception as e:
        print(f"{label:25} | Error: {e}")

import requests

assets = [
    "https://hosseinykala.ir/wp-content/litespeed/css/4660ba7e3bc699b753c29c6d02312ffd.css?ver=5255d",
    "https://hosseinykala.ir/wp-includes/js/jquery/jquery.min.js",
    "https://hosseinykala.ir/wp-content/uploads/2026/10/clover-october-sale-square-banner.webp",
    "https://hosseinykala.ir/wp-content/themes/xts-luman/fonts/iranyekanx/woff2/IRANYekanXFaNum-Regular.woff2"
]

print("--- Checking Static Asset Response Headers ---")
for a in assets:
    try:
        r = requests.head(a, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        print(f"\nAsset: {a.split('/')[-1]}")
        print(f"  Status: {r.status_code}")
        print(f"  Cache-Control: {r.headers.get('cache-control')}")
        print(f"  Expires: {r.headers.get('expires')}")
        print(f"  Last-Modified: {r.headers.get('last-modified')}")
        print(f"  ETag: {r.headers.get('etag')}")
        print(f"  Content-Length: {r.headers.get('content-length')}")
        print(f"  Content-Type: {r.headers.get('content-type')}")
    except Exception as e:
        print(f"Error checking {a}: {e}")

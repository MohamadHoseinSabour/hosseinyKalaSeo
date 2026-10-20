import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

cat_tests = [
    ("Fridge slug", "https://hosseinykala.ir/product-category/%db%8c%d8%ae%da%86%d8%a7%d9%84-%d9%81%d8%b1%db%8c%d8%b2%d8%b1/"),
    ("Washing slug", "https://hosseinykala.ir/product-category/%d9%85%d8%a7%d8%b4%db%8c%d9%86-%d9%84%d8%a8%d8%a7%d8%b3%d8%b4%d9%88%db%8c%db%8c/"),
    ("Dishwasher slug", "https://hosseinykala.ir/product-category/%d9%85%d8%a7%d8%b4%db%8c%d9%86-%d8%b8%d8%b1%d9%81%d8%b4%d9%88%db%8c%db%8c/"),
    ("Air cooler slug", "https://hosseinykala.ir/product-category/%da%a9%d9%88%d9%84%d8%b1-%d8%a2%d8%a8%db%8c/"),
    ("Water purifier slug", "https://hosseinykala.ir/product-category/%d8%aa%d8%b5%d9%81%db%8c%d9%87-%da%a9%d9%86%d9%86%d8%af%d9%87-%d8%a2%d8%a8/"),
    ("Vacuum slug", "https://hosseinykala.ir/product-category/%d8%ac%d8%a7%d8%b1%d9%88%d8%a8%d8%b1%d9%82%db%8c/"),
    
    ("Fridge query slug", "https://hosseinykala.ir/?product_cat=%db%8c%d8%ae%da%86%d8%a7%d9%84-%d9%81%d8%b1%db%8c%d8%b2%d8%b1"),
]

for label, url in cat_tests:
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        print(f"[{label}] HTTP {r.status_code} | URL: {r.url}", flush=True)
    except Exception as e:
        print(f"[{label}] Error: {e}", flush=True)

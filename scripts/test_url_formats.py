import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

test_urls = [
    # Products
    ("Product ?p=2972", "https://hosseinykala.ir/?p=2972"),
    ("Product ?post_type=product&p=2972", "https://hosseinykala.ir/?post_type=product&p=2972"),
    ("Product ?p=3707", "https://hosseinykala.ir/?p=3707"),
    ("Product ?post_type=product&p=3707", "https://hosseinykala.ir/?post_type=product&p=3707"),
    
    # Categories
    ("Cat ?product_cat=92", "https://hosseinykala.ir/?product_cat=92"),
    ("Cat ?cat=92", "https://hosseinykala.ir/?cat=92"),
    ("Cat ?taxonomy=product_cat&term=92", "https://hosseinykala.ir/?taxonomy=product_cat&term=92"),
    ("Cat /product-category/refrigerator", "https://hosseinykala.ir/product-category/%db%8c%d8%ae%da%86%d8%a7%d9%84-%d9%81%d8%b1%db%8c%d8%b2%d8%b1/"),
    
    # Sub-articles
    ("Post ?p=3851", "https://hosseinykala.ir/?p=3851"),
    ("Post ?p=3853", "https://hosseinykala.ir/?p=3853"),
]

for label, url in test_urls:
    try:
        r = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=True)
        print(f"[{label}] -> Status: {r.status_code} | Final URL: {r.url}")
    except Exception as e:
        print(f"[{label}] -> Error: {e}")

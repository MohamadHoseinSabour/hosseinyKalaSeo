import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

canonical_urls = [
    # Homepage
    ("Homepage", "https://hosseinykala.ir/"),
    
    # Categories
    ("Cat Refrigerator", "https://hosseinykala.ir/product-category/%db%8c%d8%ae%da%86%d8%a7%d9%84-%d9%81%d8%b1%db%8c%d8%b2%d8%b1/"),
    ("Cat Washing", "https://hosseinykala.ir/product-category/%d9%85%d8%a7%d8%b4%db%8c%d9%86-%d9%84%d8%a8%d8%a7%d8%b3%d8%b4%d9%88%db%8c%db%8c/"),
    ("Cat Dishwasher", "https://hosseinykala.ir/product-category/%d9%85%d8%a7%d8%b4%db%8c%d9%86-%d8%b8%d8%b1%d9%81%d8%b4%d9%88%db%8c%db%8c/"),
    ("Cat Air Cooler", "https://hosseinykala.ir/product-category/%da%a9%d9%88%d9%84%d8%b1-%d8%a2%d8%a8%db%8c/"),
    ("Cat Water Purifier", "https://hosseinykala.ir/product-category/%d8%aa%d8%b5%d9%81%db%8c%d9%87-%da%a9%d9%86%d9%86%d8%af%d9%87-%d8%a2%d8%a8/"),
    ("Cat Vacuum", "https://hosseinykala.ir/product-category/%d8%ac%d8%a7%d8%b1%d9%88%d8%a8%d8%b1%d9%82%db%8c/"),
    
    # Products
    ("Prod Clover 54ft (2972)", "https://hosseinykala.ir/product/%db%8c%d8%ae%da%86%d8%a7%d9%84-%d9%81%d8%b1%db%8c%d8%b2%d8%b1-%da%af%d9%84%d9%88%d8%b1%db%8c-%d9%be%d9%84%d8%a7%d8%b3-%d8%af%d9%88%d9%82%d9%84%d9%88-%da%a9%d9%84%d9%88%d8%b154-%d9%81%d9%88%d8%aa/"),
    ("Prod Pakshoma (3707)", "https://hosseinykala.ir/product/pakshoma-21kg-twin-tub-washer/"),
    ("Prod Depoint Max (2745)", "https://hosseinykala.ir/product/depoint-max-du-twin-refrigerator-34ft/"),
    ("Prod Soft Water (2766)", "https://hosseinykala.ir/product/soft-water-ir-06-purifier/"),
    ("Prod Clover Dishwasher (2871)", "https://hosseinykala.ir/product/clover-cdw-h15v-dishwasher-15p/")
]

for label, url in canonical_urls:
    try:
        r = requests.get(url, headers=HEADERS, timeout=12)
        print(f"[{r.status_code}] {label} -> {url}")
    except Exception as e:
        print(f"[ERR] {label} -> {e}")

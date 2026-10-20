import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

test_urls = [
    # Category query IDs (what was previously used)
    ("Cat Query ?product_cat=92", "https://hosseinykala.ir/?product_cat=92"),
    ("Cat Query ?product_cat=93", "https://hosseinykala.ir/?product_cat=93"),
    ("Cat Query ?product_cat=96", "https://hosseinykala.ir/?product_cat=96"),
    
    # Category canonical URLs
    ("Cat Canonical Refrigerator", "https://hosseinykala.ir/product-category/%db%8c%d8%ae%da%86%d8%a7%d9%84-%d9%81%d8%b1%db%8c%d8%b2%d8%b1/"),
    ("Cat Canonical Washing", "https://hosseinykala.ir/product-category/%d9%85%d8%a7%d8%b4%db%8c%d9%86-%d9%84%d8%a8%d8%a7%d8%b3%d8%b4%d9%88%db%8c%db%8c/"),
    ("Cat Canonical Purifier", "https://hosseinykala.ir/product-category/%d8%aa%d8%b5%d9%81%db%8c%d9%87-%da%a9%d9%86%d9%86%d8%af%d9%87-%d8%a2%d8%a8/"),
    
    # Product query IDs
    ("Prod Query ?p=2972", "https://hosseinykala.ir/?p=2972"),
    ("Prod Query ?p=2745", "https://hosseinykala.ir/?p=2745"),
    ("Prod Query ?p=2871", "https://hosseinykala.ir/?p=2871"),
    ("Prod Query ?p=2766", "https://hosseinykala.ir/?p=2766"),
    
    # Product canonical URLs
    ("Prod Canonical 2972", "https://hosseinykala.ir/product/%db%8c%d8%ae%da%86%d8%a7%d9%84-%d9%81%d8%b1%db%8c%d8%b2%d8%b1-%da%af%d9%84%d9%88%d8%b1%db%8c-%d9%be%d9%84%d8%a7%d8%b3-%d8%af%d9%88%d9%82%d9%84%d9%88-%da%a9%d9%84%d9%88%d8%b154-%d9%81%d9%88%d8%aa/"),
    ("Prod Canonical 2745", "https://hosseinykala.ir/product/depoint-max-du-twin-refrigerator-34ft/"),
    ("Prod Canonical 2871", "https://hosseinykala.ir/product/clover-cdw-h15v-dishwasher-15p/"),
    ("Prod Canonical 2766", "https://hosseinykala.ir/product/soft-water-ir-06-purifier/"),
    
    # Scheduled post links (public visitor without auth)
    ("Scheduled Post Query ?p=3853", "https://hosseinykala.ir/?p=3853"),
    ("Scheduled Post Slug refah-beta", "https://hosseinykala.ir/refah-bank-beta-installment-guide/")
]

for label, url in test_urls:
    try:
        r = requests.get(url, headers=HEADERS, timeout=12, allow_redirects=True)
        print(f"[{r.status_code}] {label:<32} -> Final: {r.url}", flush=True)
    except Exception as e:
        print(f"[ERR] {label:<32} -> Error: {e}", flush=True)

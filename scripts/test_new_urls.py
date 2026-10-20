import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

test_urls = [
    ('شستشو و نظافت', 'https://hosseinykala.ir/product-category/washing-cleaning/'),
    ('نوشیدنی ساز', 'https://hosseinykala.ir/product-category/drink-makers/'),
    ('سرمایش و گرمایش', 'https://hosseinykala.ir/product-category/heating-cooling/'),
    ('ماشین لباسشویی', 'https://hosseinykala.ir/product-category/washing-cleaning/%d9%85%d8%a7%d8%b4%db%8c%d9%86-%d9%84%d8%a8%d8%a7%d8%b3%d8%b4%d9%88%db%8c%db%8c/'),
    ('سرخ کن دونالکس', 'https://hosseinykala.ir/product-category/%d9%84%d9%88%d8%a7%d8%b2%d9%85-%d8%a8%d8%b1%d9%82%db%8c-%d8%a2%d8%b4%d9%be%d8%b2%d8%ae%d8%a7%d9%86%d9%87/%d8%b3%d8%b1%d8%ae-%da%a9%d9%86/donallex-air-fryers/'),
]

for name, u in test_urls:
    r = requests.get(u, headers=headers, timeout=15)
    print(f"[{r.status_code}] {name} -> {u}")

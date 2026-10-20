import requests
import urllib.parse
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

test_queries = [
    ("پارس خزر 361", "پلوپز"),
    ("RC-361", "پارس خزر"),
    ("آلتون 518", "گاز صفحه ای"),
    ("SG518", "آلتون"),
    ("H312", "هود آلتون"),
    ("H-312", "هود آلتون"),
    ("H315", "هود آلتون"),
    ("پاکشوما 21", "لباسشویی دوقلو"),
    ("PWT-21", "پاکشوما"),
    ("سیماران 8002", "اتوبخار"),
    ("ساپر 1031", "کتری برقی"),
    ("کاستلو 470", "آسیاب")
]

print("=== TESTING QUERIES ON DIGIKALA & TOROB ===")
for q, cat_hint in test_queries:
    print(f"\n--- Testing: '{q}' ---")
    
    # DK test
    try:
        r = requests.get('https://api.digikala.com/v1/search/', params={'q': q}, headers=headers, timeout=5)
        if r.status_code == 200:
            products = r.json().get('data', {}).get('products', [])
            print(f"  [Digikala] {len(products)} hits:")
            for p in products[:2]:
                print(f"    - ID {p.get('id')}: {p.get('title_fa')}")
    except Exception as e:
        print(f"  [Digikala Error]: {e}")

    # Torob test
    try:
        t_url = f"https://api.torob.com/v4/base-product/search/?sort=popularity&page=0&size=3&query={urllib.parse.quote(q)}"
        r = requests.get(t_url, headers=headers, timeout=5)
        if r.status_code == 200:
            results = r.json().get('results', [])
            print(f"  [Torob] {len(results)} hits:")
            for p in results[:2]:
                print(f"    - {p.get('name1')} (Img: {bool(p.get('image_url'))})")
    except Exception as e:
        print(f"  [Torob Error]: {e}")

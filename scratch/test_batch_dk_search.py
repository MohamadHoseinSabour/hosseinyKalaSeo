import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

test_queries = [
    ("donalex_dn150", "سالاد ساز دونالکس 150"),
    ("donalex_dn940", "ساندویچ ساز دونالکس 940"),
    ("donalex_dn965", "سرخ کن دونالکس 965"),
    ("donalex_dn955", "سرخ کن دونالکس 955"),
    ("kahler_kh812", "اتو کاخلر 812"),
    ("kahler_kh813", "اتو کاخلر 813"),
    ("kahler_kh814", "اتو کاخلر 814"),
    ("kahler_kh5512", "زودپز کاخلر 5512"),
    ("kahler_kh134", "همزن کاخلر 134"),
    ("edmilson_820", "توستر ادمیلسون 820"),
    ("edmilson_827", "توستر ادمیلسون 827"),
    ("edmilson_811", "جاروشارژی ادمیلسون 811"),
    ("tulips_625", "جاروبرقی تولیپس 625"),
    ("tulips_473", "آسیاب تولیپس 473"),
    ("ebkazo_2139", "بخارگر ابکازو 2139"),
    ("bellanzo_1136", "خردکن بلانزو 1136"),
    ("satia_9015", "سرخ کن ساتیا 9015"),
    ("satia_1215", "پنکه ساتیا 1215"),
    ("vincent_3321", "ماشین اصلاح وینسنت 3321"),
    ("shimge_1hp", "پمپ آب شیمجه 1 اسب"),
    ("green_water_heater", "آبگرمکن گرین"),
    ("green_heater", "بخاری گرین"),
    ("mixi_scale", "ترازو دیجیتال میکسی"),
    ("atman_538", "سشوار آتمن 538"),
]

found_map = {}

for key, q in test_queries:
    try:
        r = requests.get('https://api.digikala.com/v1/search/', params={'q': q}, headers=headers, timeout=6)
        if r.status_code == 200:
            prods = r.json().get('data', {}).get('products', [])
            if prods:
                p = prods[0]
                img_url = p.get('images', {}).get('main', {}).get('url', [''])[0]
                # clean up query params from img_url to get full res
                clean_img = img_url.split('?')[0] if img_url else None
                found_map[key] = {
                    'title': p.get('title_fa'),
                    'img': clean_img,
                    'query': q
                }
                print(f"✓ '{q}' -> [{p.get('id')}] {p.get('title_fa')[:50]}")
                print(f"   Img: {clean_img}")
            else:
                print(f"✗ '{q}' -> 0 products on DK")
        else:
            print(f"✗ '{q}' -> HTTP {r.status_code}")
    except Exception as e:
        print(f"Error querying '{q}': {e}")

print(f"\nTotal found on DK: {len(found_map)} / {len(test_queries)}")

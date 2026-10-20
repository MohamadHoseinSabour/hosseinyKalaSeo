import urllib.request
import json
import urllib.parse
import sys
sys.stdout.reconfigure(encoding='utf-8')

def test_query(q):
    url = f"https://api.digikala.com/v1/search/?q={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            prods = data.get('data', {}).get('products', [])
            print(f"=== Query: {q} -> Found {len(prods)} products ===")
            for p in prods[:3]:
                print(f" - ID {p.get('id')}: {p.get('title_fa')}")
                img_url = p.get('images', {}).get('main', {}).get('url', [''])[0]
                print(f"   Img: {img_url}")
    except Exception as e:
        print(f"Error for {q}: {e}")

test_queries = [
    'پتوشور پاکیزان 30',
    'پتوشور پاکیزان 40',
    'لباسشویی دوقلو پاکشوما 15',
    'لباسشویی دوقلو پاکشوما 21',
    'لباسشویی هیمالیا تسلا',
    'یخچال کمبی نیکسان 8410',
    'مینی واش فریدولین 3.5',
    'جاروبرقی پاندا 80',
    'فن هیتر پارس خزر 2000',
    'بخاری پلار 3PN',
    'چای ساز کورکماز 331',
    'فر توکار آلتون',
    'گاز صفحه ای آلتون SG518'
]

for tq in test_queries:
    test_query(tq)

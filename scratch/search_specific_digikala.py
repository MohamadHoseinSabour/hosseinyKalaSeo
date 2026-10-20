import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

queries = [
    'WKCMH1663',
    'WKWK148',
    'WKKE210',
    '55S7000',
    'DSL-55S7000',
    'بخاری پلار 28',
    'بخاری پلار سنگ',
    'ایران شرق اتوماتیک',
    'ایران شرق آیونایز',
    'دیپوینت دیسنت',
    'دیپوینت اکسپلور سفید',
    'الکترواستیل دوقلو سری 10',
    'الکترواستیل سری 10',
    'الکترواستیل کمپکت',
    'زیکو 5020',
    'زیکو 70028',
    'زیکو 4038',
    'مایر 5959',
    'ویلز 6033',
    'باخ 1454',
    'BUVCK'
]

for q in queries:
    r = requests.get('https://api.digikala.com/v1/search/', params={'q': q}, headers=headers, timeout=5)
    if r.status_code == 200:
        products = r.json().get('data', {}).get('products', [])
        print(f"\nQuery: '{q}' -> found {len(products)} products:")
        for p in products[:3]:
            print(f"  - [{p.get('id')}] {p.get('title_fa')}")
    else:
        print(f"Query: '{q}' -> HTTP {r.status_code}")

import requests
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
test_queries = [
    'پتوشور پاکیزان 30',
    'پتوشور پاکیزان 40',
    'لباسشویی دوقلو پاکشوما 15',
    'لباسشویی دوقلو پاکشوما 21',
    'فن هیتر پارس خزر FH2000P',
    'بخاری پلار 3PN',
    'چای ساز کرکماز A331',
    'مینی واش فریدولین 3.5'
]

for q in test_queries:
    try:
        r = requests.get('https://api.digikala.com/v1/search/', params={'q': q}, headers=headers, timeout=6)
        if r.status_code == 200:
            prods = r.json().get('data', {}).get('products', [])
            print(f"Query: {q} -> Found {len(prods)}")
            for p in prods[:2]:
                title = p.get('title_fa')
                img = p.get('images', {}).get('main', {}).get('url', [''])[0].split('?')[0]
                print(f"   - {title}")
                print(f"     Img: {img}")
    except Exception as e:
        print(f"Err for {q}: {e}")

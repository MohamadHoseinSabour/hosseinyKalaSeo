import sys
import requests

sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {'User-Agent': 'Mozilla/5.0'}
url = 'https://api.digikala.com/v1/search/?q=اتو+کاخلر+812'
r = requests.get(url, headers=HEADERS, timeout=10)
print('DK status:', r.status_code)
if r.status_code == 200:
    prods = r.json().get('data', {}).get('products', [])
    for p in prods[:5]:
        img = p.get('images', {}).get('main', {}).get('url', [''])[0]
        print(f"Title: {p.get('title_fa')} -> Image: {img}")

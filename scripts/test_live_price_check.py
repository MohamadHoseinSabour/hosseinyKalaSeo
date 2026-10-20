import requests
from bs4 import BeautifulSoup
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

test_urls = [
    (2972, 'https://hosseinykala.ir/?p=2972'),
    (3551, 'https://hosseinykala.ir/?p=3551'),
    (2445, 'https://hosseinykala.ir/?p=2445')
]

for pid, url in test_urls:
    r = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(r.text, 'html.parser')
    for s in soup.find_all('script', type='application/ld+json'):
        try:
            d = json.loads(s.string)
            graph = d.get('@graph', [d]) if isinstance(d, dict) else d
            for item in graph:
                if isinstance(item, dict) and item.get('@type') == 'Product':
                    offers = item.get('offers')
                    if isinstance(offers, list):
                        offers = offers[0]
                    print(f"Product {pid}: Price={offers.get('price')} {offers.get('priceCurrency')}, Avail={offers.get('availability')}")
        except:
            pass

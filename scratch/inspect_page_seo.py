import urllib.request
import json
import re
import ssl
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

urls = [
    'https://hosseinykala.ir/product/pro-omega-t5-hair-clipper/',
    'https://hosseinykala.ir/product/bost-bvc-pc18b-vacuum-cleaner/',
    'https://hosseinykala.ir/mellat-bank-200m-appliances-loan-guide/',
    'https://hosseinykala.ir/bajet-tejarat-refah-300m-appliances/'
]

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

for u in urls:
    print('='*70)
    print(f'URL: {u}')
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        html = urllib.request.urlopen(req, context=ctx, timeout=12).read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')

        title = soup.title.string.strip() if soup.title and soup.title.string else 'NO TITLE'
        print(f'Title: {title}')

        meta_desc = soup.find('meta', attrs={'name': 'description'})
        desc_text = meta_desc['content'].strip() if meta_desc and 'content' in meta_desc.attrs else 'NO META DESC'
        print(f'Meta Desc ({len(desc_text)} chars): {desc_text}')

        canonical = soup.find('link', attrs={'rel': 'canonical'})
        print(f'Canonical: {canonical["href"] if canonical and "href" in canonical.attrs else "NO CANONICAL"}')

        h1s = [h.get_text(strip=True) for h in soup.find_all('h1')]
        print(f'H1 tags: {h1s}')

        schemas = soup.find_all('script', type='application/ld+json')
        print(f'JSON-LD count: {len(schemas)}')
        for i, s in enumerate(schemas):
            try:
                data = json.loads(s.string)
                if '@graph' in data:
                    types = [item.get('@type') for item in data['@graph']]
                    print(f'  Schema #{i+1} Graph types: {types}')
                    for item in data['@graph']:
                        if item.get('@type') == 'Product':
                            offers = item.get('offers', {})
                            print(f'    Product Schema price: {offers.get("price")}, currency: {offers.get("priceCurrency")}, inStock: {offers.get("availability")}')
                        if item.get('@type') == 'FAQPage':
                            print(f'    FAQPage Schema with {len(item.get("mainEntity", []))} questions')
                else:
                    print(f'  Schema #{i+1} Direct type: {data.get("@type")}')
            except Exception as ex:
                print(f'  Schema #{i+1} parse err: {ex}')
    except Exception as e:
        print(f'Error fetching {u}: {e}')

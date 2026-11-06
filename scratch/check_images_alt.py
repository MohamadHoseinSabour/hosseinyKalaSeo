import urllib.request
import ssl
import bs4
import sys

sys.stdout.reconfigure(encoding='utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = [
    'https://hosseinykala.ir/product/bost-bvc-pc18b-vacuum-cleaner/',
    'https://hosseinykala.ir/product/pro-omega-t5-hair-clipper/'
]

for url in urls:
    print('='*70)
    print(f'URL: {url}')
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req, context=ctx, timeout=8).read().decode('utf-8', errors='ignore')
        soup = bs4.BeautifulSoup(html, 'html.parser')
        images = soup.find_all('img')
        print(f'Total images found: {len(images)}')
        for img in images:
            alt = img.get('alt', '')
            src = img.get('src', img.get('data-src', ''))
            # Filter for product gallery images (containing uploads)
            if 'uploads' in str(src):
                print(f'  ALT: "{alt}" | SRC: {src[-40:] if src else ""}')
    except Exception as e:
        print(f'Error fetching {url}: {e}')

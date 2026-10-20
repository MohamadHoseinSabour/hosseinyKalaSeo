import requests
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def check_tatakala(q):
    url = f"https://tatakala.com/?s={q}"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        products = []
        for item in soup.select('.product-inner, .product-item, .post-item'):
            title_el = item.select_one('.product-title, .title, h2, h3')
            img_el = item.select_one('img')
            title = title_el.text.strip() if title_el else ''
            img = img_el.get('src') or img_el.get('data-src') if img_el else ''
            if title:
                products.append({'title': title, 'img': img})
        return products
    except Exception as e:
        return str(e)

print("Searching Tatakala for 1663:")
print(check_tatakala('1663'))

print("\nSearching Tatakala for WKCMH1663:")
print(check_tatakala('WKCMH1663'))

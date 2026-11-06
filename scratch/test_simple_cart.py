import json
import requests
import urllib3
from bs4 import BeautifulSoup
import sys
urllib3.disable_warnings()

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'fa-IR,fa;q=0.9,en-US;q=0.8',
})

# Find product 4294 url
with open('data/products.json', encoding='utf-8') as f:
    products = json.load(f)

prod = next((p for p in products if p.get('id') == 4294), None)
print("Product 4294:", prod.get('name') if prod else 'Not found')
print("Product URL:", prod.get('url') if prod else '')

# Post to add to cart
add_url = f"https://hosseinykala.ir/?add-to-cart=4294"
r2 = session.post(add_url, data={'quantity': 1}, verify=False)
print("Add to cart response code:", r2.status_code)
print("Cookies after add to cart:")
for c in session.cookies:
    print(f"  {c.name} = {c.value}")

# Check cart
r_cart = session.get('https://hosseinykala.ir/cart/', verify=False)
soup = BeautifulSoup(r_cart.text, 'html.parser')
items = soup.find_all('tr', class_=lambda c: c and 'cart_item' in c)
print(f"Items in cart: {len(items)}")

# Check product page again with this session
r_prod = session.get(prod.get('url'), verify=False)
print(f"Product page cache header with active cart: {r_prod.headers.get('x-hosseinykala-cache', 'BYPASSED')}")

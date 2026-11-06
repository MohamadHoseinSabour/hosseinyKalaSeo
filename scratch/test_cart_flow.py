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

print("=== STEP 1: Load Product as Guest ===")
product_url = 'https://hosseinykala.ir/product/depoint-decent-combi-refrigerator-freezer/'
r1 = session.get(product_url, verify=False)
print(f"Product HTTP {r1.status_code} | Cache Header: {r1.headers.get('x-hosseinykala-cache', 'NONE')}")
soup1 = BeautifulSoup(r1.text, 'html.parser')

# Find add-to-cart form or product ID
add_to_cart_btn = soup1.find('button', {'name': 'add-to-cart'})
product_id = add_to_cart_btn.get('value') if add_to_cart_btn else None
if not product_id:
    # Try finding input name="add-to-cart"
    inp = soup1.find('input', {'name': 'add-to-cart'})
    if inp:
        product_id = inp.get('value')

print(f"Discovered Product ID: {product_id}")

if not product_id:
    # Look for standard woocommerce add-to-cart link or post ID
    link = soup1.find('a', href=lambda h: h and 'add-to-cart=' in h)
    if link:
        import re
        m = re.search(r'add-to-cart=(\d+)', link['href'])
        if m:
            product_id = m.group(1)

if not product_id:
    # Use fallback known ID from products.json or url
    product_id = '3546' # or similar
    print(f"Using fallback ID: {product_id}")

print("\n=== STEP 2: Add Product to Cart ===")
add_url = f"https://hosseinykala.ir/?add-to-cart={product_id}"
r2 = session.get(add_url, verify=False)
print(f"Add to Cart HTTP {r2.status_code}")
print("Cookies received after add to cart:")
for c in session.cookies:
    print(f"  {c.name} = {c.value[:20]}...")

print("\n=== STEP 3: Load Cart Page ===")
r3 = session.get('https://hosseinykala.ir/cart/', verify=False)
print(f"Cart HTTP {r3.status_code} | Cache Header: {r3.headers.get('x-hosseinykala-cache', 'NONE')}")
soup3 = BeautifulSoup(r3.text, 'html.parser')
cart_items = soup3.find_all('tr', class_=lambda c: c and 'cart_item' in c)
print(f"Items visible in cart table: {len(cart_items)}")

print("\n=== STEP 4: Load Checkout Page ===")
r4 = session.get('https://hosseinykala.ir/checkout/', verify=False)
print(f"Checkout HTTP {r4.status_code} | Cache Header: {r4.headers.get('x-hosseinykala-cache', 'NONE')}")
is_checkout_form = bool(r4.text.find('woocommerce-checkout') != -1)
print(f"Checkout Form Present: {is_checkout_form}")

print("\n=== STEP 5: Re-visit Product Page With Active Cart in Session ===")
r5 = session.get(product_url, verify=False)
cache_hdr = r5.headers.get('x-hosseinykala-cache', 'BYPASSED')
print(f"Product Page With Active Cart | Cache Header: {cache_hdr}")
print(f"Was static cache bypassed for cart user? {'YES (CORRECT!)' if cache_hdr != 'HIT' else 'NO (ERROR!)'}")

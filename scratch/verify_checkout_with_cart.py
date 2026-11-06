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

# Add product 4294
session.post('https://hosseinykala.ir/?add-to-cart=4294', data={'quantity': 1}, verify=False)

# Check checkout
r_checkout = session.get('https://hosseinykala.ir/checkout/', verify=False)
print("Checkout status:", r_checkout.status_code)
print("Checkout cache header:", r_checkout.headers.get('x-hosseinykala-cache', 'NONE'))
soup = BeautifulSoup(r_checkout.text, 'html.parser')
checkout_form = soup.find('form', class_=lambda c: c and 'checkout' in c)
print("Checkout form found:", bool(checkout_form))
billing_first_name = soup.find('input', id='billing_first_name')
print("Billing fields present:", bool(billing_first_name))
order_review = soup.find('div', id='order_review')
print("Order review table present:", bool(order_review))

import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# Check cat 209 and cat 210
r209 = requests.get('https://hosseinykala.ir/wp-json/wp/v2/product_cat/209', auth=AUTH, headers=headers)
c209 = r209.json()
print("Cat 209:", c209['name'], c209['link'])

r210 = requests.get('https://hosseinykala.ir/wp-json/wp/v2/product_cat/210', auth=AUTH, headers=headers)
c210 = r210.json()
print("Cat 210:", c210['name'], c210['link'])

# Test HTTP status of cat 210 URL
r_check = requests.get(c210['link'], headers=headers, timeout=15)
print("Cat 210 HTTP status before:", r_check.status_code)

# Now update cat 210 parent to 209
payload = {'parent': 209}
r_update = requests.post('https://hosseinykala.ir/wp-json/wp/v2/product_cat/210', auth=AUTH, headers={'Content-Type': 'application/json', **headers}, json=payload)
print("Update status:", r_update.status_code)
if r_update.status_code == 200:
    c210_after = r_update.json()
    print("Cat 210 link after:", c210_after['link'])
    
    # Test HTTP status of new link
    r_new = requests.get(c210_after['link'], headers=headers, timeout=15)
    print("New link HTTP status:", r_new.status_code)
    
    # Test HTTP status of OLD link (does it redirect 301 or 404?)
    r_old = requests.get(c210['link'], headers=headers, timeout=15, allow_redirects=False)
    print("Old link HTTP status (no redirect):", r_old.status_code)
    if r_old.is_redirect:
        print("Redirects to:", r_old.headers.get('Location'))

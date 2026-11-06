import requests
import json
import re

base_url = "https://hosseinykala.ir"
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
})

print("=== 1. Testing Core Frontend Pages ===")
pages = [
    ("Homepage", "/"),
    ("Product Single", "/product/depoint-decent-combi-refrigerator-freezer/"),
    ("Category Archive", "/product-category/%db%8c%d8%ae%da%86%d8%a7%d9%84-%d9%81%d8%b1%db%8c%d8%b2%d8%b1/"),
    ("Cart Page", "/cart/"),
    ("Checkout Page", "/checkout/"),
    ("My Account Page", "/my-account/"),
    ("Product Search", "/?s=یخچال&post_type=product")
]

all_passed = True
for name, path in pages:
    url = base_url + path
    try:
        r = session.get(url, timeout=20)
        has_fatal = "Fatal error" in r.text or "Parse error" in r.text or "wp-die-message" in r.text
        print(f"[{'PASS' if r.status_code == 200 and not has_fatal else 'FAIL'}] {name:18} | Status: {r.status_code} | Size: {len(r.text)} bytes | Fatal: {has_fatal}")
        if r.status_code != 200 or has_fatal:
            all_passed = False
    except Exception as e:
        print(f"[FAIL] {name:18} | Error: {e}")
        all_passed = False

print("\n=== 2. Testing WooCommerce AJAX & Mini-Cart ===")
# 2.1 Get refreshed fragments
try:
    r_frag = session.post(f"{base_url}/?wc-ajax=get_refreshed_fragments", timeout=15)
    print(f"Refreshed fragments status: {r_frag.status_code}")
    if r_frag.status_code == 200:
        data = r_frag.json()
        print("Fragments received:", list(data.keys()) if isinstance(data, dict) else "Not dict")
        has_cart_hash = 'cart_hash' in data if isinstance(data, dict) else False
        print(f"[{'PASS' if has_cart_hash else 'WARN'}] Cart hash present: {has_cart_hash}")
except Exception as e:
    print(f"[FAIL] Fragments error: {e}")

# 2.2 Test Add to Cart via AJAX for a valid product (e.g. 4302 or check single product ID)
try:
    r_prod = session.get(f"{base_url}/product/depoint-decent-combi-refrigerator-freezer/", timeout=20)
    m = re.search(r'name=["\']add-to-cart["\']\s+value=["\'](\d+)["\']', r_prod.text)
    if not m:
        m = re.search(r'data-product_id=["\'](\d+)["\']', r_prod.text)
    
    prod_id = m.group(1) if m else "4302"
    print(f"Found product ID for cart test: {prod_id}")
    
    add_data = {
        'product_id': prod_id,
        'quantity': 1
    }
    r_add = session.post(f"{base_url}/?wc-ajax=add_to_cart", data=add_data, timeout=15)
    print(f"Add to cart status: {r_add.status_code}")
    if r_add.status_code == 200:
        try:
            res_json = r_add.json()
            print(f"[{'PASS' if 'fragments' in res_json else 'WARN'}] Add to cart fragments returned: {'fragments' in res_json}")
            print(f"Cart hash after add: {res_json.get('cart_hash')}")
        except Exception:
            print("Add to cart response text:", r_add.text[:200])
except Exception as e:
    print(f"[FAIL] Add to cart test error: {e}")

# 2.3 Verify Cart page reflects active cart
try:
    r_cart_check = session.get(f"{base_url}/cart/", timeout=20)
    print(f"Cart page with item status: {r_cart_check.status_code}")
    is_empty = "کارت شما در حال حاضر خالی است" in r_cart_check.text or "سبد خرید شما در حال حاضر خالی است" in r_cart_check.text
    print(f"[{'PASS' if not is_empty else 'INFO'}] Cart has items: {not is_empty}")
except Exception as e:
    print(f"[FAIL] Cart check error: {e}")

print("\n=== Summary ===")
print("Overall Core Store Integrity:", "HEALTHY & PASSED" if all_passed else "ATTENTION NEEDED")

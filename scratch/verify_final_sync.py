import os
import sys
import random
import requests

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.sync_excel_prices_to_website import load_catalog_prices, BASE_URL, AUTH, HEADERS

simple_prods, variations_by_parent, _ = load_catalog_prices()

# Let's sample 10 simple products and 10 variations
random.seed(42)
sample_simple = random.sample(simple_prods, min(10, len(simple_prods)))
sample_vars = []
for p_id in random.sample(list(variations_by_parent.keys()), min(8, len(variations_by_parent))):
    sample_vars.extend(variations_by_parent[p_id][:1])

print(f"=== Verifying {len(sample_simple)} Simple Products ===")
simple_pass = 0
for p in sample_simple:
    url = f"{BASE_URL}/wp-json/wc/v3/products/{p['id']}"
    r = requests.get(url, auth=AUTH, headers=HEADERS, timeout=15)
    if r.status_code == 200:
        d = r.json()
        live_reg = str(d.get('regular_price') or '')
        live_sale = str(d.get('sale_price') or '')
        exp_reg = p['regular_price']
        exp_sale = p['sale_price']
        ok = (live_reg == exp_reg and live_sale == exp_sale)
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] ID {p['id']} ({p['name'][:30]}): Live Reg={live_reg} (Exp={exp_reg}) | Live Sale={live_sale} (Exp={exp_sale})")
        if ok: simple_pass += 1
    else:
        print(f"  [ERROR] ID {p['id']}: Status {r.status_code}")

print(f"\n=== Verifying {len(sample_vars)} Variations ===")
var_pass = 0
for v in sample_vars:
    url = f"{BASE_URL}/wp-json/wc/v3/products/{v['parent_id']}/variations/{v['id']}"
    r = requests.get(url, auth=AUTH, headers=HEADERS, timeout=15)
    if r.status_code == 200:
        d = r.json()
        live_reg = str(d.get('regular_price') or '')
        live_sale = str(d.get('sale_price') or '')
        exp_reg = v['regular_price']
        exp_sale = v['sale_price']
        ok = (live_reg == exp_reg and live_sale == exp_sale)
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] VID {v['id']} ({v['name'][:30]}): Live Reg={live_reg} (Exp={exp_reg}) | Live Sale={live_sale} (Exp={exp_sale})")
        if ok: var_pass += 1
    else:
        print(f"  [ERROR] VID {v['id']}: Status {r.status_code}")

print(f"\nVerification Total: Simple {simple_pass}/{len(sample_simple)} PASS | Variations {var_pass}/{len(sample_vars)} PASS")

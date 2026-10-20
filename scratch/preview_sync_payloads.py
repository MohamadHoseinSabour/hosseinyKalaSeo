import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.sync_excel_prices_to_website import load_catalog_prices

simple_prods, variations_by_parent, skipped = load_catalog_prices()
print("Sample Simple Products (first 5):")
for p in simple_prods[:5]:
    print(f"  ID: {p['id']} | Name: {p['name'][:35]} | Reg: {p['regular_price']} | Sale: {p['sale_price']} | Stock: {p['stock_status']}")

print("\nSample Variations (first 2 parents):")
for pid in list(variations_by_parent.keys())[:2]:
    print(f"Parent {pid}:")
    for v in variations_by_parent[pid]:
        print(f"  VID: {v['id']} | Name: {v['name'][:35]} | Reg: {v['regular_price']} | Sale: {v['sale_price']} | Stock: {v['stock_status']}")

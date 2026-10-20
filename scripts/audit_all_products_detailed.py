import json
import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"c:\Users\mmhhs\OneDrive\Documents\GitHub\hosseinyKalaSeo"
DATA_DIR = os.path.join(PROJECT_DIR, 'data')

with open(os.path.join(DATA_DIR, 'current_catalog_reference.json'), 'r', encoding='utf-8') as f:
    ref = json.load(f)

with open(os.path.join(DATA_DIR, 'inventory_normalized.json'), 'r', encoding='utf-8') as f:
    inv = json.load(f)

live_prods = ref['live_products']
old_excel = ref['excel_items']

print(f"Total live products: {len(live_prods)}")
total_live_vars = sum(len(p.get('variations', [])) for p in live_prods)
print(f"Total live variations: {total_live_vars}")
print(f"Total old excel items: {len(old_excel)}")
print(f"Total incoming inventory items: {len(inv)}")

# Let's inspect old excel items that are NOT live products
old_offline = [it for it in old_excel if not it.get('product_id')]
print(f"Total old offline excel items: {len(old_offline)}")

# Let's print categories of old offline items
cat_counts = {}
for it in old_offline:
    c = it.get('main_cat', 'نامشخص')
    cat_counts[c] = cat_counts.get(c, 0) + 1
print("\nOld offline items per category:")
for c, cnt in cat_counts.items():
    print(f"  {c}: {cnt}")

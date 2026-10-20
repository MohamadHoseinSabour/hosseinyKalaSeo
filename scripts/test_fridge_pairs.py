import json
import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"c:\Users\mmhhs\OneDrive\Documents\GitHub\hosseinyKalaSeo"
DATA_DIR = os.path.join(PROJECT_DIR, 'data')

with open(os.path.join(DATA_DIR, 'current_catalog_reference.json'), 'r', encoding='utf-8') as f:
    catalog_ref = json.load(f)

with open(os.path.join(DATA_DIR, 'inventory_normalized.json'), 'r', encoding='utf-8') as f:
    inv_items = json.load(f)

live_products = catalog_ref['live_products']
old_excel_items = catalog_ref['excel_items']

print("--- TESTING REFRIGERATOR PAIR LOGIC ---")

# Let's inspect all inventory items with کلور, هیمالیا, نیکسان in یخچال و فریزر
fridge_inv = [it for it in inv_items if it['category'] == 'یخچال و فریزر']
print(f"Total fridge inventory items: {len(fridge_inv)}")

for it in fridge_inv:
    print(f"[{it['raw_index']:03d}] Qty: {it['raw_quantity']:2d} | Desc: {it['cleaned_raw_desc']}")

"""
analyze_inventory_items.py
==========================
تحلیل تفصیلی اقلام لیست جدید موجودی و دسته‌بندی اولیه
"""

import os
import sys
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"c:\Users\mmhhs\OneDrive\Documents\GitHub\hosseinyKalaSeo"
PARSED_FILE = os.path.join(PROJECT_DIR, 'data', 'inventory_parsed.json')

with open(PARSED_FILE, 'r', encoding='utf-8') as f:
    items = json.load(f)

print(f"تعداد کل اقلام: {len(items)}")
in_stock = [x for x in items if x['in_stock']]
out_stock = [x for x in items if not x['in_stock']]
print(f"موجود (بزرگتر از ۰): {len(in_stock)}")
print(f"ناموجود (۰ یا منفی): {len(out_stock)}")

print("\n--- اقلام ناموجود ---")
for x in out_stock:
    print(f"تعداد: {x['raw_quantity']:3d} | شرح: {x['raw_desc']}")

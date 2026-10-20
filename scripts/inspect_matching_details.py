"""
inspect_matching_details.py
===========================
بررسی تفصیلی تطبیق ۲۳۸ قلم ورودی با:
۱. ۹۷ محصول لایو سایت + ۷۸ تنوع
۲. ۷۴ قلم آفلاین قبلی اکسل
"""

import os
import sys
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"c:\Users\mmhhs\OneDrive\Documents\GitHub\hosseinyKalaSeo"
INV_FILE = os.path.join(PROJECT_DIR, 'data', 'inventory_normalized.json')
REF_FILE = os.path.join(PROJECT_DIR, 'data', 'current_catalog_reference.json')

with open(INV_FILE, 'r', encoding='utf-8') as f:
    inventory = json.load(f)

with open(REF_FILE, 'r', encoding='utf-8') as f:
    ref = json.load(f)

live_prods = ref['live_products']
excel_items = ref['excel_items']

print(f"Total inventory items: {len(inventory)}")
print(f"Total live products: {len(live_prods)}")
print(f"Total excel items: {len(excel_items)}")

# دسته‌بندی‌ها
categories = [
    'صوتی و تصویری',
    'تصفیه کننده آب',
    'زیبایی و سلامت فردی',
    'سرمایش و گرمایش',
    'شستشو و نظافت',
    'نوشیدنی ساز',
    'لوازم برقی و پخت و پز',
    'یخچال و فریزر'
]

for cat in categories:
    inv_c = [x for x in inventory if x['category'] == cat]
    exc_c = [x for x in excel_items if x['sheet'] == cat]
    print(f"\n==================== [{cat}] Inventory: {len(inv_c)} | Excel: {len(exc_c)} ====================")
    for idx, it in enumerate(inv_c, 1):
        print(f"  {idx:2d}. [Qty: {it['raw_quantity']:2d} | {'✓' if it['in_stock'] else '✗'}] {it['cleaned_raw_desc']} (Code: {it.get('model_code')}) -> Std: {it['standard_name']}")

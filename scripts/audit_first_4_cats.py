import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DATA_DIR = r"c:\Users\mmhhs\OneDrive\Documents\GitHub\hosseinyKalaSeo\data"

with open(os.path.join(DATA_DIR, 'current_catalog_reference.json'), 'r', encoding='utf-8') as f:
    ref = json.load(f)

with open(os.path.join(DATA_DIR, 'inventory_matched_results.json'), 'r', encoding='utf-8') as f:
    matched = json.load(f)

live_prods = ref['live_products']
old_excel = ref['excel_items']
old_offline = [it for it in old_excel if not it.get('product_id')]

categories = [
    'یخچال و فریزر',
    'شستشو و نظافت',
    'لوازم برقی و پخت و پز',
    'نوشیدنی ساز',
]

for cat in categories:
    print(f"\n{'='*30} {cat} {'='*30}")
    
    # 1. Live site products
    cat_live = [p for p in live_prods if p.get('main_category') == cat or any(cat in (c if isinstance(c, str) else c.get('name', '')) for c in p.get('categories', []))]
    print(f"\n--- [1] LIVE SITE PRODUCTS ({len(cat_live)}) ---")
    for p in cat_live:
        vars_str = f" ({len(p['variations'])} vars: {[v.get('attributes') for v in p.get('variations', [])]})" if p.get('variations') else ""
        print(f"  ID {p['id']}: {p['name']}{vars_str}")
        
    # 2. Old offline items
    cat_old = [it for it in old_offline if it.get('main_cat') == cat]
    print(f"\n--- [2] OLD OFFLINE EXCEL ITEMS ({len(cat_old)}) ---")
    for it in cat_old:
        print(f"  {it.get('name')} | Brand: {it.get('brand')} | Sub: {it.get('subcat')}")
        
    # 3. New inventory items classified in this cat
    cat_new = [it for it in matched if it.get('category') == cat]
    cat_new_unmatched = [it for it in cat_new if it.get('site_status') == 'در سایت تعریف نشده']
    print(f"\n--- [3] NEW INVENTORY UNMATCHED ITEMS ({len(cat_new_unmatched)}) ---")
    for it in cat_new_unmatched:
        print(f"  [{it['raw_index']:03d}] {it['raw_desc']} (Qty: {it['raw_quantity']}) | Brand: {it['brand']} | Model: {it['model_code']}")

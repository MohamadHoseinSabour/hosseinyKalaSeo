import json
import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

DATA_DIR = r"c:\Users\mmhhs\OneDrive\Documents\GitHub\hosseinyKalaSeo\data"

with open(os.path.join(DATA_DIR, 'current_catalog_reference.json'), 'r', encoding='utf-8') as f:
    ref = json.load(f)

with open(os.path.join(DATA_DIR, 'inventory_matched_results.json'), 'r', encoding='utf-8') as f:
    matched = json.load(f)

live_prods = ref['live_products']
old_excel = ref['excel_items']
old_offline = [it for it in old_excel if not it.get('product_id')]

def norm(text):
    if not text:
        return ""
    text = str(text).lower()
    text = text.replace('ي', 'ی').replace('ك', 'ک').replace('‌', ' ').replace('-', ' ').replace('_', ' ')
    text = re.sub(r'[\(\)\/\\,\.]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

print("=================== 1. NEW ITEMS THAT MATCH OLD OFFLINE ITEMS ===================")
# Check every new unmatched item against old offline items
for new_it in matched:
    if new_it.get('site_status') == 'در سایت تعریف نشده':
        new_desc = norm(new_it['raw_desc'])
        # find matching old offline items
        for old_it in old_offline:
            old_name = norm(old_it.get('name', ''))
            # check similarity / overlap
            # tokens
            new_tokens = set(new_desc.split()) - {'مدل', 'سایز', 'رنگ', 'کاره', 'وات', 'لیتر', 'کیلو', 'طرح'}
            old_tokens = set(old_name.split()) - {'مدل', 'سایز', 'رنگ', 'کاره', 'وات', 'لیتر', 'کیلو', 'طرح'}
            overlap = new_tokens.intersection(old_tokens)
            if len(overlap) >= 2 and (len(overlap) / max(len(new_tokens), len(old_tokens)) > 0.4 or any(m in old_name and m in new_desc for m in ['361', '607', '470', '270', '430', '1113', '614', '1116', '1115', '4025', '4035', '8002', '990', '706', '721', '731', '9909', '3383', 'hv11', '1011', '1031', '750', '2022', '3115', '5515', '2000', '2600', '7600', '2013', 'b35', 'h50', '4500', '18'])):
                print(f"MATCH CANDIDATE:\n  NEW: [{new_it['raw_index']}] {new_it['raw_desc']} (Cat: {new_it['category']}, Br: {new_it['brand']}, Qty: {new_it['raw_quantity']})\n  OLD: {old_it.get('name')} (Cat: {old_it.get('main_cat')}, Br: {old_it.get('brand')})\n")

print("=================== 2. NEW ITEMS THAT MATCH LIVE SITE PRODUCTS ===================")
for new_it in matched:
    if new_it.get('site_status') == 'در سایت تعریف نشده':
        new_desc = norm(new_it['raw_desc'])
        for lp in live_prods:
            lp_name = norm(lp['name'])
            new_tokens = set(new_desc.split()) - {'مدل', 'سایز', 'رنگ', 'کاره', 'وات', 'لیتر', 'کیلو', 'طرح'}
            lp_tokens = set(lp_name.split()) - {'مدل', 'سایز', 'رنگ', 'کاره', 'وات', 'لیتر', 'کیلو', 'طرح'}
            overlap = new_tokens.intersection(lp_tokens)
            if len(overlap) >= 3 or any(m in lp_name and m in new_desc for m in ['روسو', 'رسوپلاس', 'گلوری', 't7', 'boss', 'rnt101', 'frnt101', 'bmwt2', 'bmwt3', '8vw1', '9tw1', '3596', '3510', '5040', '815', '110', '120', '614', '1113', '1115', '1116', '480', '475', '2600', '1400', '5700']):
                print(f"LIVE MATCH CANDIDATE:\n  NEW: [{new_it['raw_index']}] {new_it['raw_desc']} (Qty: {new_it['raw_quantity']})\n  LIVE: ID {lp['id']}: {lp['name']}\n")

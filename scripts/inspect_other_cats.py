import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"c:\Users\mmhhs\OneDrive\Documents\GitHub\hosseinyKalaSeo"
DATA_DIR = os.path.join(PROJECT_DIR, 'data')

with open(os.path.join(DATA_DIR, 'current_catalog_reference.json'), 'r', encoding='utf-8') as f:
    catalog_ref = json.load(f)

with open(os.path.join(DATA_DIR, 'inventory_normalized.json'), 'r', encoding='utf-8') as f:
    inv_items = json.load(f)

for cat in ['لوازم برقی و پخت و پز', 'شستشو و نظافت', 'نوشیدنی ساز', 'سرمایش و گرمایش', 'زیبایی و سلامت فردی', 'تصفیه کننده آب']:
    items = [it for it in inv_items if it['category'] == cat]
    print(f"\n{'='*20} {cat} ({len(items)} items) {'='*20}")
    for it in items:
        print(f"[{it['raw_index']:03d}] Qty:{it['raw_quantity']:2d} | Desc: {it['cleaned_raw_desc']}")

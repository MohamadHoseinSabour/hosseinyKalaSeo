"""
parse_inventory.py
==================
پارس و پاکسازی لیست جدید موجودی انبار:
- تفکیک دو ستون موازی (تعداد و شرح)
- پاکسازی خط فاصله‌های اضافی (---)
- استخراج کد مدل (که پس از - یا در انتهای شرح قرار دارد)
- تعیین وضعیت موجودی: تعداد > 0 یعنی موجود، تعداد <= 0 یعنی ناموجود
"""

import os
import sys
import json
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"c:\Users\mmhhs\OneDrive\Documents\GitHub\hosseinyKalaSeo"
INPUT_CSV = os.path.join(PROJECT_DIR, 'data', 'inventory_incoming_raw.csv')
OUTPUT_JSON = os.path.join(PROJECT_DIR, 'data', 'inventory_parsed.json')

def clean_item_description(raw_desc):
    raw_desc = raw_desc.strip()
    
    # استخراج مدل از انتهای عبارت یا بعد از خط‌فاصله‌ها
    # معمولا خط‌فاصله‌های پیاپی وجود دارند مثل: ال ای دی هاورسون75اینچ---------- یا آبگرمکن دیواری بوتان ----B3115
    # گاهی مدل داخل پرانتز است مثل R)re01(
    
    # بررسی آیا خط فاصله دارد؟
    # جدا کردن متن قبل از خط فاصله‌ها و کد پس از خط فاصله‌ها
    pattern = r'^(.*?)[-\s]+([A-Za-z0-9_\(\)\/\.\+]+)?$'
    
    # بیایید دقیق‌تر بررسی کنیم:
    # ابتدا خط‌فاصله‌های میانی طولانی را بیابیم
    m = re.search(r'[-]{2,}\s*([A-Za-z0-9_\(\)\/\.\+]+)?\s*$', raw_desc)
    model_code = ""
    clean_name = raw_desc
    
    if m:
        model_part = m.group(1) or ""
        text_before = raw_desc[:m.start()].strip()
        model_code = model_part.strip()
        clean_name = text_before
    else:
        # اگر خط فاصله طولانی نداشت، خط‌فاصله‌های انتهایی را حذف کنیم
        clean_name = raw_desc.rstrip('-').strip()
    
    return clean_name, model_code

def parse_incoming_inventory():
    with open(INPUT_CSV, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    items = []
    
    for line_idx, line in enumerate(lines):
        line = line.strip()
        if not line or line.startswith('تعداد'):
            continue
            
        parts = line.split(',,')
        
        # بخش اول
        p1 = parts[0].strip()
        if p1:
            p1_split = p1.split(',', 1)
            if len(p1_split) == 2:
                qty_str, desc = p1_split
                try:
                    qty = int(qty_str.strip())
                except ValueError:
                    qty = 0
                items.append({
                    "raw_index": len(items) + 1,
                    "line_num": line_idx + 1,
                    "raw_quantity": qty,
                    "in_stock": qty > 0,
                    "raw_desc": desc.strip(),
                })
                
        # بخش دوم
        if len(parts) > 1:
            p2 = parts[1].strip()
            if p2:
                p2_split = p2.split(',', 1)
                if len(p2_split) == 2:
                    qty_str, desc = p2_split
                    try:
                        qty = int(qty_str.strip())
                    except ValueError:
                        qty = 0
                    items.append({
                        "raw_index": len(items) + 1,
                        "line_num": line_idx + 1,
                        "raw_quantity": qty,
                        "in_stock": qty > 0,
                        "raw_desc": desc.strip(),
                    })
                    
    print(f"تعداد کل اقلام استخراج‌شده: {len(items)}")
    
    # ذخیره فایل اولیه
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
        
    print(f"فایل خروجی ذخیره شد در: {OUTPUT_JSON}")

if __name__ == '__main__':
    parse_incoming_inventory()

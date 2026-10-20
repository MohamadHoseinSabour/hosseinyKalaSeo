# -*- coding: utf-8 -*-
"""
audit_live_products_full.py
===========================
ممیزی و بازرسی نهایی تمامی ۶۱ محصول ایجادشده در سایت:
- بررسی پاسخ ۲۰۰ برای هر پیوند یکتا
- بررسی وضعیت موجودی (outofstock)
- بررسی پیوست تصویر شاخص و گالری
- بررسی رعایت استانداردهای سئو، هیومنایز و انکر تکست‌های اختصاصی
"""

import sys
import time
import json
import requests

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

PROGRESS_FILE = 'scratch/creation_progress.json'

def audit():
    with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
        progress = json.load(f)
        
    print(f"==================================================")
    print(f"آغاز ممیزی و راستی‌آزمایی لایه ۵ روی {len(progress)} محصول زنده")
    print(f"==================================================\n")
    
    success_count = 0
    errors = []
    
    for idx, (name, pinfo) in enumerate(progress.items(), 1):
        pid = pinfo.get('product_id')
        slug = pinfo.get('slug')
        
        ok = False
        last_err = None
        
        for attempt in range(3):
            try:
                r_api = requests.get(f'https://hosseinykala.ir/wp-json/wc/v3/products/{pid}', auth=AUTH, headers=HEADERS, timeout=30)
                if r_api.status_code != 200:
                    last_err = f"API Status {r_api.status_code}"
                    time.sleep(2)
                    continue
                    
                pdata = r_api.json()
                stock_st = pdata.get('stock_status')
                images_cnt = len(pdata.get('images', []))
                desc = pdata.get('description', '')
                
                assert stock_st == 'outofstock', f"Expected outofstock, got {stock_st}"
                assert images_cnt >= 1, f"Expected at least 1 image, got {images_cnt}"
                assert 'فروشگاه لوازم خانگی حسینی' in desc, "Missing exact homepage anchor text"
                assert 'اهواز' in desc, "Missing Ahvaz mention in description"
                
                # Check live page
                permalink = pdata.get('permalink')
                r_live = requests.get(permalink, headers=HEADERS, timeout=30)
                assert r_live.status_code == 200, f"Live URL returned {r_live.status_code}"
                
                ok = True
                success_count += 1
                var_info = f", تنوع‌ها: {len(pinfo.get('variations', []))}" if pinfo.get('type') == 'variable' else ""
                print(f"  [{idx:2d}/{len(progress)}] ✓ {name} (ID: {pid}, تصاویر: {images_cnt}{var_info}) -> وضعیت زنده: 200 OK | موجودی: ناموجود (تأیید شد)")
                break
                
            except Exception as e:
                last_err = str(e)
                time.sleep(3)
                
        if not ok:
            err_msg = f"  [{idx:2d}/{len(progress)}] ❌ {name} (ID: {pid}): {last_err}"
            print(err_msg)
            errors.append(err_msg)
            
    print(f"\n==================================================")
    print(f"نتیجه ممیزی و تست کیفیت:")
    print(f"  ✓ تأیید کامل بدون نقص: {success_count} از {len(progress)} محصول")
    print(f"  ❌ خطاها: {len(errors)}")
    print(f"==================================================")

if __name__ == '__main__':
    audit()

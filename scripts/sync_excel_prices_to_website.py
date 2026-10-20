"""
sync_excel_prices_to_website.py
===============================
اسکریپت همگام‌سازی و به‌روزرسانی مستقیم قیمت‌های کاتالوگ اکسل روی سایت حسینی کالا:
- خواندن قیمت‌های جدید از hosseiny_kala_catalog.xlsx
- تبدیل ریال به تومان (واحد رسمی پول ووکامرس سایت)
- به‌روزرسانی محصولات ساده از طریق WooCommerce Batch API
- به‌روزرسانی تنوع‌ها (Variations) به تفکیک محصولات والد از طریق Variations Batch API
- بررسی و صحت‌سنجی نهایی با دریافت اطلاعات زنده از سایت
"""

import os
import sys
import json
import time
import argparse
import requests
import openpyxl
from collections import defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_XLSM = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.xlsm')
CATALOG_PATH = CATALOG_XLSM if os.path.exists(CATALOG_XLSM) else os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.xlsx')
CATALOG_XLSX = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.xlsx')
CATALOG_LATEST = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog_latest.xlsx')
BASE_URL = 'https://hosseinykala.ir'
AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

def get_sheet_col_map(ws):
    mapping = {
        'name': 1, 'price_reg': 2, 'price_sale': 6,
        'stock': 8, 'type': 12, 'pid': 14, 'vid': 15
    }
    for col in range(1, ws.max_column + 1):
        val = str(ws.cell(1, col).value or '').strip()
        if 'نام محصول' in val: mapping['name'] = col
        elif 'قیمت عادی (ریال)' in val: mapping['price_reg'] = col
        elif 'قیمت حراج (ریال)' in val: mapping['price_sale'] = col
        elif 'موجودی' in val: mapping['stock'] = col
        elif 'نوع محصول' in val: mapping['type'] = col
        elif 'شناسه محصول' in val: mapping['pid'] = col
        elif 'شناسه تنوع' in val: mapping['vid'] = col
    return mapping

def load_catalog_prices():
    wb = openpyxl.load_workbook(CATALOG_PATH, data_only=True)
    sheets = [
        'یخچال و فریزر', 'شستشو و نظافت', 'لوازم برقی و پخت و پز', 'نوشیدنی ساز',
        'سرمایش و گرمایش', 'تصفیه کننده آب', 'صوتی و تصویری', 'زیبایی و سلامت فردی'
    ]

    simple_products = []
    variations_by_parent = defaultdict(list)
    skipped_items = []

    for sname in sheets:
        if sname not in wb.sheetnames:
            continue
        ws = wb[sname]
        col_map = get_sheet_col_map(ws)
        for r in range(2, ws.max_row + 1):
            name = ws.cell(r, col_map['name']).value
            if not name:
                continue
            name_str = str(name).strip()
            if name_str.startswith('📂') or name_str.startswith('•'):
                continue
            
            row_type = str(ws.cell(r, col_map['type']).value or '').strip()
            # محصولات والد متغیر نباید قیمت داشته باشند و نباید به عنوان محصول ساده ثبت شوند
            if row_type == 'متغیر':
                continue

            p_reg_rial = ws.cell(r, col_map['price_reg']).value
            p_sale_rial = ws.cell(r, col_map['price_sale']).value
            pid = ws.cell(r, col_map['pid']).value
            vid = ws.cell(r, col_map['vid']).value
            
            # If no price
            if p_reg_rial is None or not isinstance(p_reg_rial, (int, float)):
                continue

            # If no site product_id
            if pid is None or str(pid).strip() == '':
                skipped_items.append({'name': name_str, 'sheet': sname, 'row': r, 'reason': 'No product_id'})
                continue

            p_reg_toman = int(round(p_reg_rial / 10))
            p_sale_toman = int(round(p_sale_rial / 10)) if (p_sale_rial is not None and isinstance(p_sale_rial, (int, float))) else ''

            stock_val = ws.cell(r, col_map['stock']).value
            stock_str = str(stock_val or '').strip()
            stock_status = 'instock' if ('✓' in stock_str or 'موجود' in stock_str) and ('ناموجود' not in stock_str) else 'outofstock'

            item_data = {
                'name': name_str,
                'sheet': sname,
                'row': r,
                'regular_price': str(p_reg_toman),
                'sale_price': str(p_sale_toman) if p_sale_toman != '' else '',
                'stock_status': stock_status
            }

            pid = int(pid)
            if vid is not None and str(vid).strip() != '':
                vid = int(vid)
                item_data['id'] = vid
                item_data['parent_id'] = pid
                variations_by_parent[pid].append(item_data)
            else:
                item_data['id'] = pid
                simple_products.append(item_data)

    return simple_products, variations_by_parent, skipped_items

def update_simple_products(simple_products, dry_run=False):
    print(f"\n--- Updating {len(simple_products)} Simple Products ---")
    if dry_run:
        print("[DRY RUN] Would update simple products in batches.")
        return 0, 0

    chunk_size = 50
    success_count = 0
    fail_count = 0

    for i in range(0, len(simple_products), chunk_size):
        chunk = simple_products[i:i + chunk_size]
        payload = {
            'update': [
                {
                    'id': p['id'],
                    'regular_price': p['regular_price'],
                    'sale_price': p['sale_price'],
                    'stock_status': p.get('stock_status', 'instock')
                }
                for p in chunk
            ]
        }
        
        try:
            url = f"{BASE_URL}/wp-json/wc/v3/products/batch"
            resp = requests.post(url, auth=AUTH, headers=HEADERS, json=payload, timeout=45)
            if resp.status_code == 200:
                data = resp.json()
                updated_list = data.get('update', [])
                success_count += len(updated_list)
                print(f"   Batch {i // chunk_size + 1}: Successfully updated {len(updated_list)} simple products.")
            else:
                print(f"   [ERROR] Batch {i // chunk_size + 1} failed with status {resp.status_code}: {resp.text[:200]}")
                fail_count += len(chunk)
        except Exception as e:
            print(f"   [EXCEPTION] Batch {i // chunk_size + 1}: {str(e)}")
            fail_count += len(chunk)

        time.sleep(1)

    return success_count, fail_count

def update_variations(variations_by_parent, dry_run=False):
    total_vars = sum(len(v) for v in variations_by_parent.values())
    print(f"\n--- Updating {total_vars} Variations Across {len(variations_by_parent)} Parents ---")
    if dry_run:
        print("[DRY RUN] Would update variations by parent.")
        return 0, 0

    success_count = 0
    fail_count = 0

    for parent_id, vars_list in variations_by_parent.items():
        payload = {
            'update': [
                {
                    'id': v['id'],
                    'regular_price': v['regular_price'],
                    'sale_price': v['sale_price'],
                    'stock_status': v.get('stock_status', 'instock')
                }
                for v in vars_list
            ]
        }

        try:
            url = f"{BASE_URL}/wp-json/wc/v3/products/{parent_id}/variations/batch"
            resp = requests.post(url, auth=AUTH, headers=HEADERS, json=payload, timeout=45)
            if resp.status_code == 200:
                data = resp.json()
                updated_list = data.get('update', [])
                success_count += len(updated_list)
                print(f"   Parent {parent_id}: Successfully updated {len(updated_list)} variations.")
            else:
                print(f"   [ERROR] Parent {parent_id} failed with status {resp.status_code}: {resp.text[:200]}")
                fail_count += len(vars_list)
        except Exception as e:
            print(f"   [EXCEPTION] Parent {parent_id}: {str(e)}")
            fail_count += len(vars_list)

        time.sleep(0.5)

    return success_count, fail_count

def verify_live_updates(sample_items):
    print("\n--- Verifying Live Updates on Website ---")
    verified_ok = 0
    for item in sample_items:
        try:
            if 'parent_id' in item:
                url = f"{BASE_URL}/wp-json/wc/v3/products/{item['parent_id']}/variations/{item['id']}"
            else:
                url = f"{BASE_URL}/wp-json/wc/v3/products/{item['id']}"

            resp = requests.get(url, auth=AUTH, headers=HEADERS, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                live_reg = str(data.get('regular_price') or '')
                live_sale = str(data.get('sale_price') or '')
                expected_reg = item['regular_price']
                expected_sale = item['sale_price']

                reg_match = (live_reg == expected_reg)
                sale_match = (live_sale == expected_sale)

                status_str = "PASS" if (reg_match and sale_match) else "MISMATCH"
                print(f"   [{status_str}] ID: {item['id']} ({item['name'][:35]}) | Live Reg: {live_reg} (Exp: {expected_reg}) | Live Sale: {live_sale} (Exp: {expected_sale})")
                if reg_match and sale_match:
                    verified_ok += 1
            else:
                print(f"   [FAIL] Could not fetch ID {item['id']}: Status {resp.status_code}")
        except Exception as e:
            print(f"   [EXCEPTION] Checking ID {item['id']}: {str(e)}")
        time.sleep(0.3)

    print(f"\nLive Verification Result: {verified_ok}/{len(sample_items)} samples perfectly matched.")

def commit_catalog_prices(catalog_path):
    """تثبیت قیمت‌های جدید در کاتالوگ: ستون D (آخرین قیمت مشخص‌شده) با ستون B (قیمت تاییدشده) یکسان می‌شود"""
    if not os.path.exists(catalog_path):
        return 0

    is_xlsm = catalog_path.endswith('.xlsm')
    wb = openpyxl.load_workbook(catalog_path, keep_vba=is_xlsm)
    updated_count = 0
    sheets = [
        'یخچال و فریزر', 'شستشو و نظافت', 'لوازم برقی و پخت و پز', 'نوشیدنی ساز',
        'سرمایش و گرمایش', 'تصفیه کننده آب', 'صوتی و تصویری', 'زیبایی و سلامت فردی'
    ]

    for sname in sheets:
        if sname not in wb.sheetnames:
            continue
        ws = wb[sname]
        col_map = get_sheet_col_map(ws)
        b_col = col_map.get('price_reg', 2)
        d_col = 4 # آخرین قیمت مشخص‌شده (ریال)
        type_col = col_map.get('type', 12)

        for r in range(2, ws.max_row + 1):
            ptype = str(ws.cell(r, type_col).value or '').strip()
            # تضمین فرمت سه‌رقم‌سه‌رقم
            ws.cell(r, 2).number_format = '#,##0'
            ws.cell(r, 3).number_format = '#,##0'
            ws.cell(r, 4).number_format = '#,##0'
            ws.cell(r, 5).number_format = '+0.0%;-0.0%;"0.0%"'
            ws.cell(r, 6).number_format = '#,##0'
            ws.cell(r, 7).number_format = '#,##0'

            if ptype == 'متغیر':
                ws.cell(r, b_col).value = None
                ws.cell(r, d_col).value = None
                continue

            b_val = ws.cell(r, b_col).value
            if isinstance(b_val, (int, float)) and b_val > 0:
                d_val = ws.cell(r, d_col).value
                if d_val != b_val:
                    ws.cell(r, d_col, value=b_val)
                    updated_count += 1

    wb.save(catalog_path)
    return updated_count

def main():
    parser = argparse.ArgumentParser(description="همگام‌سازی قیمت‌های کاتالوگ اکسل با سایت حسینی کالا")
    parser.add_argument('--dry-run', action='store_true', help="فقط پیش‌نمایش بدون ارسال به سایت یا تغییر فایل")
    parser.add_argument('--commit-only', action='store_true', help="فقط تثبیت قیمت‌های ستون B در ستون D درون اکسل بدون ارسال به سایت")
    parser.add_argument('--no-commit', action='store_true', help="ارسال به سایت بدون به‌روزرسانی ستون D در اکسل")
    args = parser.parse_args()

    if args.commit_only:
        print("==================================================")
        print(" تثبیت مستقیم قیمت‌ها در فایل اکسل کاتالوگ")
        print("==================================================")
        for p in set([CATALOG_PATH, CATALOG_XLSX, CATALOG_LATEST]):
            commit_catalog_prices(p)
        print(f"✓ ستون D (آخرین قیمت مشخص‌شده) در تمامی فایل‌های کاتالوگ با ستون B یکسان شد و درصد تغییرات صفر شد.")
        return

    print("==================================================")
    print(" WooCommerce Price Synchronization - Hosseiny Kala")
    print("==================================================")

    simple_products, variations_by_parent, skipped_items = load_catalog_prices()
    total_vars = sum(len(v) for v in variations_by_parent.values())

    print(f"Loaded from Excel:")
    print(f" - Simple products with prices: {len(simple_products)}")
    print(f" - Variations with prices: {total_vars} (in {len(variations_by_parent)} variable products)")
    print(f" - Items without site product_id: {len(skipped_items)}")

    # Execute updates
    s_ok, s_fail = update_simple_products(simple_products, dry_run=args.dry_run)
    v_ok, v_fail = update_variations(variations_by_parent, dry_run=args.dry_run)

    print("\n==================================================")
    print(" Execution Summary")
    print("==================================================")
    print(f"Simple Products: {s_ok} successful, {s_fail} failed.")
    print(f"Variations:      {v_ok} successful, {v_fail} failed.")
    print(f"Total Live Items Updated: {s_ok + v_ok} of {len(simple_products) + total_vars}")

    # Auto-commit to Column D if not dry-run and not no-commit
    if not args.dry_run and not args.no_commit and (s_ok + v_ok > 0):
        u1 = commit_catalog_prices(CATALOG_PATH)
        u2 = commit_catalog_prices(CATALOG_LATEST)
        print(f"\n✓ ستون D (آخرین قیمت مشخص‌شده) برای {u1} کالا در فایل‌های اکسل با قیمت جدید تایید و تثبیت شد.")

    if not args.dry_run:
        # Pick samples for verification (Clover + Non-Clover)
        sample_items = []
        sample_items.extend(simple_products[:3])
        for vlist in list(variations_by_parent.values())[:3]:
            sample_items.extend(vlist[:2])
        verify_live_updates(sample_items)

if __name__ == '__main__':
    main()

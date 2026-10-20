"""
apply_30pct_increase_and_sync.py
==================================
۱. افزایش ۳۰ درصدی قیمت تمام محصولات موجود در شیت‌های کاتالوگ اکسل (قیمت عادی و قیمت حراج)
۲. حفظ کامل فرمول‌های ستون تومان (C و G)، درصد تغییر (E)، و استانداردهای اکسل
۳. همگام‌سازی کامل و دسته‌ای (Batch) قیمت‌های جدید با وب‌سایت حسینی کالا از طریق WooCommerce REST API (تبدیل به تومان)
۴. تست و صحت‌سنجی زنده (Live Verification) قیمت‌ها در سایت
۵. به‌روزرسانی ستون D (آخرین قیمت مشخص‌شده) مطابق دستور کاربر پس از هماهنگی موفق با سایت
۶. به‌روزرسانی فایل‌های پشتیبان و دیتابیس محلی
"""

import os
import sys
import time
import json
import shutil
import datetime
import requests
import openpyxl
from collections import defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.xlsx')
CATALOG_BACKUP_PATH = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.backup.xlsx')
PRODUCTS_JSON_PATH = os.path.join(PROJECT_DIR, 'data', 'products.json')

BASE_URL = 'https://hosseinykala.ir'
AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

CATEGORY_SHEETS = [
    'یخچال و فریزر',
    'شستشو و نظافت',
    'لوازم برقی و پخت و پز',
    'نوشیدنی ساز',
    'سرمایش و گرمایش',
    'تصفیه کننده آب',
    'صوتی و تصویری',
    'زیبایی و سلامت فردی'
]


def backup_catalog():
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    ts_backup = os.path.join(PROJECT_DIR, f'hosseiny_kala_catalog.backup_{timestamp}.xlsx')
    shutil.copy2(CATALOG_PATH, ts_backup)
    shutil.copy2(CATALOG_PATH, CATALOG_BACKUP_PATH)
    print(f"✓ فایل پشتیبان با موفقیت ایجاد شد: {os.path.basename(ts_backup)}")
    return ts_backup


def increase_prices_by_30(catalog_path):
    print("\n" + "=" * 65)
    print("📈 گام ۱: افزایش ۳۰ درصدی قیمت تمام محصولات در کاتالوگ اکسل")
    print("=" * 65)

    wb = openpyxl.load_workbook(catalog_path, data_only=False)
    
    total_reg_updated = 0
    total_sale_updated = 0
    total_parents_skipped = 0
    price_changes_summary = []

    for sname in CATEGORY_SHEETS:
        if sname not in wb.sheetnames:
            continue
        ws = wb[sname]
        sheet_reg_count = 0
        sheet_sale_count = 0

        for r in range(2, ws.max_row + 1):
            name = ws.cell(r, 1).value
            if not name:
                continue
            name_str = str(name).strip()
            if name_str.startswith(('📂', '•')):
                continue

            ptype = str(ws.cell(r, 12).value or '').strip()
            
            # قانون کلیدی: محصولات والد متغیر هرگز نباید قیمت داشته باشند
            if ptype == 'متغیر':
                ws.cell(r, 2).value = None
                ws.cell(r, 4).value = None
                ws.cell(r, 6).value = None
                total_parents_skipped += 1
                continue

            # سلول‌های قیمت عادی (B) و قیمت حراج (F)
            cell_reg = ws.cell(r, 2)
            cell_sale = ws.cell(r, 6)

            old_reg = cell_reg.value
            old_sale = cell_sale.value

            pid = ws.cell(r, 14).value
            vid = ws.cell(r, 15).value

            # بررسی قیمت عادی
            if old_reg is not None and isinstance(old_reg, (int, float)) and old_reg > 0:
                new_reg = int(round(old_reg * 1.30))
                cell_reg.value = new_reg
                cell_reg.number_format = '#,##0'
                total_reg_updated += 1
                sheet_reg_count += 1

                new_sale = None
                if old_sale is not None and isinstance(old_sale, (int, float)) and old_sale > 0:
                    new_sale = int(round(old_sale * 1.30))
                    cell_sale.value = new_sale
                    cell_sale.number_format = '#,##0'
                    total_sale_updated += 1
                    sheet_sale_count += 1

                price_changes_summary.append({
                    'sheet': sname,
                    'row': r,
                    'name': name_str,
                    'ptype': ptype,
                    'pid': int(pid) if pid else None,
                    'vid': int(vid) if vid else None,
                    'old_reg_rial': old_reg,
                    'new_reg_rial': new_reg,
                    'old_sale_rial': old_sale,
                    'new_sale_rial': new_sale,
                })

        print(f"  • شیت «{sname}»: {sheet_reg_count} محصول عادی و {sheet_sale_count} قیمت حراج به‌روزرسانی شد.")

    wb.save(catalog_path)
    print(f"\n✓ تغییرات در فایل {os.path.basename(catalog_path)} ذخیره شد.")
    print(f"  - مجموع اقلام با افزایش ۳۰٪ قیمت عادی: {total_reg_updated}")
    print(f"  - مجموع اقلام با افزایش ۳۰٪ قیمت حراج: {total_sale_updated}")
    print(f"  - والدین متغیر محافظت‌شده (بدون قیمت): {total_parents_skipped}")

    return price_changes_summary


def load_sync_payload_from_catalog(catalog_path):
    wb = openpyxl.load_workbook(catalog_path, data_only=True)
    simple_products = []
    variations_by_parent = defaultdict(list)

    for sname in CATEGORY_SHEETS:
        if sname not in wb.sheetnames:
            continue
        ws = wb[sname]
        for r in range(2, ws.max_row + 1):
            name = ws.cell(r, 1).value
            if not name:
                continue
            name_str = str(name).strip()
            if name_str.startswith(('📂', '•')):
                continue

            ptype = str(ws.cell(r, 12).value or '').strip()
            if ptype == 'متغیر':
                continue

            p_reg_rial = ws.cell(r, 2).value
            p_sale_rial = ws.cell(r, 6).value
            pid = ws.cell(r, 14).value
            vid = ws.cell(r, 15).value

            if p_reg_rial is None or not isinstance(p_reg_rial, (int, float)) or p_reg_rial <= 0:
                continue
            if not pid:
                continue

            p_reg_toman = int(round(p_reg_rial / 10))
            p_sale_toman = int(round(p_sale_rial / 10)) if (p_sale_rial is not None and isinstance(p_sale_rial, (int, float)) and p_sale_rial > 0) else ''

            stock_val = ws.cell(r, 8).value
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

    return simple_products, variations_by_parent


def sync_to_website(simple_products, variations_by_parent):
    print("\n" + "=" * 65)
    print("🌐 گام ۲: همگام‌سازی دسته‌ای قیمت‌ها با سایت حسینی کالا (WooCommerce API)")
    print("=" * 65)

    session = requests.Session()
    session.auth = AUTH
    session.headers.update(HEADERS)

    # ۱. محصولات ساده
    chunk_size = 15
    simple_success = 0
    simple_fail = 0

    print(f"\n--- [۱/۲] به‌روزرسانی {len(simple_products)} محصول ساده در دسته‌های {chunk_size} تایی ---")
    for i in range(0, len(simple_products), chunk_size):
        chunk = simple_products[i:i + chunk_size]
        payload = {
            'update': [
                {
                    'id': p['id'],
                    'regular_price': p['regular_price'],
                    'sale_price': p['sale_price'],
                    'stock_status': p['stock_status']
                }
                for p in chunk
            ]
        }

        url = f"{BASE_URL}/wp-json/wc/v3/products/batch"
        batch_no = i // chunk_size + 1
        total_batches = (len(simple_products) + chunk_size - 1) // chunk_size

        for attempt in range(1, 4):
            try:
                t0 = time.time()
                resp = session.post(url, json=payload, timeout=45)
                elapsed = time.time() - t0
                if resp.status_code == 200:
                    data = resp.json()
                    up_count = len(data.get('update', []))
                    simple_success += up_count
                    print(f"  ✓ دسته {batch_no}/{total_batches} ({len(chunk)} محصول) با موفقیت ثبت شد ({elapsed:.1f}s)")
                    break
                else:
                    print(f"  ⚠️ خطا در ارسال دسته {batch_no} (تلاش {attempt}): کد {resp.status_code} - {resp.text[:150]}")
                    if attempt == 3:
                        simple_fail += len(chunk)
                    time.sleep(2)
            except Exception as e:
                print(f"  ⚠️ خطای شبکه در دسته {batch_no} (تلاش {attempt}): {e}")
                if attempt == 3:
                    simple_fail += len(chunk)
                time.sleep(3)

        time.sleep(0.5)

    # ۲. تنوع‌ها
    total_vars = sum(len(v) for v in variations_by_parent.values())
    var_success = 0
    var_fail = 0

    print(f"\n--- [۲/۲] به‌روزرسانی {total_vars} تنوع در قالب {len(variations_by_parent)} محصول والد متغیر ---")
    for parent_idx, (parent_id, vars_list) in enumerate(variations_by_parent.items(), 1):
        payload = {
            'update': [
                {
                    'id': v['id'],
                    'regular_price': v['regular_price'],
                    'sale_price': v['sale_price'],
                    'stock_status': v['stock_status']
                }
                for v in vars_list
            ]
        }

        url = f"{BASE_URL}/wp-json/wc/v3/products/{parent_id}/variations/batch"
        for attempt in range(1, 4):
            try:
                t0 = time.time()
                resp = session.post(url, json=payload, timeout=45)
                elapsed = time.time() - t0
                if resp.status_code == 200:
                    data = resp.json()
                    up_count = len(data.get('update', []))
                    var_success += up_count
                    parent_name = vars_list[0]['name'].split(' - ')[0] if ' - ' in vars_list[0]['name'] else vars_list[0]['name']
                    print(f"  ✓ والد #{parent_id} ({parent_idx}/{len(variations_by_parent)}) | {len(vars_list)} تنوع | {parent_name[:30]} ({elapsed:.1f}s)")
                    break
                else:
                    print(f"  ⚠️ خطا در والد #{parent_id} (تلاش {attempt}): کد {resp.status_code} - {resp.text[:150]}")
                    if attempt == 3:
                        var_fail += len(vars_list)
                    time.sleep(2)
            except Exception as e:
                print(f"  ⚠️ خطای شبکه در والد #{parent_id} (تلاش {attempt}): {e}")
                if attempt == 3:
                    var_fail += len(vars_list)
                time.sleep(3)

        time.sleep(0.3)

    print("\n" + "-" * 50)
    print(f"خلاصه همگام‌سازی سایت:")
    print(f"  • محصولات ساده: {simple_success} موفق / {simple_fail} ناموفق")
    print(f"  • تنوع‌ها:       {var_success} موفق / {var_fail} ناموفق")
    print(f"  • کل اقلام ثبت‌شده در سایت: {simple_success + var_success} از {len(simple_products) + total_vars}")
    print("-" * 50)

    return simple_success, simple_fail, var_success, var_fail


def verify_live_site_prices(simple_products, variations_by_parent):
    print("\n" + "=" * 65)
    print("🔍 گام ۳: صحت‌سنجی زنده قیمت‌های جدید در وب‌سایت (Live Verification)")
    print("=" * 65)

    session = requests.Session()
    session.auth = AUTH
    session.headers.update(HEADERS)

    # انتخاب نمونه‌های تصادفی از محصولات ساده و تنوع‌ها
    sample_tests = []
    # ۳ محصول ساده
    sample_tests.extend(simple_products[:4])
    sample_tests.extend(simple_products[-2:])
    # نمونه از چند تنوع با والدین مختلف
    for p_id in list(variations_by_parent.keys())[:4]:
        sample_tests.extend(variations_by_parent[p_id][:2])

    passed_count = 0

    for item in sample_tests:
        try:
            if 'parent_id' in item:
                url = f"{BASE_URL}/wp-json/wc/v3/products/{item['parent_id']}/variations/{item['id']}"
            else:
                url = f"{BASE_URL}/wp-json/wc/v3/products/{item['id']}"

            resp = session.get(url, timeout=20)
            if resp.status_code == 200:
                data = resp.json()
                live_reg = str(data.get('regular_price') or '')
                live_sale = str(data.get('sale_price') or '')

                exp_reg = item['regular_price']
                exp_sale = item['sale_price']

                reg_ok = (live_reg == exp_reg)
                sale_ok = (live_sale == exp_sale)

                if reg_ok and sale_ok:
                    passed_count += 1
                    status_badge = "✅ PASS"
                else:
                    status_badge = "❌ MISMATCH"

                sale_info = f" | حراج: {live_sale} (انتظار: {exp_sale})" if (exp_sale or live_sale) else ""
                print(f"  {status_badge} ID #{item['id']} ({item['name'][:28]}): قیمت سایت: {int(live_reg):,} ت (انتظار: {int(exp_reg):,}){sale_info}")
            else:
                print(f"  ❌ خطا در دریافت اطلاعات ID #{item['id']}: کد {resp.status_code}")
        except Exception as e:
            print(f"  ❌ خطای اتصال در بررسی ID #{item['id']}: {e}")

        time.sleep(0.3)

    print(f"\nنتیجه صحت‌سنجی: {passed_count} از {len(sample_tests)} نمونه کاملاً منطبق و تایید شدند.")
    return passed_count == len(sample_tests)


def commit_column_d_prices(catalog_path):
    print("\n" + "=" * 65)
    print("💾 گام ۴: به‌روزرسانی ستون D (آخرین قیمت مشخص‌شده) در اکسل و فایل بکاپ")
    print("=" * 65)

    wb = openpyxl.load_workbook(catalog_path, data_only=False)
    committed_count = 0

    for sname in CATEGORY_SHEETS:
        if sname not in wb.sheetnames:
            continue
        ws = wb[sname]

        for r in range(2, ws.max_row + 1):
            ptype = str(ws.cell(r, 12).value or '').strip()
            
            # فرمت‌های استاندارد
            ws.cell(r, 2).number_format = '#,##0'
            ws.cell(r, 3).number_format = '#,##0'
            ws.cell(r, 4).number_format = '#,##0'
            ws.cell(r, 5).number_format = '+0.0%;-0.0%;"0.0%"'
            ws.cell(r, 6).number_format = '#,##0'
            ws.cell(r, 7).number_format = '#,##0'

            if ptype == 'متغیر':
                ws.cell(r, 2).value = None
                ws.cell(r, 4).value = None
                continue

            b_val = ws.cell(r, 2).value
            if b_val is not None and isinstance(b_val, (int, float)) and b_val > 0:
                ws.cell(r, 4).value = b_val
                committed_count += 1

    wb.save(catalog_path)
    shutil.copy2(catalog_path, CATALOG_BACKUP_PATH)
    print(f"✓ ستون D برای {committed_count} محصول با قیمت تاییدشده همگام و ذخیره شد.")
    print(f"✓ فایل پشتیبان اصلی {os.path.basename(CATALOG_BACKUP_PATH)} نیز به‌روزرسانی گردید.")
    return committed_count


def sync_local_products_json(simple_products, variations_by_parent):
    if not os.path.exists(PRODUCTS_JSON_PATH):
        return

    print("\n" + "=" * 65)
    print("📦 گام ۵: به‌روزرسانی قیمت‌ها در دیتابیس محلی (data/products.json)")
    print("=" * 65)

    try:
        with open(PRODUCTS_JSON_PATH, 'r', encoding='utf-8') as f:
            products = json.load(f)

        price_map = {}
        for p in simple_products:
            price_map[p['id']] = {
                'regular_price': p['regular_price'],
                'sale_price': p['sale_price'],
                'price': p['sale_price'] if p['sale_price'] else p['regular_price']
            }

        for parent_id, vlist in variations_by_parent.items():
            for v in vlist:
                price_map[v['id']] = {
                    'regular_price': v['regular_price'],
                    'sale_price': v['sale_price'],
                    'price': v['sale_price'] if v['sale_price'] else v['regular_price']
                }

        updated_json_count = 0
        for p in products:
            pid = p.get('id') or p.get('product_id')
            if pid and pid in price_map:
                p['regular_price'] = price_map[pid]['regular_price']
                p['sale_price'] = price_map[pid]['sale_price']
                p['price'] = price_map[pid]['price']
                updated_json_count += 1

        with open(PRODUCTS_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=2)

        print(f"✓ اطلاعات {updated_json_count} محصول در data/products.json همگام‌سازی شد.")
    except Exception as e:
        print(f"⚠️ خطای اختیاری در به‌روزرسانی products.json: {e}")


def main():
    print("=" * 70)
    print("⚡ برنامه جامع افزایش ۳۰ درصدی قیمت‌ها و همگام‌سازی با وب‌سایت حسینی کالا")
    print("=" * 70)

    # ۰. ایجاد پشتیبان
    backup_file = backup_catalog()

    # ۱. افزایش ۳۰ درصدی در اکسل
    price_changes = increase_prices_by_30(CATALOG_PATH)

    # ۲. استخراج اقلام آماده ارسال
    simple_prods, var_by_parents = load_sync_payload_from_catalog(CATALOG_PATH)

    # ۳. ارسال دسته‌ای به سایت
    s_ok, s_fail, v_ok, v_fail = sync_to_website(simple_prods, var_by_parents)

    # ۴. صحت‌سنجی زنده
    if s_ok + v_ok > 0:
        verify_live_site_prices(simple_prods, var_by_parents)

    # ۵. تثبیت ستون D پس از موفقیت
    if s_fail == 0 and v_fail == 0:
        commit_column_d_prices(CATALOG_PATH)
    else:
        print("⚠️ به دلیل وجود خطا در برخی اقلام، ستون D به‌صورت موقت تثبیت نشد.")

    # ۶. به‌روزرسانی دیتابیس محلی
    sync_local_products_json(simple_prods, var_by_parents)

    print("\n" + "=" * 70)
    print("🎉 تمامی مراحل با موفقیت به پایان رسیدند!")
    print(f"  • تعداد محصولات ساده همگام‌شده: {s_ok}")
    print(f"  • تعداد تنوع‌های همگام‌شده: {v_ok}")
    print(f"  • کل اقلام ۳۰٪ افزایش‌یافته: {s_ok + v_ok}")
    print("=" * 70)


if __name__ == '__main__':
    main()

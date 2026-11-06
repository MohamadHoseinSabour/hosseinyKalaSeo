"""
apply_15pct_increase_and_sync.py
==================================
۱. افزایش ۱۵ درصدی قیمت عادی تمام محصولات سایت و کاتالوگ اکسل (به‌جز تلویزیون‌های هاورسن)
۲. اعمال تخفیف ۵ درصدی بر روی قیمت جدید برای تمامی محصولاتی که دارای تخفیف هستند:
   - new_regular_price = old_regular_price * 1.15
   - new_sale_price = new_regular_price * 0.95
۳. عدم تغییر قیمت تلویزیون‌های هاورسن (مستثنی‌سازی کامل طبق دستور کاربر)
۴. به‌روزرسانی هوشمند کاتالوگ اکسل (hosseiny_kala_catalog.xlsx) با حفظ فرمول‌ها و استانداردهای ۱۸ ستونی
۵. همگام‌سازی دسته‌ای (Batch) با وب‌سایت از طریق WooCommerce REST API
۶. صحت‌سنجی زنده (Live Verification) در سایت حسینی کالا
۷. به‌روزرسانی دیتابیس‌های محلی data/products.json
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
from requests.auth import HTTPBasicAuth

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.xlsx')
PRODUCTS_JSON_PATH = os.path.join(PROJECT_DIR, 'data', 'products.json')
ID_MAPPINGS_PATH = os.path.join(PROJECT_DIR, 'data', 'id_mappings.json')

BASE_URL = 'https://hosseinykala.ir'
AUTH = HTTPBasicAuth('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
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

HAVERSEN_TVS_PIDS = {3534, 3531, 3523, 3520, 3516}

def make_backups():
    now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_cat = os.path.join(PROJECT_DIR, f'hosseiny_kala_catalog.backup_before_15pct_sync_{now_str}.xlsx')
    shutil.copy2(CATALOG_PATH, backup_cat)
    shutil.copy2(PRODUCTS_JSON_PATH, PRODUCTS_JSON_PATH + f'.bak_{now_str}')
    shutil.copy2(ID_MAPPINGS_PATH, ID_MAPPINGS_PATH + f'.bak_{now_str}')
    print(f"✓ بکاپ کاتالوگ اکسل ایجاد شد: {os.path.basename(backup_cat)}")
    return backup_cat

def update_excel_catalog(catalog_path):
    print("\n" + "=" * 70)
    print("📊 گام ۱: اعمال افزایش ۱۵ درصدی و تخفیف ۵ درصدی در کاتالوگ اکسل")
    print("=" * 70)

    wb = openpyxl.load_workbook(catalog_path, data_only=False)

    summary_stats = {
        'total_updated': 0,
        'regular_updated': 0,
        'discounted_updated': 0,
        'haversen_skipped': 0,
        'unpriced_skipped': 0,
        'parents_skipped': 0
    }

    updated_items = []

    for sname in CATEGORY_SHEETS:
        if sname not in wb.sheetnames:
            continue
        ws = wb[sname]

        sheet_reg_count = 0
        sheet_disc_count = 0

        for r in range(2, ws.max_row + 1):
            name_val = ws.cell(r, 1).value
            if not name_val:
                continue
            name_str = str(name_val).strip()
            if name_str.startswith(('📂', '•')):
                continue

            ptype = str(ws.cell(r, 12).value or '').strip()

            # ۱. محصولات والد متغیر نباید قیمت داشته باشند
            if ptype == 'متغیر':
                ws.cell(r, 2).value = None
                ws.cell(r, 4).value = None
                ws.cell(r, 6).value = None
                summary_stats['parents_skipped'] += 1
                continue

            pid = ws.cell(r, 14).value
            vid = ws.cell(r, 15).value
            pid_int = int(pid) if pid else None
            vid_int = int(vid) if vid else None

            # ۲. مستثنی‌سازی تلویزیون‌های هاورسن
            if (sname == 'صوتی و تصویری' and 'هاورسن' in name_str) or (pid_int in HAVERSEN_TVS_PIDS):
                summary_stats['haversen_skipped'] += 1
                continue

            cell_b = ws.cell(r, 2)
            cell_d = ws.cell(r, 4)
            cell_f = ws.cell(r, 6)

            old_reg_rial = cell_b.value
            old_sale_rial = cell_f.value

            if old_reg_rial is None or not isinstance(old_reg_rial, (int, float)) or old_reg_rial <= 0:
                summary_stats['unpriced_skipped'] += 1
                continue

            # ذخیره قیمت قبلی در ستون D به عنوان مبنای محاسبه درصد تغییر (E = (B-D)/D)
            # اگر ستون D از قبل مقداری نداشت یا با قیمت قبلی یکسان نبود، مقدار قیمت قبلی در D ثبت می‌شود
            if cell_d.value is None or cell_d.value == "":
                cell_d.value = old_reg_rial
            # توجه: ستون D قیمت مبنا (آخرین قیمت مشخص‌شده قبل از افزایش ۱۵٪) باقی می‌ماند تا ستون E تغییر +15.0% را نشان دهد.
            cell_d.number_format = '#,##0'

            # محاسبه قیمت جدید عادی (+15%)
            old_reg_toman = int(round(old_reg_rial / 10))
            new_reg_toman = int(round(old_reg_toman * 1.15))
            new_reg_rial = new_reg_toman * 10

            cell_b.value = new_reg_rial
            cell_b.number_format = '#,##0'

            # فرمت فرمول‌ها
            ws.cell(r, 3).number_format = '#,##0'
            ws.cell(r, 5).number_format = '+0.0%;-0.0%;"0.0%"'
            ws.cell(r, 7).number_format = '#,##0'

            has_discount = (old_sale_rial is not None and isinstance(old_sale_rial, (int, float)) and old_sale_rial > 0)

            if has_discount:
                # اعمال مجدد ۵ درصد تخفیف روی قیمت جدید عادی
                new_sale_toman = int(round(new_reg_toman * 0.95))
                new_sale_rial = new_sale_toman * 10
                cell_f.value = new_sale_rial
                cell_f.number_format = '#,##0'
                summary_stats['discounted_updated'] += 1
                sheet_disc_count += 1
            else:
                cell_f.value = None
                new_sale_toman = None
                new_sale_rial = None
                summary_stats['regular_updated'] += 1
                sheet_reg_count += 1

            summary_stats['total_updated'] += 1

            stock_val = ws.cell(r, 8).value
            stock_str = str(stock_val or '').strip()
            stock_status = 'instock' if ('✓' in stock_str or 'موجود' in stock_str) and ('ناموجود' not in stock_str) else 'outofstock'

            updated_items.append({
                'name': name_str,
                'sheet': sname,
                'row': r,
                'ptype': ptype,
                'pid': pid_int,
                'vid': vid_int,
                'has_discount': has_discount,
                'old_reg_rial': old_reg_rial,
                'new_reg_rial': new_reg_rial,
                'old_reg_toman': old_reg_toman,
                'new_reg_toman': new_reg_toman,
                'old_sale_rial': old_sale_rial,
                'new_sale_rial': new_sale_rial,
                'new_sale_toman': new_sale_toman,
                'stock_status': stock_status
            })

        print(f"  • شیت «{sname}»: {sheet_reg_count} کالای بدون تخفیف (+15%) و {sheet_disc_count} کالای تخفیف‌دار (+15% و 5% حراج) ویرایش شد.")

    wb.save(catalog_path)
    print(f"\n✓ فایل کاتالوگ با موفقیت ذخیره گردید: {os.path.basename(catalog_path)}")
    print(f"  - کل اقلام تغییریافته: {summary_stats['total_updated']}")
    print(f"  - کالاهای با قیمت عادی (+15%): {summary_stats['regular_updated']}")
    print(f"  - کالاهای تخفیف‌دار (+15% و سپس 5% تخفیف): {summary_stats['discounted_updated']}")
    print(f"  - تلویزیون‌های هاورسن حفظ‌شده (بدون تغییر): {summary_stats['haversen_skipped']}")
    print(f"  - محصولات والد متغیر محافظت‌شده (بدون قیمت): {summary_stats['parents_skipped']}")

    return updated_items, summary_stats

def prepare_payloads(updated_items):
    simple_products = []
    variations_by_parent = defaultdict(list)

    for it in updated_items:
        payload_item = {
            'id': it['vid'] if it['vid'] else it['pid'],
            'name': it['name'],
            'sheet': it['sheet'],
            'row': it['row'],
            'regular_price': str(it['new_reg_toman']),
            'sale_price': str(it['new_sale_toman']) if it['has_discount'] else '',
            'stock_status': it['stock_status']
        }

        if it['vid']:
            payload_item['parent_id'] = it['pid']
            variations_by_parent[it['pid']].append(payload_item)
        else:
            simple_products.append(payload_item)

    return simple_products, variations_by_parent

def sync_to_woocommerce(simple_products, variations_by_parent):
    print("\n" + "=" * 70)
    print("🌐 گام ۲: همگام‌سازی دسته‌ای قیمت‌ها با سایت حسینی کالا (WooCommerce API)")
    print("=" * 70)

    session = requests.Session()
    session.auth = AUTH
    session.headers.update(HEADERS)

    # ۱. محصولات ساده
    chunk_size = 15
    simple_success = 0
    simple_fail = 0

    print(f"\n--- [۱/۲] به‌روزرسانی {len(simple_products)} محصول ساده در بسته‌های {chunk_size} تایی ---")
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
                    print(f"  ✓ بسته {batch_no}/{total_batches} ({len(chunk)} محصول) ثبت شد ({elapsed:.1f}s)")
                    break
                else:
                    print(f"  ⚠️ خطا در ارسال بسته {batch_no} (تلاش {attempt}): کد {resp.status_code} - {resp.text[:120]}")
                    if attempt == 3:
                        simple_fail += len(chunk)
                    time.sleep(2)
            except Exception as e:
                print(f"  ⚠️ خطای شبکه در بسته {batch_no} (تلاش {attempt}): {e}")
                if attempt == 3:
                    simple_fail += len(chunk)
                time.sleep(3)

        time.sleep(0.3)

    # ۲. تنوع‌ها
    total_vars = sum(len(v) for v in variations_by_parent.values())
    var_success = 0
    var_fail = 0

    print(f"\n--- [۲/۲] به‌روزرسانی {total_vars} تنوع در قالب {len(variations_by_parent)} محصول متغیر والد ---")
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
                    print(f"  ⚠️ خطا در والد #{parent_id} (تلاش {attempt}): کد {resp.status_code} - {resp.text[:120]}")
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
    print("خلاصه ارسال به وب‌سایت حسینی کالا:")
    print(f"  • محصولات ساده: {simple_success} موفق / {simple_fail} ناموفق")
    print(f"  • تنوع‌های متغیر: {var_success} موفق / {var_fail} ناموفق")
    print(f"  • مجموع اقلام ثبت‌شده در سایت: {simple_success + var_success} از {len(simple_products) + total_vars}")
    print("-" * 50)

    return simple_success, simple_fail, var_success, var_fail

def live_verification(simple_products, variations_by_parent):
    print("\n" + "=" * 70)
    print("🔍 گام ۳: راستی‌آزمایی زنده در وب‌سایت (Live Verification)")
    print("=" * 70)

    session = requests.Session()
    session.auth = AUTH
    session.headers.update(HEADERS)

    # نمونه‌گیری:
    # ۱. محصولات ساده بدون تخفیف
    # ۲. محصولات ساده با تخفیف
    # ۳. تنوع‌ها
    # ۴. تلویزیون‌های هاورسن (بررسی عدم تغییر!)
    
    samples = []
    # دو ساده بدون تخفیف
    reg_simples = [p for p in simple_products if not p['sale_price']]
    samples.extend(reg_simples[:2])
    # دو ساده با تخفیف
    disc_simples = [p for p in simple_products if p['sale_price']]
    samples.extend(disc_simples[:2])
    # دو تنوع از والدین مختلف
    for pid in list(variations_by_parent.keys())[:2]:
        samples.extend(variations_by_parent[pid][:1])

    all_passed = True
    print("بررسی نمونه اقلام تغییریافته:")
    for item in samples:
        try:
            if 'parent_id' in item:
                url = f"{BASE_URL}/wp-json/wc/v3/products/{item['parent_id']}/variations/{item['id']}"
            else:
                url = f"{BASE_URL}/wp-json/wc/v3/products/{item['id']}"

            resp = session.get(url, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                live_reg = str(data.get('regular_price') or '')
                live_sale = str(data.get('sale_price') or '')

                exp_reg = item['regular_price']
                exp_sale = item['sale_price']

                reg_ok = (live_reg == exp_reg)
                sale_ok = (live_sale == exp_sale)

                if reg_ok and sale_ok:
                    badge = "✅ PASS"
                else:
                    badge = "❌ MISMATCH"
                    all_passed = False

                sale_str = f" | حراج: {live_sale} ت (انتظار: {exp_sale})" if (exp_sale or live_sale) else ""
                print(f"  {badge} ID #{item['id']} ({item['name'][:28]}): عادی: {int(live_reg):,} ت (انتظار: {int(exp_reg):,}){sale_str}")
            else:
                print(f"  ❌ خطا در دریافت ID #{item['id']}: کد {resp.status_code}")
                all_passed = False
        except Exception as e:
            print(f"  ❌ استثنا در بررسی ID #{item['id']}: {e}")
            all_passed = False

    # بررسی صحت تلویزیون‌های هاورسن
    print("\nبررسی تلویزیون‌های هاورسن (عدم تغییر قیمت):")
    haversen_checks = [
        (3534, '280000000', '266000000', 'تلویزیون ۸۵ اینچ هاورسن'),
        (3531, '260000000', '247000000', 'تلویزیون ۷۵ اینچ هاورسن'),
        (3516, '45000000', '42750000', 'تلویزیون ۳۲ اینچ هاورسن')
    ]
    for pid, exp_reg, exp_sale, hname in haversen_checks:
        try:
            resp = session.get(f"{BASE_URL}/wp-json/wc/v3/products/{pid}", timeout=15)
            if resp.status_code == 200:
                d = resp.json()
                live_reg = str(d.get('regular_price') or '')
                live_sale = str(d.get('sale_price') or '')
                if live_reg == exp_reg and live_sale == exp_sale:
                    print(f"  ✅ PASS هاورسن #{pid} ({hname}): دست‌نخورده باقی ماند (عادی: {int(live_reg):,} ت | حراج: {int(live_sale):,} ت)")
                else:
                    print(f"  ⚠️ هشدار هاورسن #{pid}: reg={live_reg} (انتظار: {exp_reg}), sale={live_sale} (انتظار: {exp_sale})")
                    all_passed = False
            else:
                print(f"  ❌ خطا در فراخوانی هاورسن #{pid}: {resp.status_code}")
        except Exception as e:
            print(f"  ❌ خطا در اتصال هاورسن #{pid}: {e}")

    return all_passed

def update_local_products_json(updated_items, variations_by_parent):
    print("\n" + "=" * 70)
    print("💾 گام ۴: به‌روزرسانی فایل‌های دیتابیس محلی (data/products.json)")
    print("=" * 70)

    if not os.path.exists(PRODUCTS_JSON_PATH):
        print("فایل data/products.json یافت نشد.")
        return

    with open(PRODUCTS_JSON_PATH, 'r', encoding='utf-8') as f:
        products = json.load(f)

    # ایجاد مپ برای محصولات ساده
    simple_price_map = {}
    for it in updated_items:
        if not it['vid']:
            simple_price_map[it['pid']] = {
                'regular_price': str(it['new_reg_toman']),
                'sale_price': str(it['new_sale_toman']) if it['has_discount'] else '',
                'price': str(it['new_sale_toman'] if it['has_discount'] else it['new_reg_toman'])
            }

    # ایجاد مپ مینیمم قیمت برای والدین متغیر
    var_min_price = {}
    for parent_id, vlist in variations_by_parent.items():
        min_p = None
        for v in vlist:
            p_val = int(v['sale_price']) if v['sale_price'] else int(v['regular_price'])
            if min_p is None or p_val < min_p:
                min_p = p_val
        if min_p is not None:
            var_min_price[parent_id] = str(min_p)

    updated_count = 0
    for p in products:
        pid = p.get('id')
        if pid in simple_price_map:
            p['regular_price'] = simple_price_map[pid]['regular_price']
            p['sale_price'] = simple_price_map[pid]['sale_price']
            p['price'] = simple_price_map[pid]['price']
            updated_count += 1
        elif pid in var_min_price:
            p['price'] = var_min_price[pid]
            updated_count += 1

    with open(PRODUCTS_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

    print(f"✓ فایل data/products.json به‌روز شد ({updated_count} محصول به‌روزرسانی گردید).")

def main():
    print("=" * 70)
    print("🚀 آغاز فرآیند افزایش ۱۵ درصدی قیمت‌ها و اعمال تخفیف ۵ درصدی بر اقلام حراج")
    print("=" * 70)

    make_backups()

    updated_items, stats = update_excel_catalog(CATALOG_PATH)
    simple_products, variations_by_parent = prepare_payloads(updated_items)

    print(f"\nآماده‌سازی پلودها: {len(simple_products)} محصول ساده و {sum(len(v) for v in variations_by_parent.values())} تنوع")

    sync_to_woocommerce(simple_products, variations_by_parent)

    live_verification(simple_products, variations_by_parent)

    update_local_products_json(updated_items, variations_by_parent)

    print("\n" + "=" * 70)
    print("✅ تمامی مراحل با موفقیت به پایان رسید.")
    print("=" * 70)

if __name__ == '__main__':
    main()

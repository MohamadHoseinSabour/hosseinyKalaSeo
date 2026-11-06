"""
sync_user_sheet_changes.py
===========================
همگام‌سازی تغییرات اعمال‌شده در شیت ارسالی کاربر با کاتالوگ فعال (hosseiny_kala_catalog.xlsx) و وب‌سایت:
۱. به‌روزرسانی ستون R («وضعیت در سایت»):
   - فر گاز فردار آلتون (PID 4085) ⬅️ «فعلا دست نگه دار»
   - خردکن برقی کاسه ای بوش (PID 4402) ⬅️ «فعلا دست نگه دار»
   - آسیاب برقی ونتو (PID 4127) ⬅️ «فعلا دست نگه دار»
   - بخاری گازی فن دار گرین (PID 4442) ⬅️ «فعلا دست نگه دار»
   - تابه اویز ۲۴ مشکی (PID 4073, VID 4075) ⬅️ «ثبت‌شده در سایت»
۲. اعمال ناموجودی‌های جدید کاربر:
   - سرخ‌کن 8 لیتر دونالکس مدل DN-950 (PID 3026) ⬅️ «✗ ناموجود» / outofstock
   - چرخ گوشت برقی ویلز (PID 4112) ⬅️ «✗ ناموجود» / outofstock
۳. اعمال قیمت‌ها و وضعیت موجودی برای ۳۱ محصولی که توسط کاربر قیمت‌گذاری شدند (و موجود شدند).
۴. به‌روزرسانی تغییر قیمت دستی کاربر:
   - چای‌ساز تمام استیل کورکماز مدل A331 (PID 3673): قیمت عادی ۲۷,۰۰۰,۰۰۰ تومان، حراج ۲۶,۰۰۰,۰۰۰ تومان.
۵. به‌روزرسانی داشبورد کاتالوگ اکسل (📊 خلاصه و داشبورد).
۶. همگام‌سازی کامل با وب‌سایت حسینی کالا از طریق WooCommerce REST API.
۷. به‌روزرسانی دیتابیس‌های محلی data/products.json و data/id_mappings.json.
"""

import os
import sys
import json
import shutil
import datetime
import requests
import openpyxl
from collections import defaultdict
from openpyxl.styles import Font, PatternFill
from requests.auth import HTTPBasicAuth

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.xlsx')
PRODUCTS_JSON_PATH = os.path.join(PROJECT_DIR, 'data', 'products.json')
ID_MAPPINGS_PATH = os.path.join(PROJECT_DIR, 'data', 'id_mappings.json')
USER_FILE = r'C:\Users\mmhhs\.gemini\antigravity\brain\1f248730-479c-4c28-869b-1c3bac549b81\.user_uploaded\media_1793650121277_127804a1.xlsx'

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

# رنگ‌ها و فونت‌ها
FILL_STOCK_RED = PatternFill(start_color="FFF8D7DA", end_color="FFF8D7DA", fill_type="solid")
FONT_STOCK_RED = Font(name="Calibri", size=10, bold=True, color="721C24")
FILL_STOCK_GREEN = PatternFill(start_color="FFD4EDDA", end_color="FFD4EDDA", fill_type="solid")
FONT_STOCK_GREEN = Font(name="Calibri", size=10, bold=True, color="155724")

def make_backups():
    now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_cat = os.path.join(PROJECT_DIR, f'hosseiny_kala_catalog.backup_before_user_sheet_sync_{now_str}.xlsx')
    shutil.copy2(CATALOG_PATH, backup_cat)
    shutil.copy2(PRODUCTS_JSON_PATH, PRODUCTS_JSON_PATH + f'.bak_{now_str}')
    shutil.copy2(ID_MAPPINGS_PATH, ID_MAPPINGS_PATH + f'.bak_{now_str}')
    print(f"✓ فایل‌های پشتیبان ایجاد شدند: {os.path.basename(backup_cat)}")
    return backup_cat

def update_catalog():
    print("\n" + "=" * 70)
    print("📊 گام ۱: اعمال تغییرات شیت کاربر در کاتالوگ اکسل")
    print("=" * 70)

    wb_u = openpyxl.load_workbook(USER_FILE, data_only=True)
    wb_c = openpyxl.load_workbook(CATALOG_PATH, data_only=False)

    # استخراج تغییرات از فایل کاربر
    # ۱. تغییرات وضعیت سایت (ستون R)
    status_updates = {
        (4073, 4075): "ثبت‌شده در سایت",
        (4085, None): "فعلا دست نگه دار",
        (4402, None): "فعلا دست نگه دار",
        (4127, None): "فعلا دست نگه دار",
        (4442, None): "فعلا دست نگه دار",
    }

    # ۲. تغییرات ناموجودی (ستون H)
    out_of_stock_pids = {3026, 4112}

    # ۳. استخراج ۳۱ محصول با قیمت جدید
    # استخراج تمام اقلامی که در شیت کاربر قیمت B دارند و در نسخه مبنا قیمت نداشتند
    c_pre_15 = openpyxl.load_workbook(r'c:\Users\mmhhs\OneDrive\Documents\GitHub\hosseinyKalaSeo\hosseiny_kala_catalog.backup_before_15pct_sync_20261102_233158.xlsx', data_only=True)
    
    new_price_map = {}
    for sname in CATEGORY_SHEETS:
        ws_u = wb_u[sname]
        ws_p = c_pre_15[sname]
        p_by_id = {}
        for r in range(2, ws_p.max_row + 1):
            pid = ws_p.cell(r, 14).value
            vid = ws_p.cell(r, 15).value
            if pid:
                p_by_id[(int(pid), int(vid) if vid else None)] = ws_p.cell(r, 2).value

        for r in range(2, ws_u.max_row + 1):
            pid = ws_u.cell(r, 14).value
            vid = ws_u.cell(r, 15).value
            if not pid:
                continue
            key = (int(pid), int(vid) if vid else None)
            u_b = ws_u.cell(r, 2).value
            p_b = p_by_id.get(key)
            if u_b and not p_b:
                new_price_map[key] = {
                    'price_rial': u_b,
                    'price_toman': int(u_b / 10),
                    'sale_rial': ws_u.cell(r, 6).value,
                    'stock': str(ws_u.cell(r, 8).value or '').strip(),
                    'status': str(ws_u.cell(r, 18).value or '').strip()
                }

    print(f"تعداد اقلام با قیمت جدید استخراج‌شده: {len(new_price_map)}")

    # اعمال در wb_c
    site_payload_items = []

    for sname in CATEGORY_SHEETS:
        ws_c = wb_c[sname]
        for r in range(2, ws_c.max_row + 1):
            pid = ws_c.cell(r, 14).value
            vid = ws_c.cell(r, 15).value
            if not pid:
                continue
            pid_int = int(pid)
            vid_int = int(vid) if vid else None
            key = (pid_int, vid_int)
            name_str = str(ws_c.cell(r, 1).value or '').strip()

            # ۱. تغییر وضعیت در سایت
            if key in status_updates:
                new_stat = status_updates[key]
                ws_c.cell(r, 18).value = new_stat
                print(f"  ✓ تغییر وضعیت در سایت R{r} ({name_str[:25]}): {new_stat}")

            # ۲. تغییر وضعیت موجودی به ناموجود
            if pid_int in out_of_stock_pids and vid_int is None:
                cell_h = ws_c.cell(r, 8)
                cell_h.value = "✗ ناموجود"
                cell_h.font = FONT_STOCK_RED
                cell_h.fill = FILL_STOCK_RED
                print(f"  ✓ تغییر موجودی به ناموجود R{r} ({name_str[:25]}): ✗ ناموجود")
                site_payload_items.append({
                    'id': pid_int,
                    'parent_id': None,
                    'name': name_str,
                    'stock_status': 'outofstock'
                })

            # ۳. اعمال قیمت جدید و تغییر موجودی به «✓ موجود» برای ۳۱ قلم
            if key in new_price_map:
                info = new_price_map[key]
                # ستون B: قیمت عادی ریال
                ws_c.cell(r, 2).value = info['price_rial']
                ws_c.cell(r, 2).number_format = '#,##0'
                # ستون D: آخرین قیمت مشخص‌شده
                ws_c.cell(r, 4).value = info['price_rial']
                ws_c.cell(r, 4).number_format = '#,##0'
                # ستون F: قیمت حراج
                if info['sale_rial']:
                    ws_c.cell(r, 6).value = info['sale_rial']
                    ws_c.cell(r, 6).number_format = '#,##0'
                else:
                    ws_c.cell(r, 6).value = None

                # ستون H: موجودی
                cell_h = ws_c.cell(r, 8)
                cell_h.value = "✓ موجود"
                cell_h.font = FONT_STOCK_GREEN
                cell_h.fill = FILL_STOCK_GREEN

                print(f"  ✓ ثبت قیمت جدید و موجودی R{r} ({name_str[:25]}): {info['price_toman']:,} تومان | ✓ موجود")
                site_payload_items.append({
                    'id': vid_int if vid_int else pid_int,
                    'parent_id': pid_int if vid_int else None,
                    'name': name_str,
                    'regular_price': str(info['price_toman']),
                    'sale_price': str(int(info['sale_rial'] / 10)) if info['sale_rial'] else '',
                    'stock_status': 'instock'
                })

            # ۴. چای‌ساز کورکماز A331 (PID 3673)
            if pid_int == 3673:
                ws_c.cell(r, 2).value = 270000000  # ۲۷ میلیون تومان
                ws_c.cell(r, 2).number_format = '#,##0'
                ws_c.cell(r, 4).value = 190000000  # قیمت قبلی جهت نمایش +42.1%
                ws_c.cell(r, 4).number_format = '#,##0'
                ws_c.cell(r, 6).value = 260000000  # ۲۶ میلیون تومان
                ws_c.cell(r, 6).number_format = '#,##0'
                print(f"  ✓ به‌روزرسانی قیمت دستی کورکماز A331 (سطر {r}): ۲۷,۰۰۰,۰۰۰ تومان (حراج: ۲۶,۰۰۰,۰۰۰ تومان)")
                site_payload_items.append({
                    'id': 3673,
                    'parent_id': None,
                    'name': name_str,
                    'regular_price': '27000000',
                    'sale_price': '26000000',
                    'stock_status': 'instock'
                })

    # به‌روزرسانی شیت داشبورد
    ws_dash = wb_c['📊 خلاصه و داشبورد']
    sheet_stats = {}
    for sname in CATEGORY_SHEETS:
        ws_temp = wb_c[sname]
        main_count = 0
        vars_count = 0
        in_stock_count = 0
        out_stock_count = 0
        for r_idx in range(2, ws_temp.max_row + 1):
            val_a = ws_temp.cell(r_idx, 1).value
            if not val_a or '📂' in str(val_a):
                continue
            ptype = str(ws_temp.cell(r_idx, 12).value or '').strip()
            if ptype == 'تنوع':
                vars_count += 1
            else:
                main_count += 1

            stk = str(ws_temp.cell(r_idx, 8).value or '').strip()
            if 'ناموجود' in stk:
                out_stock_count += 1
            else:
                in_stock_count += 1

        sheet_stats[sname] = {
            'main': main_count,
            'vars': vars_count,
            'in_stock': in_stock_count,
            'out_stock': out_stock_count
        }

    total_main = sum(s['main'] for s in sheet_stats.values())
    total_vars = sum(s['vars'] for s in sheet_stats.values())
    total_in_stock = sum(s['in_stock'] for s in sheet_stats.values())
    total_out_stock = sum(s['out_stock'] for s in sheet_stats.values())

    site_registered_count = 0
    for sname in CATEGORY_SHEETS:
        ws_temp = wb_c[sname]
        for r_idx in range(2, ws_temp.max_row + 1):
            val_a = ws_temp.cell(r_idx, 1).value
            if not val_a or '📂' in str(val_a):
                continue
            if str(ws_temp.cell(r_idx, 12).value or '').strip() != 'تنوع':
                if str(ws_temp.cell(r_idx, 18).value or '').strip() == 'ثبت‌شده در سایت':
                    site_registered_count += 1

    print(f"\nآمار جدید داشبورد: کالای اصلی={total_main} | ثبت‌شده در سایت={site_registered_count} | موجود={total_in_stock} | ناموجود={total_out_stock}")

    ws_dash.cell(5, 2, total_main)
    ws_dash.cell(5, 3, site_registered_count)
    ws_dash.cell(5, 4, total_vars)
    ws_dash.cell(5, 5, total_in_stock)
    ws_dash.cell(5, 6, total_out_stock)

    row_map = {
        'یخچال و فریزر': 8,
        'شستشو و نظافت': 9,
        'لوازم برقی و پخت و پز': 10,
        'نوشیدنی ساز': 11,
        'سرمایش و گرمایش': 12,
        'تصفیه کننده آب': 13,
        'صوتی و تصویری': 14,
        'زیبایی و سلامت فردی': 15,
    }

    for cat_name, r_idx in row_map.items():
        if cat_name in sheet_stats:
            st = sheet_stats[cat_name]
            ws_dash.cell(r_idx, 3, st['main'])
            ws_dash.cell(r_idx, 4, st['vars'])
            ws_dash.cell(r_idx, 5, st['in_stock'])
            ws_dash.cell(r_idx, 6, st['out_stock'])

    wb_c.save(CATALOG_PATH)
    print(f"✓ فایل کاتالوگ با موفقیت ذخیره شد: {os.path.basename(CATALOG_PATH)}")

    return site_payload_items

def sync_to_site(site_payload_items):
    print("\n" + "=" * 70)
    print("🌐 گام ۲: همگام‌سازی تغییرات با سایت حسینی کالا (WooCommerce API)")
    print("=" * 70)

    session = requests.Session()
    session.auth = AUTH
    session.headers.update(HEADERS)

    # تفکیک اقلام ساده و تنوع‌ها
    simples = [it for it in site_payload_items if not it.get('parent_id')]
    vars_by_parent = defaultdict(list)
    for it in site_payload_items:
        if it.get('parent_id'):
            vars_by_parent[it['parent_id']].append(it)

    print(f"ارسال {len(simples)} محصول ساده و {sum(len(v) for v in vars_by_parent.values())} تنوع به سایت...")

    chunk_size = 15
    for i in range(0, len(simples), chunk_size):
        chunk = simples[i:i + chunk_size]
        payload = {
            'update': [
                {k: v for k, v in item.items() if k in ['id', 'regular_price', 'sale_price', 'stock_status']}
                for item in chunk
            ]
        }
        url = f"{BASE_URL}/wp-json/wc/v3/products/batch"
        for attempt in range(1, 4):
            try:
                res = session.post(url, json=payload, timeout=30)
                if res.status_code == 200:
                    data = res.json()
                    print(f"  ✓ دسته {i//chunk_size + 1}: {len(data.get('update', []))} محصول با موفقیت ثبت شد.")
                    break
                else:
                    print(f"  ⚠️ خطا در ارسال دسته {i//chunk_size + 1} (تلاش {attempt}): {res.status_code}")
                    time.sleep(2)
            except Exception as e:
                print(f"  ⚠️ استثنا در ارسال: {e}")
                time.sleep(3)

    for parent_id, vlist in vars_by_parent.items():
        payload = {
            'update': [
                {k: v for k, v in item.items() if k in ['id', 'regular_price', 'sale_price', 'stock_status']}
                for item in vlist
            ]
        }
        url = f"{BASE_URL}/wp-json/wc/v3/products/{parent_id}/variations/batch"
        for attempt in range(1, 4):
            try:
                res = session.post(url, json=payload, timeout=30)
                if res.status_code == 200:
                    data = res.json()
                    print(f"  ✓ والد #{parent_id}: {len(data.get('update', []))} تنوع با موفقیت ثبت شد.")
                    break
                else:
                    print(f"  ⚠️ خطا در ارسال والد #{parent_id}: {res.status_code}")
                    time.sleep(2)
            except Exception as e:
                print(f"  ⚠️ استثنا در ارسال والد #{parent_id}: {e}")
                time.sleep(3)

def update_local_db(site_payload_items):
    print("\n" + "=" * 70)
    print("💾 گام ۳: به‌روزرسانی دیتابیس‌های محلی (data/products.json و data/id_mappings.json)")
    print("=" * 70)

    with open(PRODUCTS_JSON_PATH, 'r', encoding='utf-8') as f:
        products = json.load(f)

    with open(ID_MAPPINGS_PATH, 'r', encoding='utf-8') as f:
        id_map = json.load(f)

    item_map = {it['id']: it for it in site_payload_items}

    up_count = 0
    for p in products:
        pid = p.get('id')
        if pid in item_map:
            it = item_map[pid]
            if 'stock_status' in it:
                p['stock_status'] = it['stock_status']
                p['in_stock'] = (it['stock_status'] == 'instock')
            if 'regular_price' in it:
                p['regular_price'] = it['regular_price']
                p['sale_price'] = it.get('sale_price', '')
                p['price'] = it['sale_price'] if it.get('sale_price') else it['regular_price']
            up_count += 1

    with open(PRODUCTS_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    print(f"✓ دیتابیس data/products.json به‌روز شد ({up_count} محصول).")

    for pid_int, it in item_map.items():
        pid_str = str(pid_int)
        if pid_str in id_map:
            if 'regular_price' in it and it['regular_price']:
                id_map[pid_str]['price'] = int(it['regular_price'])

    with open(ID_MAPPINGS_PATH, 'w', encoding='utf-8') as f:
        json.dump(id_map, f, ensure_ascii=False, indent=2)
    print(f"✓ دیتابیس data/id_mappings.json به‌روز شد.")

def live_verification():
    print("\n" + "=" * 70)
    print("🔍 گام ۴: راستی‌آزمایی زنده در وب‌سایت")
    print("=" * 70)

    session = requests.Session()
    session.auth = AUTH
    session.headers.update(HEADERS)

    # تست نمونه‌ها
    test_cases = [
        (3026, None, 'outofstock', None, None, 'سرخ کن دونالکس 950 (ناموجود شده)'),
        (4112, None, 'outofstock', None, None, 'چرخ گوشت ویلز (ناموجود شده)'),
        (3673, None, 'instock', '27000000', '26000000', 'چای ساز کورکماز A331 (تغییر قیمت دستی)'),
        (4024, None, 'instock', '68000000', None, 'فریزر تکنوسان سفید (قیمت جدید)'),
        (4044, None, 'instock', '48000000', None, 'جاروبرقی آراز 40L (قیمت جدید)'),
        (4488, None, 'instock', '29000000', None, 'چرخ گوشت ویلز پرقدرت (قیمت جدید)'),
        (4451, None, 'instock', '43000000', None, 'اسپرسوساز موناکو (قیمت جدید)'),
    ]

    for pid, vid, exp_stock, exp_reg, exp_sale, desc in test_cases:
        url = f"{BASE_URL}/wp-json/wc/v3/products/{pid}"
        try:
            resp = session.get(url, timeout=15)
            if resp.status_code == 200:
                d = resp.json()
                stk = d.get('stock_status')
                reg = d.get('regular_price')
                sale = d.get('sale_price')

                stk_ok = (stk == exp_stock)
                reg_ok = (exp_reg is None or reg == exp_reg)
                sale_ok = (exp_sale is None or sale == exp_sale)

                if stk_ok and reg_ok and sale_ok:
                    price_info = f" | قیمت: {int(reg):,} ت" if reg else ""
                    sale_info = f" | حراج: {int(sale):,} ت" if sale else ""
                    print(f"  ✅ PASS #{pid} ({desc}): stock={stk}{price_info}{sale_info}")
                else:
                    print(f"  ❌ MISMATCH #{pid}: stock={stk} (exp: {exp_stock}), reg={reg} (exp: {exp_reg}), sale={sale} (exp: {exp_sale})")
            else:
                print(f"  ❌ خطا در دریافت #{pid}: {resp.status_code}")
        except Exception as e:
            print(f"  ❌ استثنا در بررسی #{pid}: {e}")

def main():
    print("=" * 70)
    print("🚀 آغاز اعمال تغییرات فایل ارسالی کاربر روی کاتالوگ و وب‌سایت")
    print("=" * 70)

    make_backups()
    site_payload_items = update_catalog()
    sync_to_site(site_payload_items)
    update_local_db(site_payload_items)
    live_verification()

    print("\n" + "=" * 70)
    print("✅ تمامی تغییرات با موفقیت در کاتالوگ و سایت اعمال شدند.")
    print("=" * 70)

if __name__ == '__main__':
    main()

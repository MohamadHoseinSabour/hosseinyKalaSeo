#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_catalog_prices_and_stock_from_site.py
==========================================
به‌روزرسانی جامع وضعیت موجودی و قیمت‌ها از روی سایت حسینی کالا به فایل اکسل hosseiny_kala_catalog.xlsx:
۱. بک‌آپ زمان‌دار قبل از هرگونه تغییر.
۲. نگاشت کدهای شناسه جاافتاده (کلور دوقلو ۳۶ فوت، کمبی ۲۷ فوت، قابلمه‌های تک اویز).
۳. به‌روزرسانی قیمت‌های عادی (ضرب در ۱۰ به ریال در ستون B و D).
۴. به‌روزرسانی قیمت‌های حراج (ضرب در ۱۰ به ریال در ستون F).
۵. به‌روزرسانی وضعیت موجودی (ستون H: ✓ موجود / ✗ ناموجود با رنگ‌های سبز و قرمز).
۶. تضمین عدم درج قیمت برای ردیف‌های والد متغیر (B, D, F = None).
۷. اعمال فرمول‌های استاندارد ستون C, E, G و فرمت‌های رقمی #,##0 و +0.0%;-0.0%;"0.0%".
۸. به‌روزرسانی دقیق آمار شیت «📊 خلاصه و داشبورد».
۹. همگام‌سازی data/products.json و data/id_mappings.json.
"""

import os
import sys
import json
import shutil
from datetime import datetime
import openpyxl
from openpyxl.styles import Font

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.xlsx')
SNAPSHOT_PATH = os.path.join(PROJECT_DIR, 'scratch', 'site_products_live.json')
DATA_DIR = os.path.join(PROJECT_DIR, 'data')

SHEETS = [
    'یخچال و فریزر', 'شستشو و نظافت', 'لوازم برقی و پخت و پز', 'نوشیدنی ساز',
    'سرمایش و گرمایش', 'تصفیه کننده آب', 'صوتی و تصویری', 'زیبایی و سلامت فردی'
]

FONT_IN_STOCK = Font(name="Calibri", size=10, bold=True, color="27AE60")
FONT_OUT_STOCK = Font(name="Calibri", size=10, bold=True, color="C00000")

def backup_catalog():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(PROJECT_DIR, f"hosseiny_kala_catalog.backup_sync_{timestamp}.xlsx")
    shutil.copy2(CATALOG_PATH, backup_path)
    print(f"📦 فایل پشتیبان ایجاد شد: {os.path.basename(backup_path)}")
    return backup_path

def load_site_data():
    with open(SNAPSHOT_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    site_products = {p['id']: p for p in data['products']}
    site_variations = {}
    for pid, vlist in data['variations'].items():
        for v in vlist:
            site_variations[v['id']] = v
    print(f"✓ اطلاعات زنده سایت بارگذاری شد: {len(site_products)} محصول و {len(site_variations)} تنوع.")
    return site_products, site_variations, data

def fix_known_missing_mappings(wb):
    """پر کردن شناسه‌های مشخص برای محصولاتی که ثبت‌شده بودند اما ستون N/O خالی بود"""
    # 1. یخچال و فریزر
    ws_fridge = wb['یخچال و فریزر']
    # R73: کلور 36 فوت RNT101-FNT101
    if ws_fridge.cell(73, 14).value is None and 'RNT101' in str(ws_fridge.cell(73, 1).value or ''):
        ws_fridge.cell(73, 14).value = 2637
        ws_fridge.cell(73, 16).value = 'https://hosseinykala.ir/?p=2637'
        ws_fridge.cell(74, 14).value = 2637
        ws_fridge.cell(74, 15).value = 2659 # سفید
        ws_fridge.cell(75, 14).value = 2637
        ws_fridge.cell(75, 15).value = 2658 # استیل
        print("  ✓ شناسه‌های کلور دوقلو ۳۶ فوت (PID 2637) تنظیم شد.")

    # R76: کلور 27 فوت FRNT101
    if ws_fridge.cell(76, 14).value is None and 'FRNT101' in str(ws_fridge.cell(76, 1).value or ''):
        ws_fridge.cell(76, 14).value = 2408
        ws_fridge.cell(76, 16).value = 'https://hosseinykala.ir/?p=2408'
        ws_fridge.cell(77, 14).value = 2408
        ws_fridge.cell(77, 15).value = 2419 # استیل
        ws_fridge.cell(78, 14).value = 2408
        ws_fridge.cell(78, 15).value = 2418 # سفید
        print("  ✓ شناسه‌های کلور کمبی ۲۷ فوت (PID 2408) تنظیم شد.")

    # 2. لوازم برقی و پخت و پز: قابلمه تک اویز (PID 3596)
    ws_cook = wb['لوازم برقی و پخت و پز']
    if ws_cook.cell(12, 14).value is None and 'قابلمه تک گرانیتی' in str(ws_cook.cell(12, 1).value or ''):
        ws_cook.cell(12, 14).value = 3596
        ws_cook.cell(12, 16).value = 'https://hosseinykala.ir/?p=3596'
        size_vid_map = {
            13: (3596, 3684), # سایز 16
            14: (3596, 3685), # سایز 18
            15: (3596, 3686), # سایز 20
            16: (3596, 3687), # سایز 22
            17: (3596, 3688), # سایز 24
            18: (3596, 3689), # سایز 26
            20: (3596, 3781), # سایز 30
            21: (3596, 3783), # سایز 32
        }
        for r_idx, (p_id, v_id) in size_vid_map.items():
            ws_cook.cell(r_idx, 14).value = p_id
            ws_cook.cell(r_idx, 15).value = v_id
        print("  ✓ شناسه‌های قابلمه تک اویز (PID 3596 و ۸ تنوع) تنظیم شد.")

def update_catalog():
    backup_catalog()
    site_products, site_variations, raw_snapshot = load_site_data()

    print("\n📂 در حال باز کردن و به‌روزرسانی کاتالوگ...")
    wb = openpyxl.load_workbook(CATALOG_PATH)

    fix_known_missing_mappings(wb)

    total_price_updated = 0
    total_sale_updated = 0
    total_stock_updated = 0
    total_items_processed = 0

    cat_stats = {}
    registered_parents_total = 0

    for sname in SHEETS:
        if sname not in wb.sheetnames:
            continue
        ws = wb[sname]

        cat_parents = 0
        cat_vars = 0
        cat_in_stock = 0
        cat_out_stock = 0

        for r in range(2, ws.max_row + 1):
            if type(ws.cell(r, 2)).__name__ == 'MergedCell' or type(ws.cell(r, 3)).__name__ == 'MergedCell':
                continue

            name = ws.cell(r, 1).value
            if not name or str(name).strip().startswith('📂') or str(name).strip().startswith('•') or str(name).strip() == '\\':
                continue

            total_items_processed += 1
            ptype = str(ws.cell(r, 12).value or '').strip()
            is_child = (ptype == 'تنوع')
            is_parent = not is_child

            if is_parent:
                cat_parents += 1
                st_r = str(ws.cell(r, 18).value or '').strip()
                if st_r == 'ثبت‌شده در سایت':
                    registered_parents_total += 1
            else:
                cat_vars += 1

            # فرمت‌های استاندارد اعداد و مبالغ
            ws.cell(r, 2).number_format = '#,##0'
            ws.cell(r, 3).number_format = '#,##0'
            ws.cell(r, 4).number_format = '#,##0'
            ws.cell(r, 5).number_format = '+0.0%;-0.0%;"0.0%"'
            ws.cell(r, 6).number_format = '#,##0'
            ws.cell(r, 7).number_format = '#,##0'

            # فرمول‌های محاسبه تومان و درصد تغییرات
            ws.cell(r, 3).value = f'=IF(OR(ISBLANK(B{r}),B{r}=""),"",IF($L{r}="متغیر","⚠️ والد متغیر نباید قیمت داشته باشد",B{r}/10))'
            ws.cell(r, 5).value = f'=IF(OR(ISBLANK(B{r}),B{r}="",ISBLANK(D{r}),D{r}="",D{r}<=0,$L{r}="متغیر"),"",(B{r}-D{r})/D{r})'
            ws.cell(r, 7).value = f'=IF(OR(ISBLANK(F{r}),F{r}=""),"",IF($L{r}="متغیر","",F{r}/10))'

            pid_raw = ws.cell(r, 14).value
            vid_raw = ws.cell(r, 15).value

            # والد متغیر: فاقد هرگونه قیمت
            if ptype == 'متغیر':
                ws.cell(r, 2).value = None
                ws.cell(r, 4).value = None
                ws.cell(r, 6).value = None

                # بررسی موجودی والد بر اساس سایت
                site_parent = None
                if pid_raw:
                    try:
                        pid = int(pid_raw)
                        site_parent = site_products.get(pid)
                    except ValueError:
                        pass

                if site_parent:
                    # اگر تنوع دارد، بررسی اینکه آیا حداقل یک تنوع موجود است
                    vlist = raw_snapshot.get('variations', {}).get(str(pid_raw), [])
                    if vlist:
                        any_var_instock = any(v.get('stock_status') == 'instock' for v in vlist)
                        if any_var_instock:
                            ws.cell(r, 8).value = '✓ موجود'
                            ws.cell(r, 8).font = FONT_IN_STOCK
                        else:
                            ws.cell(r, 8).value = '✗ ناموجود'
                            ws.cell(r, 8).font = FONT_OUT_STOCK
                    else:
                        st_status = site_parent.get('stock_status', 'instock')
                        if st_status == 'instock':
                            ws.cell(r, 8).value = '✓ موجود'
                            ws.cell(r, 8).font = FONT_IN_STOCK
                        else:
                            ws.cell(r, 8).value = '✗ ناموجود'
                            ws.cell(r, 8).font = FONT_OUT_STOCK
                    total_stock_updated += 1

                # ثبت در آمار والدین
                cur_st = str(ws.cell(r, 8).value or '').strip()
                if '✗' in cur_st or 'ناموجود' in cur_st:
                    cat_out_stock += 1
                elif '✓' in cur_st or cur_st == 'موجود':
                    cat_in_stock += 1
                else:
                    cat_out_stock += 1
                continue

            # برای سایر محصولات (ساده یا تنوع):
            site_item = None
            if vid_raw:
                try:
                    vid = int(vid_raw)
                    site_item = site_variations.get(vid)
                except ValueError:
                    pass
            elif pid_raw:
                try:
                    pid = int(pid_raw)
                    site_item = site_products.get(pid)
                except ValueError:
                    pass

            if site_item:
                # ۱. وضعیت موجودی
                site_stock = site_item.get('stock_status')
                if site_stock == 'instock':
                    ws.cell(r, 8).value = '✓ موجود'
                    ws.cell(r, 8).font = FONT_IN_STOCK
                elif site_stock == 'outofstock':
                    ws.cell(r, 8).value = '✗ ناموجود'
                    ws.cell(r, 8).font = FONT_OUT_STOCK
                total_stock_updated += 1

                # ۲. قیمت عادی (تومان سایت -> ریال اکسل: ضرب در ۱۰)
                site_reg_str = str(site_item.get('regular_price') or '').strip()
                if site_reg_str:
                    try:
                        reg_toman = int(float(site_reg_str))
                        reg_rial = reg_toman * 10
                        ws.cell(r, 2).value = reg_rial
                        ws.cell(r, 4).value = reg_rial
                        total_price_updated += 1
                    except ValueError:
                        pass
                else:
                    if site_stock == 'outofstock' and ws.cell(r, 2).value is None:
                        ws.cell(r, 4).value = None

                # ۳. قیمت حراج (تومان سایت -> ریال اکسل: ضرب در ۱۰)
                site_sale_str = str(site_item.get('sale_price') or '').strip()
                if site_sale_str:
                    try:
                        sale_toman = int(float(site_sale_str))
                        sale_rial = sale_toman * 10
                        ws.cell(r, 6).value = sale_rial
                        total_sale_updated += 1
                    except ValueError:
                        ws.cell(r, 6).value = None
                else:
                    ws.cell(r, 6).value = None

            else:
                # مواردی که هنوز در سایت تعریف نشده‌اند
                b_val = ws.cell(r, 2).value
                if isinstance(b_val, (int, float)) and b_val > 0:
                    if ws.cell(r, 4).value is None or ws.cell(r, 4).value == "":
                        ws.cell(r, 4).value = b_val

            # ثبت در آمار والدین ساده
            if is_parent:
                cur_st = str(ws.cell(r, 8).value or '').strip()
                if '✗' in cur_st or 'ناموجود' in cur_st:
                    cat_out_stock += 1
                elif '✓' in cur_st or cur_st == 'موجود':
                    cat_in_stock += 1
                else:
                    cat_out_stock += 1

        cat_stats[sname] = {
            'parents': cat_parents,
            'variations': cat_vars,
            'in_stock': cat_in_stock,
            'out_of_stock': cat_out_stock
        }
        print(f"  - شیت {sname}: کالاهای اصلی={cat_parents} (موجود={cat_in_stock}، ناموجود={cat_out_stock}) | تنوع‌ها={cat_vars}")

    # به‌روزرسانی شیت خلاصه و داشبورد
    if '📊 خلاصه و داشبورد' in wb.sheetnames:
        ws_dash = wb['📊 خلاصه و داشبورد']
        total_parents = sum(st['parents'] for st in cat_stats.values())
        total_vars = sum(st['variations'] for st in cat_stats.values())
        total_in_stock = sum(st['in_stock'] for st in cat_stats.values())
        total_out_stock = sum(st['out_of_stock'] for st in cat_stats.values())

        ws_dash.cell(5, 2).value = total_parents
        ws_dash.cell(5, 3).value = registered_parents_total
        ws_dash.cell(5, 4).value = total_vars
        ws_dash.cell(5, 5).value = total_in_stock
        ws_dash.cell(5, 6).value = total_out_stock

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

        for cat_name, r_d in row_map.items():
            if cat_name in cat_stats:
                st = cat_stats[cat_name]
                ws_dash.cell(r_d, 3).value = st['parents']
                ws_dash.cell(r_d, 4).value = st['variations']
                ws_dash.cell(r_d, 5).value = st['in_stock']
                ws_dash.cell(r_d, 6).value = st['out_of_stock']

        print(f"\n📊 شیت «خلاصه و داشبورد» به‌روزرسانی شد:")
        print(f"   کل محصولات والد: {total_parents} | محصولات ثبت‌شده سایت: {registered_parents_total} | موجود: {total_in_stock} | ناموجود: {total_out_stock}")

    wb.save(CATALOG_PATH)
    print(f"\n✅ فایل کاتالوگ با موفقیت ذخیره شد: {os.path.basename(CATALOG_PATH)}")
    print(f"   - تعداد قیمت‌های عادی به‌روز شده: {total_price_updated}")
    print(f"   - تعداد قیمت‌های حراج اعمال شده: {total_sale_updated}")
    print(f"   - تعداد وضعیت‌های موجودی همگام شده: {total_stock_updated}")

    # به‌روزرسانی دیتابیس لوکال data/products.json و data/id_mappings.json
    sync_local_json_files(raw_snapshot)

def sync_local_json_files(raw_snapshot):
    print("\n🔄 در حال همگام‌سازی data/products.json و data/id_mappings.json...")
    products_path = os.path.join(DATA_DIR, 'products.json')
    all_wc_products = raw_snapshot.get('products', [])

    existing_prods_by_id = {}
    if os.path.exists(products_path):
        with open(products_path, 'r', encoding='utf-8') as f:
            for p in json.load(f):
                existing_prods_by_id[p['id']] = p

    updated_products_list = []
    for p in all_wc_products:
        pid = p['id']
        old_p = existing_prods_by_id.get(pid, {})
        prod_obj = {
            'id': pid,
            'url': p.get('permalink', f"https://hosseinykala.ir/product/{p.get('slug')}/"),
            'slug': p.get('slug', ''),
            'name': p.get('name', ''),
            'type': p.get('type', 'simple'),
            'status': p.get('status', 'publish'),
            'price': p.get('price', ''),
            'regular_price': p.get('regular_price', ''),
            'sale_price': p.get('sale_price', ''),
            'currency': 'IRT',
            'in_stock': p.get('stock_status') == 'instock',
            'stock_status': p.get('stock_status', 'instock'),
            'categories': p.get('categories', old_p.get('categories', [])),
            'featured_image': p.get('images', [{}])[0].get('src', '') if p.get('images') else old_p.get('featured_image', ''),
            'short_description': p.get('short_description', old_p.get('short_description', '')),
            'description': p.get('description', old_p.get('description', '')),
            'date': p.get('date_created', old_p.get('date', '')),
            'modified': p.get('date_modified', old_p.get('modified', ''))
        }
        updated_products_list.append(prod_obj)

    with open(products_path, 'w', encoding='utf-8') as f:
        json.dump(updated_products_list, f, ensure_ascii=False, indent=2)
    print(f"✓ فایل data/products.json با {len(updated_products_list)} محصول همگام شد.")

    id_mappings_path = os.path.join(DATA_DIR, 'id_mappings.json')
    if os.path.exists(id_mappings_path):
        with open(id_mappings_path, 'r', encoding='utf-8') as f:
            id_maps = json.load(f)
        id_maps['products'] = [
            {
                'id': item['id'],
                'name': item['name'],
                'slug': item['slug'],
                'shortlink': f"https://hosseinykala.ir/?p={item['id']}"
            }
            for item in sorted(updated_products_list, key=lambda x: x['id'], reverse=True)
        ]
        with open(id_mappings_path, 'w', encoding='utf-8') as f:
            json.dump(id_maps, f, ensure_ascii=False, indent=2)
        print("✓ فایل data/id_mappings.json با موفقیت به‌روزرسانی شد.")

if __name__ == '__main__':
    update_catalog()

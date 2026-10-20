"""
build_full_updated_catalog.py
=============================
اسکریپت نهایی ساخت و به‌روزرسانی کامل کاتالوگ اکسل حسینی کالا:
۱. درج تمامی ۹۷ محصول لایو سایت + ۷۸ تنوع رنگ/سایز
۲. اعمال وضعیت موجودی جدید (✓ موجود / ✗ ناموجود) بر اساس لیست انبار
۳. درج اقلام آفلاین قبلی با وضعیت موجودی جدید
۴. افزودن کلیه ۱۰۴ محصول جدید انبار به تفکیک ۸ دسته‌بندی اصلی و برندها
۵. استفاده از کدهای مدل در نام کالا جهت جلوگیری از تداخل
۶. فرمول‌های خودکار تومان، منوی کشویی، رنگ‌بندی حرفه‌ای، داشبورد تحلیلی و راهنما
"""

import os
import sys
import json
import re
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from collections import defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"c:\Users\mmhhs\OneDrive\Documents\GitHub\hosseinyKalaSeo"
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
MATCHED_FILE = os.path.join(DATA_DIR, 'inventory_matched_results.json')
REF_FILE = os.path.join(DATA_DIR, 'current_catalog_reference.json')
EXCEL_OUT_MAIN = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.xlsx')
EXCEL_OUT_LATEST = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog_latest.xlsx')

# فایل‌ها در داخل build_complete_catalog خوانده می‌شوند

# ستون‌های استاندارد جدول
COLUMNS = [
    # (key,              header_text,                 width,  align,   is_price,  is_formula)
    ("name",             "نام محصول",                  44,     "right",   False,     False),
    ("price_regular",    "قیمت عادی (ریال)",          18,     "center",  True,      False),
    ("price_reg_toman",  "قیمت عادی (تومان)",          18,     "center",  True,      True),
    ("price_sale",       "قیمت حراج (ریال)",          18,     "center",  True,      False),
    ("price_sale_toman", "قیمت حراج (تومان)",          18,     "center",  True,      True),
    ("in_stock",         "وضعیت موجودی",               15,     "center",  False,     False),
    ("main_cat",         "دسته‌بندی اصلی سایت",        22,     "center",  False,     False),
    ("subcat",           "زیردسته / گروه کالا",       22,     "center",  False,     False),
    ("brand",            "برند",                       16,     "center",  False,     False),
    ("type",             "نوع محصول",                  14,     "center",  False,     False),
    ("variant_attr",     "مشخصه تنوع / متغیر",         22,     "center",  False,     False),
    ("product_id",       "شناسه محصول (ID)",           16,     "center",  False,     False),
    ("variation_id",     "شناسه تنوع",                 15,     "center",  False,     False),
    ("link",             "لینک مستقیم در سایت",        36,     "left",    False,     False),
    ("sku",              "کد SKU",                     15,     "center",  False,     False),
    ("status_note",      "وضعیت در سایت",              22,     "center",  False,     False),
]

COLOR_HEADER_BG = "1F4E79"
COLOR_HEADER_TEXT = "FFFFFF"
COLOR_BANNER_BG = "D9E1F2"
COLOR_BANNER_TEXT = "1F4E79"
COLOR_VAR_PARENT_BG = "EBF1F5"
COLOR_VARIATION_BG = "F8F9FA"
COLOR_OFFLINE_BG = "FFF9E6"
COLOR_NEW_OFFLINE_BG = "FEF2E4"
COLOR_IN_STOCK = "27AE60"
COLOR_OUT_OF_STOCK = "C00000"
COLOR_BORDER = "D9D9D9"

def get_border():
    s = Side(style='thin', color=COLOR_BORDER)
    return Border(top=s, bottom=s, left=s, right=s)

def normalize_text(text):
    if not text:
        return ""
    text = str(text).lower()
    text = text.replace('ي', 'ی').replace('ك', 'ک').replace('‌', ' ').replace('-', ' ').replace('_', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def build_complete_catalog():
    print("=" * 70)
    print("تولید فایل نهایی کاتالوگ اکسل حسینی کالا بر اساس لیست جدید موجودی...")
    print("=" * 70)

    with open(MATCHED_FILE, 'r', encoding='utf-8') as f:
        matched_inventory = json.load(f)

    with open(REF_FILE, 'r', encoding='utf-8') as f:
        catalog_ref = json.load(f)

    live_products = catalog_ref['live_products']
    live_by_id = {p['id']: p for p in live_products}
    old_excel_items = catalog_ref['excel_items']

    # ایجاد مپ وضعیت موجودی بر اساس مطابقت‌های انجام‌شده
    # product_id -> in_stock
    # variation_id -> in_stock
    # standard_name / old_name -> in_stock
    stock_by_pid = {}
    stock_by_vid = {}
    stock_by_name = {}

    for it in matched_inventory:
        in_stock_val = "✓ موجود" if "✓" in it['in_stock_label'] else "✗ ناموجود"
        if it.get('variation_id'):
            stock_by_vid[it['variation_id']] = in_stock_val
        elif it.get('product_id'):
            stock_by_pid[it['product_id']] = in_stock_val
        stock_by_name[it['standard_name']] = in_stock_val
        stock_by_name[it['raw_desc']] = in_stock_val
        stock_by_name[normalize_text(it['standard_name'])] = in_stock_val
        stock_by_name[normalize_text(it['raw_desc'])] = in_stock_val
        if it.get('model_code') and len(it['model_code']) > 2:
            stock_by_name[normalize_text(it['model_code'])] = in_stock_val

    # استخراج اقلام جدید (New Additions)
    new_items_by_cat = defaultdict(lambda: defaultdict(list))
    added_new_keys = set()

    for it in matched_inventory:
        if it['match_type'] == 'NEW_OFFLINE_ITEM':
            cat = it['category']
            brand = it['brand'] or 'متفرقه'
            key = (cat, brand, it['standard_name'])
            if key not in added_new_keys:
                added_new_keys.add(key)
                new_items_by_cat[cat][brand].append(it)

    print(f"تعداد اقلام کاملاً جدید منحصر‌به‌فرد: {len(added_new_keys)}")

    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    dv_stock = DataValidation(type="list", formula1='"✓ موجود,✗ ناموجود"', allow_blank=True)
    dv_stock.error = 'لطفاً «✓ موجود» یا «✗ ناموجود» را انتخاب کنید.'
    dv_stock.errorTitle = 'مقدار نامعتبر'

    stats = {
        "total_parent_rows": 0,
        "total_variation_rows": 0,
        "total_site_products": 0,
        "total_offline_products": 0,
        "in_stock_count": 0,
        "out_of_stock_count": 0,
        "by_category": {}
    }

    border_thin = get_border()

    # لیست ۸ دسته‌بندی اصلی
    ordered_cats = [
        "یخچال و فریزر",
        "شستشو و نظافت",
        "لوازم برقی و پخت و پز",
        "نوشیدنی ساز",
        "سرمایش و گرمایش",
        "تصفیه کننده آب",
        "صوتی و تصویری",
        "زیبایی و سلامت فردی"
    ]

    for sheet_title in ordered_cats:
        print(f"در حال ساخت شیت: '{sheet_title}' ...")
        ws = wb.create_sheet(title=sheet_title[:31])
        ws.sheet_view.rightToLeft = True
        ws.add_data_validation(dv_stock)

        # هدر جدول
        ws.row_dimensions[1].height = 32
        for col_idx, (key, header_text, width, align_str, is_price, is_formula) in enumerate(COLUMNS, 1):
            cell = ws.cell(row=1, column=col_idx, value=header_text)
            cell.font = Font(name="Calibri", size=11, bold=True, color=COLOR_HEADER_TEXT)
            cell.fill = PatternFill(fill_type="solid", fgColor=COLOR_HEADER_BG)
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = border_thin
            ws.column_dimensions[get_column_letter(col_idx)].width = width

        current_row = 2
        cat_stats = {
            "total_items": 0,
            "in_stock": 0,
            "out_of_stock": 0,
            "variations": 0,
        }

        # خواندن اقلام موجود قبلی در این شیت از reference
        sheet_old_items = [e for e in old_excel_items if e['sheet'] == sheet_title]
        
        # گروه‌بندی اقلام قبلی بر اساس subcat/brand
        grouped_old = defaultdict(list)
        for e in sheet_old_items:
            sub = e.get('subcat') or e.get('brand') or 'عمومی'
            grouped_old[sub].append(e)

        # گروه‌بندی اقلام جدید این شیت
        grouped_new = new_items_by_cat[sheet_title]

        # ادغام تمام زیردسته‌ها
        all_subcats = list(grouped_old.keys())
        for sub in grouped_new.keys():
            if sub not in all_subcats:
                all_subcats.append(sub)

        for subcat_name in all_subcats:
            # سطر بنر بخش
            ws.row_dimensions[current_row].height = 24
            ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=len(COLUMNS))
            banner_cell = ws.cell(row=current_row, column=1, value=f"  📂 {sheet_title}  ◀  {subcat_name}")
            banner_cell.font = Font(name="Calibri", size=11, bold=True, color=COLOR_BANNER_TEXT)
            banner_cell.fill = PatternFill(fill_type="solid", fgColor=COLOR_BANNER_BG)
            banner_cell.alignment = Alignment(horizontal="right", vertical="center")
            for c in range(1, len(COLUMNS) + 1):
                ws.cell(row=current_row, column=c).border = border_thin
            current_row += 1

            # ۱. درج اقلام قبلی با وضعیت موجودی به‌روزشده
            old_items_in_sub = grouped_old.get(subcat_name, [])
            for item in old_items_in_sub:
                is_var_child = (item.get('type') == 'تنوع' or bool(item.get('variation_id')))
                pid = item.get('product_id')
                vid = item.get('variation_id')
                item_name = item['name']
                is_site = (item.get('status_note') == 'ثبت‌شده در سایت' and bool(pid))

                # تعیین موجودی به‌روزشده
                if vid and vid in stock_by_vid:
                    stock_label = stock_by_vid[vid]
                elif pid and pid in stock_by_pid:
                    stock_label = stock_by_pid[pid]
                elif item_name in stock_by_name:
                    stock_label = stock_by_name[item_name]
                elif normalize_text(item_name) in stock_by_name:
                    stock_label = stock_by_name[normalize_text(item_name)]
                else:
                    found_s = None
                    norm_i = normalize_text(item_name)
                    for k_sub, s_val in stock_by_name.items():
                        if len(k_sub) > 3 and k_sub in norm_i:
                            found_s = s_val
                            break
                    stock_label = found_s or item.get('in_stock') or "✓ موجود"

                is_in_stock = ("✓" in str(stock_label))

                # آمار
                if is_var_child:
                    stats["total_variation_rows"] += 1
                    cat_stats["variations"] += 1
                else:
                    stats["total_parent_rows"] += 1
                    cat_stats["total_items"] += 1
                    if is_site:
                        stats["total_site_products"] += 1
                    else:
                        stats["total_offline_products"] += 1

                    if is_in_stock:
                        stats["in_stock_count"] += 1
                        cat_stats["in_stock"] += 1
                    else:
                        stats["out_of_stock_count"] += 1
                        cat_stats["out_of_stock"] += 1

                # استایل و رنگ
                ws.row_dimensions[current_row].height = 20 if is_var_child else 21
                is_var_parent = (item.get('type') == 'متغیر')

                if is_var_child:
                    row_bg = COLOR_VARIATION_BG
                elif is_var_parent:
                    row_bg = COLOR_VAR_PARENT_BG
                elif not is_site:
                    row_bg = COLOR_OFFLINE_BG
                else:
                    row_bg = "FFFFFF"

                fill_row = PatternFill(fill_type="solid", fgColor=row_bg)

                reg_price = item.get('price_regular')
                sale_price = item.get('price_sale')

                formula_reg_toman = f'=IF(ISBLANK(B{current_row}),"",B{current_row}/10)'
                formula_sale_toman = f'=IF(OR(ISBLANK(D{current_row}),D{current_row}=""),"",D{current_row}/10)'

                row_values = [
                    item_name,
                    reg_price if reg_price else "",
                    formula_reg_toman if reg_price else "",
                    sale_price if sale_price else "",
                    formula_sale_toman if sale_price else "",
                    stock_label,
                    sheet_title,
                    subcat_name,
                    item.get('brand') or subcat_name,
                    item.get('type', 'ساده'),
                    item.get('variant_attr', ''),
                    pid if pid else "",
                    vid if vid else "",
                    item.get('link', ''),
                    item.get('sku', ''),
                    item.get('status_note', 'ثبت‌شده در سایت' if is_site else 'در سایت تعریف نشده')
                ]

                for col_idx, val in enumerate(row_values, 1):
                    cell = ws.cell(row=current_row, column=col_idx, value=val)
                    cell.fill = fill_row
                    cell.border = border_thin
                    cell.font = Font(name="Calibri", size=9 if is_var_child else 10, italic=is_var_child, bold=is_var_parent)

                    if col_idx == 1:
                        cell.alignment = Alignment(horizontal="right", vertical="center")
                    elif col_idx in [2, 3, 4, 5, 12, 13]:
                        cell.alignment = Alignment(horizontal="center", vertical="center")
                    elif col_idx == 14:
                        cell.alignment = Alignment(horizontal="left", vertical="center")
                    else:
                        cell.alignment = Alignment(horizontal="center", vertical="center")

                    if col_idx in [2, 3, 4, 5] and val:
                        cell.number_format = '#,##0'

                    if col_idx == 6:
                        dv_stock.add(cell)
                        if "✓" in str(val):
                            cell.font = Font(name="Calibri", size=9 if is_var_child else 10, bold=True, color=COLOR_IN_STOCK)
                        elif "✗" in str(val):
                            cell.font = Font(name="Calibri", size=9 if is_var_child else 10, bold=True, color=COLOR_OUT_OF_STOCK)

                    if col_idx == 14 and val:
                        cell.hyperlink = str(val)
                        cell.font = Font(name="Calibri", size=9 if is_var_child else 10, color="0563C1", underline="single")

                current_row += 1

            # ۲. درج اقلام کاملاً جدید این زیردسته (New Additions)
            new_items_in_sub = grouped_new.get(subcat_name, [])
            for n_it in new_items_in_sub:
                stats["total_parent_rows"] += 1
                stats["total_offline_products"] += 1
                cat_stats["total_items"] += 1

                stock_label = n_it['in_stock_label']
                if "✓" in stock_label:
                    stats["in_stock_count"] += 1
                    cat_stats["in_stock"] += 1
                else:
                    stats["out_of_stock_count"] += 1
                    cat_stats["out_of_stock"] += 1

                ws.row_dimensions[current_row].height = 21
                fill_new = PatternFill(fill_type="solid", fgColor=COLOR_NEW_OFFLINE_BG)

                formula_reg_toman = f'=IF(ISBLANK(B{current_row}),"",B{current_row}/10)'
                formula_sale_toman = f'=IF(OR(ISBLANK(D{current_row}),D{current_row}=""),"",D{current_row}/10)'

                row_values = [
                    n_it['standard_name'],
                    "", # قیمت ندارد (آفلاین)
                    formula_reg_toman,
                    "",
                    formula_sale_toman,
                    stock_label,
                    sheet_title,
                    subcat_name,
                    n_it['brand'],
                    "ساده",
                    n_it.get('model_code', ''),
                    "", # بدون ID
                    "", # بدون VID
                    "", # بدون لینک
                    "", # بدون SKU
                    "در سایت تعریف نشده"
                ]

                for col_idx, val in enumerate(row_values, 1):
                    cell = ws.cell(row=current_row, column=col_idx, value=val)
                    cell.fill = fill_new
                    cell.border = border_thin
                    cell.font = Font(name="Calibri", size=10)

                    if col_idx == 1:
                        cell.alignment = Alignment(horizontal="right", vertical="center")
                    elif col_idx in [2, 3, 4, 5, 12, 13]:
                        cell.alignment = Alignment(horizontal="center", vertical="center")
                    elif col_idx == 14:
                        cell.alignment = Alignment(horizontal="left", vertical="center")
                    else:
                        cell.alignment = Alignment(horizontal="center", vertical="center")

                    if col_idx == 6:
                        dv_stock.add(cell)
                        if "✓" in str(val):
                            cell.font = Font(name="Calibri", size=10, bold=True, color=COLOR_IN_STOCK)
                        elif "✗" in str(val):
                            cell.font = Font(name="Calibri", size=10, bold=True, color=COLOR_OUT_OF_STOCK)

                current_row += 1

        # فریز هدر و اعمال فیلتر
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = f"A1:{get_column_letter(len(COLUMNS))}{current_row-1}"
        stats["by_category"][sheet_title] = cat_stats
        print(f"  ✓ شیت '{sheet_title}' نهایی شد: {cat_stats['total_items']} کالا ({cat_stats['in_stock']} موجود، {cat_stats['out_of_stock']} ناموجود).")

    # =========================================================
    # ساخت شیت ۱: داشبورد جامع KPI
    # =========================================================
    print("\nدر حال ساخت داشبورد مدیریتی و تحلیلی KPI...")
    ws_dash = wb.create_sheet(title="📊 خلاصه و داشبورد", index=0)
    ws_dash.sheet_view.rightToLeft = True

    ws_dash.merge_cells("A1:H2")
    t_cell = ws_dash.cell(row=1, column=1, value="📊 داشبورد کاتالوگ جامع و وضعیت انبار — فروشگاه لوازم خانگی حسینی")
    t_cell.font = Font(name="Calibri", size=15, bold=True, color="FFFFFF")
    t_cell.fill = PatternFill(fill_type="solid", fgColor=COLOR_HEADER_BG)
    t_cell.alignment = Alignment(horizontal="center", vertical="center")

    kpis = [
        ("کل مدل‌ها و اقلام کاتالوگ", stats["total_parent_rows"], "1F4E79"),
        ("محصولات فعال در سایت", stats["total_site_products"], "2E75B6"),
        ("تنوع‌ها و رنگ‌های متغیر", stats["total_variation_rows"], "5B9BD5"),
        ("مجموع گزینه‌های خرید", stats["total_site_products"] + stats["total_variation_rows"], "1E4E79"),
        ("اقلام موجود در انبار", stats["in_stock_count"], "27AE60"),
        ("اقلام ناموجود یا سفارشی", stats["out_of_stock_count"], "C00000"),
        ("اقلام جدید نیازمند ثبت در سایت", stats["total_offline_products"], "ED7D31"),
    ]

    col_kpi = 1
    for label, val, bg_color in kpis[:4]:
        ws_dash.merge_cells(start_row=4, start_column=col_kpi, end_row=4, end_column=col_kpi+1)
        ws_dash.merge_cells(start_row=5, start_column=col_kpi, end_row=5, end_column=col_kpi+1)

        c_lbl = ws_dash.cell(row=4, column=col_kpi, value=label)
        c_lbl.font = Font(name="Calibri", size=10, color="FFFFFF", bold=True)
        c_lbl.fill = PatternFill(fill_type="solid", fgColor=bg_color)
        c_lbl.alignment = Alignment(horizontal="center", vertical="center")

        c_val = ws_dash.cell(row=5, column=col_kpi, value=val)
        c_val.font = Font(name="Calibri", size=16, color="FFFFFF", bold=True)
        c_val.fill = PatternFill(fill_type="solid", fgColor=bg_color)
        c_val.alignment = Alignment(horizontal="center", vertical="center")

        for r in [4, 5]:
            for c in range(col_kpi, col_kpi+2):
                ws_dash.cell(row=r, column=c).border = border_thin
        col_kpi += 2

    col_kpi = 1
    for label, val, bg_color in kpis[4:]:
        ws_dash.merge_cells(start_row=7, start_column=col_kpi, end_row=7, end_column=col_kpi+1)
        ws_dash.merge_cells(start_row=8, start_column=col_kpi, end_row=8, end_column=col_kpi+1)

        c_lbl = ws_dash.cell(row=7, column=col_kpi, value=label)
        c_lbl.font = Font(name="Calibri", size=10, color="FFFFFF", bold=True)
        c_lbl.fill = PatternFill(fill_type="solid", fgColor=bg_color)
        c_lbl.alignment = Alignment(horizontal="center", vertical="center")

        c_val = ws_dash.cell(row=8, column=col_kpi, value=val)
        c_val.font = Font(name="Calibri", size=16, color="FFFFFF", bold=True)
        c_val.fill = PatternFill(fill_type="solid", fgColor=bg_color)
        c_val.alignment = Alignment(horizontal="center", vertical="center")

        for r in [7, 8]:
            for c in range(col_kpi, col_kpi+2):
                ws_dash.cell(row=r, column=c).border = border_thin
        col_kpi += 2

    # جدول تفکیک آمار
    ws_dash.cell(row=10, column=1, value="جدول تفکیک آمار محصولات در ۸ دسته‌بندی اصلی سایت").font = Font(name="Calibri", size=12, bold=True, color=COLOR_HEADER_BG)

    headers_table = ["ردیف", "نام دسته‌بندی اصلی", "تعداد مدل‌های محصول", "تعداد تنوع و رنگ‌ها", "موجود", "ناموجود", "درصد موجودی"]
    col_widths_table = [8, 28, 20, 20, 14, 14, 16]

    for col_idx, (h_text, w) in enumerate(zip(headers_table, col_widths_table), 1):
        cell = ws_dash.cell(row=11, column=col_idx, value=h_text)
        cell.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
        cell.fill = PatternFill(fill_type="solid", fgColor=COLOR_HEADER_BG)
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border_thin
        ws_dash.column_dimensions[get_column_letter(col_idx)].width = w

    t_row = 12
    for idx, (cat_name, cdata) in enumerate(stats["by_category"].items(), 1):
        total_p = cdata["total_items"]
        in_s = cdata["in_stock"]
        out_s = cdata["out_of_stock"]
        pct = f"{(in_s / total_p * 100):.1f}%" if total_p > 0 else "0%"

        row_vals = [idx, cat_name, total_p, cdata["variations"], in_s, out_s, pct]
        for col_idx, val in enumerate(row_vals, 1):
            cell = ws_dash.cell(row=t_row, column=col_idx, value=val)
            cell.font = Font(name="Calibri", size=10)
            cell.border = border_thin
            cell.alignment = Alignment(horizontal="center", vertical="center")
            if col_idx == 2:
                cell.alignment = Alignment(horizontal="right", vertical="center")
            if col_idx == 5:
                cell.font = Font(name="Calibri", size=10, bold=True, color=COLOR_IN_STOCK)
            if col_idx == 6:
                cell.font = Font(name="Calibri", size=10, bold=True, color=COLOR_OUT_OF_STOCK)

        t_row += 1

    # سطر مجموع جدول
    ws_dash.cell(row=t_row, column=1, value="")
    ws_dash.cell(row=t_row, column=2, value="مجموع کل").font = Font(name="Calibri", size=10, bold=True)
    ws_dash.cell(row=t_row, column=3, value=f"=SUM(C12:C{t_row-1})").font = Font(name="Calibri", size=10, bold=True)
    ws_dash.cell(row=t_row, column=4, value=f"=SUM(D12:D{t_row-1})").font = Font(name="Calibri", size=10, bold=True)
    ws_dash.cell(row=t_row, column=5, value=f"=SUM(E12:E{t_row-1})").font = Font(name="Calibri", size=10, bold=True, color=COLOR_IN_STOCK)
    ws_dash.cell(row=t_row, column=6, value=f"=SUM(F12:F{t_row-1})").font = Font(name="Calibri", size=10, bold=True, color=COLOR_OUT_OF_STOCK)
    ws_dash.cell(row=t_row, column=7, value=f"=(E{t_row}/C{t_row})*100").font = Font(name="Calibri", size=10, bold=True)
    ws_dash.cell(row=t_row, column=7).number_format = '0.0"%"'

    for col_idx in range(1, 8):
        cell = ws_dash.cell(row=t_row, column=col_idx)
        cell.fill = PatternFill(fill_type="solid", fgColor="EBF1F5")
        cell.border = border_thin
        cell.alignment = Alignment(horizontal="center", vertical="center")

    # =========================================================
    # ساخت شیت راهنما
    # =========================================================
    ws_guide = wb.create_sheet(title="📖 راهنمای کاربری")
    ws_guide.sheet_view.rightToLeft = True

    guide_lines = [
        ("راهنمای جامع کار با فایل اکسل کاتالوگ حسینی کالا", "", "HEADER"),
        ("", "", "EMPTY"),
        ("۱. معماری ۸ دسته‌بندی اصلی سایت:", "دسته‌بندی‌های این فایل مطابق منوی رسمی وب‌سایت در ۸ دسته‌بندی اصلی سازماندهی شده‌اند.", "SECTION"),
        ("• یخچال و فریزر", "شامل یخچال‌های ساید، دوقلو، کمبی، مینی و هتلی از برندهای کلور، دیپوینت، هیمالیا، الکترواستیل، ایستکول، نیکسان و بست.", "BULLET"),
        ("• شستشو و نظافت", "شامل ماشین‌های لباسشویی اتوماتیک و دوقلو، ظرفشویی، جاروبرقی‌های کیسه‌ای و سطلی، پتوشور و اتو بخار.", "BULLET"),
        ("• لوازم برقی و پخت و پز", "شامل سرخ‌کن بدون روغن، غذاساز، گوشت‌کوب برقی، اجاق گاز، فر توکار، سرویس قابلمه، تابه و زودپز.", "BULLET"),
        ("• نوشیدنی ساز", "شامل اسپرسوساز، چای‌ساز، سماور برقی، کتری برقی، آبمیوه‌گیری، مخلوط‌کن، آسیاب و همزن.", "BULLET"),
        ("• سرمایش و گرمایش", "شامل کولرهای آبی سلولزی و معمولی، اسپلیت دیواری، پنکه ایستاده و بخاری‌های گازی و برقی.", "BULLET"),
        ("• تصفیه کننده آب", "شامل دستگاه‌های تصفیه آب خانگی، آبسردکن‌های اداری و ایستاده و آبگرمکن دیواری.", "BULLET"),
        ("• صوتی و تصویری", "شامل تلویزیون‌های هوشمند 4K و ال‌ای‌دی در سایزهای ۳۲ تا ۸۵ اینچ.", "BULLET"),
        ("• زیبایی و سلامت فردی", "شامل ماشین‌های اصلاح سر و صورت، ریش‌تراش، سشوار، اتو مو و اپیلاتورهای حرفه‌ای.", "BULLET"),
        ("", "", "EMPTY"),
        ("۲. وضعیت موجودی انبار:", "وضعیت کالاها بر اساس آخرین لیست انبار با «✓ موجود» (تعداد بیشتر از صفر) و «✗ ناموجود» (صفر یا منفی) ثبت شده و به کمک منوی کشویی قابل تغییر است.", "SECTION"),
        ("", "", "EMPTY"),
        ("۳. تفکیک اقلام لایو سایت و اقلام جدید:", "اقلامی که در سایت ثبت شده‌اند دارای لینک مستقیم و قیمت هستند. اقلام جدید که در سایت هنوز تعریف نشده‌اند، با پس‌زمینه رنگی مشخص و برچسب «در سایت تعریف نشده» در شیت دسته‌بندی مربوطه افزوده شده‌اند.", "SECTION"),
        ("", "", "EMPTY"),
        ("۴. فرمول خودکار قیمت تومان:", "قیمت‌ها به ریال وارد می‌شوند و اکسل به‌صورت خودکار قیمت تومان را با فرمول (=B/10) محاسبه می‌کند.", "SECTION"),
    ]

    ws_guide.column_dimensions['A'].width = 35
    ws_guide.column_dimensions['B'].width = 75

    for r_idx, (col1, col2, stype) in enumerate(guide_lines, 1):
        c1 = ws_guide.cell(row=r_idx, column=1, value=col1)
        c2 = ws_guide.cell(row=r_idx, column=2, value=col2)

        if stype == "HEADER":
            ws_guide.merge_cells(start_row=r_idx, start_column=1, end_row=r_idx, end_column=2)
            c1.font = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
            c1.fill = PatternFill(fill_type="solid", fgColor=COLOR_HEADER_BG)
            c1.alignment = Alignment(horizontal="center", vertical="center")
            ws_guide.row_dimensions[r_idx].height = 30
        elif stype == "SECTION":
            c1.font = Font(name="Calibri", size=11, bold=True, color=COLOR_HEADER_BG)
            c2.font = Font(name="Calibri", size=10, bold=True)
            c1.alignment = Alignment(horizontal="right", vertical="center")
            c2.alignment = Alignment(horizontal="right", vertical="center")
            ws_guide.row_dimensions[r_idx].height = 24
        elif stype == "BULLET":
            c1.font = Font(name="Calibri", size=10, bold=True, color="2E75B6")
            c2.font = Font(name="Calibri", size=10)
            c1.alignment = Alignment(horizontal="right", vertical="center")
            c2.alignment = Alignment(horizontal="right", vertical="center")
            ws_guide.row_dimensions[r_idx].height = 20
        else:
            ws_guide.row_dimensions[r_idx].height = 16

    wb.save(EXCEL_OUT_LATEST)
    print(f"✓ ذخیره موفق در: {EXCEL_OUT_LATEST}")

    try:
        wb.save(EXCEL_OUT_MAIN)
        print(f"✓ ذخیره موفق در: {EXCEL_OUT_MAIN}")
    except PermissionError:
        print(f"⚠️ توجه: فایل '{os.path.basename(EXCEL_OUT_MAIN)}' در Excel باز است. داده‌ها در {os.path.basename(EXCEL_OUT_LATEST)} به‌طور کامل ذخیره شدند.")

    try:
        from scripts.bulk_edit_catalog import add_bulk_edit_sheet_to_catalog
        add_bulk_edit_sheet_to_catalog(EXCEL_OUT_LATEST)
        add_bulk_edit_sheet_to_catalog(EXCEL_OUT_MAIN)
    except Exception as e:
        pass

    print("\n" + "=" * 60)
    print("✓ کاتالوگ با موفقیت به پایان رسید.")
    print(f"- کل مدل‌های والد کاتالوگ: {stats['total_parent_rows']}")
    print(f"- اقلام فعال در سایت: {stats['total_site_products']}")
    print(f"- تنوع‌ها و رنگ‌ها: {stats['total_variation_rows']}")
    print(f"- اقلام تعریف‌نشده در سایت (نیازمند ثبت): {stats['total_offline_products']}")
    print(f"- کل اقلام موجود: {stats['in_stock_count']}")
    print(f"- کل اقلام ناموجود: {stats['out_of_stock_count']}")
    print("=" * 60)

if __name__ == '__main__':
    build_complete_catalog()

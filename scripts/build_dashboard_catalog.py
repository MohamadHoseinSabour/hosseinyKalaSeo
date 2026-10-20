"""
build_dashboard_catalog.py
==========================
ایجاد کاتالوگ جامع با داشبورد آماری، نمودارهای تحلیلی، KPIها و راهنمای کاربری در شیت اول
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
import os, json, datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.chart import BarChart, DoughnutChart, PieChart, Reference, Series

PROJECT_DIR = r"c:\Users\mmhhs\OneDrive\Documents\GitHub\hosseinyKalaSeo"
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
RAW_FILE = os.path.join(DATA_DIR, 'products_raw.json')
EXCEL_OUTPUT = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.xlsx')
EXCEL_UPDATED = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog_updated.xlsx')

with open(RAW_FILE, encoding='utf-8') as f:
    site_products = json.load(f)

site_by_id = {p['product_id']: p for p in site_products}

# ساختار محصولات (ساده و متغیر با سطرهای والد و تنوع)
from generate_perfect_catalog_v2 import STRUCTURE, COLUMNS, COLOR_HEADER_BG, COLOR_HEADER_TEXT, COLOR_SUBCAT_BG, COLOR_SUBCAT_TEXT, COLOR_VAR_PARENT_BG, COLOR_VARIATION_BG, COLOR_MISSING_BG, COLOR_TOMAN_HEADER_BG, COLOR_IN_STOCK_TEXT, COLOR_OUT_OF_STOCK, make_border

def build_full_catalog_with_dashboard():
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    border_thin = make_border()

    # ─────────────────────────────────────────────────────────
    # مرحله ۱: ایجاد شیت‌های دسته‌بندی و جمع‌آوری آمار واقعی
    # ─────────────────────────────────────────────────────────
    category_stats = []
    total_products_global = 0
    total_parent_variable = 0
    total_variations = 0
    total_simple = 0
    total_in_site = 0
    total_missing = 0
    total_in_stock = 0
    total_out_of_stock = 0
    prices_toman_list = []

    subcats_count_global = 0

    for sheet_name, subcats in STRUCTURE.items():
        ws = wb.create_sheet(title=sheet_name[:31])
        ws.sheet_view.rightToLeft = True

        # هدر شیت
        ws.row_dimensions[1].height = 28
        for col_idx, (f_key, h_text, width, align_mode, is_price, is_formula) in enumerate(COLUMNS, start=1):
            cell = ws.cell(row=1, column=col_idx, value=h_text)
            cell.font = Font(bold=True, color=COLOR_HEADER_TEXT, size=10, name="Calibri")
            h_bg = COLOR_TOMAN_HEADER_BG if is_formula else COLOR_HEADER_BG
            cell.fill = PatternFill(fill_type='solid', fgColor=h_bg)
            cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            cell.border = border_thin
            ws.column_dimensions[get_column_letter(col_idx)].width = width

        ws.freeze_panes = 'A2'
        ws.auto_filter.ref = f"A1:{get_column_letter(len(COLUMNS))}1"

        row_idx = 2
        sheet_prod_count = 0
        sheet_in_site_count = 0
        sheet_missing_count = 0
        sheet_prices_toman = []

        subcats_count_global += len(subcats)

        for subcat_name, products_list in subcats.items():
            # هدر زیردسته
            ws.row_dimensions[row_idx].height = 22
            ws.merge_cells(start_row=row_idx, start_column=1, end_row=row_idx, end_column=len(COLUMNS))
            sub_cell = ws.cell(row=row_idx, column=1, value=f"  📂 {sheet_name}  ◀  {subcat_name}")
            sub_cell.font = Font(bold=True, color=COLOR_SUBCAT_TEXT, size=10, name="Calibri")
            sub_cell.fill = PatternFill(fill_type='solid', fgColor=COLOR_SUBCAT_BG)
            sub_cell.alignment = Alignment(horizontal='right', vertical='center')
            for c in range(1, len(COLUMNS) + 1):
                ws.cell(row=row_idx, column=c).border = border_thin
            row_idx += 1

            cat_path = f"{sheet_name} / {subcat_name}"

            for prod in products_list:
                ptype = prod.get("type", "simple")
                pname = prod.get("name")
                site_id = prod.get("site_id")
                site_prod = site_by_id.get(site_id) if site_id else None

                # ۱. محصول ساده
                if ptype == "simple":
                    sheet_prod_count += 1
                    total_products_global += 1
                    total_simple += 1

                    if site_prod:
                        sheet_in_site_count += 1
                        total_in_site += 1
                        reg_price = prod.get("price") or site_prod.get("price_regular") or ""
                        sale_price = prod.get("sale_price") or site_prod.get("price_sale") or ""
                        in_stk = prod.get("in_stock") or ("موجود" if site_prod.get("in_stock", True) else "ناموجود")
                        stk_color = COLOR_IN_STOCK_TEXT if in_stk == "موجود" else COLOR_OUT_OF_STOCK
                        row_fill = PatternFill(fill_type='solid', fgColor="FFFFFF")
                        link_val = site_prod.get("shortlink", "")
                        sku_val = site_prod.get("sku", "")
                        status_val = "✓ موجود در سایت"
                        status_color = "27AE60"
                        if in_stk == "موجود": total_in_stock += 1
                        else: total_out_of_stock += 1
                        if reg_price:
                            sheet_prices_toman.append(int(reg_price) // 10)
                            prices_toman_list.append(int(reg_price) // 10)
                    else:
                        sheet_missing_count += 1
                        total_missing += 1
                        total_out_of_stock += 1
                        reg_price = ""
                        sale_price = ""
                        in_stk = "ناموجود"
                        stk_color = COLOR_OUT_OF_STOCK
                        row_fill = PatternFill(fill_type='solid', fgColor=COLOR_MISSING_BG)
                        link_val = ""
                        sku_val = ""
                        status_val = "نیازمند ثبت در سایت"
                        status_color = "806000"

                    row_data = {
                        "name": pname,
                        "price_regular": reg_price,
                        "price_reg_toman": f'=IF(OR(B{row_idx}="",B{row_idx}=0),"",B{row_idx}/10)',
                        "price_sale": sale_price,
                        "price_sale_toman": f'=IF(OR(D{row_idx}="",D{row_idx}=0),"",D{row_idx}/10)',
                        "in_stock": in_stk,
                        "category_path": cat_path,
                        "type": "ساده",
                        "variant_attr": "-",
                        "product_id": site_id or "",
                        "variation_id": "",
                        "link": link_val,
                        "sku": sku_val,
                        "status_note": status_val,
                    }

                    ws.row_dimensions[row_idx].height = 20
                    for c_idx, (f_key, _, _, align_mode, is_price, is_formula) in enumerate(COLUMNS, start=1):
                        val = row_data.get(f_key, "")
                        c = ws.cell(row=row_idx, column=c_idx, value=val)
                        c.fill = row_fill
                        c.alignment = Alignment(horizontal=align_mode, vertical='center')
                        c.border = border_thin
                        c.font = Font(size=10, name="Calibri")

                        if is_price or is_formula:
                            c.number_format = '#,##0'
                            if isinstance(val, int) or is_formula:
                                c.font = Font(bold=True, size=10, color="1F4E79" if is_formula else "000000", name="Calibri")
                        if f_key == "in_stock":
                            c.font = Font(bold=True, color=stk_color, size=10, name="Calibri")
                        if f_key == "link" and val:
                            c.hyperlink = val
                            c.style = "Hyperlink"
                            c.fill = row_fill
                        if f_key == "status_note":
                            c.font = Font(size=9, italic=not site_prod, color=status_color, bold=bool(site_prod), name="Calibri")

                    row_idx += 1

                # ۲. محصول متغیر (والد + تنوع‌ها)
                elif ptype == "variable":
                    variants = prod.get("variants", [])
                    var_count_str = f"شامل {len(variants)} رنگ / تنوع"
                    total_parent_variable += 1

                    if site_prod:
                        sheet_in_site_count += 1
                        total_in_site += 1
                        parent_reg_price = site_prod.get("price_regular") or (variants[0].get("price") if variants else "")
                        parent_sale_price = site_prod.get("price_sale") or ""
                        parent_in_stk = "موجود" if site_prod.get("in_stock", True) else "ناموجود"
                        parent_stk_color = COLOR_IN_STOCK_TEXT if parent_in_stk == "موجود" else COLOR_OUT_OF_STOCK
                        parent_link = site_prod.get("shortlink", "")
                        parent_sku = site_prod.get("sku", "")
                        parent_status = "✓ محصول متغیر در سایت"
                        parent_status_color = "27AE60"
                        parent_fill = PatternFill(fill_type='solid', fgColor=COLOR_VAR_PARENT_BG)
                        if parent_in_stk == "موجود": total_in_stock += 1
                        else: total_out_of_stock += 1
                        if parent_reg_price:
                            sheet_prices_toman.append(int(parent_reg_price) // 10)
                            prices_toman_list.append(int(parent_reg_price) // 10)
                    else:
                        sheet_missing_count += 1
                        total_missing += 1
                        total_out_of_stock += 1
                        parent_reg_price = ""
                        parent_sale_price = ""
                        parent_in_stk = "ناموجود"
                        parent_stk_color = COLOR_OUT_OF_STOCK
                        parent_link = ""
                        parent_sku = ""
                        parent_status = "نیازمند ثبت متغیر در سایت"
                        parent_status_color = "806000"
                        parent_fill = PatternFill(fill_type='solid', fgColor=COLOR_VAR_PARENT_BG)

                    parent_row_data = {
                        "name": pname,
                        "price_regular": parent_reg_price,
                        "price_reg_toman": f'=IF(OR(B{row_idx}="",B{row_idx}=0),"",B{row_idx}/10)',
                        "price_sale": parent_sale_price,
                        "price_sale_toman": f'=IF(OR(D{row_idx}="",D{row_idx}=0),"",D{row_idx}/10)',
                        "in_stock": parent_in_stk,
                        "category_path": cat_path,
                        "type": "متغیر",
                        "variant_attr": var_count_str,
                        "product_id": site_id or "",
                        "variation_id": "",
                        "link": parent_link,
                        "sku": parent_sku,
                        "status_note": parent_status,
                    }

                    ws.row_dimensions[row_idx].height = 21
                    for c_idx, (f_key, _, _, align_mode, is_price, is_formula) in enumerate(COLUMNS, start=1):
                        val = parent_row_data.get(f_key, "")
                        c = ws.cell(row=row_idx, column=c_idx, value=val)
                        c.fill = parent_fill
                        c.alignment = Alignment(horizontal=align_mode, vertical='center')
                        c.border = border_thin
                        c.font = Font(bold=(f_key in ("name", "type")), size=10, name="Calibri")

                        if is_price or is_formula:
                            c.number_format = '#,##0'
                            if isinstance(val, int) or is_formula:
                                c.font = Font(bold=True, size=10, color="1F4E79" if is_formula else "000000", name="Calibri")
                        if f_key == "in_stock":
                            c.font = Font(bold=True, color=parent_stk_color, size=10, name="Calibri")
                        if f_key == "link" and val:
                            c.hyperlink = val
                            c.style = "Hyperlink"
                            c.fill = parent_fill
                        if f_key == "status_note":
                            c.font = Font(size=9, color=parent_status_color, bold=bool(site_prod), name="Calibri")

                    row_idx += 1

                    # سطرهای فرزند
                    for v in variants:
                        sheet_prod_count += 1
                        total_products_global += 1
                        total_variations += 1

                        vname = v.get("name")
                        vattr = v.get("attr", "-")
                        vid = v.get("vid")
                        vprice = v.get("price") or ""
                        vsale = v.get("sale_price") or ""
                        vstock = v.get("in_stock", "ناموجود")
                        vstk_color = COLOR_IN_STOCK_TEXT if vstock == "موجود" else COLOR_OUT_OF_STOCK
                        vsite_id = v.get("site_id") or site_id

                        if vid:
                            vlink = f"https://hosseinykala.ir/?p={vid}"
                            vstatus = "✓ تنوع فعال در سایت"
                            vstatus_color = "555555"
                            if vprice:
                                sheet_prices_toman.append(int(vprice) // 10)
                                prices_toman_list.append(int(vprice) // 10)
                        elif vsite_id:
                            vlink = f"https://hosseinykala.ir/?p={vsite_id}"
                            vstatus = "✓ تنوع در سایت"
                            vstatus_color = "555555"
                            if vprice:
                                sheet_prices_toman.append(int(vprice) // 10)
                                prices_toman_list.append(int(vprice) // 10)
                        else:
                            vlink = ""
                            vstatus = "نیازمند تعریف تنوع"
                            vstatus_color = "806000"

                        var_fill = PatternFill(fill_type='solid', fgColor=COLOR_VARIATION_BG)

                        var_row_data = {
                            "name": vname,
                            "price_regular": vprice,
                            "price_reg_toman": f'=IF(OR(B{row_idx}="",B{row_idx}=0),"",B{row_idx}/10)',
                            "price_sale": vsale,
                            "price_sale_toman": f'=IF(OR(D{row_idx}="",D{row_idx}=0),"",D{row_idx}/10)',
                            "in_stock": vstock,
                            "category_path": cat_path,
                            "type": "تنوع (واریاسیون)",
                            "variant_attr": vattr,
                            "product_id": vsite_id or "",
                            "variation_id": vid or "",
                            "link": vlink,
                            "sku": "",
                            "status_note": vstatus,
                        }

                        ws.row_dimensions[row_idx].height = 19
                        for c_idx, (f_key, _, _, align_mode, is_price, is_formula) in enumerate(COLUMNS, start=1):
                            val = var_row_data.get(f_key, "")
                            c = ws.cell(row=row_idx, column=c_idx, value=val)
                            c.fill = var_fill
                            c.alignment = Alignment(horizontal=align_mode, vertical='center')
                            c.border = border_thin
                            c.font = Font(size=9.5, name="Calibri")

                            if f_key == "name":
                                c.font = Font(size=9.5, italic=True, color="333333", name="Calibri")
                            if is_price or is_formula:
                                c.number_format = '#,##0'
                                c.font = Font(bold=True, size=9.5, color="1F4E79", name="Calibri")
                            if f_key == "in_stock":
                                c.font = Font(bold=True, color=vstk_color, size=9.5, name="Calibri")
                            if f_key == "link" and val:
                                c.hyperlink = val
                                c.style = "Hyperlink"
                                c.fill = var_fill
                            if f_key == "status_note":
                                c.font = Font(size=9, color=vstatus_color, name="Calibri")

                        row_idx += 1

        # منوی کشویی انتخاب موجودی
        dv_stock = DataValidation(
            type="list",
            formula1='"موجود,ناموجود"',
            allow_blank=True,
            showDropDown=False,
            showErrorMessage=True,
            errorTitle="خطای انتخاب",
            error="لطفاً وضعیت موجودی را از بین گزینه‌های «موجود» یا «ناموجود» انتخاب کنید."
        )
        ws.add_data_validation(dv_stock)
        dv_stock.add(f"F2:F{row_idx}")

        avg_price = (sum(sheet_prices_toman) // len(sheet_prices_toman)) if sheet_prices_toman else 0
        category_stats.append({
            "name": sheet_name,
            "subcats_count": len(subcats),
            "total_items": sheet_prod_count,
            "in_site": sheet_in_site_count,
            "missing": sheet_missing_count,
            "avg_price_toman": avg_price,
        })

    # ─────────────────────────────────────────────────────────
    # مرحله ۲: ساخت داشبورد مدیریتی و تحلیلی در شیت اول
    # ─────────────────────────────────────────────────────────
    ws_dash = wb.create_sheet("داشبورد و آمار کاتالوگ", index=0)
    ws_dash.sheet_view.rightToLeft = True

    # تاریخ و زمان آخرین به‌روزرسانی
    now_str = datetime.datetime.now().strftime("%Y/%m/%d - %H:%M")
    avg_global_price_toman = (sum(prices_toman_list) // len(prices_toman_list)) if prices_toman_list else 0
    max_price_toman = max(prices_toman_list) if prices_toman_list else 0
    min_price_toman = min(prices_toman_list) if prices_toman_list else 0

    # ── ۱. عنوان داشبورد ──
    ws_dash.merge_cells("A1:J1")
    t_cell = ws_dash["A1"]
    t_cell.value = "📊 داشبورد آماری، وضعیت کاتالوگ و گزارش سئو — حسینی کالا"
    t_cell.font = Font(bold=True, size=14, color="FFFFFF", name="Calibri")
    t_cell.fill = PatternFill(fill_type='solid', fgColor="1F4E79")
    t_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws_dash.row_dimensions[1].height = 36

    # محاسبه دقیق تعداد مدل‌های والد و ساده
    total_base_models = total_simple + total_parent_variable

    # ── ۲. کارت‌های شاخص‌های کلیدی (KPI Summary Cards) ──
    cards = [
        ("کل تنوع‌ها و سطرهای قیمت", f"{total_products_global} ردیف", f"{total_base_models} مدل اصلی + {total_variations} تنوع رنگ/سایز", "2E75B6"),
        ("مدل‌های کالا (لیست کاربر)", f"{total_base_models} مدل", "۱۱۷ تک‌مدل + ۳۴ مدل متغیر", "1F4E79"),
        ("دسته‌ها و برندها", f"{len(STRUCTURE)} دسته / {subcats_count_global} برند", "تفکیک‌شده در ۱۲ شیت مجزا", "2E75B6"),
        ("ثبت‌شده در سایت", f"{total_in_site} مدل", f"{total_in_site} کالا دارای شناسه و لینک فعال", "27AE60"),
        ("نیازمند ثبت در سایت", f"{total_missing} مدل", "اقلام جدید آماده ورود قیمت", "C00000"),
    ]

    ws_dash.row_dimensions[3].height = 20
    ws_dash.row_dimensions[4].height = 26
    ws_dash.row_dimensions[5].height = 18

    col_starts = [1, 3, 5, 7, 9]  # A, C, E, G, I
    for (title, value, subtext, color), c_start in zip(cards, col_starts):
        c_end = c_start + 1
        ws_dash.merge_cells(start_row=3, start_column=c_start, end_row=3, end_column=c_end)
        ws_dash.merge_cells(start_row=4, start_column=c_start, end_row=4, end_column=c_end)
        ws_dash.merge_cells(start_row=5, start_column=c_start, end_row=5, end_column=c_end)

        c3 = ws_dash.cell(row=3, column=c_start, value=title)
        c3.font = Font(bold=True, size=9.5, color="FFFFFF", name="Calibri")
        c3.fill = PatternFill(fill_type='solid', fgColor=color)
        c3.alignment = Alignment(horizontal="center", vertical="center")

        c4 = ws_dash.cell(row=4, column=c_start, value=value)
        c4.font = Font(bold=True, size=13, color=color, name="Calibri")
        c4.fill = PatternFill(fill_type='solid', fgColor="F2F5F9")
        c4.alignment = Alignment(horizontal="center", vertical="center")

        c5 = ws_dash.cell(row=5, column=c_start, value=subtext)
        c5.font = Font(size=8, italic=True, color="555555", name="Calibri")
        c5.fill = PatternFill(fill_type='solid', fgColor="F2F5F9")
        c5.alignment = Alignment(horizontal="center", vertical="center")

        for r in range(3, 6):
            for col in range(c_start, c_end + 1):
                ws_dash.cell(row=r, column=col).border = border_thin

    # نوار اطلاعات زمان و قیمت‌ها
    ws_dash.merge_cells("A7:J7")
    info_bar = ws_dash["A7"]
    info_bar.value = f"⏱ آخرین به‌روزرسانی قیمت‌ها: {now_str}  |  💰 میانگین قیمت اقلام موجود: {avg_global_price_toman:,} تومان  |  🔺 بالاترین قیمت: {max_price_toman:,} تومان  |  🔻 پایین‌ترین قیمت: {min_price_toman:,} تومان"
    info_bar.font = Font(bold=True, size=9.5, color="1F4E79", name="Calibri")
    info_bar.fill = PatternFill(fill_type='solid', fgColor="E2EFDA")
    info_bar.alignment = Alignment(horizontal="center", vertical="center")
    info_bar.border = border_thin
    ws_dash.row_dimensions[7].height = 24

    # ── ۳. جدول تفکیک دسته‌بندی‌ها (Summary Table) ──
    table_headers = [
        ("ردیف", 8),
        ("نام دسته‌بندی اصلی", 25),
        ("تعداد زیردسته / برند", 20),
        ("کل اقلام و تنوع‌ها", 18),
        ("ثبت‌شده در سایت", 16),
        ("نیازمند ثبت در سایت", 18),
        ("میانگین قیمت (تومان)", 20),
        ("درصد پوشش در سایت", 18),
    ]

    ws_dash.merge_cells("A9:H9")
    t_header = ws_dash["A9"]
    t_header.value = "📋 جدول تفکیک وضعیت دسته‌بندی‌های فروشگاه حسینی کالا"
    t_header.font = Font(bold=True, size=11, color="1F4E79", name="Calibri")
    t_header.alignment = Alignment(horizontal="right", vertical="center")

    ws_dash.row_dimensions[10].height = 26
    for c_i, (h_text, w) in enumerate(table_headers, start=1):
        cell = ws_dash.cell(row=10, column=c_i, value=h_text)
        cell.font = Font(bold=True, color="FFFFFF", size=9.5, name="Calibri")
        cell.fill = PatternFill(fill_type='solid', fgColor="1F4E79")
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border_thin
        ws_dash.column_dimensions[get_column_letter(c_i)].width = w

    t_row_start = 11
    for idx, stat in enumerate(category_stats, start=1):
        r_num = t_row_start + idx - 1
        ws_dash.row_dimensions[r_num].height = 20
        coverage_pct = f"{round((stat['in_site'] / stat['total_items'] * 100), 1)}%" if stat['total_items'] else "0%"

        row_vals = [
            (idx, "center", False),
            (stat["name"], "right", True),
            (stat["subcats_count"], "center", False),
            (stat["total_items"], "center", True),
            (stat["in_site"], "center", False),
            (stat["missing"], "center", False),
            (stat["avg_price_toman"], "center", False),
            (coverage_pct, "center", False),
        ]

        r_fill = PatternFill(fill_type='solid', fgColor="FFFFFF" if idx % 2 != 0 else "F9FAFB")
        for col_i, (val, aln_mode, is_bold) in enumerate(row_vals, start=1):
            c = ws_dash.cell(row=r_num, column=col_i, value=val)
            c.fill = r_fill
            c.alignment = Alignment(horizontal=aln_mode, vertical="center")
            c.border = border_thin
            c.font = Font(size=9.5, bold=is_bold, name="Calibri")
            if col_i == 7 and isinstance(val, int) and val > 0:
                c.number_format = '#,##0'
            if col_i == 5 and val > 0:
                c.font = Font(bold=True, color="27AE60", size=9.5, name="Calibri")
            if col_i == 6 and val > 0:
                c.font = Font(color="806000", size=9.5, name="Calibri")

    # سطر مجموع جدول
    tot_row = t_row_start + len(category_stats)
    ws_dash.row_dimensions[tot_row].height = 22
    tot_vals = [
        "مجموع",
        f"{len(category_stats)} دسته",
        subcats_count_global,
        total_products_global,
        total_in_site,
        total_missing,
        avg_global_price_toman,
        f"{round((total_in_site/total_products_global)*100, 1)}%",
    ]
    ws_dash.merge_cells(start_row=tot_row, start_column=1, end_row=tot_row, end_column=2)
    for col_i, val in enumerate(tot_vals, start=1):
        if col_i == 2: continue
        target_col = 1 if col_i == 1 else col_i
        c = ws_dash.cell(row=tot_row, column=target_col, value=val)
        c.fill = PatternFill(fill_type='solid', fgColor="D9E1F2")
        c.font = Font(bold=True, size=10, color="1F4E79", name="Calibri")
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.border = border_thin
        if col_i == 7 and isinstance(val, int):
            c.number_format = '#,##0'

    # ── ۴. نمودارهای اکسل (Excel Charts) ──
    # نمودار ۱: نمودار میله‌ای توزیع کالاها در دسته‌بندی‌ها
    chart_bar = BarChart()
    chart_bar.type = "col"
    chart_bar.style = 10
    chart_bar.title = "توزیع تعداد کالاها در هر دسته‌بندی"
    chart_bar.y_axis.title = "تعداد کالا"
    chart_bar.x_axis.title = "دسته‌بندی"
    chart_bar.height = 11
    chart_bar.width = 16

    data_ref = Reference(ws_dash, min_col=4, min_row=10, max_row=10 + len(category_stats))
    cats_ref = Reference(ws_dash, min_col=2, min_row=11, max_row=10 + len(category_stats))
    chart_bar.add_data(data_ref, titles_from_data=True)
    chart_bar.set_categories(cats_ref)
    ws_dash.add_chart(chart_bar, "J9")

    # جدول داده‌های وضعیت ثبت برای نمودار دونات
    donut_data_start = tot_row + 2
    ws_dash.cell(row=donut_data_start, column=1, value="وضعیت ثبت کالا")
    ws_dash.cell(row=donut_data_start, column=2, value="تعداد")
    ws_dash.cell(row=donut_data_start + 1, column=1, value="ثبت‌شده در سایت")
    ws_dash.cell(row=donut_data_start + 1, column=2, value=total_in_site)
    ws_dash.cell(row=donut_data_start + 2, column=1, value="نیازمند ثبت در سایت")
    ws_dash.cell(row=donut_data_start + 2, column=2, value=total_missing)

    for r in range(donut_data_start, donut_data_start + 3):
        for c in range(1, 3):
            ws_dash.cell(row=r, column=c).font = Font(size=8, color="888888")

    # نمودار ۲: نمودار دونات نسبت ثبت در سایت
    chart_pie = DoughnutChart()
    chart_pie.title = "نسبت محصولات موجود در سایت به اقلام جدید"
    chart_pie.style = 2
    chart_pie.height = 11
    chart_pie.width = 14

    pie_data = Reference(ws_dash, min_col=2, min_row=donut_data_start, max_row=donut_data_start + 2)
    pie_cats = Reference(ws_dash, min_col=1, min_row=donut_data_start + 1, max_row=donut_data_start + 2)
    chart_pie.add_data(pie_data, titles_from_data=True)
    chart_pie.set_categories(pie_cats)
    ws_dash.add_chart(chart_pie, "J25")

    # ── ۵. راهنمای استفاده و توضیحات کاربری (در زیر نمودارها و جداول) ──
    guide_start_row = 38
    ws_dash.merge_cells(start_row=guide_start_row, start_column=1, end_row=guide_start_row, end_column=10)
    g_title = ws_dash.cell(row=guide_start_row, column=1, value="📖 راهنمای جامع استفاده، ساختار ستون‌ها و به‌روزرسانی قیمت‌ها")
    g_title.font = Font(bold=True, size=12, color="FFFFFF", name="Calibri")
    g_title.fill = PatternFill(fill_type='solid', fgColor="1F4E79")
    g_title.alignment = Alignment(horizontal="right", vertical="center")
    ws_dash.row_dimensions[guide_start_row].height = 28

    guide_entries = [
        ("ستون‌های شیت‌ها (از راست به چپ):", ""),
        ("• نام محصول (ستون A):", "نام کامل و استاندارد کالا (شامل سطر والد یا سطرهای مجزای رنگ/مدل با تورفتگی ↳)."),
        ("• قیمت عادی (ریال) (ستون B):", "قیمت پایه بدون تخفیف به ریال (عدد خالص). به صورت خودکار ۳ رقم ۳ رقم تفکیک می‌شود (#,##0)."),
        ("• قیمت عادی (تومان) (ستون C):", "محاسبه خودکار با فرمول اکسل (=B2/10). با وارد کردن قیمت ریال، معادل تومان بلافاصله نمایش داده می‌شود."),
        ("• قیمت حراج (ریال و تومان) (ستون D و E):", "قیمت با تخفیف کالا در فروشگاه (در صورت وجود تخفیف فعال در سایت)."),
        ("• وضعیت موجودی (ستون F):", "دارای دکمه و منوی کشویی (Dropdown) جهت تغییر سریع موجودی بین گزینه‌های «موجود» و «ناموجود»."),
        ("• دسته‌بندی و نوع محصول (ستون G و H):", "مسیر دسته‌بندی و نوع کالا (ساده: قیمت ثابت | متغیر: کالای چندرنگ | تنوع: رنگ اختصاصی)."),
        ("• شناسه‌ها و لینک (ستون I تا L):", "شامل Product ID و Variation ID جهت اتصال دوطرفه به وردپرس و لینک مستقیم عددی ?p=ID بدون خطای انکودینگ."),
        ("", ""),
        ("راهنمای رنگ‌بندی سطرها:", ""),
        ("• آبی ملایم:", "سطر والد محصولات متغیر (کالاهایی که دارای چند رنگ یا مشخصه هستند)."),
        ("• خاکستری روشن:", "سطرهای تنوع اختصاصی هر رنگ/مدل با قیمت و شناسه تنوع (Variation ID) مجزا."),
        ("• زرد ملایم:", "کالاهایی که هنوز روی سایت ایجاد یا منتشر نشده‌اند (قیمت‌ها خالی و آماده ورود اطلاعات)."),
        ("• سفید:", "کالاهای ساده موجود در سایت با اطلاعات و قیمت کامل."),
        ("", ""),
        ("دستورالعمل به‌روزرسانی قیمت‌ها به سایت:", ""),
        ("۱. قیمت‌های جدید را در ستون 'قیمت عادی (ریال)' هر شیت ویرایش یا وارد کنید (ستون تومان به صورت خودکار آپدیت می‌شود).", ""),
        ("۲. در صورت نیاز وضعیت موجودی را از منوی کشویی تنظیم نمایید.", ""),
        ("۳. دستور زیر را در ترمینال اجرا کنید تا قیمت‌ها مستقیماً روی فروشگاه اینترنتی اعمال شوند:", ""),
        ("   python scripts/update_prices.py --apply", ""),
    ]

    for g_idx, (g_col1, g_col2) in enumerate(guide_entries, start=guide_start_row + 2):
        ws_dash.cell(row=g_idx, column=1, value=g_col1)
        ws_dash.cell(row=g_idx, column=2, value=g_col2)
        ws_dash.merge_cells(start_row=g_idx, start_column=2, end_row=g_idx, end_column=10)

        c1 = ws_dash.cell(row=g_idx, column=1)
        c2 = ws_dash.cell(row=g_idx, column=2)

        c1.alignment = Alignment(horizontal="right", vertical="center")
        c2.alignment = Alignment(horizontal="right", vertical="center")

        if g_col1.startswith("ستون‌های") or g_col1.startswith("راهنمای") or g_col1.startswith("دستورالعمل"):
            c1.font = Font(bold=True, size=10.5, color="1F4E79", name="Calibri")
            c2.font = Font(bold=True, size=10.5, color="1F4E79", name="Calibri")
        elif "update_prices.py" in g_col1:
            c1.font = Font(bold=True, color="2E75B6", size=10, name="Consolas")
        else:
            c1.font = Font(bold=True, size=9.5, color="333333", name="Calibri")
            c2.font = Font(size=9.5, color="555555", name="Calibri")

    try:
        wb.save(EXCEL_OUTPUT)
        final_file = EXCEL_OUTPUT
    except PermissionError:
        wb.save(EXCEL_UPDATED)
        final_file = EXCEL_UPDATED
        print(f"⚠️ فایل اصلی در اکسل باز است. فایل در مسیر زیر ذخیره شد:\n   {EXCEL_UPDATED}")

    print("=" * 60)
    print("✓ ساخت کاتالوگ جامع با داشبورد مدیریتی و نمودارها به پایان رسید.")
    print(f"📁 مسیر فایل خروجی: {final_file}")
    print(f"📊 کل دسته‌بندی‌ها: {len(STRUCTURE)}")
    print(f"🏢 کل زیردسته‌ها و برندها: {subcats_count_global}")
    print(f"📦 کل اقلام و تنوع‌ها: {total_products_global}")
    print(f"✅ ثبت‌شده در سایت: {total_in_site}")
    print(f"🟡 نیازمند ثبت در سایت: {total_missing}")
    print("=" * 60)

if __name__ == '__main__':
    build_full_catalog_with_dashboard()

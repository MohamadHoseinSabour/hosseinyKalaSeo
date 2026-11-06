import os
import sys
import json
import shutil
import datetime
from collections import OrderedDict
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import FormulaRule

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.xlsx')
PUBLISHED_PATH = os.path.join(PROJECT_DIR, 'scratch', 'published_5_tvs_result.json')
ID_MAPPINGS_PATH = os.path.join(PROJECT_DIR, 'data', 'id_mappings.json')
PRODUCTS_JSON_PATH = os.path.join(PROJECT_DIR, 'data', 'products.json')

# Styling Palette
COLOR_BORDER = "D9D9D9"
COLOR_BANNER_BG = "EBF1F5"
COLOR_BANNER_TEXT = "375623"

FONT_BANNER = Font(name="Calibri", size=10, bold=True, color=COLOR_BANNER_TEXT)
FONT_REGULAR = Font(name="Calibri", size=9.5, bold=False, color="000000")
FONT_LINK = Font(name="Calibri", size=9.5, color="0563C1", underline="single")
FONT_STOCK_RED = Font(name="Calibri", size=10, bold=True, color="721C24")

FILL_BANNER = PatternFill(start_color=COLOR_BANNER_BG, end_color=COLOR_BANNER_BG, fill_type="solid")
FILL_STOCK_RED = PatternFill(start_color="FFF8D7DA", end_color="FFF8D7DA", fill_type="solid")
FILL_STOCK_GREEN = PatternFill(start_color="FFD4EDDA", end_color="FFD4EDDA", fill_type="solid")
FONT_STOCK_GREEN = Font(color="FF155724", bold=True)

FILL_WARNING_ORANGE = PatternFill(start_color="FFFCE4D6", end_color="FFFCE4D6", fill_type="solid")
FONT_WARNING_ORANGE = Font(color="FFC65911", bold=True)

FILL_PARENT_PRICE_RED = PatternFill(start_color="FFFCE8E6", end_color="FFFCE8E6", fill_type="solid")
FONT_PARENT_PRICE_RED = Font(color="FFC00000", bold=True)

FILL_ROW_HOLD = PatternFill(start_color="FFFCE4D6", end_color="FFFCE4D6", fill_type="solid")
FILL_ROW_UNREG = PatternFill(start_color="FFFFF2CC", end_color="FFFFF2CC", fill_type="solid")

def get_border():
    s = Side(style='thin', color=COLOR_BORDER)
    return Border(top=s, bottom=s, left=s, right=s)

BORDER_THIN = get_border()

CATEGORY_SHEETS = [
    'یخچال و فریزر', 'شستشو و نظافت', 'لوازم برقی و پخت و پز', 'نوشیدنی ساز',
    'سرمایش و گرمایش', 'تصفیه کننده آب', 'صوتی و تصویری', 'زیبایی و سلامت فردی'
]

def add_product_row(ws, r, name, brand, pid, link, sku):
    ws.cell(r, 1, name)
    ws.cell(r, 2, None)
    ws.cell(r, 3, f'=IF(OR(ISBLANK(B{r}),B{r}=""),"",IF($L{r}="متغیر","⚠️ والد متغیر نباید قیمت داشته باشد",B{r}/10))')
    ws.cell(r, 4, None)
    ws.cell(r, 5, f'=IF(OR(ISBLANK(B{r}),B{r}="",ISBLANK(D{r}),D{r}="",D{r}<=0,$L{r}="متغیر"),"",(B{r}-D{r})/D{r})')
    ws.cell(r, 6, None)
    ws.cell(r, 7, f'=IF(OR(ISBLANK(F{r}),F{r}=""),"",IF($L{r}="متغیر","",F{r}/10))')
    cell_h = ws.cell(r, 8, "ناموجود")
    cell_h.font = FONT_STOCK_RED
    cell_h.fill = FILL_STOCK_RED
    ws.cell(r, 9, "صوتی و تصویری")
    ws.cell(r, 10, "تلویزیون")
    ws.cell(r, 11, brand)
    ws.cell(r, 12, "ساده")
    ws.cell(r, 13, None)
    ws.cell(r, 14, pid)
    ws.cell(r, 15, None)
    cell_p = ws.cell(r, 16, link)
    cell_p.hyperlink = link
    cell_p.font = FONT_LINK
    ws.cell(r, 17, sku)
    ws.cell(r, 18, "ثبت‌شده در سایت")

    for c in range(1, 19):
        cell = ws.cell(r, c)
        cell.border = BORDER_THIN
        if c == 1:
            cell.alignment = Alignment(horizontal="right", vertical="center")
        else:
            cell.alignment = Alignment(horizontal="center", vertical="center")
        if c in [2, 3, 4, 6, 7]:
            cell.number_format = '#,##0'
        elif c == 5:
            cell.number_format = '0.0%'
    ws.row_dimensions[r].height = 20

def add_banner_row(ws, r, brand_name):
    ws.cell(r, 1, f"  📂 صوتی و تصویری  ◀  {brand_name}")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=18)
    for c in range(1, 19):
        cell = ws.cell(r, c)
        cell.fill = FILL_BANNER
        cell.font = FONT_BANNER
        cell.border = BORDER_THIN
        cell.alignment = Alignment(horizontal="right", vertical="center")
    ws.row_dimensions[r].height = 22

def main():
    print("=== ۱. ایجاد نسخه‌های پشتیبان ===", flush=True)
    now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_cat = os.path.join(PROJECT_DIR, f'hosseiny_kala_catalog.backup_before_5_tvs_sync_{now_str}.xlsx')
    shutil.copy2(CATALOG_PATH, backup_cat)
    shutil.copy2(ID_MAPPINGS_PATH, ID_MAPPINGS_PATH + f'.bak_{now_str}')
    shutil.copy2(PRODUCTS_JSON_PATH, PRODUCTS_JSON_PATH + f'.bak_{now_str}')
    print(f"✓ بکاپ کاتالوگ ایجاد شد: {os.path.basename(backup_cat)}", flush=True)

    with open(PUBLISHED_PATH, 'r', encoding='utf-8') as f:
        published_map = json.load(f)

    wb = openpyxl.load_workbook(CATALOG_PATH, data_only=False)
    ws_av = wb['صوتی و تصویری']

    print("\n=== ۲. افزودن ۵ تلویزیون جدید به شیت «صوتی و تصویری» ===", flush=True)
    
    # برند ایکس ویژن
    r = ws_av.max_row + 1
    add_banner_row(ws_av, r, "ایکس ویژن")
    r += 1
    p_xv = published_map["xvision-43-inch-43xt515-smart-tv"]
    add_product_row(ws_av, r, p_xv['name'], "ایکس ویژن", p_xv['product_id'], p_xv['permalink'], p_xv['sku'])
    print(f"✓ سطر {r}: {p_xv['name']}", flush=True)

    # برند توشیبا (۳ مدل: 50, 55, 43)
    r += 1
    add_banner_row(ws_av, r, "توشیبا")
    
    for slug in ["toshiba-50-inch-50l2300ee-led-tv", "toshiba-55-inch-4k-smart-led-tv", "toshiba-43-inch-fhd-led-tv"]:
        r += 1
        p_tosh = published_map[slug]
        add_product_row(ws_av, r, p_tosh['name'], "توشیبا", p_tosh['product_id'], p_tosh['permalink'], p_tosh['sku'])
        print(f"✓ سطر {r}: {p_tosh['name']}", flush=True)

    # برند هایسنس (مدل 43)
    r += 1
    add_banner_row(ws_av, r, "هایسنس")
    r += 1
    p_his = published_map["hisense-43-inch-4k-smart-tv"]
    add_product_row(ws_av, r, p_his['name'], "هایسنس", p_his['product_id'], p_his['permalink'], p_his['sku'])
    print(f"✓ سطر {r}: {p_his['name']}", flush=True)

    # به‌روزرسانی فرمت‌بندی شرطی شیت صوتی و تصویری
    final_max_r = ws_av.max_row
    ws_av.conditional_formatting._cf_rules = OrderedDict()
    ws_av.conditional_formatting.max_priority = 0

    rule_stock_red = FormulaRule(formula=[f'ISNUMBER(SEARCH("ناموجود", H2))'], stopIfTrue=True, fill=FILL_STOCK_RED, font=FONT_STOCK_RED)
    rule_stock_red.priority = 1
    rule_stock_green = FormulaRule(formula=[f'AND(ISNUMBER(SEARCH("موجود", H2)), NOT(ISNUMBER(SEARCH("ناموجود", H2))))'], stopIfTrue=True, fill=FILL_STOCK_GREEN, font=FONT_STOCK_GREEN)
    rule_stock_green.priority = 2
    ws_av.conditional_formatting.add(f"H2:H{final_max_r}", rule_stock_red)
    ws_av.conditional_formatting.add(f"H2:H{final_max_r}", rule_stock_green)

    rule_parent_b = FormulaRule(formula=[f'AND($L2="متغیر", OR(ISNUMBER(B2), ISNUMBER(F2)))'], stopIfTrue=True, fill=FILL_PARENT_PRICE_RED, font=FONT_PARENT_PRICE_RED)
    rule_parent_b.priority = 3
    ws_av.conditional_formatting.add(f"B2:B{final_max_r}", rule_parent_b)

    rule_parent_f = FormulaRule(formula=[f'AND($L2="متغیر", OR(ISNUMBER(B2), ISNUMBER(F2)))'], stopIfTrue=True, fill=FILL_PARENT_PRICE_RED, font=FONT_PARENT_PRICE_RED)
    rule_parent_f.priority = 4
    ws_av.conditional_formatting.add(f"F2:F{final_max_r}", rule_parent_f)

    rule_price_b = FormulaRule(formula=[f'AND(ISNUMBER($B2), ISNUMBER($D2), $D2>0, ABS(($B2-$D2)/$D2)>=0.5, $L2<>"متغیر")'], stopIfTrue=True, fill=FILL_WARNING_ORANGE, font=FONT_WARNING_ORANGE)
    rule_price_b.priority = 5
    ws_av.conditional_formatting.add(f"B2:B{final_max_r}", rule_price_b)

    rule_price_e = FormulaRule(formula=[f'AND(ISNUMBER($B2), ISNUMBER($D2), $D2>0, ABS(($B2-$D2)/$D2)>=0.5, $L2<>"متغیر")'], stopIfTrue=True, fill=FILL_WARNING_ORANGE, font=FONT_WARNING_ORANGE)
    rule_price_e.priority = 6
    ws_av.conditional_formatting.add(f"E2:E{final_max_r}", rule_price_e)

    rule_row_hold = FormulaRule(formula=[f'$R2="فعلا دست نگه دار"'], stopIfTrue=False, fill=FILL_ROW_HOLD)
    rule_row_hold.priority = 7
    rule_row_unreg = FormulaRule(formula=[f'$R2="در سایت تعریف نشده"'], stopIfTrue=False, fill=FILL_ROW_UNREG)
    rule_row_unreg.priority = 8
    ws_av.conditional_formatting.add(f"A2:R{final_max_r}", rule_row_hold)
    ws_av.conditional_formatting.add(f"A2:R{final_max_r}", rule_row_unreg)

    print("\n=== ۳. به‌روزرسانی داشبورد مدیریتی (📊 خلاصه و داشبورد) ===", flush=True)
    ws_dash = wb['📊 خلاصه و داشبورد']

    sheet_stats = {}
    for sname in CATEGORY_SHEETS:
        ws_temp = wb[sname]
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
        ws_temp = wb[sname]
        for r_idx in range(2, ws_temp.max_row + 1):
            val_a = ws_temp.cell(r_idx, 1).value
            if not val_a or '📂' in str(val_a):
                continue
            if str(ws_temp.cell(r_idx, 12).value or '').strip() != 'تنوع':
                if str(ws_temp.cell(r_idx, 18).value or '').strip() == 'ثبت‌شده در سایت':
                    site_registered_count += 1

    print(f"آمار جدید: محصولات اصلی={total_main} | ثبت‌شده در سایت={site_registered_count} | موجود={total_in_stock} | ناموجود={total_out_stock}", flush=True)

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

    wb.save(CATALOG_PATH)
    print(f"✓ فایل اکسل کاتالوگ با موفقیت ذخیره گردید: {os.path.basename(CATALOG_PATH)}", flush=True)

    print("\n=== ۴. به‌روزرسانی دیتابیس‌های id_mappings.json و products.json ===", flush=True)
    with open(ID_MAPPINGS_PATH, 'r', encoding='utf-8') as f:
        id_mappings = json.load(f)

    with open(PRODUCTS_JSON_PATH, 'r', encoding='utf-8') as f:
        products_list = json.load(f)

    existing_pids = {p['id'] for p in products_list}

    for slug, p in published_map.items():
        pid = p['product_id']
        id_mappings[str(pid)] = {
            'name': p['name'],
            'slug': slug,
            'type': 'simple',
            'url': p['permalink'],
            'price': 0
        }

        if pid not in existing_pids:
            with open(os.path.join(PROJECT_DIR, 'data', 'new_products', slug, 'info.json'), 'r', encoding='utf-8') as inf_f:
                inf = json.load(inf_f)

            products_list.append({
                'id': pid,
                'url': p['permalink'],
                'slug': slug,
                'name': p['name'],
                'type': 'simple',
                'status': 'publish',
                'price': '0',
                'regular_price': '',
                'sale_price': '',
                'currency': 'IRT',
                'in_stock': False,
                'stock_status': 'outofstock',
                'categories': [{'id': 243, 'name': 'تلویزیون', 'slug': 'audio-video/television'}],
                'featured_image': p['media_url'],
                'short_description': inf['short_description'],
                'description': inf['description'],
                'date': p['published_at'],
                'modified': p['published_at']
            })

    with open(ID_MAPPINGS_PATH, 'w', encoding='utf-8') as f:
        json.dump(id_mappings, f, ensure_ascii=False, indent=2)
    print(f"✓ دیتابیس id_mappings.json به‌روز شد (تعداد کل: {len(id_mappings)})", flush=True)

    with open(PRODUCTS_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(products_list, f, ensure_ascii=False, indent=2)
    print(f"✓ دیتابیس products.json به‌روز شد (تعداد کل: {len(products_list)})", flush=True)

    print("\n✅ همگام‌سازی کامل ۵ تلویزیون جدید انجام شد.", flush=True)

if __name__ == '__main__':
    main()

import os
import sys
import json
import shutil
import datetime
from collections import OrderedDict
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
from openpyxl.utils import get_column_letter

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.xlsx')
PUBLISHED_PATH = os.path.join(PROJECT_DIR, 'scratch', 'published_2_products_result.json')
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

ALIGN_RIGHT = Alignment(horizontal="right", vertical="center")
ALIGN_CENTER = Alignment(horizontal="center", vertical="center")

def get_border():
    s = Side(style='thin', color=COLOR_BORDER)
    return Border(top=s, bottom=s, left=s, right=s)

BORDER_THIN = get_border()

CATEGORY_SHEETS = [
    'یخچال و فریزر', 'شستشو و نظافت', 'لوازم برقی و پخت و پز', 'نوشیدنی ساز',
    'سرمایش و گرمایش', 'تصفیه کننده آب', 'صوتی و تصویری', 'زیبایی و سلامت فردی'
]

def main():
    print("=== ۱. ایجاد نسخه‌های پشتیبان ===")
    now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_cat = os.path.join(PROJECT_DIR, f'hosseiny_kala_catalog.backup_before_2_new_sync_{now_str}.xlsx')
    shutil.copy2(CATALOG_PATH, backup_cat)
    shutil.copy2(ID_MAPPINGS_PATH, ID_MAPPINGS_PATH + f'.bak_{now_str}')
    shutil.copy2(PRODUCTS_JSON_PATH, PRODUCTS_JSON_PATH + f'.bak_{now_str}')
    print(f"✓ بکاپ کاتالوگ ایجاد شد: {os.path.basename(backup_cat)}")

    with open(PUBLISHED_PATH, 'r', encoding='utf-8') as f:
        published_map = json.load(f)

    candy_pub = published_map["candy-kcv-325-g-vacuum-cleaner"]
    olive_pub = published_map["olive-43-inch-ol-43fss30-smart-tv"]

    wb = openpyxl.load_workbook(CATALOG_PATH, data_only=False)

    print("\n=== ۲. افزودن جاروبرقی کندی به شیت «شستشو و نظافت» ===")
    ws_wash = wb['شستشو و نظافت']
    r_wash_banner = ws_wash.max_row + 1
    ws_wash.cell(r_wash_banner, 1, "  📂 شستشو و نظافت  ◀  کندی")
    ws_wash.merge_cells(start_row=r_wash_banner, start_column=1, end_row=r_wash_banner, end_column=18)
    for c in range(1, 19):
        cell = ws_wash.cell(r_wash_banner, c)
        cell.fill = FILL_BANNER
        cell.font = FONT_BANNER
        cell.border = BORDER_THIN
        cell.alignment = ALIGN_RIGHT
    ws_wash.row_dimensions[r_wash_banner].height = 22

    r_candy = r_wash_banner + 1
    ws_wash.cell(r_candy, 1, candy_pub['name'])
    ws_wash.cell(r_candy, 2, 24449000) # قیمت مصرف‌کننده ریال
    ws_wash.cell(r_candy, 3, f'=IF(OR(ISBLANK(B{r_candy}),B{r_candy}=""),"",IF($L{r_candy}="متغیر","⚠️ والد متغیر نباید قیمت داشته باشد",B{r_candy}/10))')
    ws_wash.cell(r_candy, 4, 24449000)
    ws_wash.cell(r_candy, 5, f'=IF(OR(ISBLANK(B{r_candy}),B{r_candy}="",ISBLANK(D{r_candy}),D{r_candy}="",D{r_candy}<=0,$L{r_candy}="متغیر"),"",(B{r_candy}-D{r_candy})/D{r_candy})')
    ws_wash.cell(r_candy, 6, None)
    ws_wash.cell(r_candy, 7, f'=IF(OR(ISBLANK(F{r_candy}),F{r_candy}=""),"",IF($L{r_candy}="متغیر","",F{r_candy}/10))')
    cell_h = ws_wash.cell(r_candy, 8, "ناموجود")
    cell_h.font = FONT_STOCK_RED
    cell_h.fill = FILL_STOCK_RED
    ws_wash.cell(r_candy, 9, "شستشو و نظافت")
    ws_wash.cell(r_candy, 10, "جاروبرقی")
    ws_wash.cell(r_candy, 11, "کندی")
    ws_wash.cell(r_candy, 12, "ساده")
    ws_wash.cell(r_candy, 13, None)
    ws_wash.cell(r_candy, 14, candy_pub['product_id'])
    ws_wash.cell(r_candy, 15, None)
    cell_p = ws_wash.cell(r_candy, 16, candy_pub['permalink'])
    cell_p.hyperlink = candy_pub['permalink']
    cell_p.font = FONT_LINK
    ws_wash.cell(r_candy, 17, candy_pub['sku'])
    ws_wash.cell(r_candy, 18, "ثبت‌شده در سایت")

    for c in range(1, 19):
        cell = ws_wash.cell(r_candy, c)
        cell.border = BORDER_THIN
        if c == 1:
            cell.alignment = ALIGN_RIGHT
        else:
            cell.alignment = ALIGN_CENTER
        if c in [2, 3, 4, 6, 7]:
            cell.number_format = '#,##0'
        elif c == 5:
            cell.number_format = '0.0%'
    ws_wash.row_dimensions[r_candy].height = 20
    print(f"✓ جاروبرقی کندی در سطر {r_candy} شیت «شستشو و نظافت» اضافه شد.")

    print("\n=== ۳. افزودن تلویزیون الیو به شیت «صوتی و تصویری» ===")
    ws_av = wb['صوتی و تصویری']
    r_av_banner = ws_av.max_row + 1
    ws_av.cell(r_av_banner, 1, "  📂 صوتی و تصویری  ◀  الیو")
    ws_av.merge_cells(start_row=r_av_banner, start_column=1, end_row=r_av_banner, end_column=18)
    for c in range(1, 19):
        cell = ws_av.cell(r_av_banner, c)
        cell.fill = FILL_BANNER
        cell.font = FONT_BANNER
        cell.border = BORDER_THIN
        cell.alignment = ALIGN_RIGHT
    ws_av.row_dimensions[r_av_banner].height = 22

    r_olive = r_av_banner + 1
    ws_av.cell(r_olive, 1, olive_pub['name'])
    ws_av.cell(r_olive, 2, None)
    ws_av.cell(r_olive, 3, f'=IF(OR(ISBLANK(B{r_olive}),B{r_olive}=""),"",IF($L{r_olive}="متغیر","⚠️ والد متغیر نباید قیمت داشته باشد",B{r_olive}/10))')
    ws_av.cell(r_olive, 4, None)
    ws_av.cell(r_olive, 5, f'=IF(OR(ISBLANK(B{r_olive}),B{r_olive}="",ISBLANK(D{r_olive}),D{r_olive}="",D{r_olive}<=0,$L{r_olive}="متغیر"),"",(B{r_olive}-D{r_olive})/D{r_olive})')
    ws_av.cell(r_olive, 6, None)
    ws_av.cell(r_olive, 7, f'=IF(OR(ISBLANK(F{r_olive}),F{r_olive}=""),"",IF($L{r_olive}="متغیر","",F{r_olive}/10))')
    cell_h_ol = ws_av.cell(r_olive, 8, "ناموجود")
    cell_h_ol.font = FONT_STOCK_RED
    cell_h_ol.fill = FILL_STOCK_RED
    ws_av.cell(r_olive, 9, "صوتی و تصویری")
    ws_av.cell(r_olive, 10, "تلویزیون")
    ws_av.cell(r_olive, 11, "الیو")
    ws_av.cell(r_olive, 12, "ساده")
    ws_av.cell(r_olive, 13, None)
    ws_av.cell(r_olive, 14, olive_pub['product_id'])
    ws_av.cell(r_olive, 15, None)
    cell_p_ol = ws_av.cell(r_olive, 16, olive_pub['permalink'])
    cell_p_ol.hyperlink = olive_pub['permalink']
    cell_p_ol.font = FONT_LINK
    ws_av.cell(r_olive, 17, olive_pub['sku'])
    ws_av.cell(r_olive, 18, "ثبت‌شده در سایت")

    for c in range(1, 19):
        cell = ws_av.cell(r_olive, c)
        cell.border = BORDER_THIN
        if c == 1:
            cell.alignment = ALIGN_RIGHT
        else:
            cell.alignment = ALIGN_CENTER
        if c in [2, 3, 4, 6, 7]:
            cell.number_format = '#,##0'
        elif c == 5:
            cell.number_format = '0.0%'
    ws_av.row_dimensions[r_olive].height = 20
    print(f"✓ تلویزیون الیو در سطر {r_olive} شیت «صوتی و تصویری» اضافه شد.")

    # ۴. به‌روزرسانی قوانین اعتبارسنجی و فرمت‌بندی شرطی
    for ws_target in [ws_wash, ws_av]:
        final_max_r = ws_target.max_row
        ws_target.conditional_formatting._cf_rules = OrderedDict()
        ws_target.conditional_formatting.max_priority = 0

        rule_stock_red = FormulaRule(formula=[f'ISNUMBER(SEARCH("ناموجود", H2))'], stopIfTrue=True, fill=FILL_STOCK_RED, font=FONT_STOCK_RED)
        rule_stock_red.priority = 1
        rule_stock_green = FormulaRule(formula=[f'AND(ISNUMBER(SEARCH("موجود", H2)), NOT(ISNUMBER(SEARCH("ناموجود", H2))))'], stopIfTrue=True, fill=FILL_STOCK_GREEN, font=FONT_STOCK_GREEN)
        rule_stock_green.priority = 2
        ws_target.conditional_formatting.add(f"H2:H{final_max_r}", rule_stock_red)
        ws_target.conditional_formatting.add(f"H2:H{final_max_r}", rule_stock_green)

        rule_parent_b = FormulaRule(formula=[f'AND($L2="متغیر", OR(ISNUMBER(B2), ISNUMBER(F2)))'], stopIfTrue=True, fill=FILL_PARENT_PRICE_RED, font=FONT_PARENT_PRICE_RED)
        rule_parent_b.priority = 3
        ws_target.conditional_formatting.add(f"B2:B{final_max_r}", rule_parent_b)

        rule_parent_f = FormulaRule(formula=[f'AND($L2="متغیر", OR(ISNUMBER(B2), ISNUMBER(F2)))'], stopIfTrue=True, fill=FILL_PARENT_PRICE_RED, font=FONT_PARENT_PRICE_RED)
        rule_parent_f.priority = 4
        ws_target.conditional_formatting.add(f"F2:F{final_max_r}", rule_parent_f)

        rule_price_b = FormulaRule(formula=[f'AND(ISNUMBER($B2), ISNUMBER($D2), $D2>0, ABS(($B2-$D2)/$D2)>=0.5, $L2<>"متغیر")'], stopIfTrue=True, fill=FILL_WARNING_ORANGE, font=FONT_WARNING_ORANGE)
        rule_price_b.priority = 5
        ws_target.conditional_formatting.add(f"B2:B{final_max_r}", rule_price_b)

        rule_price_e = FormulaRule(formula=[f'AND(ISNUMBER($B2), ISNUMBER($D2), $D2>0, ABS(($B2-$D2)/$D2)>=0.5, $L2<>"متغیر")'], stopIfTrue=True, fill=FILL_WARNING_ORANGE, font=FONT_WARNING_ORANGE)
        rule_price_e.priority = 6
        ws_target.conditional_formatting.add(f"E2:E{final_max_r}", rule_price_e)

        rule_row_hold = FormulaRule(formula=[f'$R2="فعلا دست نگه دار"'], stopIfTrue=False, fill=FILL_ROW_HOLD)
        rule_row_hold.priority = 7
        rule_row_unreg = FormulaRule(formula=[f'$R2="در سایت تعریف نشده"'], stopIfTrue=False, fill=FILL_ROW_UNREG)
        rule_row_unreg.priority = 8
        ws_target.conditional_formatting.add(f"A2:R{final_max_r}", rule_row_hold)
        ws_target.conditional_formatting.add(f"A2:R{final_max_r}", rule_row_unreg)

    print("\n=== ۵. به‌روزرسانی داشبورد مدیریتی (📊 خلاصه و داشبورد) ===")
    ws_dash = wb['📊 خلاصه و داشبورد']

    sheet_stats = {}
    for sname in CATEGORY_SHEETS:
        ws_temp = wb[sname]
        main_count = 0
        vars_count = 0
        in_stock_count = 0
        out_stock_count = 0
        for r in range(2, ws_temp.max_row + 1):
            val_a = ws_temp.cell(r, 1).value
            if not val_a or '📂' in str(val_a):
                continue
            ptype = str(ws_temp.cell(r, 12).value or '').strip()
            if ptype == 'تنوع':
                vars_count += 1
            else:
                main_count += 1

            stk = str(ws_temp.cell(r, 8).value or '').strip()
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
        for r in range(2, ws_temp.max_row + 1):
            val_a = ws_temp.cell(r, 1).value
            if not val_a or '📂' in str(val_a):
                continue
            if str(ws_temp.cell(r, 12).value or '').strip() != 'تنوع':
                if str(ws_temp.cell(r, 18).value or '').strip() == 'ثبت‌شده در سایت':
                    site_registered_count += 1

    print(f"آمار جدید داشبورد: کل محصولات اصلی={total_main} | ثبت‌شده سایت={site_registered_count} | موجود={total_in_stock} | ناموجود={total_out_stock}")

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
    print(f"✓ فایل اکسل کاتالوگ با موفقیت ذخیره شد: {os.path.basename(CATALOG_PATH)}")

    print("\n=== ۶. به‌روزرسانی دیتابیس‌های id_mappings.json و products.json ===")
    with open(ID_MAPPINGS_PATH, 'r', encoding='utf-8') as f:
        id_mappings = json.load(f)

    for slug, p in [("candy-kcv-325-g-vacuum-cleaner", candy_pub), ("olive-43-inch-ol-43fss30-smart-tv", olive_pub)]:
        pid = p['product_id']
        id_mappings[str(pid)] = {
            'name': p['name'],
            'slug': slug,
            'type': 'simple',
            'url': p['permalink'],
            'price': 0
        }

    with open(ID_MAPPINGS_PATH, 'w', encoding='utf-8') as f:
        json.dump(id_mappings, f, ensure_ascii=False, indent=2)
    print(f"✓ دیتابیس id_mappings.json به‌روز شد (تعداد کل: {len(id_mappings)})")

    with open(PRODUCTS_JSON_PATH, 'r', encoding='utf-8') as f:
        products_list = json.load(f)

    existing_pids = {p['id'] for p in products_list}
    for slug, p, cat_id, cat_name, cat_slug in [
        ("candy-kcv-325-g-vacuum-cleaner", candy_pub, 21, "جاروبرقی", "washing-cleaning/%d8%ac%d8%a7%d8%b1%d9%88%d8%a8%d8%b1%d9%82%db%8c"),
        ("olive-43-inch-ol-43fss30-smart-tv", olive_pub, 243, "تلویزیون", "audio-video/television")
    ]:
        pid = p['product_id']
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
                'categories': [{'id': cat_id, 'name': cat_name, 'slug': cat_slug}],
                'featured_image': p['media_url'],
                'short_description': inf['short_description'],
                'description': inf['description'],
                'date': p['published_at'],
                'modified': p['published_at']
            })

    with open(PRODUCTS_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(products_list, f, ensure_ascii=False, indent=2)
    print(f"✓ دیتابیس products.json به‌روز شد (تعداد کل: {len(products_list)})")

    print("\n✅ همگام‌سازی کامل کاتالوگ و پایگاه‌های داده انجام گردید.")

if __name__ == '__main__':
    main()

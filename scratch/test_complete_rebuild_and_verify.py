import os
import sys
import json
import shutil
import openpyxl
from collections import OrderedDict
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
from openpyxl.utils import get_column_letter

sys.stdout.reconfigure(encoding='utf-8')

COLOR_HEADER_BG = "1F4E79"
COLOR_HEADER_TEXT = "FFFFFF"
COLOR_BANNER_BG = "EBF1F5"
COLOR_BANNER_TEXT = "375623"
COLOR_VAR_PARENT_BG = "D9E1F2"
COLOR_VARIATION_BG = "F2F2F2"
COLOR_BORDER = "D9D9D9"

FONT_BANNER = Font(name="Calibri", size=10, bold=True, color=COLOR_BANNER_TEXT)
FONT_PARENT = Font(name="Calibri", size=9.5, bold=True, color="000000")
FONT_CHILD = Font(name="Calibri", size=9, bold=False, color="000000")
FONT_SIMPLE_NAME = Font(name="Calibri", size=9.5, bold=True, color="000000")
FONT_REGULAR = Font(name="Calibri", size=9.5, bold=False, color="000000")
FONT_STOCK = Font(name="Calibri", size=10, bold=True, color="000000")

FILL_BANNER = PatternFill(start_color=COLOR_BANNER_BG, end_color=COLOR_BANNER_BG, fill_type="solid")
FILL_PARENT = PatternFill(start_color=COLOR_VAR_PARENT_BG, end_color=COLOR_VAR_PARENT_BG, fill_type="solid")
FILL_CHILD = PatternFill(start_color=COLOR_VARIATION_BG, end_color=COLOR_VARIATION_BG, fill_type="solid")

ALIGN_RIGHT = Alignment(horizontal="right", vertical="center")
ALIGN_CENTER = Alignment(horizontal="center", vertical="center")

def get_border():
    s = Side(style='thin', color=COLOR_BORDER)
    return Border(top=s, bottom=s, left=s, right=s)

BORDER_THIN = get_border()

# CF Fills and Fonts
fill_stock_red = PatternFill(start_color="FFF8D7DA", end_color="FFF8D7DA", fill_type="solid")
font_stock_red = Font(color="FF721C24", bold=True)

fill_stock_green = PatternFill(start_color="FFD4EDDA", end_color="FFD4EDDA", fill_type="solid")
font_stock_green = Font(color="FF155724", bold=True)

fill_warning_orange = PatternFill(start_color="FFFCE4D6", end_color="FFFCE4D6", fill_type="solid")
font_warning_orange = Font(color="FFC65911", bold=True)

fill_parent_price_red = PatternFill(start_color="FFFCE8E6", end_color="FFFCE8E6", fill_type="solid")
font_parent_price_red = Font(color="FFC00000", bold=True)

fill_row_hold = PatternFill(start_color="FFFCE4D6", end_color="FFFCE4D6", fill_type="solid")
fill_row_unreg = PatternFill(start_color="FFFFF2CC", end_color="FFFFF2CC", fill_type="solid")

# Load 44 new products
with open('scratch/structured_44_new_products.json', 'r', encoding='utf-8') as f:
    new_products_list = json.load(f)

new_by_sheet = {}
for p in new_products_list:
    s = p['sheet']
    if s not in new_by_sheet:
        new_by_sheet[s] = []
    new_by_sheet[s].append(p)

# We will test on scratch/test_catalog.xlsx
TEST_CATALOG = 'scratch/test_catalog.xlsx'
wb = openpyxl.load_workbook(TEST_CATALOG, data_only=False)

CATEGORY_SHEETS = [
    'یخچال و فریزر', 'شستشو و نظافت', 'لوازم برقی و پخت و پز', 'نوشیدنی ساز',
    'سرمایش و گرمایش', 'تصفیه کننده آب', 'صوتی و تصویری', 'زیبایی و سلامت فردی'
]

sheet_stats = {}

for sname in CATEGORY_SHEETS:
    ws = wb[sname]
    col_widths = {get_column_letter(c): ws.column_dimensions[get_column_letter(c)].width for c in range(1, 19)}
    header_vals = [ws.cell(1, c).value for c in range(1, 19)]
    
    # 1. Extract existing blocks
    blocks = []
    curr_brand = None
    curr_banner = None
    curr_prods = []

    for r in range(2, ws.max_row + 1):
        val_a = ws.cell(r, 1).value
        val_a_str = str(val_a).strip() if val_a is not None else ""
        if '📂' in val_a_str:
            if curr_brand is not None or curr_prods:
                blocks.append({'brand': curr_brand, 'banner': curr_banner, 'products': curr_prods})
            parts = val_a_str.split('◀')
            b_name = parts[1].strip() if len(parts) > 1 else "نامشخص"
            curr_brand = b_name
            curr_banner = val_a_str
            curr_prods = []
        elif val_a is not None and val_a_str != "":
            curr_prods.append({
                'name': val_a,
                'b': ws.cell(r, 2).value,
                'd': ws.cell(r, 4).value,
                'f': ws.cell(r, 6).value,
                'stock': ws.cell(r, 8).value,
                'main_cat': ws.cell(r, 9).value,
                'subcat': ws.cell(r, 10).value,
                'brand': ws.cell(r, 11).value,
                'type': ws.cell(r, 12).value,
                'variant': ws.cell(r, 13).value,
                'pid': ws.cell(r, 14).value,
                'vid': ws.cell(r, 15).value,
                'link': ws.cell(r, 16).value,
                'sku': ws.cell(r, 17).value,
                'status_r': ws.cell(r, 18).value,
            })

    if curr_brand is not None or curr_prods:
        blocks.append({'brand': curr_brand, 'banner': curr_banner, 'products': curr_prods})

    # 2. Add new products if any for this sheet
    if sname in new_by_sheet:
        for np in new_by_sheet[sname]:
            b = np['brand']
            matched = False
            for blk in blocks:
                if blk['brand'] == b:
                    blk['products'].append({
                        'name': np['name'],
                        'b': None,
                        'd': None,
                        'f': None,
                        'stock': np['stock'],
                        'main_cat': np['main_cat'],
                        'subcat': np['subcat'],
                        'brand': np['brand'],
                        'type': np['type'],
                        'variant': None,
                        'pid': None,
                        'vid': None,
                        'link': None,
                        'sku': None,
                        'status_r': np['status_r']
                    })
                    matched = True
                    break
            if not matched:
                blocks.append({
                    'brand': b,
                    'banner': f"  📂 {sname}  ◀  {b}",
                    'products': [{
                        'name': np['name'],
                        'b': None,
                        'd': None,
                        'f': None,
                        'stock': np['stock'],
                        'main_cat': np['main_cat'],
                        'subcat': np['subcat'],
                        'brand': np['brand'],
                        'type': np['type'],
                        'variant': None,
                        'pid': None,
                        'vid': None,
                        'link': None,
                        'sku': None,
                        'status_r': np['status_r']
                    }]
                })

    # 3. Clear sheet rows below header cleanly
    ws.merged_cells.ranges.clear()
    if ws.max_row > 1:
        ws.delete_rows(2, ws.max_row)

    # 4. Write blocks back
    curr_r = 2
    for blk in blocks:
        # Write banner row
        ws.cell(curr_r, 1, blk['banner'])
        ws.merge_cells(start_row=curr_r, start_column=1, end_row=curr_r, end_column=18)
        for c in range(1, 19):
            cell = ws.cell(curr_r, c)
            cell.fill = FILL_BANNER
            cell.font = FONT_BANNER
            cell.border = BORDER_THIN
            cell.alignment = ALIGN_RIGHT
        ws.row_dimensions[curr_r].height = 22
        curr_r += 1

        # Write products
        for p in blk['products']:
            ws.cell(curr_r, 1, p['name'])
            ws.cell(curr_r, 2, p['b'])
            ws.cell(curr_r, 3, f'=IF(OR(ISBLANK(B{curr_r}),B{curr_r}=""),"",IF($L{curr_r}="متغیر","⚠️ والد متغیر نباید قیمت داشته باشد",B{curr_r}/10))')
            ws.cell(curr_r, 4, p['d'])
            ws.cell(curr_r, 5, f'=IF(OR(ISBLANK(B{curr_r}),B{curr_r}="",ISBLANK(D{curr_r}),D{curr_r}="",D{curr_r}<=0,$L{curr_r}="متغیر"),"",(B{curr_r}-D{curr_r})/D{curr_r})')
            ws.cell(curr_r, 6, p['f'])
            ws.cell(curr_r, 7, f'=IF(OR(ISBLANK(F{curr_r}),F{curr_r}=""),"",IF($L{curr_r}="متغیر","",F{curr_r}/10))')
            ws.cell(curr_r, 8, p['stock'])
            ws.cell(curr_r, 9, p['main_cat'])
            ws.cell(curr_r, 10, p['subcat'])
            ws.cell(curr_r, 11, p['brand'])
            ws.cell(curr_r, 12, p['type'])
            ws.cell(curr_r, 13, p['variant'])
            ws.cell(curr_r, 14, p['pid'])
            ws.cell(curr_r, 15, p['vid'])
            ws.cell(curr_r, 16, p['link'])
            ws.cell(curr_r, 17, p['sku'])
            ws.cell(curr_r, 18, p['status_r'])

            ptype = str(p['type'] or '').strip()
            # Styling
            for c in range(1, 19):
                cell = ws.cell(curr_r, c)
                cell.border = BORDER_THIN
                if c == 1:
                    cell.alignment = ALIGN_RIGHT
                else:
                    cell.alignment = ALIGN_CENTER

                # Number formats
                if c in [2, 3, 4, 6, 7]:
                    cell.number_format = '#,##0'
                elif c == 5:
                    cell.number_format = '0.0%'
                else:
                    cell.number_format = 'General'

                # Fonts and fills
                if ptype == 'متغیر':
                    cell.fill = FILL_PARENT
                    cell.font = FONT_PARENT
                elif ptype == 'تنوع':
                    cell.fill = FILL_CHILD
                    cell.font = FONT_CHILD
                else:
                    # ساده
                    cell.fill = PatternFill(fill_type=None)
                    if c == 1:
                        cell.font = FONT_SIMPLE_NAME
                    elif c == 8:
                        cell.font = FONT_STOCK
                    else:
                        cell.font = FONT_REGULAR

            ws.row_dimensions[curr_r].height = 20
            curr_r += 1

    final_max_r = curr_r - 1

    # 5. Set column dimensions
    for col_letter, width in col_widths.items():
        if width:
            ws.column_dimensions[col_letter].width = width

    # 6. Set sheet view & freeze panes
    ws.views.sheetView[0].rightToLeft = True
    ws.freeze_panes = 'A2'

    # 7. Data Validations
    ws.data_validations.dataValidation.clear()
    dv_stock = DataValidation(
        type="list",
        formula1='"✓ موجود,✗ ناموجود"',
        allow_blank=True,
        showErrorMessage=True,
        errorTitle="ورود نامعتبر",
        error="لطفاً یکی از گزینه‌های «✓ موجود» یا «✗ ناموجود» را انتخاب کنید."
    )
    dv_stock.add(f"H2:H{final_max_r}")
    ws.add_data_validation(dv_stock)

    dv_status = DataValidation(
        type="list",
        formula1='"ثبت‌شده در سایت,در سایت تعریف نشده,فعلا دست نگه دار"',
        allow_blank=True,
        showErrorMessage=True,
        errorTitle="وضعیت نامعتبر",
        error="لطفاً یکی از گزینه‌های معتبر وضعیت در سایت را انتخاب کنید."
    )
    dv_status.add(f"R2:R{final_max_r}")
    ws.add_data_validation(dv_status)

    # 8. Conditional Formatting
    ws.conditional_formatting._cf_rules = OrderedDict()
    ws.conditional_formatting.max_priority = 0

    rule_stock_red = FormulaRule(formula=[f'ISNUMBER(SEARCH("ناموجود", H2))'], stopIfTrue=True, fill=fill_stock_red, font=font_stock_red)
    rule_stock_red.priority = 1
    rule_stock_green = FormulaRule(formula=[f'AND(ISNUMBER(SEARCH("موجود", H2)), NOT(ISNUMBER(SEARCH("ناموجود", H2))))'], stopIfTrue=True, fill=fill_stock_green, font=font_stock_green)
    rule_stock_green.priority = 2
    ws.conditional_formatting.add(f"H2:H{final_max_r}", rule_stock_red)
    ws.conditional_formatting.add(f"H2:H{final_max_r}", rule_stock_green)

    rule_parent_b = FormulaRule(formula=[f'AND($L2="متغیر", OR(ISNUMBER(B2), ISNUMBER(F2)))'], stopIfTrue=True, fill=fill_parent_price_red, font=font_parent_price_red)
    rule_parent_b.priority = 3
    ws.conditional_formatting.add(f"B2:B{final_max_r}", rule_parent_b)

    rule_parent_f = FormulaRule(formula=[f'AND($L2="متغیر", OR(ISNUMBER(B2), ISNUMBER(F2)))'], stopIfTrue=True, fill=fill_parent_price_red, font=font_parent_price_red)
    rule_parent_f.priority = 4
    ws.conditional_formatting.add(f"F2:F{final_max_r}", rule_parent_f)

    rule_price_b = FormulaRule(formula=[f'AND(ISNUMBER($B2), ISNUMBER($D2), $D2>0, ABS(($B2-$D2)/$D2)>=0.5, $L2<>"متغیر")'], stopIfTrue=True, fill=fill_warning_orange, font=font_warning_orange)
    rule_price_b.priority = 5
    ws.conditional_formatting.add(f"B2:B{final_max_r}", rule_price_b)

    rule_price_e = FormulaRule(formula=[f'AND(ISNUMBER($B2), ISNUMBER($D2), $D2>0, ABS(($B2-$D2)/$D2)>=0.5, $L2<>"متغیر")'], stopIfTrue=True, fill=fill_warning_orange, font=font_warning_orange)
    rule_price_e.priority = 6
    ws.conditional_formatting.add(f"E2:E{final_max_r}", rule_price_e)

    rule_row_hold = FormulaRule(formula=[f'$R2="فعلا دست نگه دار"'], stopIfTrue=False, fill=fill_row_hold)
    rule_row_hold.priority = 7
    rule_row_unreg = FormulaRule(formula=[f'$R2="در سایت تعریف نشده"'], stopIfTrue=False, fill=fill_row_unreg)
    rule_row_unreg.priority = 8
    ws.conditional_formatting.add(f"A2:R{final_max_r}", rule_row_hold)
    ws.conditional_formatting.add(f"A2:R{final_max_r}", rule_row_unreg)

    # 9. Compute stats for this sheet
    main_prods_count = 0
    vars_count = 0
    in_stock_count = 0
    out_stock_count = 0
    for blk in blocks:
        for p in blk['products']:
            pt = str(p['type'] or '').strip()
            st = str(p['stock'] or '').strip()
            if pt == 'تنوع':
                vars_count += 1
            else:
                main_prods_count += 1
            if 'ناموجود' in st or '✗' in st:
                out_stock_count += 1
            elif 'موجود' in st or '✓' in st:
                in_stock_count += 1

    sheet_stats[sname] = {
        'main_prods': main_prods_count,
        'vars': vars_count,
        'in_stock': in_stock_count,
        'out_stock': out_stock_count,
        'rows': final_max_r
    }
    print(f"Sheet '{sname}' -> Rows: {final_max_r}, Main: {main_prods_count}, Vars: {vars_count}, InStock: {in_stock_count}, OutStock: {out_stock_count}")

# 10. Update Dashboard Sheet
ws_dash = wb['📊 خلاصه و داشبورد']

total_main = sum(s['main_prods'] for s in sheet_stats.values())
total_vars = sum(s['vars'] for s in sheet_stats.values())
total_in_stock = sum(s['in_stock'] for s in sheet_stats.values())
total_out_stock = sum(s['out_stock'] for s in sheet_stats.values())

# Count registered on site
site_registered_count = 0
for sname in CATEGORY_SHEETS:
    ws_temp = wb[sname]
    for r in range(2, ws_temp.max_row + 1):
        if str(ws_temp.cell(r, 12).value or '').strip() != 'تنوع':
            if str(ws_temp.cell(r, 18).value or '').strip() == 'ثبت‌شده در سایت':
                site_registered_count += 1

ws_dash.cell(5, 2, total_main)
ws_dash.cell(5, 3, site_registered_count)
ws_dash.cell(5, 4, total_vars)
ws_dash.cell(5, 5, total_in_stock)
ws_dash.cell(5, 6, total_out_stock)

# Update rows 8-15
for r in range(8, 16):
    cat_name = ws_dash.cell(r, 2).value
    if cat_name in sheet_stats:
        st = sheet_stats[cat_name]
        ws_dash.cell(r, 3, st['main_prods'])
        ws_dash.cell(r, 4, st['vars'])
        ws_dash.cell(r, 5, st['in_stock'])
        ws_dash.cell(r, 6, st['out_stock'])

wb.save('scratch/test_rebuilt_catalog_out.xlsx')
print("\nRebuild complete! Saved to scratch/test_rebuilt_catalog_out.xlsx.")
print(f"Summary Dashboard: Total Main: {total_main}, Site Registered: {site_registered_count}, Vars: {total_vars}, InStock: {total_in_stock}, OutStock: {total_out_stock}")

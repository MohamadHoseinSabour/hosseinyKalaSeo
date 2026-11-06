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

# Palettes
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

# Load 44 structured new products
with open('scratch/structured_44_new_products.json', 'r', encoding='utf-8') as f:
    new_products_list = json.load(f)

# Group new products by sheet
new_by_sheet = {}
for p in new_products_list:
    s = p['sheet']
    if s not in new_by_sheet:
        new_by_sheet[s] = []
    new_by_sheet[s].append(p)

print("New products grouped by sheet:")
for s, prods in new_by_sheet.items():
    print(f"  {s}: {len(prods)} products")

# Load test catalog
wb = openpyxl.load_workbook('scratch/test_catalog.xlsx', data_only=False)

# Let's test on 'شستشو و نظافت'
sname = 'شستشو و نظافت'
ws = wb[sname]
col_widths = {get_column_letter(c): ws.column_dimensions[get_column_letter(c)].width for c in range(1, 19)}

# Extract blocks
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

print(f"Existing blocks in {sname}: {len(blocks)}")

# Add new products for this sheet
for np in new_by_sheet.get(sname, []):
    b = np['brand']
    # Check if brand exists in blocks
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
        # Create new brand block
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

print(f"After adding new products, total blocks in {sname}: {len(blocks)}")

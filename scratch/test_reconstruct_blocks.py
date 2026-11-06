import sys
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles.differential import DifferentialStyle

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('scratch/test_catalog.xlsx', data_only=False)
ws = wb['لوازم برقی و پخت و پز']

print(f"Initial max_row: {ws.max_row}, merged cells: {len(ws.merged_cells.ranges)}")

# Read all rows into structured brand blocks
header = [ws.cell(1, c).value for c in range(1, 19)]
print("Header:", header)

# Let's inspect all rows
blocks = [] # list of (brand_name, banner_text, list of product dicts)
current_brand = None
current_banner = None
current_prods = []

for r in range(2, ws.max_row + 1):
    val_a = ws.cell(r, 1).value
    val_a_str = str(val_a).strip() if val_a is not None else ""
    
    if val_a_str.startswith('📂') or val_a_str.startswith('📂') or '📂' in val_a_str:
        if current_brand is not None or current_prods:
            blocks.append((current_brand, current_banner, current_prods))
        parts = val_a_str.split('◀')
        b_name = parts[1].strip() if len(parts) > 1 else "نامشخص"
        current_brand = b_name
        current_banner = val_a_str
        current_prods = []
    elif val_a is not None and val_a_str != "":
        # product row
        p_data = {
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
        }
        current_prods.append(p_data)

if current_brand is not None or current_prods:
    blocks.append((current_brand, current_banner, current_prods))

print(f"Extracted {len(blocks)} brand blocks.")
for b, banner, prods in blocks[:5]:
    print(f"  Brand: '{b}' -> {len(prods)} products")

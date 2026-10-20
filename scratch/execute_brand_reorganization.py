import openpyxl
from copy import copy
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

SOURCE_FILE = 'hosseiny_kala_catalog.xlsx'
wb = openpyxl.load_workbook(SOURCE_FILE)

# 1. First, extract all product blocks from all sheets
# A block is: {
#   'sheet': sheet_name,
#   'section_brand': brand,
#   'parent_row': [18 vals],
#   'variation_rows': [[18 vals], ...]
# }

all_sheet_blocks = {}

for sname in wb.sheetnames:
    if sname in ['📊 خلاصه و داشبورد', '📖 راهنمای کاربری']:
        continue
    ws = wb[sname]
    blocks = []
    current_brand = "متفرقه"
    current_block = None
    
    for r in range(2, ws.max_row + 1):
        vA = ws.cell(row=r, column=1).value
        if not vA:
            continue
        vA_str = str(vA).strip()
        if '📂' in vA_str:
            parts = vA_str.split('◀')
            current_brand = parts[-1].strip() if len(parts) > 1 else vA_str
            continue
            
        row_vals = [ws.cell(row=r, column=c).value for c in range(1, 19)]
        
        if vA_str.startswith('↳'):
            if current_block:
                current_block['variations'].append(row_vals)
        else:
            current_block = {
                'source_sheet': sname,
                'brand': current_brand,
                'parent': row_vals,
                'variations': []
            }
            blocks.append(current_block)
            
    all_sheet_blocks[sname] = blocks

print("Extracted all blocks successfully.")
for sname, bks in all_sheet_blocks.items():
    print(f"  {sname}: {len(bks)} blocks")

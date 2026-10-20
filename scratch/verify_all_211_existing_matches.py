import sys
import json
import pickle

sys.stdout.reconfigure(encoding='utf-8')

with open('data/raw_parsed_new_list.json', 'r', encoding='utf-8') as f:
    raw_list = json.load(f)

import os
sys.path.insert(0, os.path.abspath('.'))
from scratch.verify_all_255_coverage import NEW_ITEM_INDICES

print(f"Total raw items: {len(raw_list)}")

# Load catalog to display what each existing item matched
import openpyxl
wb = openpyxl.load_workbook('hosseiny_kala_catalog.xlsx', data_only=True)
catalog = []
for sname in wb.sheetnames:
    if sname.startswith('📊') or sname.startswith('📖'): continue
    ws = wb[sname]
    for r in range(2, ws.max_row + 1):
        name = str(ws.cell(r, 1).value or '')
        if name and not name.startswith('  📂'):
            catalog.append({
                'sheet': sname,
                'row': r,
                'name': name,
                'brand': str(ws.cell(r, 11).value or ''),
                'status': str(ws.cell(r, 18).value or '')
            })

existing_rows = [x for x in catalog if x['status'] != 'در سایت تعریف نشده']
print(f"Existing rows in catalog: {len(existing_rows)}")

# Print all 43 raw indices that became new
print("\n=== RAW ITEMS ADDED AS NEW (43 raw lines -> 42 catalog rows) ===")
for idx in sorted(NEW_ITEM_INDICES.keys()):
    raw_it = raw_list[idx - 1]
    info = NEW_ITEM_INDICES[idx]
    print(f"#{idx:3d} (Qty: {raw_it['qty']:2d}) Raw: '{raw_it['desc']}' -> [{info[0]} - {info[1]}] {info[2]} ({info[3]})")

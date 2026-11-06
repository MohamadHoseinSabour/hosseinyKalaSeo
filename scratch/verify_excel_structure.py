import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('scratch/test_rebuilt_catalog_out.xlsx', data_only=False)

print("--- Checking All Category Sheets ---")
total_new_found = 0
for sname in wb.sheetnames[1:9]:
    ws = wb[sname]
    new_in_sheet = 0
    hold_in_sheet = 0
    registered_in_sheet = 0
    for r in range(2, ws.max_row + 1):
        status = str(ws.cell(r, 18).value or '').strip()
        if status == 'در سایت تعریف نشده':
            new_in_sheet += 1
            total_new_found += 1
        elif status == 'فعلا دست نگه دار':
            hold_in_sheet += 1
        elif status == 'ثبت‌شده در سایت':
            registered_in_sheet += 1
    
    # check merged ranges
    merged_banners = len(ws.merged_cells.ranges)
    # check DV
    dv_count = len(ws.data_validations.dataValidation)
    # check CF
    cf_count = len(ws.conditional_formatting)
    
    print(f"Sheet '{sname:20s}': MaxRow={ws.max_row:3d} | Registered={registered_in_sheet:3d} | Unregistered={new_in_sheet:2d} | Hold={hold_in_sheet:2d} | Banners={merged_banners:2d} | DVs={dv_count} | CFs={cf_count}")

print(f"\nTotal 'در سایت تعریف نشده' items found across sheets: {total_new_found}")

# Inspect first few new items in 'شستشو و نظافت'
ws = wb['شستشو و نظافت']
for r in range(ws.max_row - 10, ws.max_row + 1):
    vals = [ws.cell(r, c).value for c in [1, 2, 3, 8, 11, 12, 18]]
    print(f"Row {r:3d}: {vals}")

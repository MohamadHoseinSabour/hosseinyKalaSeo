import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('hosseiny_kala_catalog.xlsx', data_only=False)

sheets_to_check = [
    'شستشو و نظافت',
    'نوشیدنی ساز',
    'سرمایش و گرمایش',
    'تصفیه کننده آب',
    'زیبایی و سلامت فردی',
    'لوازم برقی و پخت و پز'
]

for sname in sheets_to_check:
    ws = wb[sname]
    print(f"\n================ SHEET: {sname} (max_row: {ws.max_row}) ================")
    # List all banner rows and sample product row
    for r in range(1, ws.max_row + 1):
        v1 = ws.cell(r, 1).value
        v1_str = str(v1) if v1 is not None else ""
        if v1_str.startswith('  📂') or v1_str.startswith('📂'):
            print(f"Row {r:3d} [BANNER]: {v1_str}")
        elif r in [2, 3, ws.max_row]:
            # print sample
            print(f"Row {r:3d} [DATA]: {v1_str[:40]} | B: {ws.cell(r, 2).value} | C: {ws.cell(r, 3).value} | H: {ws.cell(r, 8).value} | K: {ws.cell(r, 11).value} | R: {ws.cell(r, 18).value}")

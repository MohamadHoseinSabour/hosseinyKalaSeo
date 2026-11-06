import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('scratch/test_rebuilt_catalog_out.xlsx', data_only=False)
ws = wb['📊 خلاصه و داشبورد']

print("--- Dashboard Row Values ---")
for r in range(1, ws.max_row + 1):
    vals = [ws.cell(r, c).value for c in range(1, ws.max_column + 1)]
    if any(vals):
        print(f"Row {r:2d}: {vals}")

import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('scratch/test_catalog.xlsx', data_only=False)
ws = wb['لوازم برقی و پخت و پز']

print("Before insert middle:")
print("Row 46 value:", ws.cell(46, 1).value)
print("Row 47 value:", ws.cell(47, 1).value)
print("Row 47 formula C:", ws.cell(47, 3).value)
print("Merged ranges:", [str(m) for m in ws.merged_cells.ranges if '47' in str(m)])

ws.insert_rows(47, 2)

print("\nAfter insert middle:")
print("Row 46 value:", ws.cell(46, 1).value)
print("Row 47 value:", ws.cell(47, 1).value)
print("Row 48 value:", ws.cell(48, 1).value)
print("Row 49 value:", ws.cell(49, 1).value)
print("Row 49 formula C:", ws.cell(49, 3).value)
print("Merged ranges:", [str(m) for m in ws.merged_cells.ranges if '49' in str(m)])

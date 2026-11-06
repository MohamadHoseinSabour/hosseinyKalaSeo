import sys
import openpyxl
import shutil

sys.stdout.reconfigure(encoding='utf-8')

# Copy catalog to a test file
shutil.copy2('hosseiny_kala_catalog.xlsx', 'scratch/test_catalog.xlsx')

wb = openpyxl.load_workbook('scratch/test_catalog.xlsx', data_only=False)
ws = wb['شستشو و نظافت']

print("Before insert, max_row:", ws.max_row)
print("Row 98 value:", ws.cell(98, 1).value)
print("Row 99 value:", ws.cell(99, 1).value)
print("Row 99 formula C:", ws.cell(99, 3).value)
print("Merged ranges count:", len(ws.merged_cells.ranges))

# Let's try inserting 2 rows at row 100
ws.insert_rows(100, 2)
print("After insert at 100, max_row:", ws.max_row)
print("Row 99 formula C:", ws.cell(99, 3).value)
print("Merged ranges count:", len(ws.merged_cells.ranges))

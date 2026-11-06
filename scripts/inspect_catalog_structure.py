import sys
import io
import openpyxl

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

wb = openpyxl.load_workbook('hosseiny_kala_catalog.xlsx', data_only=False)
print("Sheet names:", wb.sheetnames)

for sheetname in wb.sheetnames:
    ws = wb[sheetname]
    print(f"\n================ SHEET: {sheetname} (max_row: {ws.max_row}, max_col: {ws.max_column}) ================")
    # Header row (usually row 2 or 3)
    for r in range(1, min(6, ws.max_row + 1)):
        row_vals = [ws.cell(r, c).value for c in range(1, min(20, ws.max_column + 1))]
        if any(row_vals):
            print(f"Row {r}: {row_vals}")
    # Show last 2 rows
    if ws.max_row > 5:
        print("...")
        for r in range(max(6, ws.max_row - 2), ws.max_row + 1):
            row_vals = [ws.cell(r, c).value for c in range(1, min(20, ws.max_column + 1))]
            print(f"Row {r}: {row_vals}")

import sys
import io
import openpyxl

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

wb = openpyxl.load_workbook('hosseiny_kala_catalog.xlsx', data_only=False)

# Check conditional formatting and data validation
for sheetname in ['شستشو و نظافت', 'لوازم برقی و پخت و پز', 'سرمایش و گرمایش']:
    ws = wb[sheetname]
    print(f"\n--- Sheet: {sheetname} ---")
    print(f"Data validations: {len(ws.data_validations.dataValidation)}")
    for dv in ws.data_validations.dataValidation:
        print(f"  DV sqref: {dv.sqref}, formula1: {dv.formula1}")
    print(f"Conditional formattings: {len(ws.conditional_formatting)}")
    for cf in ws.conditional_formatting:
        print(f"  CF sqref: {cf.sqref}")
        for rule in cf.rules:
            print(f"    Rule type: {rule.type}, formula: {rule.formula}")

# Check Dashboard formulas
ws_dash = wb['📊 خلاصه و داشبورد']
print("\n--- Dashboard Content ---")
for r in range(1, ws_dash.max_row + 1):
    vals = [ws_dash.cell(r, c).value for c in range(1, ws_dash.max_column + 1)]
    print(f"Row {r}: {vals}")

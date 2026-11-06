import sys
import openpyxl
from openpyxl.styles import Font, PatternFill
from openpyxl.formatting.rule import FormulaRule

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('hosseiny_kala_catalog.xlsx', data_only=False)
ws = wb['شستشو و نظافت']

print("Existing CF list length:", len(ws.conditional_formatting))
for i, cf in enumerate(ws.conditional_formatting):
    print(f"CF {i}: sqref={cf.sqref}")
    for r in cf.rules:
        print(f"  rule: type={r.type}, formula={r.formula}, stopIfTrue={r.stopIfTrue}")

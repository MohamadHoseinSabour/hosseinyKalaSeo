import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('hosseiny_kala_catalog.xlsx', data_only=False)
ws = wb['شستشو و نظافت']

print("--- Conditional Formattings in شستشو و نظافت ---")
for i, cf in enumerate(ws.conditional_formatting):
    print(f"CF {i}: sqref={cf.sqref}")
    for r in cf.rules:
        print(f"  rule: type={r.type}, dxfId={r.dxfId}, formula={r.formula}, stopIfTrue={r.stopIfTrue}")
        if r.dxf:
            print(f"    fill: {r.dxf.fill.fill_type if r.dxf.fill else None}, color: {r.dxf.fill.bgColor.rgb if r.dxf.fill and r.dxf.fill.bgColor else None}")
            print(f"    font: {r.dxf.font.color.rgb if r.dxf.font and r.dxf.font.color else None}")

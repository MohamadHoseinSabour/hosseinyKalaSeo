import openpyxl
from openpyxl.styles import Font, PatternFill
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles.differential import DifferentialStyle

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Test"

ws.cell(1, 1, "Name")
ws.cell(1, 18, "Status")
ws.cell(2, 1, "Product 1")
ws.cell(2, 18, "در سایت تعریف نشده")

dxf_yellow = DifferentialStyle(fill=PatternFill(bgColor="FFFFF2CC", fill_type="solid"))
rule_offline = FormulaRule(formula=['$R2="در سایت تعریف نشده"'], dxf=dxf_yellow)
ws.conditional_formatting.add("A2:R2", rule_offline)

wb.save("scratch/test_cf_out.xlsx")
print("Saved scratch/test_cf_out.xlsx successfully!")

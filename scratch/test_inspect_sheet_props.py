import sys
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles.differential import DifferentialStyle
from openpyxl.utils import get_column_letter

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('scratch/test_catalog.xlsx', data_only=False)

# Let's inspect column widths and views on 'لوازم برقی و پخت و پز'
ws = wb['لوازم برقی و پخت و پز']
col_widths = {get_column_letter(c): ws.column_dimensions[get_column_letter(c)].width for c in range(1, 19)}
print("Col widths:", col_widths)
print("Sheet view rightToLeft:", ws.views.sheetView[0].rightToLeft)
print("Freeze panes:", ws.freeze_panes)

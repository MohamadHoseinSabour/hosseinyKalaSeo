import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
import re
import copy

SOURCE_FILE = 'hosseiny_kala_catalog.xlsx'

wb = openpyxl.load_workbook(SOURCE_FILE)

# Let's inspect the sheets and build a clean reorganized structure.
print("Reorganizing catalog sheets...")

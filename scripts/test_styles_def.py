import os
import sys
import json
import shutil
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles.differential import DifferentialStyle
from openpyxl.utils import get_column_letter

sys.stdout.reconfigure(encoding='utf-8')

# Professional Palette
COLOR_HEADER_BG = "1F4E79"
COLOR_HEADER_TEXT = "FFFFFF"
COLOR_BANNER_BG = "EBF1F5"
COLOR_BANNER_TEXT = "375623"
COLOR_VAR_PARENT_BG = "D9E1F2"
COLOR_VARIATION_BG = "F2F2F2"
COLOR_BORDER = "D9D9D9"

FONT_HEADER = Font(name="Calibri", size=10, bold=True, color=COLOR_HEADER_TEXT)
FONT_BANNER = Font(name="Calibri", size=10, bold=True, color=COLOR_BANNER_TEXT)
FONT_PARENT = Font(name="Calibri", size=9.5, bold=True, color="000000")
FONT_CHILD = Font(name="Calibri", size=9, bold=False, color="000000")
FONT_SIMPLE_NAME = Font(name="Calibri", size=9.5, bold=True, color="000000")
FONT_REGULAR = Font(name="Calibri", size=9.5, bold=False, color="000000")
FONT_STOCK = Font(name="Calibri", size=10, bold=True, color="000000")

FILL_HEADER = PatternFill(start_color=COLOR_HEADER_BG, end_color=COLOR_HEADER_BG, fill_type="solid")
FILL_BANNER = PatternFill(start_color=COLOR_BANNER_BG, end_color=COLOR_BANNER_BG, fill_type="solid")
FILL_PARENT = PatternFill(start_color=COLOR_VAR_PARENT_BG, end_color=COLOR_VAR_PARENT_BG, fill_type="solid")
FILL_CHILD = PatternFill(start_color=COLOR_VARIATION_BG, end_color=COLOR_VARIATION_BG, fill_type="solid")

ALIGN_RIGHT = Alignment(horizontal="right", vertical="center")
ALIGN_CENTER = Alignment(horizontal="center", vertical="center")
ALIGN_LEFT = Alignment(horizontal="left", vertical="center")

def get_border():
    s = Side(style='thin', color=COLOR_BORDER)
    return Border(top=s, bottom=s, left=s, right=s)

print("Style definitions ready.")

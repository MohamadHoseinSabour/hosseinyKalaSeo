import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

USER_FILE = r'C:\Users\mmhhs\.gemini\antigravity\brain\1f248730-479c-4c28-869b-1c3bac549b81\.user_uploaded\media_1793650121277_127804a1.xlsx'
CURRENT = r'c:\Users\mmhhs\OneDrive\Documents\GitHub\hosseinyKalaSeo\hosseiny_kala_catalog.xlsx'

wb_u = openpyxl.load_workbook(USER_FILE, data_only=True)
wb_c = openpyxl.load_workbook(CURRENT, data_only=True)

sheets = [
    'یخچال و فریزر', 'شستشو و نظافت', 'لوازم برقی و پخت و پز', 'نوشیدنی ساز',
    'سرمایش و گرمایش', 'تصفیه کننده آب', 'صوتی و تصویری', 'زیبایی و سلامت فردی'
]

print("=== CHECKING ALL DIFFERENCES BETWEEN USER SHEET AND CURRENT SHEET ===")

# Summary of categories
for s in sheets:
    ws_u = wb_u[s]
    ws_c = wb_c[s]
    print(f"Sheet {s}: User rows={ws_u.max_row}, Current rows={ws_c.max_row}")


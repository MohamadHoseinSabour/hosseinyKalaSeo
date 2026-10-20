import os
import sys
import openpyxl
from openpyxl.styles import PatternFill, Font
from openpyxl.formatting.rule import FormulaRule
from openpyxl.worksheet.datavalidation import DataValidation
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.xlsx')
BACKUP_PATH = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.backup.xlsx')

SHEETS = [
    'یخچال و فریزر', 'شستشو و نظافت', 'لوازم برقی و پخت و پز', 'نوشیدنی ساز',
    'سرمایش و گرمایش', 'تصفیه کننده آب', 'صوتی و تصویری', 'زیبایی و سلامت فردی'
]

def apply_dynamic_stock_formatting():
    print(f"Opening {CATALOG_PATH}...")
    wb = openpyxl.load_workbook(CATALOG_PATH)

    # Note the 8-character ARGB codes: FF prefix ensures 100% opacity in Excel!
    fill_red = PatternFill(start_color="FFF8D7DA", end_color="FFF8D7DA", fill_type="solid")
    font_red = Font(color="FF721C24", bold=True)

    fill_green = PatternFill(start_color="FFD4EDDA", end_color="FFD4EDDA", fill_type="solid")
    font_green = Font(color="FF155724", bold=True)

    for sname in SHEETS:
        if sname not in wb.sheetnames:
            continue
        ws = wb[sname]
        max_r = ws.max_row
        col_range = f"H2:H{max_r}"

        # 1. Remove any existing CF rules targeting H
        new_cf_list = []
        for cf in list(ws.conditional_formatting):
            # Check if this CF targets column H specifically
            if 'H' in str(cf.sqref) and str(cf.sqref).startswith('H'):
                continue
            new_cf_list.append(cf)
        
        # Clear and re-assign non-H CF rules
        ws.conditional_formatting._cf_rules = {}
        for cf in new_cf_list:
            for r in cf.rules:
                ws.conditional_formatting.add(str(cf.sqref), r)

        # 2. Define clean, non-conflicting stock rules
        # Rule 1: Red for out of stock
        rule_red = FormulaRule(
            formula=[f'ISNUMBER(SEARCH("ناموجود", H2))'],
            stopIfTrue=True,
            fill=fill_red,
            font=font_red
        )

        # Rule 2: Green for in stock (only if NOT out of stock)
        rule_green = FormulaRule(
            formula=[f'AND(ISNUMBER(SEARCH("موجود", H2)), NOT(ISNUMBER(SEARCH("ناموجود", H2))))'],
            stopIfTrue=True,
            fill=fill_green,
            font=font_green
        )

        # Add red first, then green
        ws.conditional_formatting.add(col_range, rule_red)
        ws.conditional_formatting.add(col_range, rule_green)

        # 3. Fix Data Validations (clean up sqref)
        # Rebuild data validations cleanly
        ws.data_validations.dataValidation.clear()
        
        dv_stock = DataValidation(
            type="list",
            formula1='"✓ موجود,✗ ناموجود"',
            allow_blank=True,
            showErrorMessage=True,
            errorTitle="ورود نامعتبر",
            error="لطفاً یکی از گزینه‌های «✓ موجود» یا «✗ ناموجود» را انتخاب کنید."
        )
        dv_stock.add(col_range)
        ws.add_data_validation(dv_stock)

        dv_status = DataValidation(
            type="list",
            formula1='"ثبت‌شده در سایت,در سایت تعریف نشده,فعلا دست نگه دار"',
            allow_blank=True,
            showErrorMessage=True,
            errorTitle="وضعیت نامعتبر",
            error="لطفاً یکی از گزینه‌های معتبر وضعیت در سایت را انتخاب کنید."
        )
        dv_status.add(f"R2:R{max_r}")
        ws.add_data_validation(dv_status)

        print(f"  ✓ Sheet '{sname}': Range {col_range} updated with dynamic Red & Green CF + clean Data Validation.")

    wb.save(CATALOG_PATH)
    print(f"Saved {CATALOG_PATH}.")
    
    # Also save backup
    wb.save(BACKUP_PATH)
    print(f"Saved {BACKUP_PATH}.")

def test_via_excel_com():
    print("\nVerifying dynamic behavior in Microsoft Excel COM...")
    ps_script = f"""
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$excel.DisplayAlerts = $false

$wbPath = (Resolve-Path "{CATALOG_PATH}").Path
$wb = $excel.Workbooks.Open($wbPath)
$ws = $wb.Sheets.Item("یخچال و فریزر")

Write-Host "--- Test Row 3 (Original: $($ws.Range("H3").Text)) ---"
Write-Host "H3 Interior Color:" $ws.Range("H3").DisplayFormat.Interior.Color
Write-Host "H3 Font Color:" $ws.Range("H3").DisplayFormat.Font.Color

# Dynamic change: make H3 ✗ ناموجود
$ws.Range("H3").Value = "✗ ناموجود"
Write-Host "`n--- Dynamically Changed H3 to ✗ ناموجود ---"
Write-Host "H3 Interior Color (Expected Red 14342136):" $ws.Range("H3").DisplayFormat.Interior.Color
Write-Host "H3 Font Color (Expected Dark Red 2366578):" $ws.Range("H3").DisplayFormat.Font.Color

# Dynamic change: make H3 ✓ موجود
$ws.Range("H3").Value = "✓ موجود"
Write-Host "`n--- Dynamically Changed H3 to ✓ موجود ---"
Write-Host "H3 Interior Color (Expected Green 14347732):" $ws.Range("H3").DisplayFormat.Interior.Color
Write-Host "H3 Font Color (Expected Dark Green 2381589):" $ws.Range("H3").DisplayFormat.Font.Color

# Test Row 8 (Original out of stock)
Write-Host "`n--- Test Row 8 (Original: $($ws.Range("H8").Text)) ---"
Write-Host "H8 Interior Color (Expected Red 14342136):" $ws.Range("H8").DisplayFormat.Interior.Color

# Test Row 4 (Parent unpriced, empty stock)
Write-Host "`n--- Test Row 2 (Parent unpriced, empty H2: '$($ws.Range("H2").Text)') ---"
Write-Host "H2 Interior Color (Expected Default 16777215):" $ws.Range("H2").DisplayFormat.Interior.Color

$wb.Close($false)
$excel.Quit()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($ws) | Out-Null
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($wb) | Out-Null
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($excel) | Out-Null
"""
    with open('verify_cf_dynamic.ps1', 'w', encoding='utf-8-sig') as f:
        f.write(ps_script)

    res = subprocess.run(['powershell', '-NoProfile', '-File', 'verify_cf_dynamic.ps1'], capture_output=True, encoding='utf-8', errors='replace')
    print('Excel COM Output:\n', res.stdout)
    if res.stderr:
        print('Excel COM Stderr:\n', res.stderr)
    if os.path.exists('verify_cf_dynamic.ps1'):
        os.remove('verify_cf_dynamic.ps1')

if __name__ == '__main__':
    apply_dynamic_stock_formatting()
    test_via_excel_com()

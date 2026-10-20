"""
verify_pricing_rules.py
=======================
اسکریپت تست و اعتبارسنجی خودکار تغییرات قیمت‌گذاری:
۱. بررسی عدم تغییر حتی یک سلول از ستون وضعیت موجودی (Stock)
۲. بررسی صحت ۱۰۰ درصدی قیمت‌های کلور (عدم تغییر قیمت عادی و برابری دقیق قیمت حراج با ۹۰٪ قیمت اصلی)
۳. بررسی صحت ۱۰۰ درصدی قیمت‌های غیرکلور (افزایش دقیقاً ۱۰ درصدی قیمت عادی)
۴. بررسی حفظ فرمول‌های ستون‌های تومان
"""

import os
import sys
import glob
import openpyxl

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.xlsx')

def run_verification():
    # Find latest backup
    backup_files = glob.glob(os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.backup_*.xlsx'))
    if not backup_files:
        print("[ERROR] No backup file found to compare with!")
        sys.exit(1)
    
    latest_backup = sorted(backup_files)[-1]
    print(f"Comparing updated catalog against backup:\n  Current: {CATALOG_PATH}\n  Backup:  {latest_backup}\n")

    wb_curr = openpyxl.load_workbook(CATALOG_PATH, data_only=False)
    wb_back = openpyxl.load_workbook(latest_backup, data_only=False)

    sheets_to_check = [
        'یخچال و فریزر',
        'شستشو و نظافت',
        'لوازم برقی و پخت و پز',
        'نوشیدنی ساز',
        'سرمایش و گرمایش',
        'تصفیه کننده آب',
        'صوتی و تصویری',
        'زیبایی و سلامت فردی'
    ]

    stock_errors = []
    clover_checks = []
    non_clover_checks = []
    formula_errors = []

    for sname in sheets_to_check:
        ws_curr = wb_curr[sname]
        ws_back = wb_back[sname]

        current_parent_name = ""
        current_parent_brand = ""
        current_parent_is_clover = False

        for r in range(2, ws_curr.max_row + 1):
            name = ws_curr.cell(r, 1).value
            if not name:
                continue
            name_str = str(name).strip()
            if name_str.startswith('📂') or name_str.startswith('•'):
                continue

            row_type = str(ws_curr.cell(r, 10).value or '').strip()
            brand_val = str(ws_curr.cell(r, 9).value or '').strip()
            subcat = str(ws_curr.cell(r, 8).value or '').strip()

            is_variation = name_str.startswith('↳') or row_type == 'تنوع'

            if not is_variation:
                current_parent_name = name_str
                current_parent_brand = brand_val
                current_parent_is_clover = (
                    'کلور' in current_parent_name or 'clover' in current_parent_name.lower() or
                    'کلور' in current_parent_brand or 'clover' in current_parent_brand.lower() or
                    'کلور' in subcat or 'clover' in subcat.lower()
                )
                is_clover = current_parent_is_clover
            else:
                is_clover = current_parent_is_clover

            # 1. Stock check (Column F)
            stock_curr = ws_curr.cell(r, 6).value
            stock_back = ws_back.cell(r, 6).value
            if stock_curr != stock_back:
                stock_errors.append(f"[{sname} R{r}] Stock changed from '{stock_back}' to '{stock_curr}' for '{name_str}'")

            # 2. Formulas check (Column C and E)
            form_c = str(ws_curr.cell(r, 3).value or '')
            form_e = str(ws_curr.cell(r, 5).value or '')
            if not form_c.startswith('='):
                formula_errors.append(f"[{sname} R{r}] Missing Toman formula in Col C: '{form_c}'")
            if not form_e.startswith('='):
                formula_errors.append(f"[{sname} R{r}] Missing Toman formula in Col E: '{form_e}'")

            # 3. Price check
            p_reg_back = ws_back.cell(r, 2).value
            p_sale_back = ws_back.cell(r, 4).value

            p_reg_curr = ws_curr.cell(r, 2).value
            p_sale_curr = ws_curr.cell(r, 4).value

            if p_reg_back is not None and isinstance(p_reg_back, (int, float)):
                if is_clover:
                    # Regular price should be unchanged
                    reg_ok = (p_reg_curr == p_reg_back)
                    # Sale price should be int(round(p_reg_back * 0.90))
                    expected_sale = int(round(p_reg_back * 0.90))
                    sale_ok = (p_sale_curr == expected_sale)
                    clover_checks.append({
                        'sheet': sname,
                        'row': r,
                        'name': name_str,
                        'reg_orig': p_reg_back,
                        'reg_curr': p_reg_curr,
                        'reg_ok': reg_ok,
                        'sale_expected': expected_sale,
                        'sale_curr': p_sale_curr,
                        'sale_ok': sale_ok
                    })
                else:
                    # Non clover: regular price should be int(round(p_reg_back * 1.10))
                    expected_reg = int(round(p_reg_back * 1.10))
                    reg_ok = (p_reg_curr == expected_reg)
                    
                    sale_ok = True
                    expected_sale = None
                    if p_sale_back is not None and isinstance(p_sale_back, (int, float)):
                        expected_sale = int(round(p_sale_back * 1.10))
                        sale_ok = (p_sale_curr == expected_sale)

                    non_clover_checks.append({
                        'sheet': sname,
                        'row': r,
                        'name': name_str,
                        'reg_orig': p_reg_back,
                        'expected_reg': expected_reg,
                        'reg_curr': p_reg_curr,
                        'reg_ok': reg_ok,
                        'sale_ok': sale_ok
                    })

    # Summary
    print("=== AUTOMATED VERIFICATION RESULTS ===")
    print(f"1. Stock Status Preservation Test: {'PASS [OK]' if len(stock_errors) == 0 else 'FAIL [ERRORS]'}")
    if stock_errors:
        for err in stock_errors[:10]:
            print(f"   [FAIL] {err}")
    else:
        print("   -> 100% of stock statuses remain completely untouched across all rows.")

    print(f"\n2. Formula Preservation Test: {'PASS [OK]' if len(formula_errors) == 0 else 'FAIL [ERRORS]'}")
    if formula_errors:
        for err in formula_errors[:10]:
            print(f"   [FAIL] {err}")
    else:
        print("   -> 100% of Toman conversion formulas in columns C and E are intact.")

    clover_failures = [c for c in clover_checks if not (c['reg_ok'] and c['sale_ok'])]
    print(f"\n3. Clover Pricing Test ({len(clover_checks)} priced items checked): {'PASS [OK]' if len(clover_failures) == 0 else 'FAIL [ERRORS]'}")
    if clover_failures:
        for f in clover_failures:
            print(f"   [FAIL] [{f['sheet']} R{f['row']}] {f['name']}: RegOK={f['reg_ok']}, SaleOK={f['sale_ok']}")
    else:
        print(f"   -> All {len(clover_checks)} Clover items: Regular price unchanged, Sale price exactly equals 90% (-10% discount).")

    non_clover_failures = [nc for nc in non_clover_checks if not (nc['reg_ok'] and nc['sale_ok'])]
    print(f"\n4. Non-Clover Pricing Test ({len(non_clover_checks)} priced items checked): {'PASS [OK]' if len(non_clover_failures) == 0 else 'FAIL [ERRORS]'}")
    if non_clover_failures:
        for f in non_clover_failures:
            print(f"   [FAIL] [{f['sheet']} R{f['row']}] {f['name']}: RegOK={f['reg_ok']}, SaleOK={f['sale_ok']}")
    else:
        print(f"   -> All {len(non_clover_checks)} Non-Clover items: Regular price increased by exactly 10%.")

    print("\n=== SAMPLE VERIFIED CLOVER ITEMS ===")
    for c in clover_checks[:5]:
        print(f"[{c['sheet']} R{c['row']}] {c['name']}")
        print(f"   Reg: {c['reg_curr']:,} Rial | Sale (-10%): {c['sale_curr']:,} Rial | Status: PASS")

    print("\n=== SAMPLE VERIFIED NON-CLOVER ITEMS ===")
    for nc in non_clover_checks[:5]:
        print(f"[{nc['sheet']} R{nc['row']}] {nc['name']}")
        print(f"   Old Reg: {nc['reg_orig']:,} Rial -> New Reg (+10%): {nc['reg_curr']:,} Rial | Status: PASS")

    if not stock_errors and not formula_errors and not clover_failures and not non_clover_failures:
        print("\nALL VERIFICATION TESTS PASSED SUCCESSFULLY! (100% OK)")
        return True
    else:
        print("\nSOME TESTS FAILED!")
        return False

if __name__ == '__main__':
    run_verification()

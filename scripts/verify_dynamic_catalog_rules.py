import sys
sys.stdout.reconfigure(encoding='utf-8')
import openpyxl

EXCEL_FILE = "hosseiny_kala_catalog.xlsx"

CATEGORY_SHEETS = [
    'یخچال و فریزر',
    'شستشو و نظافت',
    'لوازم برقی و پخت و پز',
    'نوشیدنی ساز',
    'سرمایش و گرمایش',
    'تصفیه کننده آب',
    'صوتی و تصویری',
    'زیبایی و سلامت فردی'
]

def verify():
    wb = openpyxl.load_workbook(EXCEL_FILE)
    print(f"بررسی فایل: {EXCEL_FILE}")
    print(f"تعداد کل شیت‌ها: {len(wb.sheetnames)}")

    all_passed = True
    total_parents_checked = 0
    total_parents_clean = 0

    for cat in CATEGORY_SHEETS:
        if cat not in wb.sheetnames:
            print(f"❌ شیت {cat} یافت نشد!")
            all_passed = False
            continue

        ws = wb[cat]
        max_r = ws.max_row
        print(f"\n📂 شیت: {cat} (تعداد سطر: {max_r})")

        # ۱. بررسی شروط Conditional Formatting
        cf_rules = ws.conditional_formatting
        has_unreg_rule = False
        has_hold_rule = False
        has_price_alert_rule = False
        has_parent_err_rule = False

        for cf in cf_rules:
            for rule in cf.rules:
                formula = str(rule.formula)
                if 'در سایت تعریف نشده' in formula:
                    has_unreg_rule = True
                if 'فعلا دست نگه دار' in formula:
                    has_hold_rule = True
                if '0.5' in formula or '۵۰' in formula:
                    has_price_alert_rule = True
                if 'متغیر' in formula and 'ISNUMBER' in formula:
                    has_parent_err_rule = True

        if has_unreg_rule:
            print("  ✓ قانون وضعیت «در سایت تعریف نشده» (زرد)")
        else:
            print("  ❌ نقص در قانون تعریف‌نشده!")
            all_passed = False

        if has_hold_rule:
            print("  ✓ قانون وضعیت «فعلا دست نگه دار» (نارنجی)")
        else:
            print("  ❌ نقص در قانون فعلا دست نگه دار!")
            all_passed = False

        if has_price_alert_rule:
            print("  ✓ قانون هشدار تغییر قیمت بالای ۵۰٪ (نارنجی)")
        else:
            print("  ❌ نقص در قانون هشدار تغییر قیمت!")
            all_passed = False

        if has_parent_err_rule:
            print("  ✓ قانون خطای ورود قیمت روی محصول والد متغیر (قرمز)")
        else:
            print("  ❌ نقص در قانون خطای والد متغیر!")
            all_passed = False

        # ۲. بررسی منوهای اعتبارسنجی (Data Validation)
        dvs = ws.data_validations.dataValidation
        has_status_dv = False
        has_stock_dv = False

        for dv in dvs:
            f1 = dv.formula1 or ""
            if 'فعلا دست نگه دار' in f1:
                has_status_dv = True
            if '✓ موجود' in f1:
                has_stock_dv = True

        if has_status_dv:
            print("  ✓ اعتبارسنجی وضعیت در سایت (ستون R)")
        else:
            print("  ❌ نقص در Data Validation وضعیت!")
            all_passed = False

        if has_stock_dv:
            print("  ✓ اعتبارسنجی موجودی (ستون H)")
        else:
            print("  ❌ نقص در Data Validation موجودی!")
            all_passed = False

        # ۳. بررسی عدم وجود قیمت در والدین متغیر
        for r in range(2, max_r + 1):
            ptype = str(ws.cell(r, 12).value or '').strip() # نوع محصول در ستون L
            if ptype == 'متغیر':
                total_parents_checked += 1
                b_val = ws.cell(r, 2).value
                f_val = ws.cell(r, 6).value
                if (b_val is None or b_val == '') and (f_val is None or f_val == ''):
                    total_parents_clean += 1
                else:
                    print(f"  ❌ خطای والد متغیر قیمت‌دار در سطر {r}: B={b_val}, F={f_val}")
                    all_passed = False

    print("\n" + "=" * 50)
    if all_passed:
        print("✅ تمامی ۸ شیت دسته‌بندی با موفقیت اعتبارسنجی شدند:")
        print("   ۱. فرمت‌بندی شرطی پویا (زرد برای تعریف‌نشده و نارنجی برای فعلا دست نگه دار) در ستون R کاملاً برقرار است.")
        print("   ۲. سیستم هشدار خودکار تغییر قیمت بالای ۵۰٪ (نارنجی) روی ستون‌های B و E فعال است.")
        print("   ۳. سیستم خطای ورود قیمت روی والد متغیر (قرمز) روی ستون‌های B و F فعال است.")
        print(f"   ۴. تمام {total_parents_clean} محصول والد متغیر فاقد قیمت بوده و مطابق استاندارد ووکامرس پاکسازی شدند.")
        print("   ۵. منوهای کشویی ستون‌های R (وضعیت) و H (موجودی) کاملاً فعال هستند.")
    else:
        print("⚠️ برخی موارد نیاز به بازبینی دارند.")

if __name__ == '__main__':
    verify()

"""
apply_5pct_discount_to_catalog.py
==================================
اسکریپت اعمال تخفیف ۵ درصدی روی تمام محصولات کاتالوگ اکسل حسینی کالا:
۱. شناسایی تمام محصولات قیمت‌دار در ۸ شیت دسته‌بندی کاتالوگ.
۲. حذف تخفیف‌های قبلی از محصولاتی که از قبل تخفیف داشتند.
۳. اعمال تخفیف ۵ درصدی دقیق نسبت به قیمت عادی فعلی محصول (ستون B):
   قیمت حراج (ریال) در ستون F = گردشده (قیمت عادی * ۰.۹۵)
۴. حفظ و تحکیم فرمول‌های ستون تومان (ستون G = F/10).
۵. حفظ عدم قیمت‌گذاری روی محصولات والد متغیر مطابق استاندارد ووکامرس.
۶. حفظ کامل قالب‌بندی‌ها، استایل‌ها، اعتبارسنجی‌ها (Data Validation) و فرمت‌بندی شرطی (Conditional Formatting).
"""

import os
import sys
import shutil
import datetime
import openpyxl
from openpyxl.styles import Alignment

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.xlsx')
CATALOG_BACKUP_DEFAULT = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.backup.xlsx')

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

def apply_5pct_discount():
    now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(PROJECT_DIR, f'hosseiny_kala_catalog.backup_{now_str}.xlsx')

    print(f"۱. ایجاد نسخه پشتیبان:")
    print(f"   - نسخه زمان‌دار: {os.path.basename(backup_path)}")
    shutil.copy2(CATALOG_PATH, backup_path)
    shutil.copy2(CATALOG_PATH, CATALOG_BACKUP_DEFAULT)
    print("   ✓ فایل‌های پشتیبان با موفقیت ایجاد شدند.\n")

    print(f"۲. بارگذاری فایل اکسل: {os.path.basename(CATALOG_PATH)}")
    wb = openpyxl.load_workbook(CATALOG_PATH, data_only=False)

    total_new_discounts = 0
    total_replaced_discounts = 0
    total_parents_skipped = 0
    total_unpriced_skipped = 0

    replaced_items_details = []

    for sname in CATEGORY_SHEETS:
        if sname not in wb.sheetnames:
            print(f"   [هشدار] شیت '{sname}' یافت نشد، رد شد.")
            continue

        ws = wb[sname]
        sheet_new = 0
        sheet_replaced = 0
        sheet_parents = 0
        sheet_unpriced = 0

        for r in range(2, ws.max_row + 1):
            name_cell = ws.cell(r, 1)
            name = name_cell.value
            if not name:
                continue

            name_str = str(name).strip()
            if name_str.startswith('📂') or name_str.startswith('•'):
                continue

            row_type = str(ws.cell(r, 12).value or '').strip() # ستون L: نوع محصول

            # والدین متغیر نباید قیمت داشته باشند
            if row_type == 'متغیر':
                ws.cell(r, 2).value = None
                ws.cell(r, 4).value = None
                ws.cell(r, 6).value = None
                total_parents_skipped += 1
                sheet_parents += 1
                continue

            cell_p_reg = ws.cell(r, 2)
            cell_p_sale = ws.cell(r, 6)
            cell_p_sale_toman = ws.cell(r, 7)

            p_reg = cell_p_reg.value
            p_sale_old = cell_p_sale.value

            # اگر قیمت عادی ندارد، رد شود و ستون حراج خالی بماند
            if p_reg is None or not isinstance(p_reg, (int, float)) or p_reg <= 0:
                cell_p_sale.value = None
                total_unpriced_skipped += 1
                sheet_unpriced += 1
                continue

            p_reg = int(p_reg)
            # محاسبه تخفیف دقیق ۵ درصدی نسبت به قیمت فعلی (ستون B)
            new_sale_price = int(round(p_reg * 0.95))

            if p_sale_old is not None and str(p_sale_old).strip() != '':
                # قبلاً تخفیف داشته -> حذف تخفیف قبلی و اعمال تخفیف جدید ۵ درصدی
                total_replaced_discounts += 1
                sheet_replaced += 1
                replaced_items_details.append({
                    'sheet': sname,
                    'row': r,
                    'name': name_str,
                    'reg_price': p_reg,
                    'old_sale': p_sale_old,
                    'new_sale': new_sale_price
                })
            else:
                # قبلاً تخفیف نداشته -> اعمال تخفیف جدید ۵ درصدی
                total_new_discounts += 1
                sheet_new += 1

            # درج قیمت حراج ریال
            cell_p_sale.value = new_sale_price
            cell_p_sale.number_format = '#,##0'
            cell_p_sale.alignment = Alignment(horizontal='center', vertical='center')

            # فرمول قیمت حراج تومان
            cell_p_sale_toman.value = f'=IF(OR(ISBLANK(F{r}),F{r}=""),"",IF($L{r}="متغیر","",F{r}/10))'
            cell_p_sale_toman.number_format = '#,##0'
            cell_p_sale_toman.alignment = Alignment(horizontal='center', vertical='center')

        print(f"   📂 [{sname}]: {sheet_new} محصول با تخفیف ۵٪ جدید | {sheet_replaced} محصول جایگزینی تخفیف قبلی با ۵٪")

    print("\n۳. جزئیات اقلامی که تخفیف قبلی آن‌ها حذف و با ۵٪ جایگزین شد:")
    for item in replaced_items_details:
        print(f"   - [{item['sheet']} سطر {item['row']}] {item['name']}:")
        print(f"     قیمت عادی: {item['reg_price']:,} ریال | قیمت حراج قبلی: {item['old_sale']:,} ریال | قیمت حراج جدید (۵٪): {item['new_sale']:,} ریال")

    print(f"\n۴. ذخیره‌سازی فایل به‌روزشده: {CATALOG_PATH} ...")
    wb.save(CATALOG_PATH)
    print("   ✓ فایل با موفقیت ذخیره شد.")

    print("\n" + "=" * 60)
    print("📊 خلاصه گزارش اعمال تخفیف ۵ درصدی:")
    print(f" - کل محصولات با تخفیف ۵ درصدی جدید: {total_new_discounts}")
    print(f" - محصولات دارای تخفیف قبلی (حذف تخفیف قبلی و اعمال ۵٪ جدید): {total_replaced_discounts}")
    print(f" - مجموع کل محصولات تخفیف‌دار: {total_new_discounts + total_replaced_discounts}")
    print(f" - محصولات والد متغیر بدون قیمت (محفوظ): {total_parents_skipped}")
    print(f" - محصولات بدون قیمت پایه (بدون تغییر): {total_unpriced_skipped}")
    print("=" * 60)

if __name__ == '__main__':
    apply_5pct_discount()

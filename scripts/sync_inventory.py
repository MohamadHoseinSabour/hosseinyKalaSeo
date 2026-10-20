"""
sync_inventory.py
=================
استاندارد رسمی و خودکار همگام‌سازی موجودی انبار با کاتالوگ محصولات حسینی کالا

نحوه استفاده:
  python scripts/sync_inventory.py [مسیر_فایل_انبار]

اگر مسیر فایل مشخص نشود، به‌طور پیش‌فرض فایل data/inventory_incoming_raw.csv پردازش می‌شود.

قابلیت‌ها:
۱. پارس خودکار انواع فرمت‌های خروجی انبارداری (تک‌ستونی، دو‌ستونی موازی و CSV)
۲. استخراج هوشمند کد مدل و تفکیک نام کالا از خط‌فاصله‌ها
۳. تطبیق قطعی با پایگاه دانش نگاشت استاندارد (data/inventory_mapping_standard.json)
۴. تطبیق با ۹۷ محصول لایو سایت + ۷۸ تنوع (Variations)
۵. افزودن خودکار کالاهای جدید به ۸ دسته‌بندی اصلی اکسل
۶. به‌روزرسانی آنی وضعیت موجودی (✓ موجود / ✗ ناموجود بر اساس تعداد)
۷. تولید مجدد کاتالوگ اکسل (hosseiny_kala_catalog.xlsx و hosseiny_kala_catalog_latest.xlsx)
۸. آموزش و تکامل پایگاه داده نگاشت استاندارد جهت پردازش‌های سریع‌تر در آینده
"""

import os
import sys
import json
import re
import argparse
import openpyxl

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
DEFAULT_INPUT = os.path.join(DATA_DIR, 'inventory_incoming_raw.csv')
STANDARD_MAP_FILE = os.path.join(DATA_DIR, 'inventory_mapping_standard.json')
REF_FILE = os.path.join(DATA_DIR, 'current_catalog_reference.json')
EXCEL_OUT_MAIN = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.xlsx')
EXCEL_OUT_LATEST = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog_latest.xlsx')
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from build_full_updated_catalog import build_complete_catalog
from match_and_audit_catalog import run_matching_and_auditing
from parse_inventory import clean_item_description

def parse_input_file(file_path):
    print(f"📖 در حال خواندن فایل موجودی از: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    items = []
    for line_idx, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith('تعداد'):
            continue

        parts = line.split(',,')
        # بخش اول
        p1 = parts[0].strip()
        if p1:
            s1 = p1.split(',', 1)
            if len(s1) == 2:
                try:
                    q = int(s1[0].strip())
                except ValueError:
                    q = 0
                items.append({
                    "raw_index": len(items) + 1,
                    "line_num": line_idx,
                    "raw_quantity": q,
                    "in_stock": q > 0,
                    "raw_desc": s1[1].strip()
                })

        # بخش دوم (در صورت وجود ستون موازی)
        if len(parts) > 1 and parts[1].strip():
            s2 = parts[1].strip().split(',', 1)
            if len(s2) == 2:
                try:
                    q = int(s2[0].strip())
                except ValueError:
                    q = 0
                items.append({
                    "raw_index": len(items) + 1,
                    "line_num": line_idx,
                    "raw_quantity": q,
                    "in_stock": q > 0,
                    "raw_desc": s2[1].strip()
                })

    print(f"✓ تعداد {len(items)} قلم با موفقیت استخراج شد.")
    return items

def main():
    parser = argparse.ArgumentParser(description="همگام‌سازی استاندارد موجودی انبار با کاتالوگ حسینی کالا")
    parser.add_argument("input_file", nargs="?", default=DEFAULT_INPUT, help="مسیر فایل ورودی لیست موجودی")
    args = parser.parse_args()

    input_file = args.input_file
    if not os.path.exists(input_file):
        print(f"❌ خطا: فایل ورودی '{input_file}' یافت نشد.")
        sys.exit(1)

    print("\n" + "=" * 70)
    print("🚀 اجرای فرآیند استاندارد همگام‌سازی موجودی حسینی کالا")
    print("=" * 70)

    # مرحله ۱: پارس فایل
    raw_items = parse_input_file(input_file)
    parsed_json_path = os.path.join(DATA_DIR, 'inventory_parsed.json')
    with open(parsed_json_path, 'w', encoding='utf-8') as f:
        json.dump(raw_items, f, ensure_ascii=False, indent=2)

    # مرحله ۲: نرمال‌سازی کدهای مدل
    print("\n⚙️ مرحله ۲: نرمال‌سازی و استخراج کدهای مدل...")
    from normalize_inventory import run_normalization
    run_normalization()

    # مرحله ۳: تطبیق و ممیزی کاتالوگ
    print("\n🔍 مرحله ۳: تطبیق با کاتالوگ لایو و پایگاه نگاشت استاندارد...")
    run_matching_and_auditing()

    # مرحله ۴: تولید فایل نهایی اکسل
    print("\n📊 مرحله ۴: تولید کاتالوگ اکسل با داشبورد و فرمول‌های هوشمند...")
    build_complete_catalog()

    print("\n" + "=" * 70)
    print("✅ تمامی مراحل با موفقیت انجام شد و کاتالوگ به‌روزرسانی گردید.")
    print(f"📁 فایل نهایی: {EXCEL_OUT_LATEST}")
    print("=" * 70)

if __name__ == '__main__':
    main()

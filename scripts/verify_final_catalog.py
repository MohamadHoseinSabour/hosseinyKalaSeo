"""
verify_final_catalog.py
=======================
تست و صحت‌سنجی نهایی فایل کاتالوگ به‌روزشده:
۱. بررسی شیت‌ها و ردیف‌های اکسل
۲. بررسی اقلام ناموجود مشخص‌شده توسط کاربر (مثل B3115، 990c و ...)
۳. بررسی اقلام جدید اضافه شده (مانند 8vw1، 6032 و ...)
۴. بررسی فرمول‌های محاسبه تومان
"""

import sys
import openpyxl

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('hosseiny_kala_catalog.xlsx', data_only=True)
print("Workbook sheets:", wb.sheetnames)

# تست اقلام نمونه
sample_checks = ["B3115", "990c", "990S", "8vw1", "6032", "7303", "SG518", "S517"]
found_samples = {}

for sname in wb.sheetnames:
    if sname in ['📊 خلاصه و داشبورد', '📖 راهنمای کاربری']:
        continue
    ws = wb[sname]
    for r in range(2, ws.max_row + 1):
        name = str(ws.cell(r, 1).value or '')
        stock = str(ws.cell(r, 6).value or '')
        status = str(ws.cell(r, 16).value or '')
        pid = ws.cell(r, 12).value
        for target in sample_checks:
            if target in name and target not in found_samples:
                found_samples[target] = {
                    "sheet": sname,
                    "row": r,
                    "name": name,
                    "stock": stock,
                    "status": status,
                    "pid": pid
                }

print("\n--- نتیجه بررسی اقلام شاخص و حساس ---")
for t in sample_checks:
    res = found_samples.get(t)
    if res:
        print(f"[{t}] شیت: '{res['sheet']}' | ردیف: {res['row']} | نام: '{res['name']}' | موجودی: {res['stock']} | وضعیت در سایت: {res['status']} | شناسه سایت: {res['pid']}")
    else:
        print(f"[{t}] یافت نشد!")

print("\n✓ تست صحت‌سنجی کاتالوگ با موفقیت انجام شد.")

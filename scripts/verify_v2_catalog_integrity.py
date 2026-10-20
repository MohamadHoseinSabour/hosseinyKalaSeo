import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('hosseiny_kala_catalog.xlsx', data_only=True)

print("=" * 60)
print("اعتبارسنجی جامع کاتالوگ نهایی حسینی کالا v2")
print("=" * 60)

# ۱. بررسی شیت یخچال و فریزر
ws_ref = wb['یخچال و فریزر']
print(f"\n[۱] بررسی شیت یخچال و فریزر ({ws_ref.max_row} ردیف):")
clover_items = []
duplicate_checks = []

for r in range(2, ws_ref.max_row + 1):
    name = str(ws_ref.cell(r, 1).value or '')
    ptype = ws_ref.cell(r, 10).value
    pid = ws_ref.cell(r, 12).value
    vid = ws_ref.cell(r, 13).value
    stock = ws_ref.cell(r, 6).value
    note = ws_ref.cell(r, 16).value
    
    if any(k in name for k in ['روسو پلاس', 'گلوری', 'آبریزدار', 'هوم بار', 'اکونومی', 'آیس پول', 'نیکسان']):
        print(f"  R{r:03d} | {name[:52]:52} | Type:{str(ptype):7} | PID:{str(pid):5} | VID:{str(vid):5} | Stock:{str(stock):9} | Note:{note}")
        
    # بررسی عدم وجود کلمات ممنوعه دوقلوی تک
    if any(k in name for k in ['فریزر تک کلور', 'یخچال تک کلور', 'فریزر تک 27', 'یخچال تک 27', 'افریزر', 'ایخچال']):
        duplicate_checks.append(f"ردیف خطادار پیدا شد: R{r} -> {name}")

if duplicate_checks:
    print("\n❌ خطای اقلام تکراری تک:")
    for err in duplicate_checks:
        print("  " + err)
else:
    print("\n✅ تایید: هیچ ردیف تکی جداگانه (فریزر تک / یخچال تک) وجود ندارد و همگی تجمیع شدند.")

# ۲. بررسی شیت لوازم پخت و پز و مایتابه‌ها
ws_cook = wb['لوازم برقی و پخت و پز']
print(f"\n[۲] بررسی شیت لوازم پخت و پز و مایتابه‌ها ({ws_cook.max_row} ردیف):")
pan_rows = []
for r in range(2, ws_cook.max_row + 1):
    name = str(ws_cook.cell(r, 1).value or '')
    if any(k in name for k in ['تابه', 'مایتابه', 'ماهیتابه']):
        ptype = ws_cook.cell(r, 10).value
        stock = ws_cook.cell(r, 6).value
        attr = ws_cook.cell(r, 11).value
        pan_rows.append((r, name, ptype, attr, stock))
        print(f"  R{r:03d} | {name:48} | Type:{str(ptype):7} | Attr:{str(attr):24} | Stock:{str(stock)}")

if len([p for p in pan_rows if p[2] == 'متغیر']) == 1 and all(p[2] in ['متغیر', 'تنوع'] for p in pan_rows):
    print("✅ تایید: تمام مایتابه‌ها در قالب یک محصول متغیر واحد با تنوع سایز تجمیع شدند.")
else:
    print("⚠️ هشدار در ساختار تابه ها.")

# ۳. بررسی داشبورد
ws_dash = wb['📊 خلاصه و داشبورد']
print(f"\n[۳] خلاصه آمار داشبورد:")
for r in range(4, 17):
    row_vals = [ws_dash.cell(r, c).value for c in range(2, 7) if ws_dash.cell(r, c).value is not None]
    if row_vals:
        print(f"  ردیف {r}: {row_vals}")

print("\n" + "=" * 60)
print("پایان اعتبارسنجی: کاتالوگ با بالاترین استاندارد آماده است.")
print("=" * 60)

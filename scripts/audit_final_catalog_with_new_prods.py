import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('hosseiny_kala_catalog.xlsx', data_only=False)

print("=================================================================")
print("         ممیزی جامع و نهایی کاتالوگ حسینی کالا پس از افزودن ۴۴ محصول جدید")
print("=================================================================")

dash = wb['📊 خلاصه و داشبورد']
dash_vals = [dash.cell(5, c).value for c in range(2, 7)]
print(f"📊 مقادیر داشبورد کل: کالای اصلی={dash_vals[0]}, ثبت سایت={dash_vals[1]}, تنوع={dash_vals[2]}, موجود={dash_vals[3]}, ناموجود={dash_vals[4]}")

total_unreg = 0
total_registered = 0
total_hold = 0
total_vars = 0
total_parents = 0
total_in_stock = 0
total_out_stock = 0

issues = []

for sname in wb.sheetnames[1:9]:
    ws = wb[sname]
    s_unreg = 0
    s_reg = 0
    s_hold = 0
    s_vars = 0
    s_parents = 0
    s_in = 0
    s_out = 0

    # check DV
    dvs = ws.data_validations.dataValidation
    if len(dvs) != 2:
        issues.append(f"Sheet {sname} has {len(dvs)} DataValidations (expected 2)")
    
    # check CF
    cfs = ws.conditional_formatting
    if len(cfs) != 5:
        issues.append(f"Sheet {sname} has {len(cfs)} ConditionalFormattings (expected 5)")

    for r in range(2, ws.max_row + 1):
        name = ws.cell(r, 1).value
        ptype = str(ws.cell(r, 12).value or '').strip()
        status_r = str(ws.cell(r, 18).value or '').strip()
        stock = str(ws.cell(r, 8).value or '').strip()
        
        # Check banner
        if '📂' in str(name):
            continue

        # Check formulas in C, E, G
        formula_c = str(ws.cell(r, 3).value or '')
        formula_e = str(ws.cell(r, 5).value or '')
        formula_g = str(ws.cell(r, 7).value or '')

        if not formula_c.startswith(f'=IF(OR(ISBLANK(B{r})'):
            issues.append(f"Sheet {sname} Row {r}: Col C formula mismatch '{formula_c}'")
        if not formula_e.startswith(f'=IF(OR(ISBLANK(B{r})'):
            issues.append(f"Sheet {sname} Row {r}: Col E formula mismatch '{formula_e}'")
        if not formula_g.startswith(f'=IF(OR(ISBLANK(F{r})'):
            issues.append(f"Sheet {sname} Row {r}: Col G formula mismatch '{formula_g}'")

        # Check variable parent prices
        if ptype == 'متغیر':
            val_b = ws.cell(r, 2).value
            val_d = ws.cell(r, 4).value
            val_f = ws.cell(r, 6).value
            if val_b is not None or val_f is not None:
                issues.append(f"Sheet {sname} Row {r}: Variable parent '{name}' has price in B/F: B={val_b}, F={val_f}")

        if ptype == 'تنوع':
            s_vars += 1
            total_vars += 1
        else:
            s_parents += 1
            total_parents += 1
            if 'ناموجود' in stock or '✗' in stock:
                s_out += 1
                total_out_stock += 1
            else:
                s_in += 1
                total_in_stock += 1

            if status_r == 'در سایت تعریف نشده':
                s_unreg += 1
                total_unreg += 1
            elif status_r == 'ثبت‌شده در سایت':
                s_reg += 1
                total_registered += 1
            elif status_r == 'فعلا دست نگه دار':
                s_hold += 1
                total_hold += 1

    print(f"Sheet {sname:20s}: سطرها={ws.max_row:3d} | والد={s_parents:2d} (ثبت={s_reg:2d}, تعریف‌نشده={s_unreg:2d}, نگهدار={s_hold:2d}) | تنوع={s_vars:2d} | موجود={s_in:2d}, ناموجود={s_out:2d}")

print("\n--- جمع‌بندی تطبیق با داشبورد ---")
print(f"کل کالای اصلی: {total_parents} (داشبورد: {dash_vals[0]}) -> {'✓ منطبق' if total_parents == dash_vals[0] else '❌ مغایرت'}")
print(f"ثبت‌شده در سایت: {total_registered} (داشبورد: {dash_vals[1]}) -> {'✓ منطبق' if total_registered == dash_vals[1] else '❌ مغایرت'}")
print(f"تنوع متغیرها: {total_vars} (داشبورد: {dash_vals[2]}) -> {'✓ منطبق' if total_vars == dash_vals[2] else '❌ مغایرت'}")
print(f"کالای اصلی موجود: {total_in_stock} (داشبورد: {dash_vals[3]}) -> {'✓ منطبق' if total_in_stock == dash_vals[3] else '❌ مغایرت'}")
print(f"کالای اصلی ناموجود: {total_out_stock} (داشبورد: {dash_vals[4]}) -> {'✓ منطبق' if total_out_stock == dash_vals[4] else '❌ مغایرت'}")
print(f"تعداد کل اقلام 'در سایت تعریف نشده': {total_unreg} (باید دقیقاً ۴۴ باشد) -> {'✓ دقیقاً ۴۴ قلم' if total_unreg == 44 else '❌ مغایرت'}")

if issues:
    print(f"\n⚠️ تعداد خطاهای یافت‌شده: {len(issues)}")
    for iss in issues[:10]:
        print("  -", iss)
else:
    print("\n🎉 هیچ خطایی در فرمول‌ها، ساختار، قیمت‌های والد یا اعتبارسنجی‌ها یافت نشد. همه چیز ۱۰۰٪ استاندارد و بی‌نقص است.")

import os
import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

USER_FILE = r'C:\Users\mmhhs\.gemini\antigravity\brain\1f248730-479c-4c28-869b-1c3bac549b81\.user_uploaded\media_1793650121277_127804a1.xlsx'
PRE_15_BACKUP = r'c:\Users\mmhhs\OneDrive\Documents\GitHub\hosseinyKalaSeo\hosseiny_kala_catalog.backup_before_15pct_sync_20261102_233158.xlsx'
CURRENT_CATALOG = r'c:\Users\mmhhs\OneDrive\Documents\GitHub\hosseinyKalaSeo\hosseiny_kala_catalog.xlsx'

wb_user = openpyxl.load_workbook(USER_FILE, data_only=True)
wb_pre = openpyxl.load_workbook(PRE_15_BACKUP, data_only=True)
wb_curr = openpyxl.load_workbook(CURRENT_CATALOG, data_only=True)

sheets = [
    'یخچال و فریزر', 'شستشو و نظافت', 'لوازم برقی و پخت و پز', 'نوشیدنی ساز',
    'سرمایش و گرمایش', 'تصفیه کننده آب', 'صوتی و تصویری', 'زیبایی و سلامت فردی'
]

print("=" * 80)
print("🔍 مقایسه فایل ارسالی کاربر با نسخه مبنا (قبل از افزایش ۱۵٪)")
print("=" * 80)

# ۱. استخراج محصولات بر اساس کلید یکتا (pid, vid, نام)
def load_sheet_items(wb):
    items = {}
    for s in sheets:
        if s not in wb.sheetnames:
            continue
        ws = wb[s]
        for r in range(2, ws.max_row + 1):
            name = ws.cell(r, 1).value
            if not name:
                continue
            name_str = str(name).strip()
            if name_str.startswith(('📂', '•')):
                continue

            pid = ws.cell(r, 14).value
            vid = ws.cell(r, 15).value
            ptype = str(ws.cell(r, 12).value or '').strip()

            b = ws.cell(r, 2).value  # قیمت عادی ریال
            d = ws.cell(r, 4).value  # آخرین قیمت
            f = ws.cell(r, 6).value  # قیمت حراج
            stock = str(ws.cell(r, 8).value or '').strip()
            status_site = str(ws.cell(r, 18).value or '').strip()

            key = (int(pid) if pid else None, int(vid) if vid else None, name_str)
            items[key] = {
                'sheet': s,
                'row': r,
                'name': name_str,
                'pid': int(pid) if pid else None,
                'vid': int(vid) if vid else None,
                'ptype': ptype,
                'price_b': b,
                'price_d': d,
                'price_f': f,
                'stock': stock,
                'status_site': status_site
            }
    return items

items_user = load_sheet_items(wb_user)
items_pre = load_sheet_items(wb_pre)

print(f"تعداد اقلام فایل ارسالی کاربر: {len(items_user)}")
print(f"تعداد اقلام نسخه مبنا (قبل از ۱۵٪): {len(items_pre)}")

# پیدا کردن تفاوت‌ها
diff_status_site = []
diff_stock = []
newly_priced = []
manually_re为其_priced = []

for key, u in items_user.items():
    p = items_pre.get(key)
    if not p:
        # اگر کلید بر اساس (pid, vid, name) پیدا نشد، بر اساس pid/vid بررسی کنیم
        matches = [v for k, v in items_pre.items() if (k[0] == key[0] and k[1] == key[1] and key[0] is not None)]
        if matches:
            p = matches[0]

    if not p:
        # کالایی که فقط در فایل کاربر هست (اگر وجود داشته باشد)
        continue

    # ۱. بررسی وضعیت در سایت (ستون R)
    u_stat = u['status_site']
    p_stat = p['status_site']
    if u_stat != p_stat:
        diff_status_site.append({
            'name': u['name'],
            'sheet': u['sheet'],
            'pid': u['pid'],
            'vid': u['vid'],
            'user_val': u_stat,
            'pre_val': p_stat
        })

    # ۲. بررسی موجودی (ستون H)
    u_stock = u['stock']
    p_stock = p['stock']
    if u_stock != p_stock:
        diff_stock.append({
            'name': u['name'],
            'sheet': u['sheet'],
            'pid': u['pid'],
            'vid': u['vid'],
            'user_val': u_stock,
            'pre_val': p_stock
        })

    # ۳. بررسی قیمت‌ها (ستون B)
    u_b = u['price_b']
    p_b = p['price_b']

    u_has_b = (u_b is not None and isinstance(u_b, (int, float)) and u_b > 0)
    p_has_b = (p_b is not None and isinstance(p_b, (int, float)) and p_b > 0)

    if u_has_b and not p_has_b:
        newly_priced.append({
            'name': u['name'],
            'sheet': u['sheet'],
            'pid': u['pid'],
            'vid': u['vid'],
            'user_price_rial': u_b,
            'user_price_toman': u_b / 10,
            'user_sale_rial': u['price_f'],
            'pre_price': p_b
        })
    elif u_has_b and p_has_b and u_b != p_b:
        manually_re为其_priced.append({
            'name': u['name'],
            'sheet': u['sheet'],
            'pid': u['pid'],
            'vid': u['vid'],
            'user_price_rial': u_b,
            'user_price_toman': u_b / 10,
            'user_sale_rial': u['price_f'],
            'pre_price_rial': p_b,
            'pre_price_toman': p_b / 10,
            'diff_ratio': (u_b - p_b) / p_b if p_b else 0
        })

print("\n" + "=" * 80)
print(f"۱. تفاوت‌های وضعیت در سایت (ستون R): {len(diff_status_site)} مورد")
print("=" * 80)
for it in diff_status_site:
    print(f"  • {it['name'][:35]} (PID {it['pid']}): قبل='{it['pre_val']}' ⬅️ کاربر='{it['user_val']}'")

print("\n" + "=" * 80)
print(f"۲. تفاوت‌های وضعیت موجودی (ستون H): {len(diff_stock)} مورد")
print("=" * 80)
for it in diff_stock:
    print(f"  • {it['name'][:35]} (PID {it['pid']}): قبل='{it['pre_val']}' ⬅️ کاربر='{it['user_val']}'")

print("\n" + "=" * 80)
print(f"۳. محصولاتی که قبلاً قیمت نداشتند ولی کاربر قیمت داده: {len(newly_priced)} مورد")
print("=" * 80)
for it in newly_priced:
    print(f"  • {it['name'][:35]} (PID {it['pid']}): قیمت کاربر={it['user_price_toman']:,.0f} تومان ({it['user_price_rial']:,} ریال) | حراج={it['user_sale_rial']}")

print("\n" + "=" * 80)
print(f"۴. تغییرات دستی قیمت توسط کاربر: {len(manually_re为其_priced)} مورد")
print("=" * 80)
for it in manually_re为其_priced:
    print(f"  • {it['name'][:35]} (PID {it['pid']}): قبلی={it['pre_price_toman']:,.0f} تومان ⬅️ کاربر={it['user_price_toman']:,.0f} تومان ({it['diff_ratio']*100:+.1f}%)")

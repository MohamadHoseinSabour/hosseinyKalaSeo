import sys
import json
import openpyxl
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('hosseiny_kala_catalog.xlsx', data_only=True)
category_sheets = [
    'یخچال و فریزر', 'شستشو و نظافت', 'لوازم برقی و پخت و پز', 'نوشیدنی ساز',
    'سرمایش و گرمایش', 'تصفیه کننده آب', 'صوتی و تصویری', 'زیبایی و سلامت فردی'
]

haversen_pids = {3534, 3531, 3523, 3520, 3516}

total_items = 0
items_with_price = 0
items_without_price = 0
haversen_items = 0
discounted_items = 0
regular_items = 0

plan_items = []

for s in category_sheets:
    ws = wb[s]
    for r in range(2, ws.max_row + 1):
        name = ws.cell(r, 1).value
        if not name or '📂' in str(name):
            continue
        ptype = str(ws.cell(r, 12).value or '').strip()
        if ptype == 'متغیر':
            continue

        total_items += 1
        pid = ws.cell(r, 14).value
        vid = ws.cell(r, 15).value
        reg_rial = ws.cell(r, 2).value
        sale_rial = ws.cell(r, 6).value

        pid_int = int(pid) if pid else None
        vid_int = int(vid) if vid else None

        if pid_int in haversen_pids or 'هاورسن' in str(name):
            haversen_items += 1
            continue

        if not reg_rial or not isinstance(reg_rial, (int, float)) or reg_rial <= 0:
            items_without_price += 1
            continue

        items_with_price += 1
        has_discount = (sale_rial is not None and isinstance(sale_rial, (int, float)) and sale_rial > 0)
        
        old_reg_toman = int(round(reg_rial / 10))
        new_reg_toman = int(round(old_reg_toman * 1.15))
        new_reg_rial = new_reg_toman * 10

        if has_discount:
            discounted_items += 1
            new_sale_toman = int(round(new_reg_toman * 0.95))
            new_sale_rial = new_sale_toman * 10
            old_sale_toman = int(round(sale_rial / 10))
        else:
            regular_items += 1
            new_sale_toman = None
            new_sale_rial = None
            old_sale_toman = None

        plan_items.append({
            'sheet': s,
            'row': r,
            'name': str(name),
            'ptype': ptype,
            'pid': pid_int,
            'vid': vid_int,
            'has_discount': has_discount,
            'old_reg_rial': reg_rial,
            'new_reg_rial': new_reg_rial,
            'old_reg_toman': old_reg_toman,
            'new_reg_toman': new_reg_toman,
            'old_sale_rial': sale_rial,
            'new_sale_rial': new_sale_rial,
            'old_sale_toman': old_sale_toman,
            'new_sale_toman': new_sale_toman,
        })

print(f"Total items analyzed: {total_items}")
print(f"Haversen TVs skipped: {haversen_items}")
print(f"Items without price (skipped): {items_without_price}")
print(f"Items to update with price: {items_with_price}")
print(f"  - Regular items (no discount): {regular_items}")
print(f"  - Discounted items (reg + 15%, then 5% sale): {discounted_items}")

print("\nSample 5 regular items:")
for it in [x for x in plan_items if not x['has_discount']][:5]:
    print(f"  • {it['name'][:35]}: Reg {it['old_reg_toman']:,} -> {it['new_reg_toman']:,} Toman (+15.0%)")

print("\nSample 5 discounted items:")
for it in [x for x in plan_items if x['has_discount']][:5]:
    print(f"  • {it['name'][:35]}: Reg {it['old_reg_toman']:,} -> {it['new_reg_toman']:,} Toman | Sale {it['old_sale_toman']:,} -> {it['new_sale_toman']:,} Toman (5% off)")

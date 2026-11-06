import sys
import json
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('hosseiny_kala_catalog.xlsx', data_only=True)
category_sheets = [
    'یخچال و فریزر', 'شستشو و نظافت', 'لوازم برقی و پخت و پز', 'نوشیدنی ساز',
    'سرمایش و گرمایش', 'تصفیه کننده آب', 'صوتی و تصویری', 'زیبایی و سلامت فردی'
]

with open('data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

prods_by_id = {p['id']: p for p in products}

cat_discounted = 0
cat_regular = 0
site_discounted = 0

for s in category_sheets:
    ws = wb[s]
    for r in range(2, ws.max_row + 1):
        name = ws.cell(r, 1).value
        if not name or '📂' in str(name):
            continue
        ptype = str(ws.cell(r, 12).value or '').strip()
        if ptype == 'متغیر':
            continue
        pid = ws.cell(r, 14).value
        vid = ws.cell(r, 15).value
        b = ws.cell(r, 2).value
        f = ws.cell(r, 6).value

        if not b or not pid:
            continue

        if f and f > 0:
            cat_discounted += 1
        else:
            cat_regular += 1

print(f"Catalog priced items: {cat_discounted + cat_regular}")
print(f"Catalog discounted (F > 0): {cat_discounted}")
print(f"Catalog regular (no F): {cat_regular}")

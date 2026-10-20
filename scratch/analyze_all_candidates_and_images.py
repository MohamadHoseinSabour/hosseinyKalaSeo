import os
import sys
import json
import re
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('hosseiny_kala_catalog.xlsx', data_only=True)
category_sheets = [
    'یخچال و فریزر',
    'شستشو و نظافت',
    'لوازم برقی و پخت و پز',
    'نوشیدنی ساز',
    'سرمایش و گرمایش',
    'تصفیه کننده آب',
    'صوتی و تصویری',
    'زیبایی و سلامت فردی'
]

# Collect all catalog rows
catalog_rows = []
for sheet in category_sheets:
    if sheet not in wb.sheetnames:
        continue
    ws = wb[sheet]
    current_parent = None
    for r in range(2, ws.max_row + 1):
        name = ws.cell(row=r, column=1).value
        if not name or '📂' in str(name):
            continue
        name_str = str(name).strip()
        status = str(ws.cell(row=r, column=18).value or '').strip()
        stock = str(ws.cell(row=r, column=8).value or '').strip()
        pid = ws.cell(row=r, column=14).value
        ptype = str(ws.cell(row=r, column=12).value or 'ساده').strip()
        var_attr = str(ws.cell(row=r, column=13).value or '').strip()

        if not name_str.startswith('↳'):
            current_parent = name_str
            parent_name = None
        else:
            parent_name = current_parent

        catalog_rows.append({
            'sheet': sheet,
            'row': r,
            'name': name_str,
            'parent_name': parent_name,
            'status': status,
            'stock': stock,
            'price_rial': ws.cell(row=r, column=2).value,
            'price_toman': ws.cell(row=r, column=3).value,
            'main_cat': str(ws.cell(row=r, column=9).value or sheet).strip(),
            'subcat': str(ws.cell(row=r, column=10).value or '').strip(),
            'brand': str(ws.cell(row=r, column=11).value or '').strip(),
            'ptype': ptype,
            'variant_attr': var_attr,
            'pid': pid,
            'vid': ws.cell(row=r, column=15).value,
            'link': ws.cell(row=r, column=16).value,
            'sku': ws.cell(row=r, column=17).value
        })

print(f"Total rows in catalog: {len(catalog_rows)}")

# Collect all images from product_images_2026-10-05 and extracted_products
# Let's map each product to images
pi_base = 'product_images_2026-10-05'

# Folders inside product_images_2026-10-05
folder_images = {}
for cat in os.listdir(pi_base):
    cat_p = os.path.join(pi_base, cat)
    if not os.path.isdir(cat_p):
        continue
    for sub in os.listdir(cat_p):
        sub_p = os.path.join(cat_p, sub)
        if os.path.isdir(sub_p):
            imgs = [os.path.join(sub_p, f) for f in os.listdir(sub_p) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
            spec_file = os.path.join(sub_p, 'مشخصات_محصول.txt')
            specs = ""
            if os.path.exists(spec_file):
                with open(spec_file, 'r', encoding='utf-8') as sf:
                    specs = sf.read()
            folder_images[sub] = {
                'category_dir': cat,
                'path': sub_p,
                'images': imgs,
                'specs': specs
            }

print(f"Total product folders found in {pi_base}: {len(folder_images)}")

# Standalone files inside product_images_2026-10-05
standalone_files = {}
for cat in os.listdir(pi_base):
    cat_p = os.path.join(pi_base, cat)
    if not os.path.isdir(cat_p):
        continue
    for f in os.listdir(cat_p):
        fp = os.path.join(cat_p, f)
        if os.path.isfile(fp) and fp.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            standalone_files[f] = {
                'category_dir': cat,
                'path': fp
            }
print(f"Total standalone verified image files: {len(standalone_files)}")

# Filter for products to create: status == 'در سایت تعریف نشده'
# Remember rule: 'فعلا دست نگه دار' MUST BE EXCLUDED!
unregistered = [r for r in catalog_rows if r['status'] == 'در سایت تعریف نشده']
print(f"Total unregistered items in Excel: {len(unregistered)}")

# Group unregistered into products (parent items and simple items)
products_to_create = []
i = 0
while i < len(unregistered):
    item = unregistered[i]
    if item['ptype'] == 'متغیر' and not item['parent_name']:
        # This is a variable parent!
        # Gather all its variations
        variations = []
        j = i + 1
        while j < len(unregistered) and unregistered[j]['parent_name'] == item['name']:
            variations.append(unregistered[j])
            j += 1
        products_to_create.append({
            'type': 'variable',
            'parent': item,
            'variations': variations
        })
        i = j
    elif not item['parent_name']:
        # Simple product
        products_to_create.append({
            'type': 'simple',
            'parent': item,
            'variations': []
        })
        i += 1
    else:
        # It's an orphan variation or variation listed without parent in unregistered?
        # Let's check
        products_to_create.append({
            'type': 'orphan_variation',
            'parent': item,
            'variations': []
        })
        i += 1

print(f"\nGrouped products to create: {len(products_to_create)}")
for idx, p in enumerate(products_to_create, 1):
    ptype = p['type']
    parent = p['parent']
    vars_cnt = len(p['variations'])
    print(f"{idx:2d}. [{parent['sheet']}] Row {parent['row']}: {parent['name']} ({ptype}, vars: {vars_cnt}, brand: {parent['brand']})")

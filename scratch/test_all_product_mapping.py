import os
import sys
import json
import re
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

# Run analysis and matching for all 61 products
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

unregistered = [r for r in catalog_rows if r['status'] == 'در سایت تعریف نشده']

products = []
i = 0
while i < len(unregistered):
    item = unregistered[i]
    if item['ptype'] == 'متغیر' and not item['parent_name']:
        variations = []
        j = i + 1
        while j < len(unregistered) and unregistered[j]['parent_name'] == item['name']:
            variations.append(unregistered[j])
            j += 1
        products.append({
            'type': 'variable',
            'parent': item,
            'variations': variations
        })
        i = j
    elif not item['parent_name']:
        products.append({
            'type': 'simple',
            'parent': item,
            'variations': []
        })
        i += 1
    else:
        products.append({
            'type': 'simple',
            'parent': item,
            'variations': []
        })
        i += 1

print(f"Total products to create: {len(products)}")

# Gather all images across system
pi_dir = 'product_images_2026-10-05'

def find_images_for_product(p):
    pname = p['parent']['name']
    brand = p['parent']['brand']
    sheet = p['parent']['sheet']
    
    found = []
    specs = ""
    
    # 1. Search in product_images_2026-10-05 folders
    for cat in os.listdir(pi_dir):
        cat_p = os.path.join(pi_dir, cat)
        if not os.path.isdir(cat_p):
            continue
        for sub in os.listdir(cat_p):
            sub_p = os.path.join(cat_p, sub)
            if os.path.isdir(sub_p):
                # match sub name
                if sub.strip() == pname.strip() or sub.strip() in pname.strip() or pname.strip() in sub.strip():
                    imgs = [os.path.join(sub_p, f) for f in os.listdir(sub_p) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
                    if imgs:
                        found.extend(imgs)
                        sp_p = os.path.join(sub_p, 'مشخصات_محصول.txt')
                        if os.path.exists(sp_p):
                            with open(sp_p, 'r', encoding='utf-8') as sf:
                                specs = sf.read()
    
    # 2. Search standalone verified files in product_images_2026-10-05
    if not found:
        # Check mapping rules
        # e.g., himalia-ice-pool-60mw-twin-white.jpg
        name_lower = pname.lower()
        for cat in os.listdir(pi_dir):
            cat_p = os.path.join(pi_dir, cat)
            if not os.path.isdir(cat_p):
                continue
            for f in os.listdir(cat_p):
                fp = os.path.join(cat_p, f)
                if os.path.isfile(fp) and fp.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    f_base = os.path.splitext(f)[0].lower()
                    
                    # Custom matching logic for known verified files
                    if 'himalia' in f_base and '60mw' in f_base and 'هیمالیا' in pname and '60mw' in name_lower:
                        found.append(fp)
                    elif 'niksan' in f_base and 'rf8410' in f_base and 'نیکسان' in pname and 'rf8410' in name_lower:
                        found.append(fp)
                    elif 'clover' in f_base and 'rosso' in f_base and 'water' in f_base and 'کلور' in pname and 'روسو' in pname and 'آبریز' in pname:
                        found.append(fp)
                    elif 'clover' in f_base and 'rosso' in f_base and 'homebar' in f_base and 'کلور' in pname and 'روسو' in pname and 'هوم بار' in pname:
                        found.append(fp)
                    elif 'clover' in f_base and 'mini' in f_base and 'کلور' in pname and 'مینی' in pname:
                        found.append(fp)
                    elif 'pakshoma' in f_base and 'twin-tub' in f_base and 'پاکشوما' in pname and 'دوقلو' in pname:
                        found.append(fp)
                    elif 'saper' in f_base and '4025' in f_base and 'ساپر' in pname and '4025' in pname:
                        found.append(fp)
                    elif 'saper' in f_base and 'iron' in f_base and 'ساپر' in pname and '4035' in pname:
                        found.append(fp)
                    elif 'feridolin' in f_base and 'sw35' in f_base and 'فریدولین' in pname:
                        found.append(fp)
                    elif 'panda' in f_base and '80l' in f_base and 'پاندا' in pname:
                        found.append(fp)
                    elif 'pakizan' in f_base and 'blanket' in f_base and 'پاکیزان' in pname:
                        found.append(fp)
                    elif 'aviz' in f_base and 'granite-pan' in f_base and 'اویز' in pname:
                        found.append(fp)
                    elif 'alton' in f_base and 'oven' in f_base and 'آلتون' in pname and '7303' in pname:
                        found.append(fp)
                    elif 'willez' in f_base and 'chopper' in f_base and 'ویلز' in pname and 'خردکن' in pname:
                        found.append(fp)
                    elif 'volga' in f_base and 'kettle' in f_base and 'وولگا' in pname:
                        found.append(fp)
                    elif 'kenwood' in f_base and 'hm430' in f_base and 'کنوود' in pname:
                        found.append(fp)
                    elif 'korkmaz' in f_base and 'a331' in f_base and 'کورکماز' in pname:
                        found.append(fp)
                    elif 'parskhazar' in f_base and 'fh2000p' in f_base and 'پارس خزر' in pname and '2000' in pname:
                        found.append(fp)
                    elif 'parskhazar' in f_base and '4060' in f_base and 'پارس خزر' in pname and 'پنکه' in pname:
                        found.append(fp)
                    elif 'polar' in f_base and '3pn' in f_base and 'پلار' in pname:
                        found.append(fp)
                    elif 'promaron' in f_base and 'پرومارون' in pname and '731' in pname:
                        found.append(fp)

    # 3. If still not found, search in extracted_products or new_products or scratch/candidates
    if not found:
        # Search extracted_products
        for root, dirs, files in os.walk('extracted_products'):
            folder_name = os.path.basename(root)
            if folder_name and (folder_name in pname or pname in folder_name):
                imgs = [os.path.join(root, f) for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
                if imgs:
                    found.extend(imgs)
                    break
                    
    return list(set(found)), specs

results = []
for idx, p in enumerate(products, 1):
    imgs, specs = find_images_for_product(p)
    p['images'] = imgs
    p['specs'] = specs
    results.append(p)
    status_str = f"✅ {len(imgs)} images" if imgs else "❌ NO IMAGE"
    print(f"{idx:2d}. [{p['parent']['sheet']}] Row {p['parent']['row']:2d}: {p['parent']['name']} -> {status_str}")

with_images = [p for p in results if p['images']]
without_images = [p for p in results if not p['images']]
print(f"\nSummary:")
print(f"Total products: {len(results)}")
print(f"Products WITH images: {len(with_images)}")
print(f"Products WITHOUT images: {len(without_images)}")

if without_images:
    print("\nProducts without images:")
    for p in without_images:
        print(f"  - Row {p['parent']['row']}: {p['parent']['name']}")

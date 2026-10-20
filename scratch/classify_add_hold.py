import os, sys, openpyxl

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('hosseiny_kala_catalog.xlsx', data_only=True)
img_base = 'new_product_images'

# Get all folders and image files
cat_folders = {}
for c in os.listdir(img_base):
    cp = os.path.join(img_base, c)
    if os.path.isdir(cp):
        cat_folders[c] = {}
        for p in os.listdir(cp):
            pp = os.path.join(cp, p)
            if os.path.isdir(pp):
                imgs = [f for f in os.listdir(pp) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
                cat_folders[c][p] = {
                    'path': pp,
                    'images': imgs,
                    'txts': [f for f in os.listdir(pp) if f.lower().endswith('.txt')]
                }

print("Loaded available folders with images.")

# Now scan catalog
to_add = []
to_hold = []

for sname in wb.sheetnames:
    ws = wb[sname]
    for r in range(2, ws.max_row + 1):
        name = ws.cell(r, 1).value
        status_r = ws.cell(r, 18).value
        if not name or str(name).strip().startswith('📂'):
            continue
        if status_r == 'در سایت تعریف نشده':
            name_str = str(name).strip()
            
            # Find matching folder across cat_folders
            matched = None
            matched_cat = None
            
            # 1. Exact match in corresponding sheet category or any category
            if sname in cat_folders and name_str in cat_folders[sname]:
                matched = cat_folders[sname][name_str]
                matched_cat = sname
            else:
                for c, prods in cat_folders.items():
                    if name_str in prods:
                        matched = prods[name_str]
                        matched_cat = c
                        break
            
            # 2. If not matched, try fuzzy
            if not matched:
                # variations handling or partial match
                for c, prods in cat_folders.items():
                    for pname, pdata in prods.items():
                        if name_str in pname or pname in name_str:
                            matched = pdata
                            matched_cat = c
                            break
                    if matched:
                        break
            
            # Check if variation of a parent
            # e.g. Row 23, 24 under 'یخچال و فریزر دوقلو دیپوینت مدل اکسپلور (Explore)'
            # Row 26, 27 under 'یخچال و فریزر کمبی دیپوینت مدل دیسنت (Decent)'
            # Row 79 under 'خردکن برقی کاسه دار ویلز'
            # Row 21 under 'کتری برقی رترو ۲۲۰۰ وات وستینگهاوس مدل WKKE210'
            
            # Let's inspect if matched and has images
            has_img = matched and len(matched['images']) > 0
            
            item_info = {
                'sheet': sname,
                'row': r,
                'name': name_str,
                'status_r': status_r,
                'pid': ws.cell(r, 15).value,
                'matched': matched,
                'matched_cat': matched_cat,
                'has_images': has_img
            }
            
            if has_img:
                to_add.append(item_info)
            else:
                to_hold.append(item_info)

print(f"\nTotal TO_ADD (with images): {len(to_add)}")
for item in to_add:
    imgs = item['matched']['images']
    print(f"  [ADD] [{item['sheet']} | Row {item['row']}] '{item['name']}' -> Folder: {item['matched']['path']} ({len(imgs)} images: {imgs})")

print(f"\nTotal TO_HOLD (no images / folder deleted): {len(to_hold)}")
for item in to_hold:
    print(f"  [HOLD] [{item['sheet']} | Row {item['row']}] '{item['name']}'")

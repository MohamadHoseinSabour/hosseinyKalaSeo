import os, sys, openpyxl

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('hosseiny_kala_catalog.xlsx', data_only=True)

img_base = 'new_product_images'

# Collect all image folders
# new_product_images/<category_folder>/<product_folder>/...
available_folders = {}
for cat_dir in os.listdir(img_base):
    cat_path = os.path.join(img_base, cat_dir)
    if os.path.isdir(cat_path):
        for prod_dir in os.listdir(cat_path):
            prod_path = os.path.join(cat_path, prod_dir)
            if os.path.isdir(prod_path):
                files = [f for f in os.listdir(prod_path) if os.path.isfile(os.path.join(prod_path, f))]
                available_folders[prod_dir.strip()] = {
                    'cat_dir': cat_dir,
                    'prod_dir': prod_dir,
                    'path': prod_path,
                    'files': files
                }

print(f"Total product folders found in new_product_images: {len(available_folders)}")
for k, v in available_folders.items():
    print(f"  [{v['cat_dir']}] '{k}' -> {len(v['files'])} files: {v['files']}")

print("\n" + "="*80)
print("Matching with catalog rows where status is 'در سایت تعریف نشده':")
print("="*80)

has_images = []
no_images = []

for sheetname in wb.sheetnames:
    ws = wb[sheetname]
    for r in range(2, ws.max_row + 1):
        name = ws.cell(r, 1).value
        status_r = ws.cell(r, 18).value
        if not name or str(name).strip().startswith('📂'):
            continue
        
        name_str = str(name).strip()
        
        if status_r == 'در سایت تعریف نشده':
            # Check if matching folder exists
            # Direct match
            matched = None
            if name_str in available_folders:
                matched = available_folders[name_str]
            else:
                # Try fuzzy or stripped match
                for folder_name, folder_info in available_folders.items():
                    if folder_name in name_str or name_str in folder_name:
                        matched = folder_info
                        break
            
            item_data = {
                'sheet': sheetname,
                'row': r,
                'name': name_str,
                'matched_folder': matched,
                'price_rial': ws.cell(r, 2).value,
                'brand': ws.cell(r, 10).value,
                'cat_col': ws.cell(r, 12).value
            }
            
            if matched and len(matched['files']) > 0:
                has_images.append(item_data)
            else:
                no_images.append(item_data)

print(f"\nItems WITH images ({len(has_images)}):")
for item in has_images:
    mf = item['matched_folder']
    print(f"  [{item['sheet']} | Row {item['row']}] '{item['name']}' -> Folder: '{mf['prod_dir']}' ({len(mf['files'])} files)")

print(f"\nItems WITHOUT images or folder deleted ({len(no_images)}):")
for item in no_images:
    mf_name = item['matched_folder']['prod_dir'] if item['matched_folder'] else 'None'
    print(f"  [{item['sheet']} | Row {item['row']}] '{item['name']}' -> Match: {mf_name}")

print("\n" + "="*80)
print("Are there any folders in new_product_images that were NOT matched to 'در سایت تعریف نشده' rows?")
matched_folder_names = set(item['matched_folder']['prod_dir'] for item in has_images)
unmatched_folders = [f for f in available_folders if f not in matched_folder_names]
if unmatched_folders:
    print(f"Unmatched folders ({len(unmatched_folders)}):")
    for f in unmatched_folders:
        print(f"  '{f}' in {available_folders[f]['cat_dir']}")
else:
    print("All folders in new_product_images were successfully matched!")

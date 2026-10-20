import json
import glob
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/missing_products.json', encoding='utf-8') as f:
    missing = json.load(f)

# Get all current approved slugs/files
approved_files = glob.glob('product_images_2026-10-05/**/*.jpg', recursive=True)
approved_basenames = [os.path.splitext(os.path.basename(f))[0] for f in approved_files]

print(f"Total missing in catalog: {len(missing)}")
print(f"Total approved image files: {len(approved_files)}")

# Let's map sheet to folder
SHEET_MAP = {
    'یخچال و فریزر': 'refrigerators',
    'شستشو و نظافت': 'washing_and_cleaning',
    'لوازم برقی و پخت و پز': 'cooking_appliances',
    'سرمایش و گرمایش': 'cooling_heating',
    'نوشیدنی ساز': 'beverage_makers',
    'زیبایی و سلامت فردی': 'beauty_health',
    'تصفیه کننده آب': 'water_purifiers'
}

remaining = []
for item in missing:
    sheet = item.get('sheet')
    folder = SHEET_MAP.get(sheet, 'misc')
    name = item.get('name')
    parent = item.get('parent_name')
    brand = item.get('brand')
    row = item.get('row')
    
    # Check if any approved file matches this item
    # We can check by slug or name
    # Let's print remaining by categories
    remaining.append({
        'row': row,
        'sheet': sheet,
        'folder': folder,
        'brand': brand,
        'name': name,
        'parent_name': parent,
        'is_variation': item.get('is_variation')
    })

print(f"Remaining list count: {len(remaining)}")

# Group remaining by folder
grouped = {}
for r in remaining:
    grouped.setdefault(r['folder'], []).append(r)

for f, lst in grouped.items():
    print(f"\nFolder [{f}]: {len(lst)} items")
    for r in lst[:5]:
        p = r['parent_name']
        n = r['name']
        full = f"{p} -> {n}" if p else n
        print(f"  Row {r['row']}: [{r['brand']}] {full}")

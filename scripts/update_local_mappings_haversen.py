import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"c:\Users\mmhhs\OneDrive\Documents\GitHub\hosseinyKalaSeo"
DATA_DIR = os.path.join(PROJECT_DIR, 'data')

# ۱. به‌روزرسانی data/products.json
prod_file = os.path.join(DATA_DIR, 'products.json')
with open(prod_file, 'r', encoding='utf-8') as f:
    products = json.load(f)

for p in products:
    if p.get('id') == 3516:
        p['name'] = 'تلویزیون ال ای دی ۳۲ اینچ هاورسن مدل HD'
        p['slug'] = 'haverson-32-inch-hd-led-tv'
        p['brand'] = 'هاورسن'
    elif p.get('id') == 3534:
        p['name'] = 'تلویزیون ال ای دی ۸۵ اینچ هوشمند 4K اسمارت هاورسن مدل Ultra HD'
        p['slug'] = 'haverson-85-inch-4k-smart-tv'
        p['brand'] = 'هاورسن'
    elif p.get('id') in [3520, 3523, 3531]:
        # هماهنگ‌سازی برند تمامی مدل‌های هاورسن
        p['brand'] = 'هاورسن'

with open(prod_file, 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=2)
print("✅ data/products.json به‌روزرسانی شد.")

# ۲. به‌روزرسانی data/id_mappings.json
id_map_file = os.path.join(DATA_DIR, 'id_mappings.json')
with open(id_map_file, 'r', encoding='utf-8') as f:
    id_mappings = json.load(f)

if '3516' in id_mappings:
    id_mappings['3516']['name'] = 'تلویزیون ال ای دی ۳۲ اینچ هاورسن مدل HD'
    id_mappings['3516']['slug'] = 'haverson-32-inch-hd-led-tv'
    id_mappings['3516']['url'] = 'https://hosseinykala.ir/product/haverson-32-inch-hd-led-tv/'

if '3534' in id_mappings:
    id_mappings['3534']['name'] = 'تلویزیون ال ای دی ۸۵ اینچ هوشمند 4K اسمارت هاورسن مدل Ultra HD'
    id_mappings['3534']['slug'] = 'haverson-85-inch-4k-smart-tv'
    id_mappings['3534']['url'] = 'https://hosseinykala.ir/product/haverson-85-inch-4k-smart-tv/'

with open(id_map_file, 'w', encoding='utf-8') as f:
    json.dump(id_mappings, f, ensure_ascii=False, indent=2)
print("✅ data/id_mappings.json به‌روزرسانی شد.")

# ۳. به‌روزرسانی data/current_catalog_reference.json
ref_file = os.path.join(DATA_DIR, 'current_catalog_reference.json')
with open(ref_file, 'r', encoding='utf-8') as f:
    ref = json.load(f)

for p in ref.get('live_products', []):
    if p.get('id') == 3516:
        p['name'] = 'تلویزیون ال ای دی ۳۲ اینچ هاورسن مدل HD'
        p['slug'] = 'haverson-32-inch-hd-led-tv'
        p['brand'] = 'هاورسن'
    elif p.get('id') == 3534:
        p['name'] = 'تلویزیون ال ای دی ۸۵ اینچ هوشمند 4K اسمارت هاورسن مدل Ultra HD'
        p['slug'] = 'haverson-85-inch-4k-smart-tv'
        p['brand'] = 'هاورسن'
    elif p.get('id') in [3520, 3523, 3531]:
        p['brand'] = 'هاورسن'

with open(ref_file, 'w', encoding='utf-8') as f:
    json.dump(ref, f, ensure_ascii=False, indent=2)
print("✅ data/current_catalog_reference.json به‌روزرسانی شد.")

# ۴. نگاشت صریح و ماندگار حسابداری در data/inventory_mapping_standard.json
mapping_std_file = os.path.join(DATA_DIR, 'inventory_mapping_standard.json')
mapping_std = {}
if os.path.exists(mapping_std_file):
    try:
        with open(mapping_std_file, 'r', encoding='utf-8') as f:
            mapping_std = json.load(f)
    except Exception:
        mapping_std = {}

if "accounting_aliases" not in mapping_std:
    mapping_std["accounting_aliases"] = {}

# ثبت نگاشت‌های نرم‌افزار حسابداری (شامل عبارات انگلیسی انبار به شناسه‌های معتبر سایت)
mapping_std["accounting_aliases"].update({
    "32aversen": {"product_id": 3516, "brand": "هاورسن", "name": "تلویزیون ال ای دی ۳۲ اینچ هاورسن مدل HD"},
    "32averson": {"product_id": 3516, "brand": "هاورسن", "name": "تلویزیون ال ای دی ۳۲ اینچ هاورسن مدل HD"},
    "85aversen": {"product_id": 3534, "brand": "هاورسن", "name": "تلویزیون ال ای دی ۸۵ اینچ هوشمند 4K اسمارت هاورسن مدل Ultra HD"},
    "85averson": {"product_id": 3534, "brand": "هاورسن", "name": "تلویزیون ال ای دی ۸۵ اینچ هوشمند 4K اسمارت هاورسن مدل Ultra HD"},
    "75aversen": {"product_id": 3531, "brand": "هاورسن", "name": "تلویزیون ال ای دی ۷۵ اینچ هوشمند 4K هاورسون مدل Cinema HDR"},
    "65aversen": {"product_id": 3523, "brand": "هاورسن", "name": "تلویزیون ال ای دی ۶۵ اینچ هوشمند 4K هاورسون مدل Frameless IPS"},
    "55aversen": {"product_id": 3520, "brand": "هاورسن", "name": "تلویزیون ال ای دی ۵۵ اینچ هوشمند 4K هاورسون مدل Smart Android"},
})

with open(mapping_std_file, 'w', encoding='utf-8') as f:
    json.dump(mapping_std, f, ensure_ascii=False, indent=2)
print("✅ data/inventory_mapping_standard.json با نگاشت‌های حسابداری به‌روزرسانی شد.")

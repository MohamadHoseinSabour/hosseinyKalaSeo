import json
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/catalog_current_rows.json', encoding='utf-8') as f:
    rows = json.load(f)

# Load entities
entities = []
curr = None
for r in rows:
    if not r['is_variation']:
        curr = {
            'sheet': r['sheet'],
            'folder': r['folder'],
            'parent_row': r['row'],
            'name': r['name'],
            'brand': r['brand'],
            'ptype': r['ptype'],
            'status': r['status'],
            'variations': []
        }
        entities.append(curr)
    else:
        if curr:
            curr['variations'].append(r)

# Approved mapped keys
from map_all_images_to_catalog import image_mapping

unlisted_active = [e for e in entities if e['status'] == 'در سایت تعریف نشده']
mapped_active = set()
for img_name, meta in image_mapping.items():
    ent = next((e for e in entities if e['sheet'] == meta['sheet'] and e['parent_row'] == meta['row']), None)
    if ent and ent['status'] == 'در سایت تعریف نشده':
        mapped_active.add((ent['sheet'], ent['parent_row']))

missing_63 = [e for e in unlisted_active if (e['sheet'], e['parent_row']) not in mapped_active]
print(f"Total missing: {len(missing_63)}")

def sanitize(name):
    for c in '<>:"/\\|?*':
        name = name.replace(c, '-')
    return name.strip(' .')

for i, e in enumerate(missing_63, 1):
    brand = e['brand']
    pname = e['name']
    # If brand not in pname, prepend brand
    folder_name = pname if brand.lower() in pname.lower() or brand in ['متفرقه', ''] else f"{brand} - {pname}"
    folder_name = sanitize(folder_name)
    e['proposed_folder'] = folder_name
    print(f"{i:2d}. [{e['folder']}] {folder_name}")

with open('scratch/proposed_folders.json', 'w', encoding='utf-8') as f:
    json.dump(missing_63, f, ensure_ascii=False, indent=2)

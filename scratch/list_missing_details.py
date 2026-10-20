import json
import os
import glob
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_candidates_harvested.json', encoding='utf-8') as f:
    items = json.load(f)

approved_files = [os.path.basename(f) for f in glob.glob('product_images_2026-10-05/*/*.jpg')]

missing_items = []
for it in items:
    slug = it.get('slug', '')
    matched = False
    for af in approved_files:
        af_base = os.path.splitext(af)[0]
        if slug == af_base or af_base.startswith(slug) or slug.startswith(af_base):
            matched = True
            break
    if not matched:
        missing_items.append(it)

print(f"Total catalog items needing exact matching: {len(missing_items)}")

by_cat = {}
for it in missing_items:
    c = it.get('sheet_folder', 'other')
    by_cat.setdefault(c, []).append(it)

for c, it_list in by_cat.items():
    print(f"\n=== Category: {c} ({len(it_list)} items) ===")
    for it in it_list:
        row = it.get('row')
        p = it.get('parent_name', '')
        n = it.get('name', '')
        b = it.get('brand', '')
        full = f"{p} -> {n}" if p else n
        print(f"  Row {row}: [{b}] {full}")

import sys
import os
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('product_images_2026-10-05/verification_report.json', 'r', encoding='utf-8') as f:
    rep = json.load(f)

approved = rep.get('approved_items', [])
print(f"Total approved: {len(approved)}")
for it in approved:
    row = it.get('row')
    sheet = it.get('sheet_folder') or it.get('category')
    name = it.get('name') or it.get('filename')
    slug = it.get('slug')
    path = it.get('dest_path') or it.get('relative_path')
    print(f"Row {row} [{sheet}] - Name: {name} | Slug: {slug} | Path: {path}")

if os.path.exists('scratch/all_candidates_harvested.json'):
    with open('scratch/all_candidates_harvested.json', 'r', encoding='utf-8') as f:
        harv = json.load(f)
    print(f"\nHarvested candidates count: {len(harv)}")

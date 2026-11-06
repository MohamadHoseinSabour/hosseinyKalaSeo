import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/products_44_master_data.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

print(f"{'#':2s} | {'Slug':38s} | {'Brand':10s} | {'Model':12s} | {'Persian Name'}")
print("-" * 100)
for i, p in enumerate(master):
    img_info_path = os.path.join('data', 'new_products', p['slug'], 'images', 'image_info.json')
    curr_title = ""
    if os.path.exists(img_info_path):
        with open(img_info_path, 'r', encoding='utf-8') as fi:
            curr_title = json.load(fi).get('source_title', '')[:30]
    print(f"{i+1:2d} | {p['slug']:38s} | {p['brand_fa']:10s} | {p['model']:12s} | {p['name'][:30]} | {curr_title}")

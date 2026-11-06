import os
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

base = 'data/new_products'
for folder in sorted(os.listdir(base)):
    fpath = os.path.join(base, folder, 'images', 'image_info.json')
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            d = json.load(f)
            st = d.get('source_title', '')
            print(f"{folder[:38]:38s} | {st[:45]}")

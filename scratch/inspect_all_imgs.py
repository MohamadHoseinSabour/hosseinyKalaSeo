import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_61_products.json', 'r', encoding='utf-8') as f:
    prods = json.load(f)

print(f"Total products: {len(prods)}")
total_imgs = 0
for i, p in enumerate(prods, 1):
    imgs = p.get('images', [])
    total_imgs += len(imgs)
    print(f"{i:2d}. {p['name']} ({p['type']}) -> {len(imgs)} images:")
    for img in imgs:
        size_kb = os.path.getsize(img) / 1024 if os.path.exists(img) else -1
        print(f"     - {os.path.basename(img)} ({size_kb:.1f} KB)")

print(f"\nTotal image files to process & upload: {total_imgs}")

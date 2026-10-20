import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

img_dir = 'product_images_2026-10-05'
print(f"Listing all files in {img_dir}:")
for root, dirs, files in os.walk(img_dir):
    for f in sorted(files):
        rel_p = os.path.relpath(os.path.join(root, f), img_dir)
        size_kb = os.path.getsize(os.path.join(root, f)) / 1024
        print(f"  {rel_p} ({size_kb:.1f} KB)")

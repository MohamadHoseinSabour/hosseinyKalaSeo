import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

img_dir = 'product_images_2026-10-05'
for cat in sorted(os.listdir(img_dir)):
    p = os.path.join(img_dir, cat)
    if os.path.isdir(p):
        print(f"\nCategory dir: {cat}")
        subitems = sorted(os.listdir(p))
        for item in subitems:
            item_p = os.path.join(p, item)
            if os.path.isdir(item_p):
                files = os.listdir(item_p)
                print(f"  [Folder] {item} -> files: {files}")
            else:
                size_kb = os.path.getsize(item_p) / 1024
                print(f"  [File] {item} ({size_kb:.1f} KB)")

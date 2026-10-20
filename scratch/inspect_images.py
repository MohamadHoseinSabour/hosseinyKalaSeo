import os, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

img_dir = 'new_product_images'
print("Folders and files in new_product_images:")
if os.path.exists(img_dir):
    for root, dirs, files in os.walk(img_dir):
        rel = os.path.relpath(root, img_dir)
        if rel == '.':
            print("Direct subfolders in new_product_images:")
            for d in dirs:
                sub_files = os.listdir(os.path.join(img_dir, d))
                print(f"  Folder: '{d}' -> {len(sub_files)} files: {sub_files[:5]}")
            for f in files:
                print(f"  File: {f}")
        else:
            pass
else:
    print("new_product_images directory does not exist!")

print("\nLet's check any other image folders in workspace:")
for d in os.listdir('.'):
    if 'image' in d.lower() or 'prod' in d.lower():
        print(f"  {d}")

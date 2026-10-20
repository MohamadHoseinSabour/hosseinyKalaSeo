import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/created_product_folders.json', encoding='utf-8') as f:
    created = json.load(f)

print(f"Total folders originally created: {len(created)}")

existing_with_images = []
existing_without_images = []
deleted_folders = []

img_exts = ('.jpg', '.jpeg', '.png', '.webp', '.avif')

for item in created:
    path = item['path']
    if not os.path.exists(path):
        deleted_folders.append(item)
    else:
        files = os.listdir(path)
        imgs = [f for f in files if f.lower().endswith(img_exts)]
        if len(imgs) > 0:
            item['images'] = imgs
            existing_with_images.append(item)
        else:
            item['images'] = []
            existing_without_images.append(item)

print(f"1. Folders that were DELETED by user: {len(deleted_folders)}")
print(f"2. Folders that EXIST but have NO images: {len(existing_without_images)}")
print(f"3. Folders that EXIST and HAVE images: {len(existing_with_images)}")
print(f"Sum: {len(deleted_folders) + len(existing_without_images) + len(existing_with_images)}")

hold_candidates = deleted_folders + existing_without_images
print(f"\nTotal items to set to 'فعلا دست نگه دار': {len(hold_candidates)}")

for h in hold_candidates:
    reason = "Deleted folder" if h in deleted_folders else "Folder has no images"
    print(f"[{h['sheet']} | Row {h['row']}] {h['folder_name']} ({reason})")

print(f"\n--- Details of Folders that HAVE images ({len(existing_with_images)} items) ---")
for a in existing_with_images:
    print(f"[{a['sheet']} | Row {a['row']}] {a['folder_name']} -> {len(a['images'])} image(s)")

with open('scratch/user_changes_audit.json', 'w', encoding='utf-8') as f:
    json.dump({
        'deleted_folders': deleted_folders,
        'existing_without_images': existing_without_images,
        'existing_with_images': existing_with_images,
        'hold_candidates': hold_candidates
    }, f, ensure_ascii=False, indent=2)

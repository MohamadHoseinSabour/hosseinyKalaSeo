import json
import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. Backup hold images first
hold_images = [
    'cooling_heating/butan-b3115-water-heater.jpg',
    'cooling_heating/sunny-fan.jpg',
    'refrigerators/himalia-omega-homebar-combi-white.jpg',
    'refrigerators/himalia-5mode-homebar-combi-leather.jpg',
    'refrigerators/himalia-combi-850-titanium-70-30.jpg',
    'washing_and_cleaning/daewoo-dwk-990-washing-machine-white.jpg',
    'washing_and_cleaning/daewoo-dwk-990s-washing-machine-silver.jpg',
    'washing_and_cleaning/donalex-vacuum.jpg',
    'cooking_appliances/parskhazar-rc181ts-silver-rice-cooker.jpg',
]

os.makedirs('scratch/hold_images_backup', exist_ok=True)
for rel in hold_images:
    src = os.path.join('product_images_2026-10-05', rel)
    if os.path.exists(src):
        dst = os.path.join('scratch/hold_images_backup', os.path.basename(rel))
        shutil.copy2(src, dst)
        print(f"Backed up to scratch: {rel}")

# 2. Delete hold images from product_images_2026-10-05
deleted_count = 0
for rel in hold_images:
    src = os.path.join('product_images_2026-10-05', rel)
    if os.path.exists(src):
        os.remove(src)
        deleted_count += 1
        print(f"Deleted from product_images: {rel}")

print(f"\nTotal hold images deleted: {deleted_count}")

# 3. Check remaining images in product_images_2026-10-05
import glob
remaining_images = glob.glob('product_images_2026-10-05/*/*.jpg')
print(f"Total remaining approved images in product_images_2026-10-05: {len(remaining_images)}")

# 4. Update verification_report.json
rep_file = 'product_images_2026-10-05/verification_report.json'
if os.path.exists(rep_file):
    with open(rep_file, encoding='utf-8') as f:
        rep = json.load(f)
    
    # Filter out deleted items from approved_items
    hold_basenames = [os.path.basename(x) for x in hold_images]
    rep['approved_items'] = [it for it in rep['approved_items'] if it['filename'] not in hold_basenames]
    rep['total_approved_images'] = len(rep['approved_items'])
    
    # Update categories breakdown
    from collections import Counter
    cb = Counter([it['category'] for it in rep['approved_items']])
    rep['categories_breakdown'] = dict(cb)
    
    with open(rep_file, 'w', encoding='utf-8') as f:
        json.dump(rep, f, ensure_ascii=False, indent=2)
    print(f"Updated {rep_file} successfully. New total: {rep['total_approved_images']}")

import os
import sys
import json
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

base = 'new_product_images'

with open('scratch/phase1_image_results.json', 'r', encoding='utf-8') as f:
    phase1 = json.load(f)

downloaded = []
pending = []

for root, dirs, files in os.walk(base):
    for file in files:
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            fpath = os.path.join(root, file)
            rel_path = os.path.relpath(fpath, base)
            parts = rel_path.split(os.sep)
            cat = parts[0]
            prod = parts[1]
            try:
                im = Image.open(fpath)
                sz = os.path.getsize(fpath) // 1024
                # find match info from phase1
                m_info = next((p for p in phase1 if p.get('name') == prod), None)
                matched_title = m_info.get('matched_title') if m_info else "Manual / Direct Match"
                downloaded.append({
                    'category': cat,
                    'prod': prod,
                    'file': file,
                    'size': im.size,
                    'size_kb': sz,
                    'matched_title': matched_title,
                    'path': fpath
                })
            except Exception as e:
                print(f"Error reading {fpath}: {e}")

print("==================================================")
print(f"DOWNLOADED & VERIFIED IMAGES ({len(downloaded)} items):")
print("==================================================")
for idx, d in enumerate(downloaded, 1):
    print(f"[{idx:02d}] 📁 {d['category']} -> {d['prod']}")
    print(f"     ابعاد: {d['size'][0]}x{d['size'][1]} | حجم: {d['size_kb']} KB")
    print(f"     عنوان تطبیق‌یافته: {d['matched_title']}\n")

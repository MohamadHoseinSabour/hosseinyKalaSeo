import json
import os
import glob
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_candidates_harvested.json', encoding='utf-8') as f:
    items = json.load(f)

print(f"Total catalog items: {len(items)}")

verified_matches = []

for item in items:
    name = item.get('name', '')
    parent = item.get('parent_name', '')
    full_name = f"{parent} - {name}" if parent else name
    brand = item.get('brand', '')
    sheet = item.get('sheet_folder', '')
    slug = item.get('slug', '')
    candidates = item.get('candidates', [])
    
    for idx, c in enumerate(candidates):
        matched_title = c.get('matched_title', '')
        file_path = c.get('file_path', '')
        
        if not file_path or not os.path.exists(file_path):
            continue
            
        try:
            im = Image.open(file_path)
            w, h = im.size
            
            # Check corners
            tl = im.getpixel((5, 5))
            tr = im.getpixel((w - 5, 5))
            bl = im.getpixel((5, h - 5))
            br = im.getpixel((w - 5, h - 5))
            
            # Corner variance
            is_white_corner = (tl == (255, 255, 255) and tr == (255, 255, 255) and 
                               bl == (255, 255, 255) and br == (255, 255, 255))
            
            verified_matches.append({
                'row': item.get('row'),
                'sheet': sheet,
                'slug': slug,
                'target_name': full_name,
                'brand': brand,
                'cand_index': idx + 1,
                'matched_title': matched_title,
                'file_path': file_path,
                'dimensions': f"{w}x{h}",
                'is_white_corner': is_white_corner
            })
        except Exception as e:
            pass

print(f"Total usable local candidates: {len(verified_matches)}")
with open('scratch/local_candidates_audited.json', 'w', encoding='utf-8') as f:
    json.dump(verified_matches, f, ensure_ascii=False, indent=2)

# Print candidates where brand and key model tokens match!
print("\n=== HIGH CONFIDENCE CANDIDATES WITH WHITE BACKGROUND ===")
for m in verified_matches:
    brand = m['brand'].lower()
    t_name = m['target_name'].lower()
    c_title = m['matched_title'].lower()
    
    # check if brand in title
    if brand in c_title and m['is_white_corner']:
        # Extract numbers or English codes
        import re
        tokens = re.findall(r'[a-zA-Z0-9]+', t_name)
        sig = [t for t in tokens if len(t) >= 2 and not (t.isdigit() and len(t) < 3)]
        
        matched_sig = [s for s in sig if s in c_title]
        if matched_sig or any(w in c_title for w in ['اکونومی', 'روسو', 'سینیور', 'تسلا', 'پاندا', 'پاکیزان', 'فریدولین', 'آیس پول']):
            print(f"Row {m['row']} [{m['sheet']}]: {m['target_name']}")
            print(f"   -> Cand: {m['matched_title']} ({m['dimensions']})")
            print(f"   -> File: {m['file_path']}\n")

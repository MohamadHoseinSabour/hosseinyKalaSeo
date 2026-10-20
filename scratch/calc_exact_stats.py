import json
import glob
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_candidates_harvested.json', encoding='utf-8') as f:
    catalog_items = json.load(f)

approved_files = glob.glob('product_images_2026-10-05/*/*.jpg')
approved_filenames = [os.path.basename(f) for f in approved_files]

print(f"Total catalog items needing images: {len(catalog_items)}")
print(f"Total approved image files in folder: {len(approved_files)}")

# Map each approved file to catalog item(s)
# Let's inspect which catalog items are covered
def check_match(item, filename):
    fname = os.path.splitext(filename)[0].lower()
    slug = (item.get('slug') or '').lower()
    name = (item.get('name') or '').lower()
    parent = (item.get('parent_name') or '').lower()
    brand = (item.get('brand') or '').lower()
    
    # Direct slug matches
    if slug and (slug == fname or fname.startswith(slug) or slug.startswith(fname)):
        return True
        
    # Specific known mappings
    if 'himalia-ice-pool-60mw-twin-white' in fname and 'آیس پول' in (name + parent) and 'سفید' in (name + parent):
        return True
    if 'himalia-omega-homebar-combi-white' in fname and 'امگا' in (name + parent):
        return True
    if 'himalia-5mode-homebar-combi-leather' in fname and '5 کاره' in (name + parent):
        return True
    if 'himalia-combi-850-titanium-70-30' in fname and '850' in (name + parent):
        return True
    if 'niksan-rf8410-combi-fridge' in fname and 'rf8410' in (name + parent).lower():
        return True
    if 'clover-rosso-homebar-70cm-twin-white' in fname and 'روسو هوم بار' in (name + parent):
        return True
    if 'clover-rosso-water-dispenser-70cm-twin-white' in fname and 'روسو آبریزدار' in (name + parent):
        return True
    if 'clover-twin-freezer-fridge-homebar-rosso' in fname and 'روسو هوم بار' in (name + parent):
        return True
    if 'clover-twin-freezer-fridge-water-dispenser-rosso' in fname and 'روسو آبریزدار' in (name + parent):
        return True
    if 'clover-mini-refrigerator-patterned' in fname and 'فانتزی' in (name + parent):
        return True
    if 'daewoo-dwk-990' in fname and '990' in (name + parent):
        return True
    if 'pakshoma-15kg-twin-tub-washer' in fname and 'پاکشوما' in (name + parent) and '15' in (name + parent):
        return True
    if 'pakshoma-21kg-twin-tub-washer' in fname and 'پاکشوما' in (name + parent) and '21' in (name + parent):
        return True
    if 'donalex-vacuum' in fname and '770' in (name + parent):
        return True
    if 'feridolin-sw35-mini-wash' in fname and 'فریدولین' in (name + parent) and '3.5' in (name + parent):
        return True
    if 'pakizan-blanket-washer-30kg' in fname and 'پاکیزان' in (name + parent) and '30' in (name + parent):
        return True
    if 'pakizan-blanket-washer-40kg' in fname and 'پاکیزان' in (name + parent) and '40' in (name + parent):
        return True
    if 'panda-80l-industrial-vacuum' in fname and 'پاندا' in (name + parent) and '80' in (name + parent):
        return True
    if 'saper-4025' in fname and '4025' in (name + parent):
        return True
    if 'saper-iron' in fname and '4035' in (name + parent):
        return True
    if 'alton-v303' in fname and ('7303' in (name + parent) or 'v303' in (name + parent).lower()):
        return True
    if 'aviz-granite-pan-28cm' in fname and '28' in (name + parent) and 'اویز' in (name + parent):
        return True
    if 'aviz-granite-pan-32cm' in fname and '32' in (name + parent) and 'اویز' in (name + parent):
        return True
    if 'parskhazar-rc181ts' in fname and 'نقره ای' in (name + parent) and 'پارس خزر' in (name + parent):
        return True
    if 'willez-chopper-steel' in fname and '6031' in (name + parent):
        return True
    if 'willez-chopper' in fname and ('6032' in (name + parent) or ('ویلز' in (name + parent) and 'خردکن' in (name + parent))):
        return True
    if 'butan-b3115' in fname and 'b3115' in (name + parent).lower():
        return True
    if 'parskhazar-4060' in fname and ('4060' in (name + parent) or 'پنکه پایه بلند پارس خزر' in (name + parent)):
        return True
    if 'parskhazar-fh2000p' in fname and 'fh-2000p' in (name + parent).lower():
        return True
    if 'polar-3pn' in fname and '3pn' in (name + parent).lower():
        return True
    if 'sunny-fan' in fname and '2013' in (name + parent):
        return True
    if 'korkmaz-a331' in fname and 'a331' in (name + parent).lower():
        return True
    if 'kenwood-hm430' in fname and 'hm430' in (name + parent).lower():
        return True
    if 'volga-f164' in fname and 'وولگا' in (name + parent):
        return True
    if 'promaron' in fname and '731' in (name + parent):
        return True
    return False

items_with_images = []
items_without_images = []

for it in catalog_items:
    matched = False
    matched_file = None
    for af in approved_filenames:
        if check_match(it, af):
            matched = True
            matched_file = af
            break
    if matched:
        items_with_images.append((it, matched_file))
    else:
        items_without_images.append(it)

print(f"\n==========================================")
print(f"Products WITH approved image: {len(items_with_images)}")
print(f"Products WITHOUT approved image: {len(items_without_images)}")
print(f"Total: {len(items_with_images) + len(items_without_images)}")
print(f"==========================================")

from collections import Counter
print("\n[Breakdown of products WITH images by category]:")
for cat, cnt in Counter([x[0]['sheet_folder'] for x in items_with_images]).items():
    print(f"  - {cat}: {cnt}")

print("\n[Breakdown of products WITHOUT images by category]:")
for cat, cnt in Counter([x['sheet_folder'] for x in items_without_images]).items():
    print(f"  - {cat}: {cnt}")

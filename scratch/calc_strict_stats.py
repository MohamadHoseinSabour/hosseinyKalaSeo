import json
import glob
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_candidates_harvested.json', encoding='utf-8') as f:
    catalog_items = json.load(f)

approved_files = glob.glob('product_images_2026-10-05/*/*.jpg')
approved_filenames = [os.path.basename(f) for f in approved_files]

def get_exact_match(item):
    cat = item.get('sheet_folder')
    name = (item.get('name') or '').lower()
    parent = (item.get('parent_name') or '').lower()
    full = f"{parent} {name}".lower()
    
    # 1. Refrigerators
    if cat == 'refrigerators':
        if 'himalia-ice-pool-60mw-twin-white.jpg' in approved_filenames and 'آیس پول' in full and 'سفید' in full:
            return 'himalia-ice-pool-60mw-twin-white.jpg'
        if 'himalia-omega-homebar-combi-white.jpg' in approved_filenames and 'امگا' in full:
            return 'himalia-omega-homebar-combi-white.jpg'
        if 'himalia-5mode-homebar-combi-leather.jpg' in approved_filenames and '5 کاره' in full:
            return 'himalia-5mode-homebar-combi-leather.jpg'
        if 'himalia-combi-850-titanium-70-30.jpg' in approved_filenames and '850' in full:
            return 'himalia-combi-850-titanium-70-30.jpg'
        if 'niksan-rf8410-combi-fridge-white-leather.jpg' in approved_filenames and 'rf8410' in full and 'سفید' in full:
            return 'niksan-rf8410-combi-fridge-white-leather.jpg'
        if 'niksan-rf8410-combi-fridge.jpg' in approved_filenames and 'rf8410' in full and not parent:
            return 'niksan-rf8410-combi-fridge.jpg'
        if 'clover-rosso-homebar-70cm-twin-white.jpg' in approved_filenames and 'روسو هوم بار' in full and ('عرض 70' in full or 'سفید' in full):
            return 'clover-rosso-homebar-70cm-twin-white.jpg'
        if 'clover-twin-freezer-fridge-homebar-rosso-steel.jpg' in approved_filenames and 'روسو هوم بار' in full and 'استیل' in full:
            return 'clover-twin-freezer-fridge-homebar-rosso-steel.jpg'
        if 'clover-twin-freezer-fridge-homebar-rosso-white.jpg' in approved_filenames and 'روسو هوم بار' in full and 'سفید' in full:
            return 'clover-twin-freezer-fridge-homebar-rosso-white.jpg'
        if 'clover-twin-freezer-fridge-homebar-rosso.jpg' in approved_filenames and 'روسو هوم بار' in full and not parent:
            return 'clover-twin-freezer-fridge-homebar-rosso.jpg'
        if 'clover-rosso-water-dispenser-70cm-twin-white.jpg' in approved_filenames and 'روسو آبریزدار' in full and ('عرض 70' in full or 'سفید' in full):
            return 'clover-rosso-water-dispenser-70cm-twin-white.jpg'
        if 'clover-twin-freezer-fridge-water-dispenser-rosso-steel.jpg' in approved_filenames and 'روسو آبریزدار' in full and 'استیل' in full:
            return 'clover-twin-freezer-fridge-water-dispenser-rosso-steel.jpg'
        if 'clover-twin-freezer-fridge-water-dispenser-rosso-white.jpg' in approved_filenames and 'روسو آبریزدار' in full and 'سفید' in full:
            return 'clover-twin-freezer-fridge-water-dispenser-rosso-white.jpg'
        if 'clover-twin-freezer-fridge-water-dispenser-rosso.jpg' in approved_filenames and 'روسو آبریزدار' in full and not parent:
            return 'clover-twin-freezer-fridge-water-dispenser-rosso.jpg'
        if 'clover-mini-refrigerator-patterned-white.jpg' in approved_filenames and 'فانتزی' in full and 'سفید' in full:
            return 'clover-mini-refrigerator-patterned-white.jpg'
        if 'clover-mini-refrigerator-patterned-blue.jpg' in approved_filenames and 'فانتزی' in full and 'آبی' in full:
            return 'clover-mini-refrigerator-patterned-blue.jpg'
        if 'clover-mini-refrigerator-patterned.jpg' in approved_filenames and 'فانتزی' in full and not parent:
            return 'clover-mini-refrigerator-patterned.jpg'

    # 2. Washing & Cleaning
    if cat == 'washing_and_cleaning':
        if 'daewoo-dwk-990-washing-machine-white.jpg' in approved_filenames and 'dwk-990' in full and ('سفید' in full or not parent):
            return 'daewoo-dwk-990-washing-machine-white.jpg'
        if 'daewoo-dwk-990s-washing-machine-silver.jpg' in approved_filenames and 'dwk-990' in full and 'سیلور' in full:
            return 'daewoo-dwk-990s-washing-machine-silver.jpg'
        if 'pakshoma-15kg-twin-tub-washer.jpg' in approved_filenames and 'پاکشوما' in full and '15' in full:
            return 'pakshoma-15kg-twin-tub-washer.jpg'
        if 'pakshoma-21kg-twin-tub-washer.jpg' in approved_filenames and 'پاکشوما' in full and '21' in full:
            return 'pakshoma-21kg-twin-tub-washer.jpg'
        if 'donalex-vacuum.jpg' in approved_filenames and 'دونالکس' in full and '770' in full:
            return 'donalex-vacuum.jpg'
        if 'feridolin-sw35-mini-wash.jpg' in approved_filenames and 'فریدولین' in full and '3.5' in full:
            return 'feridolin-sw35-mini-wash.jpg'
        if 'pakizan-blanket-washer-30kg.jpg' in approved_filenames and 'پاکیزان' in full and '30' in full:
            return 'pakizan-blanket-washer-30kg.jpg'
        if 'pakizan-blanket-washer-40kg.jpg' in approved_filenames and 'پاکیزان' in full and '40' in full:
            return 'pakizan-blanket-washer-40kg.jpg'
        if 'panda-80l-industrial-vacuum.jpg' in approved_filenames and 'پاندا' in full and '80' in full:
            return 'panda-80l-industrial-vacuum.jpg'
        if 'saper-4025-ceramic-steam-iron.jpg' in approved_filenames and 'ساپر' in full and '4025' in full:
            return 'saper-4025-ceramic-steam-iron.jpg'
        if 'saper-iron.jpg' in approved_filenames and 'ساپر' in full and '4035' in full:
            return 'saper-iron.jpg'

    # 3. Cooking appliances
    if cat == 'cooking_appliances':
        if 'alton-v303bn-built-in-oven.jpg' in approved_filenames and ('7303' in full or 'v303' in full):
            return 'alton-v303bn-built-in-oven.jpg'
        if 'aviz-granite-pan-28cm.jpg' in approved_filenames and 'اویز' in full and '28' in full:
            return 'aviz-granite-pan-28cm.jpg'
        if 'aviz-granite-pan-32cm.jpg' in approved_filenames and 'اویز' in full and '32' in full:
            return 'aviz-granite-pan-32cm.jpg'
        if 'parskhazar-rc181ts-silver-rice-cooker.jpg' in approved_filenames and 'پارس خزر' in full and 'نقره ای' in full:
            return 'parskhazar-rc181ts-silver-rice-cooker.jpg'
        if 'willez-chopper-steel.jpg' in approved_filenames and 'ویلز' in full and '6031' in full:
            return 'willez-chopper-steel.jpg'
        if 'willez-chopper.jpg' in approved_filenames and 'ویلز' in full and '6032' in full:
            return 'willez-chopper.jpg'

    # 4. Cooling & Heating
    if cat == 'cooling_heating':
        if 'butan-b3115-water-heater.jpg' in approved_filenames and 'b3115' in full:
            return 'butan-b3115-water-heater.jpg'
        if 'parskhazar-4060-fan.jpg' in approved_filenames and 'پارس خزر' in full and ('4060' in full or 'پنکه پایه بلند' in full):
            return 'parskhazar-4060-fan.jpg'
        if 'parskhazar-fh2000p-heater.jpg' in approved_filenames and 'fh-2000p' in full:
            return 'parskhazar-fh2000p-heater.jpg'
        if 'polar-3pn-new-heater.jpg' in approved_filenames and '3pn' in full:
            return 'polar-3pn-new-heater.jpg'
        if 'sunny-fan.jpg' in approved_filenames and 'سانی' in full and '2013' in full:
            return 'sunny-fan.jpg'

    # 5. Beverage makers
    if cat == 'beverage_makers':
        if 'korkmaz-a331-tea-maker.jpg' in approved_filenames and 'a331' in full:
            return 'korkmaz-a331-tea-maker.jpg'
        if 'kenwood-hm430-hand-mixer.jpg' in approved_filenames and 'hm430' in full:
            return 'kenwood-hm430-hand-mixer.jpg'
        if 'volga-f164-kettle.jpg' in approved_filenames and 'وولگا' in full:
            return 'volga-f164-kettle.jpg'

    # 6. Beauty & Health
    if cat == 'beauty_health':
        if 'promaron.jpg' in approved_filenames and 'پرومارون' in full and '731' in full:
            return 'promaron.jpg'

    return None

matched_items = []
unmatched_items = []

for it in catalog_items:
    m = get_exact_match(it)
    if m:
        matched_items.append((it, m))
    else:
        unmatched_items.append(it)

print(f"Total catalog missing items: {len(catalog_items)}")
print(f"Total approved image files: {len(approved_files)}")
print(f"Products WITH verified image: {len(matched_items)}")
print(f"Products WITHOUT verified image: {len(unmatched_items)}")

from collections import Counter
print("\n[WITH IMAGES by sheet]:")
for cat, cnt in Counter([x[0]['sheet_folder'] for x in matched_items]).items():
    print(f"  - {cat}: {cnt}")

print("\n[WITHOUT IMAGES by sheet]:")
for cat, cnt in Counter([x['sheet_folder'] for x in unmatched_items]).items():
    print(f"  - {cat}: {cnt}")

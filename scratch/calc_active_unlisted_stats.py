import openpyxl
import json
import glob
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. Load catalog rows
with open('scratch/catalog_current_rows.json', encoding='utf-8') as f:
    rows = json.load(f)

# 2. Get list of approved images
approved_images = glob.glob('product_images_2026-10-05/*/*.jpg')
approved_basenames = [os.path.basename(f) for f in approved_images]

# 3. Build product entities (families)
entities = []
curr = None
for r in rows:
    if not r['is_variation']:
        curr = {
            'sheet': r['sheet'],
            'folder': r['folder'],
            'parent_row': r['row'],
            'name': r['name'],
            'brand': r['brand'],
            'ptype': r['ptype'],
            'status': r['status'],
            'variations': []
        }
        entities.append(curr)
    else:
        if curr:
            curr['variations'].append(r)

def matches_image(entity_or_row, img_name):
    img = img_name.lower()
    full_text = f"{entity_or_row['name']} {entity_or_row.get('brand', '')}".lower()
    folder = entity_or_row['folder']
    
    if folder == 'refrigerators':
        if 'himalia-ice-pool-60mw-twin-white' in img and 'آیس پول' in full_text:
            return True
        if 'himalia-omega-homebar-combi-white' in img and 'امگا' in full_text:
            return True
        if 'himalia-5mode-homebar-combi-leather' in img and '5 کاره' in full_text:
            return True
        if 'himalia-combi-850-titanium-70-30' in img and '850' in full_text:
            return True
        if 'clover-rosso-water-dispenser' in img and 'روسو آبریزدار' in full_text:
            return True
        if 'clover-twin-freezer-fridge-water-dispenser-rosso' in img and 'روسو آبریزدار' in full_text:
            return True
        if 'clover-rosso-homebar' in img and 'روسو هوم بار' in full_text:
            return True
        if 'clover-twin-freezer-fridge-homebar-rosso' in img and 'روسو هوم بار' in full_text:
            return True
        if 'clover-mini-refrigerator-patterned' in img and 'فانتزی' in full_text:
            return True
        if 'niksan-rf8410-combi-fridge' in img and '8410' in full_text:
            return True

    if folder == 'washing_and_cleaning':
        if 'daewoo-dwk-990' in img and '990' in full_text:
            return True
        if 'pakshoma-15kg-twin-tub-washer' in img and 'پاکشوما' in full_text and '15' in full_text:
            return True
        if 'pakshoma-21kg-twin-tub-washer' in img and 'پاکشوما' in full_text and '21' in full_text:
            return True
        if 'donalex-vacuum' in img and '770' in full_text:
            return True
        if 'feridolin-sw35-mini-wash' in img and 'فریدولین' in full_text and '3.5' in full_text:
            return True
        if 'pakizan-blanket-washer-30kg' in img and 'پاکیزان' in full_text and '30' in full_text:
            return True
        if 'pakizan-blanket-washer-40kg' in img and 'پاکیزان' in full_text and '40' in full_text:
            return True
        if 'pakizan-blanket-washer' in img and 'پاکیزان' in full_text:
            return True
        if 'panda-80l-industrial-vacuum' in img and 'پاندا' in full_text and '80' in full_text:
            return True
        if 'saper-4025' in img and '4025' in full_text:
            return True
        if 'saper-iron' in img and '4035' in full_text:
            return True

    if folder == 'cooking_appliances':
        if 'alton-v303bn-built-in-oven' in img and ('7303' in full_text or 'v303' in full_text):
            return True
        if 'aviz-granite-pan-28cm' in img and '28' in full_text:
            return True
        if 'aviz-granite-pan-32cm' in img and '32' in full_text:
            return True
        if 'aviz-granite-pan' in img and 'اویز' in full_text:
            return True
        if 'parskhazar-rc181ts-silver-rice-cooker' in img and 'نقره ای' in full_text:
            return True
        if 'willez-chopper-steel' in img and '6031' in full_text:
            return True
        if 'willez-chopper' in img and ('6032' in full_text or 'خردکن' in full_text):
            return True

    if folder == 'cooling_heating':
        if 'butan-b3115-water-heater' in img and 'b3115' in full_text:
            return True
        if 'parskhazar-4060-fan' in img and ('4060' in full_text or 'پایه بلند' in full_text):
            return True
        if 'parskhazar-fh2000p-heater' in img and 'fh-2000p' in full_text:
            return True
        if 'polar-3pn-new-heater' in img and '3pn' in full_text:
            return True
        if 'sunny-fan' in img and '2013' in full_text:
            return True

    if folder == 'beverage_makers':
        if 'korkmaz-a331-tea-maker' in img and 'a331' in full_text:
            return True
        if 'kenwood-hm430-hand-mixer' in img and 'hm430' in full_text:
            return True
        if 'volga-f164-kettle' in img and 'وولگا' in full_text:
            return True

    if folder == 'beauty_health':
        if 'promaron.jpg' in img and '731' in full_text:
            return True

    return False

# Match images to entities
for p in entities:
    matched_images = []
    for img in approved_basenames:
        if matches_image(p, img):
            matched_images.append(img)
            
    for v in p['variations']:
        for img in approved_basenames:
            if matches_image(v, img) and img not in matched_images:
                matched_images.append(img)
                
    p['has_image'] = (len(matched_images) > 0)
    p['matched_images'] = matched_images

# Let's filter product entities:
# 1. Registered: status == 'ثبت‌شده در سایت' and all vars == 'ثبت‌شده در سایت'
# 2. Hold: status == 'فعلا دست نگه دار' or all vars == 'فعلا دست نگه دار'
# 3. Unlisted: status == 'در سایت تعریف نشده' or any var == 'در سایت تعریف نشده'

unregistered_active_entities = []
hold_entities = []
registered_entities = []

for p in entities:
    all_statuses = set([p['status']] + [v['status'] for v in p['variations']])
    
    # Check if completely registered
    if all_statuses == {'ثبت‌شده در سایت'}:
        registered_entities.append(p)
        continue
        
    # Check if completely hold
    if all_statuses == {'فعلا دست نگه دار'}:
        hold_entities.append(p)
        continue
        
    # If it has 'در سایت تعریف نشده'
    # What if it has both 'در سایت تعریف نشده' and 'فعلا دست نگه دار'? (e.g. Aviz pan row 28)
    # The parent product itself is active and has other unlisted variations.
    if 'در سایت تعریف نشده' in all_statuses:
        # Check if parent is hold
        if p['status'] == 'فعلا دست نگه دار' and len(p['variations']) == 0:
            hold_entities.append(p)
        else:
            unregistered_active_entities.append(p)

print(f"\n=======================================================")
print(f"Total Product Entities: {len(entities)}")
print(f"Registered Entities ('ثبت‌شده در سایت'): {len(registered_entities)}")
print(f"Hold Entities ('فعلا دست نگه دار'): {len(hold_entities)}")
print(f"Unregistered Active Entities ('در سایت تعریف نشده'): {len(unregistered_active_entities)}")
print(f"=======================================================")

with_image = [p for p in unregistered_active_entities if p['has_image']]
without_image = [p for p in unregistered_active_entities if not p['has_image']]

print(f"\nAmong Unregistered Active Entities:")
print(f"  - WITH image (parent or any variation has image): {len(with_image)}")
print(f"  - WITHOUT image (NEITHER parent NOR any variation has image): {len(without_image)}")

from collections import Counter
print("\n[WITHOUT IMAGE Entities by Sheet/Category]:")
cat_counter = Counter([p['sheet'] for p in without_image])
for sname, cnt in cat_counter.items():
    print(f"  * {sname}: {cnt} محصول")

print("\n--- Detailed List of Products WITHOUT image ---")
for p in without_image:
    vars_cnt = len(p['variations'])
    v_str = f" ({vars_cnt} تنوع)" if vars_cnt > 0 else ""
    print(f"[{p['sheet']} | Row {p['parent_row']}] [{p['brand']}] {p['name']}{v_str}")

with open('scratch/products_without_image_report.json', 'w', encoding='utf-8') as f:
    json.dump([{
        'sheet': p['sheet'],
        'row': p['parent_row'],
        'brand': p['brand'],
        'name': p['name'],
        'ptype': p['ptype'],
        'variations_count': len(p['variations']),
        'variation_names': [v['name'] for v in p['variations']]
    } for p in without_image], f, ensure_ascii=False, indent=2)

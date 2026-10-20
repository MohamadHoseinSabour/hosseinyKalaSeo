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
print(f"Total approved image files: {len(approved_basenames)}")

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

print(f"Total product entities across catalog: {len(entities)}")

# 4. For each entity, check:
#    - Is it registered? ('ثبت‌شده در سایت')
#    - Is it on hold? ('فعلا دست نگه دار')
#    - Does it have an approved image (either parent or any variation)?

def matches_image(entity_or_row, img_name):
    img = img_name.lower()
    full_text = f"{entity_or_row['name']} {entity_or_row.get('brand', '')}".lower()
    folder = entity_or_row['folder']
    
    # Specific verified mappings
    # Refrigerators
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

    # Washing & Cleaning
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

    # Cooking appliances
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

    # Cooling & Heating
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

    # Beverage makers
    if folder == 'beverage_makers':
        if 'korkmaz-a331-tea-maker' in img and 'a331' in full_text:
            return True
        if 'kenwood-hm430-hand-mixer' in img and 'hm430' in full_text:
            return True
        if 'volga-f164-kettle' in img and 'وولگا' in full_text:
            return True

    # Beauty & Health
    if folder == 'beauty_health':
        if 'promaron.jpg' in img and '731' in full_text:
            return True

    return False

# Now inspect each entity
for p in entities:
    # Find matching images for parent
    matched_images = []
    for img in approved_basenames:
        if matches_image(p, img):
            matched_images.append(img)
            
    # Also check variations for images
    for v in p['variations']:
        for img in approved_basenames:
            if matches_image(v, img) and img not in matched_images:
                matched_images.append(img)
                
    p['has_image'] = (len(matched_images) > 0)
    p['matched_images'] = matched_images

print("Done matching images to product entities.")

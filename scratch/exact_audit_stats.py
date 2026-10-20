import glob
import os
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/catalog_current_rows.json', encoding='utf-8') as f:
    rows = json.load(f)

# Load entities
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

# Correct mapping for all 43 images
image_mapping = {
    # beauty_health (1)
    'promaron.jpg': ('زیبایی و سلامت فردی', 24),
    
    # beverage_makers (3)
    'kenwood-hm430-hand-mixer.jpg': ('نوشیدنی ساز', 66),
    'korkmaz-a331-tea-maker.jpg': ('نوشیدنی ساز', 68),
    'volga-f164-kettle.jpg': ('نوشیدنی ساز', 54),
    
    # cooking_appliances (6)
    'alton-v303bn-built-in-oven.jpg': ('لوازم برقی و پخت و پز', 58),
    'aviz-granite-pan-28cm.jpg': ('لوازم برقی و پخت و پز', 25),
    'aviz-granite-pan-32cm.jpg': ('لوازم برقی و پخت و پز', 25),
    'parskhazar-rc181ts-silver-rice-cooker.jpg': ('لوازم برقی و پخت و پز', 90), # پلوپز 8 نفره نقره ای
    'willez-chopper-steel.jpg': ('لوازم برقی و پخت و پز', 83),
    'willez-chopper.jpg': ('لوازم برقی و پخت و پز', 83),
    
    # cooling_heating (5)
    'butan-b3115-water-heater.jpg': ('سرمایش و گرمایش', 14),
    'parskhazar-4060-fan.jpg': ('سرمایش و گرمایش', 25),
    'parskhazar-fh2000p-heater.jpg': ('سرمایش و گرمایش', 24),
    'polar-3pn-new-heater.jpg': ('سرمایش و گرمایش', 29),
    'sunny-fan.jpg': ('سرمایش و گرمایش', 20),
    
    # refrigerators (17)
    'clover-mini-refrigerator-patterned.jpg': ('یخچال و فریزر', 57),
    'clover-mini-refrigerator-patterned-blue.jpg': ('یخچال و فریزر', 57),
    'clover-mini-refrigerator-patterned-white.jpg': ('یخچال و فریزر', 57),
    'clover-rosso-homebar-70cm-twin-white.jpg': ('یخچال و فریزر', 54),
    'clover-twin-freezer-fridge-homebar-rosso-white.jpg': ('یخچال و فریزر', 54),
    'clover-twin-freezer-fridge-homebar-rosso-steel.jpg': ('یخچال و فریزر', 54),
    'clover-twin-freezer-fridge-homebar-rosso.jpg': ('یخچال و فریزر', 54),
    'clover-rosso-water-dispenser-70cm-twin-white.jpg': ('یخچال و فریزر', 51),
    'clover-twin-freezer-fridge-water-dispenser-rosso-white.jpg': ('یخچال و فریزر', 51),
    'clover-twin-freezer-fridge-water-dispenser-rosso-steel.jpg': ('یخچال و فریزر', 51),
    'clover-twin-freezer-fridge-water-dispenser-rosso.jpg': ('یخچال و فریزر', 51),
    'himalia-ice-pool-60mw-twin-white.jpg': ('یخچال و فریزر', 22),
    'himalia-omega-homebar-combi-white.jpg': ('یخچال و فریزر', 26),
    'himalia-5mode-homebar-combi-leather.jpg': ('یخچال و فریزر', 25),
    'himalia-combi-850-titanium-70-30.jpg': ('یخچال و فریزر', 27),
    'niksan-rf8410-combi-fridge.jpg': ('یخچال و فریزر', 87),
    'niksan-rf8410-combi-fridge-white-leather.jpg': ('یخچال و فریزر', 87),
    
    # washing_and_cleaning (11)
    'daewoo-dwk-990-washing-machine-white.jpg': ('شستشو و نظافت', 12),
    'daewoo-dwk-990s-washing-machine-silver.jpg': ('شستشو و نظافت', 12),
    'donalex-vacuum.jpg': ('شستشو و نظافت', 7),
    'feridolin-sw35-mini-wash.jpg': ('شستشو و نظافت', 67),
    'pakizan-blanket-washer-30kg.jpg': ('شستشو و نظافت', 88),
    'pakizan-blanket-washer-40kg.jpg': ('شستشو و نظافت', 88),
    'pakshoma-15kg-twin-tub-washer.jpg': ('شستشو و نظافت', 25),
    'pakshoma-21kg-twin-tub-washer.jpg': ('شستشو و نظافت', 25),
    'panda-80l-industrial-vacuum.jpg': ('شستشو و نظافت', 86),
    'saper-4025-ceramic-steam-iron.jpg': ('شستشو و نظافت', 58),
    'saper-iron.jpg': ('شستشو و نظافت', 59),
}

print(f"Total mapped image files: {len(image_mapping)}")

# Verify every single image maps to a valid entity
mapped_entities = {}
for img_file, (sheet, row_num) in image_mapping.items():
    ent = next((e for e in entities if e['sheet'] == sheet and e['parent_row'] == row_num), None)
    if not ent:
        print(f"ERROR: No entity found for {img_file}: {sheet} Row {row_num}")
    else:
        key = (sheet, row_num)
        if key not in mapped_entities:
            mapped_entities[key] = {
                'entity': ent,
                'images': []
            }
        mapped_entities[key]['images'].append(img_file)

print(f"Total distinct product entities mapped to images: {len(mapped_entities)}")

# Categorize all entities in catalog:
# Unlisted active entities: status == 'در سایت تعریف نشده'
unlisted_active_entities = [e for e in entities if e['status'] == 'در سایت تعریف نشده']
hold_entities = [e for e in entities if e['status'] == 'فعلا دست نگه دار']
registered_entities = [e for e in entities if e['status'] == 'ثبت‌شده در سایت']

print("\n--- Catalog Summary by Entity ---")
print(f"Total entities: {len(entities)}")
print(f"  - Registered entities: {len(registered_entities)}")
print(f"  - Hold entities: {len(hold_entities)}")
print(f"  - Unlisted active entities: {len(unlisted_active_entities)}")

# Check among unlisted active entities: which have image, which do not
unlisted_with_image = []
unlisted_without_image = []

for e in unlisted_active_entities:
    key = (e['sheet'], e['parent_row'])
    if key in mapped_entities:
        e['approved_images'] = mapped_entities[key]['images']
        unlisted_with_image.append(e)
    else:
        e['approved_images'] = []
        unlisted_without_image.append(e)

print(f"\n--- Among {len(unlisted_active_entities)} Unlisted Active Entities ---")
print(f"  - WITH Image: {len(unlisted_with_image)}")
print(f"  - WITHOUT Image: {len(unlisted_without_image)}")

# Check among hold entities: which have image
hold_with_image = [e for e in hold_entities if (e['sheet'], e['parent_row']) in mapped_entities]
print(f"\n--- Among {len(hold_entities)} Hold Entities ---")
print(f"  - WITH Image (found earlier but now on hold): {len(hold_with_image)}")
for h in hold_with_image:
    print(f"    * [{h['sheet']} | Row {h['parent_row']}] [{h['brand']}] {h['name']} -> Images: {mapped_entities[(h['sheet'], h['parent_row'])]['images']}")

print("\n--- Breakdown of Unlisted Entities WITHOUT Image by Sheet ---")
from collections import Counter
cat_counter = Counter([e['sheet'] for e in unlisted_without_image])
for sname, cnt in cat_counter.items():
    print(f"  * {sname}: {cnt} کالا")

print("\n--- Detailed List of ALL Unlisted Entities WITHOUT Image ---")
# Calculate rows
# Note: For variable products, some variations might be hold or unlisted.
# Let's count unlisted rows specifically.
rows_with_img = sum(sum(1 for r in [e] + e['variations'] if r['status'] == 'در سایت تعریف نشده') for e in unlisted_with_image)
rows_without_img = sum(sum(1 for r in [e] + e['variations'] if r['status'] == 'در سایت تعریف نشده') for e in unlisted_without_image)

print(f"\n=======================================================")
print(f"Summary Table of Unlisted Active Products (excluding 'فعلا دست نگه دار'):")
print(f"  * Total Active Unlisted Entities (کالای مادر / مستقل): {len(unlisted_active_entities)}")
print(f"  * Total Active Unlisted Rows (سطرهای کاتالوگ): {rows_with_img + rows_without_img}")
print(f"-------------------------------------------------------")
print(f"  1. Products WITH Image (دارای تصویر تاییدشده):")
print(f"     - Entities: {len(unlisted_with_image)}")
print(f"     - Rows: {rows_with_img}")
print(f"-------------------------------------------------------")
print(f"  2. Products WITHOUT Image (فاقد هرگونه تصویر):")
print(f"     - Entities: {len(unlisted_without_image)}")
print(f"     - Rows: {rows_without_img}")
print(f"=======================================================")

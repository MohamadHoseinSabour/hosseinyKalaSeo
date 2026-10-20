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

# All approved images
images = glob.glob('product_images_2026-10-05/*/*.jpg')

# Let's map each approved image to its exact target entity/row
# Based on verification summary and manual audit:
image_mapping = {
    # beauty_health
    'promaron.jpg': {
        'sheet': 'زیبایی و سلامت فردی',
        'target_name': 'دستگاه پیرایش سیمی سر و صورت پرومارون مدل 731',
        'row': 24
    },
    # beverage_makers
    'kenwood-hm430-hand-mixer.jpg': {
        'sheet': 'نوشیدنی ساز',
        'target_name': 'همزن برقی کنوود مدل HM430',
        'row': 66
    },
    'korkmaz-a331-tea-maker.jpg': {
        'sheet': 'نوشیدنی ساز',
        'target_name': 'چای ساز کورکماز مدل A331',
        'row': 68
    },
    'volga-f164-kettle.jpg': {
        'sheet': 'نوشیدنی ساز',
        'target_name': 'کتری برقی وولگا',
        'row': 54
    },
    # cooking_appliances
    'alton-v303bn-built-in-oven.jpg': {
        'sheet': 'لوازم برقی و پخت و پز',
        'target_name': 'فر توکار آلتون مدل 7303', # (originally v303bn)
        'row': 58
    },
    'aviz-granite-pan-28cm.jpg': {
        'sheet': 'لوازم برقی و پخت و پز',
        'target_name': 'تابه گرانیتی مشکی اویز (سایزهای 22 تا 32)',
        'row': 25,
        'var_row': 29 # ↳ سایز: 28 سانتیمتر
    },
    'aviz-granite-pan-32cm.jpg': {
        'sheet': 'لوازم برقی و پخت و پز',
        'target_name': 'تابه گرانیتی مشکی اویز (سایزهای 22 تا 32)',
        'row': 25,
        'var_row': 31 # ↳ سایز: 32 سانتیمتر
    },
    'parskhazar-rc181ts-silver-rice-cooker.jpg': {
        'sheet': 'لوازم برقی و پخت و پز',
        'target_name': 'پلوپز پارس خزر مدل 361', # wait, let's verify if rc181ts was for another item!
        'row': 89
    },
    'willez-chopper-steel.jpg': {
        'sheet': 'لوازم برقی و پخت و پز',
        'target_name': 'خردکن برقی کاسه دار ویلز',
        'row': 83,
        'var_row': 84 # ↳ مدل: 6031 کاسه استیل
    },
    'willez-chopper.jpg': {
        'sheet': 'لوازم برقی و پخت و پز',
        'target_name': 'خردکن برقی کاسه دار ویلز',
        'row': 83,
        'var_row': 85 # ↳ مدل: 6032 سه لیتری پیرکس
    },
    # cooling_heating
    'butan-b3115-water-heater.jpg': {
        'sheet': 'سرمایش و گرمایش',
        'target_name': 'آبگرمکن دیواری بوتان مدل B3115',
        'row': 14
    },
    'parskhazar-4060-fan.jpg': {
        'sheet': 'سرمایش و گرمایش',
        'target_name': 'پنکه پایه بلند پارس خزر',
        'row': 25
    },
    'parskhazar-fh2000p-heater.jpg': {
        'sheet': 'سرمایش و گرمایش',
        'target_name': 'بخاری پارس خزر فن دار مدل FH-2000P',
        'row': 24
    },
    'polar-3pn-new-heater.jpg': {
        'sheet': 'سرمایش و گرمایش',
        'target_name': 'بخاری پلار مدل 3PN-NEW ماشینی',
        'row': 29
    },
    'sunny-fan.jpg': {
        'sheet': 'سرمایش و گرمایش',
        'target_name': 'پنکه سانی مدل 2013 ساده',
        'row': 20
    },
    # refrigerators
    'clover-mini-refrigerator-patterned.jpg': {
        'sheet': 'یخچال و فریزر',
        'target_name': 'مینی یخچال 10 فوت کلور مدل طرح دار فانتزی',
        'row': 57
    },
    'clover-mini-refrigerator-patterned-blue.jpg': {
        'sheet': 'یخچال و فریزر',
        'target_name': 'مینی یخچال 10 فوت کلور مدل طرح دار فانتزی',
        'row': 57,
        'var_row': 60 # طرح آکواریوم آبی
    },
    'clover-mini-refrigerator-patterned-white.jpg': {
        'sheet': 'یخچال و فریزر',
        'target_name': 'مینی یخچال 10 فوت کلور مدل طرح دار فانتزی',
        'row': 57,
        'var_row': 58 # طرح اسنوپی سفید
    },
    'clover-rosso-homebar-70cm-twin-white.jpg': {
        'sheet': 'یخچال و فریزر',
        'target_name': 'یخچال و فریزر دوقلو کلور عرض 70 مدل روسو هوم بار',
        'row': 54
    },
    'clover-twin-freezer-fridge-homebar-rosso-white.jpg': {
        'sheet': 'یخچال و فریزر',
        'target_name': 'یخچال و فریزر دوقلو کلور عرض 70 مدل روسو هوم بار',
        'row': 54,
        'var_row': 55 # ↳ رنگ: سفید
    },
    'clover-twin-freezer-fridge-homebar-rosso-steel.jpg': {
        'sheet': 'یخچال و فریزر',
        'target_name': 'یخچال و فریزر دوقلو کلور عرض 70 مدل روسو هوم بار',
        'row': 54,
        'var_row': 56 # ↳ رنگ: استیل
    },
    'clover-twin-freezer-fridge-homebar-rosso.jpg': {
        'sheet': 'یخچال و فریزر',
        'target_name': 'یخچال و فریزر دوقلو کلور عرض 70 مدل روسو هوم بار',
        'row': 54
    },
    'clover-rosso-water-dispenser-70cm-twin-white.jpg': {
        'sheet': 'یخچال و فریزر',
        'target_name': 'یخچال و فریزر دوقلو کلور عرض 70 مدل روسو آبریزدار',
        'row': 51
    },
    'clover-twin-freezer-fridge-water-dispenser-rosso-white.jpg': {
        'sheet': 'یخچال و فریزر',
        'target_name': 'یخچال و فریزر دوقلو کلور عرض 70 مدل روسو آبریزدار',
        'row': 51,
        'var_row': 52 # ↳ رنگ: سفید
    },
    'clover-twin-freezer-fridge-water-dispenser-rosso-steel.jpg': {
        'sheet': 'یخچال و فریزر',
        'target_name': 'یخچال و فریزر دوقلو کلور عرض 70 مدل روسو آبریزدار',
        'row': 51,
        'var_row': 53 # ↳ رنگ: استیل
    },
    'clover-twin-freezer-fridge-water-dispenser-rosso.jpg': {
        'sheet': 'یخچال و فریزر',
        'target_name': 'یخچال و فریزر دوقلو کلور عرض 70 مدل روسو آبریزدار',
        'row': 51
    },
    'himalia-ice-pool-60mw-twin-white.jpg': {
        'sheet': 'یخچال و فریزر',
        'target_name': 'یخچال و فریزر دوقلو هیمالیا مدل آیس پول 60MW',
        'row': 22
    },
    'himalia-omega-homebar-combi-white.jpg': {
        'sheet': 'یخچال و فریزر',
        'target_name': 'یخچال و فریزر هیمالیا مدل امگا (Omega) هوم بار سفید',
        'row': 26
    },
    'himalia-5mode-homebar-combi-leather.jpg': {
        'sheet': 'یخچال و فریزر',
        'target_name': 'یخچال و فریزر هیمالیا مدل 5 کاره هوم بار چرمی 60MW',
        'row': 25
    },
    'himalia-combi-850-titanium-70-30.jpg': {
        'sheet': 'یخچال و فریزر',
        'target_name': 'یخچال و فریزر کمبی هیمالیا عرض 850 تیتانیوم مدل 70-30',
        'row': 27
    },
    'niksan-rf8410-combi-fridge.jpg': {
        'sheet': 'یخچال و فریزر',
        'target_name': 'یخچال و فریزر کمبی نیکسان مدل RF84102E2',
        'row': 87
    },
    'niksan-rf8410-combi-fridge-white-leather.jpg': {
        'sheet': 'یخچال و فریزر',
        'target_name': 'یخچال و فریزر کمبی نیکسان مدل RF84102E2',
        'row': 87,
        'var_row': 88 # ↳ رنگ: سفید چرمی
    },
    # washing_and_cleaning
    'daewoo-dwk-990-washing-machine-white.jpg': {
        'sheet': 'شستشو و نظافت',
        'target_name': 'ماشین لباسشویی 9 کیلوگرم اتوماتیک دوو سری سینیور DWK-990',
        'row': 12,
        'var_row': 13 # ↳ رنگ: سفید
    },
    'daewoo-dwk-990s-washing-machine-silver.jpg': {
        'sheet': 'شستشو و نظافت',
        'target_name': 'ماشین لباسشویی 9 کیلوگرم اتوماتیک دوو سری سینیور DWK-990',
        'row': 12,
        'var_row': 14 # ↳ رنگ: سیلور
    },
    'donalex-vacuum.jpg': {
        'sheet': 'شستشو و نظافت',
        'target_name': 'جاروبرقی دونالکس 770',
        'row': 7
    },
    'feridolin-sw35-mini-wash.jpg': {
        'sheet': 'شستشو و نظافت',
        'target_name': 'مینی واش فریدولین 3.5 کیلوگرم مدل تک درب',
        'row': 67
    },
    'pakizan-blanket-washer-30kg.jpg': {
        'sheet': 'شستشو و نظافت',
        'target_name': 'پتوشور صنعتی و خانگی پاکیزان',
        'row': 88,
        'var_row': 89 # ↳ ظرفیت: 30 کیلوگرم
    },
    'pakizan-blanket-washer-40kg.jpg': {
        'sheet': 'شستشو و نظافت',
        'target_name': 'پتوشور صنعتی و خانگی پاکیزان',
        'row': 88,
        'var_row': 90 # ↳ ظرفیت: 40 کیلوگرم
    },
    'pakshoma-15kg-twin-tub-washer.jpg': {
        'sheet': 'شستشو و نظافت',
        'target_name': 'ماشین لباسشویی دوقلو نیمه اتوماتیک پاکشوما',
        'row': 25,
        'var_row': 26 # ↳ ظرفیت: 15.5 کیلوگرم
    },
    'pakshoma-21kg-twin-tub-washer.jpg': {
        'sheet': 'شستشو و نظافت',
        'target_name': 'ماشین لباسشویی دوقلو نیمه اتوماتیک پاکشوما',
        'row': 25,
        'var_row': 27 # ↳ ظرفیت: 21 کیلوگرم
    },
    'panda-80l-industrial-vacuum.jpg': {
        'sheet': 'شستشو و نظافت',
        'target_name': 'جاروبرقی سطلی صنعتی آب و خاک پاندا 80 لیتر',
        'row': 86
    },
    'saper-4025-ceramic-steam-iron.jpg': {
        'sheet': 'شستشو و نظافت',
        'target_name': 'اتوبخار ساپر کف سرامیک مدل 4025',
        'row': 58
    },
    'saper-iron.jpg': {
        'sheet': 'شستشو و نظافت',
        'target_name': 'اتوبخار ساپر کف سرامیک مدل 4035',
        'row': 59
    }
}

print(f"Total mapped image keys: {len(image_mapping)}")

# Let's inspect the status in the catalog for each mapped item
target_entities_matched = set()

for img_file, meta in image_mapping.items():
    row_num = meta['row']
    sheet_name = meta['sheet']
    # find entity
    ent = next((e for e in entities if e['sheet'] == sheet_name and e['parent_row'] == row_num), None)
    if not ent:
        print(f"ERROR: entity not found for {img_file}: Sheet {sheet_name}, Row {row_num}")
    else:
        var_num = meta.get('var_row')
        var_item = next((v for v in ent['variations'] if v['row'] == var_num), None) if var_num else None
        
        target_entities_matched.add((ent['sheet'], ent['parent_row']))
        
        var_status_str = f" [Var Row {var_num}: {var_item['status']}]" if var_item else ""
        print(f"Image: {img_file:<45} -> [{ent['sheet']} | Row {ent['parent_row']}] Status: {ent['status']}{var_status_str} | {ent['name']}")

print(f"\nTotal distinct product entities matched by images: {len(target_entities_matched)}")

unlisted_matched = []
hold_matched = []
registered_matched = []

for img_file, meta in image_mapping.items():
    ent = next((e for e in entities if e['sheet'] == meta['sheet'] and e['parent_row'] == meta['row']), None)
    if ent:
        st = ent['status']
        if st == 'در سایت تعریف نشده' and ent not in unlisted_matched:
            unlisted_matched.append(ent)
        elif st == 'فعلا دست نگه دار' and ent not in hold_matched:
            hold_matched.append(ent)
        elif st == 'ثبت‌شده در سایت' and ent not in registered_matched:
            registered_matched.append(ent)

print(f"\nBreakdown of Entities having Approved Images (out of 29):")
print(f"  * Unlisted active ('در سایت تعریف نشده'): {len(unlisted_matched)}")
print(f"  * Hold ('فعلا دست نگه دار'): {len(hold_matched)}")
print(f"  * Registered ('ثبت‌شده در سایت'): {len(registered_matched)}")

print("\n--- Hold entities that have images ---")
for h in hold_matched:
    print(f"[{h['sheet']} | Row {h['parent_row']}] [{h['brand']}] {h['name']}")

print("\n--- Unlisted active entities that have images ---")
for u in unlisted_matched:
    print(f"[{u['sheet']} | Row {u['parent_row']}] [{u['brand']}] {u['name']} ({len(u['variations'])} vars)")


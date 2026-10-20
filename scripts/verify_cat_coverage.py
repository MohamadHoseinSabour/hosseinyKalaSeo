import json

with open('data/categories_live.json', 'r', encoding='utf-8') as f:
    cats = json.load(f)

print(f"Loaded {len(cats)} categories.")

# Target structure mapping:
# 1. یخچال فریزر (92)
#    Children: 153, 154, 155, 156
# 2. شستشو و نظافت (NEW: wash_id)
#    Children:
#      - 93 (ماشین لباسشویی) -> [157, 158]
#      - 97 (ماشین ظرفشویی) -> [159]
#      - 21 (جاروبرقی) -> [160, 161, 162]
#      - 118 (اتو) -> [166]
# 3. لوازم برقی و پخت و پز (216)
#    Children:
#      - 121 (سرخ کن) -> [168]
#      - 122 (گوشت کوب برقی) -> [169]
#      - 209 (اجاق گاز) -> [210]
#      - 215 (ظروف و پخت و پز)
# 4. نوشیدنی ساز (NEW: drink_id)
#    Children:
#      - 119 (اسپرسو ساز) -> [167]
#      - 211 (چای ساز)
#      - 120 (آبمیوه گیری) -> [165]
#      - 123 (مخلوط کن) -> [170]
# 5. سرمایش و گرمایش (NEW: climate_id)
#    Children:
#      - 95 (کولر آبی) -> [163]
#      - 206 (کولر گازی)
#      - 214 (صوتی، تصویری و گرمایشی)
# 6. تصفیه کننده آب (96)
#    Children: 164
# 7. زیبایی و سلامت فردی (212)
#    Children:
#      - 126 (اصلاح موی سر و صورت) -> [171]
#      - 124 (سشوار) -> [174]

covered_ids = {
    92, 153, 154, 155, 156,
    93, 157, 158, 97, 159, 21, 160, 161, 162, 118, 166,
    216, 121, 168, 122, 169, 209, 210, 215,
    119, 167, 211, 120, 165, 123, 170,
    95, 163, 206, 214,
    96, 164,
    212, 126, 171, 124, 174
}

all_existing_ids = {c['id'] for c in cats}
missing = all_existing_ids - covered_ids
extra = covered_ids - all_existing_ids

print(f"Covered count: {len(covered_ids)}")
print(f"Total existing categories: {len(all_existing_ids)}")
print(f"Missing from target structure: {missing}")
if missing:
    for mid in missing:
        mc = next(c for c in cats if c['id'] == mid)
        print(f"  Missing ID {mid}: {mc['name']} (parent: {mc.get('parent')})")
print(f"Extra in target structure: {extra}")

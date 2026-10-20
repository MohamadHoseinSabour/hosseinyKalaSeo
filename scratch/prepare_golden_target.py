import openpyxl
from copy import copy
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from collections import OrderedDict
import pickle

# 1. Parse dump blocks
dump_lines = open('scratch/catalog_full_dump.txt', encoding='utf-8').readlines()

raw_sheets = {}
cur_sheet = None
cur_block = None
cur_section = None

for line in dump_lines:
    if 'SHEET:' in line:
        cur_sheet = line.split('SHEET:')[1].split()[0].strip()
        raw_sheets[cur_sheet] = []
        continue
    if '| A: ' in line and '| B: ' in line:
        parts = line.split('|')
        name = parts[1].replace('A:', '').strip()
        price_b = parts[2].replace('B:', '').strip()
        price_d = parts[3].replace('D:', '').strip()
        status_r = parts[4].replace('R:', '').strip()
        
        b_val = int(price_b) if price_b != 'None' and price_b.isdigit() else None
        d_val = int(price_d) if price_d != 'None' and price_d.isdigit() else (b_val if b_val else None)
        
        if '📂' in name:
            cur_section = name
            continue
            
        if name.startswith('↳'):
            if cur_block:
                cur_block['variations'].append({
                    'name': name,
                    'price_b': b_val,
                    'price_d': d_val,
                    'status_r': status_r
                })
        else:
            cur_block = {
                'section': cur_section,
                'name': name,
                'price_b': b_val,
                'price_d': d_val,
                'status_r': status_r,
                'variations': []
            }
            raw_sheets[cur_sheet].append(cur_block)

canonical_sheet_names = {
    'یخچال': 'یخچال و فریزر',
    'شستشو': 'شستشو و نظافت',
    'لوازم': 'لوازم برقی و پخت و پز',
    'نوشیدنی': 'نوشیدنی ساز',
    'سرمایش': 'سرمایش و گرمایش',
    'تصفیه': 'تصفیه کننده آب',
    'صوتی': 'صوتی و تصویری',
    'زیبایی': 'زیبایی و سلامت فردی'
}

sheets = {}
for k, v in raw_sheets.items():
    for c_prefix, full_name in canonical_sheet_names.items():
        if k.startswith(c_prefix):
            sheets[full_name] = v
            break

# Build reorganized structure
target = OrderedDict()

# 1. یخچال و فریزر
target['یخچال و فریزر'] = OrderedDict()
electrosan_b = None
clover_36_b = None
clover_27_rnt_b = None
for b in sheets['یخچال و فریزر']:
    if 'الکتروسان' in b['name']:
        electrosan_b = b
    elif '36 فوت' in b['name']:
        clover_36_b = b
    elif 'FRNT101' in b['name']:
        clover_27_rnt_b = b

clover_water_b = None
for b in sheets['تصفیه کننده آب']:
    if 'FRNT-70-GLORY PLUS' in b['name'] or 'GLORY PLUS-steel' in b['name']:
        clover_water_b = b

for b in sheets['یخچال و فریزر']:
    if b in [electrosan_b, clover_36_b, clover_27_rnt_b]:
        continue
    sec = b['section'] or ""
    brand = sec.split('◀')[-1].strip() if '◀' in sec else 'متفرقه'
    if brand not in target['یخچال و فریزر']:
        target['یخچال و فریزر'][brand] = []
    target['یخچال و فریزر'][brand].append(b)

if clover_36_b:
    clover_36_b['name'] = clover_36_b['name'].replace('کلوِر', 'کلور')
    target['یخچال و فریزر']['کلور'].append(clover_36_b)
if clover_27_rnt_b:
    clover_27_rnt_b['name'] = clover_27_rnt_b['name'].replace('کلوِر', 'کلور')
    target['یخچال و فریزر']['کلور'].append(clover_27_rnt_b)
if clover_water_b:
    target['یخچال و فریزر']['کلور'].append(clover_water_b)
if electrosan_b:
    target['یخچال و فریزر']['الکتروسان'] = [electrosan_b]
if 'متفرقه' in target['یخچال و فریزر']:
    del target['یخچال و فریزر']['متفرقه']


# 2. شستشو و نظافت
target['شستشو و نظافت'] = OrderedDict()
dw_16_b = None
pakizan_40_b = None
for b in sheets['شستشو و نظافت']:
    if 'ماشین ظرفشویی ۱۶ نفره' in b['name']:
        dw_16_b = b
    elif 'پتوشور صنعتی و خانگی کد 40 تمام استیل پاکیزان' in b['name']:
        pakizan_40_b = b

for b in sheets['شستشو و نظافت']:
    if b in [dw_16_b, pakizan_40_b]:
        continue
    sec = b['section'] or ""
    brand = sec.split('◀')[-1].strip() if '◀' in sec else 'متفرقه'
    if brand not in target['شستشو و نظافت']:
        target['شستشو و نظافت'][brand] = []
    target['شستشو و نظافت'][brand].append(b)

if dw_16_b:
    dw_16_b['name'] = 'ماشین ظرفشویی ۱۶ نفره کلور مدل لمسی استیل ۳ سبد'
    target['شستشو و نظافت']['کلور'].append(dw_16_b)
if pakizan_40_b:
    target['شستشو و نظافت']['پاکیزان'].append(pakizan_40_b)


# 3. لوازم برقی و پخت و پز
target['لوازم برقی و پخت و پز'] = OrderedDict()
pakshoma_ac_b = None
gronweg_promar_b = None
delmonti_toaster_b = None
kenra_chopper_b = None
dasti_luxe_b = None

for b in sheets['لوازم برقی و پخت و پز']:
    if 'کولر گازی اسپلیت دیواری 18000 دور ثابت پاکشوما' in b['name']:
        pakshoma_ac_b = b
    elif 'سرخ‌کن بدون روغن ۸ لیتری گرنویک مدل ProMar' in b['name']:
        gronweg_promar_b = b
    elif 'آون توستر ۶۰ لیتری کانوکشن نان دلمونتی مدل DN-580' in name:
        delmonti_toaster_b = b
    elif 'سبزی خردکن KENRA' in b['name']:
        kenra_chopper_b = b
    elif 'سرویس پخت و پز 10 پارچه مدل دستی لوکس' in b['name']:
        dasti_luxe_b = b

for b in sheets['لوازم برقی و پخت و پز']:
    if b in [pakshoma_ac_b, gronweg_promar_b, delmonti_toaster_b, kenra_chopper_b, dasti_luxe_b]:
        continue
    sec = b['section'] or ""
    brand = sec.split('◀')[-1].strip() if '◀' in sec else 'متفرقه'
    if brand == 'اویزپلاس':
        brand = 'اویز'
    if brand not in target['لوازم برقی و پخت و پز']:
        target['لوازم برقی و پخت و پز'][brand] = []
    target['لوازم برقی و پخت و پز'][brand].append(b)

if gronweg_promar_b:
    if 'گرنویک' not in target['لوازم برقی و پخت و پز']:
        target['لوازم برقی و پخت و پز']['گرنویک'] = []
    target['لوازم برقی و پخت و پز']['گرنویک'].append(gronweg_promar_b)
if delmonti_toaster_b:
    target['لوازم برقی و پخت و پز']['دلمونتی'] = [delmonti_toaster_b]
if kenra_chopper_b:
    kenra_chopper_b['name'] = 'سبزی خردکن خانگی کنرا مدل KENRA'
    target['لوازم برقی و پخت و پز']['کنرا'] = [kenra_chopper_b]
if dasti_luxe_b:
    target['لوازم برقی و پخت و پز']['دستی لوکس'] = [dasti_luxe_b]


# 4. نوشیدنی ساز
target['نوشیدنی ساز'] = OrderedDict()
gronweg_samovar_b = None
gronweg_espresso_b = None
korkmaz_tea_b = None
zamroti_kettle_b = None
zamroti_samovar_b = None
zamroti_blender_b = None
vogati_kettle_b = None
ericsson_kettle_b = None

for b in sheets['نوشیدنی ساز']:
    name = b['name']
    if 'سماور برقی پیرکس ۳.۲ لیتری گرنویک مدل GST-883' in name:
        gronweg_samovar_b = b
    elif 'اسپرسوساز ۲۰ بار گرنویک مدل رترو آنالوگ' in name:
        gronweg_espresso_b = b
    elif 'چای‌ساز تمام استیل کورکماز مدل A331 چای‌تما' in name:
        korkmaz_tea_b = b
    elif 'کتری برقی رترو ۱.۷ لیتری زامروتی مدل عقربه‌ای کرم' in name:
        zamroti_kettle_b = b
    elif 'سماور برقی ۳ لیتری دیجیتال پیرکس زامروتی' in name:
        zamroti_samovar_b = b
    elif 'مخلوط‌کن رترو ۱.۵ لیتری ۶۰۰ وات زامروتی مدل 10038' in name:
        zamroti_blender_b = b
    elif 'کتری برقی ۱.۸ لیتری وگاتی مدل توپی' in name:
        vogati_kettle_b = b
    elif 'کتری برقی استیل ۲۰۰۰ وات اریکسون مدل ۱.۸ لیتری' in name:
        ericsson_kettle_b = b

special_bev = [gronweg_samovar_b, gronweg_espresso_b, korkmaz_tea_b, zamroti_kettle_b,
               zamroti_samovar_b, zamroti_blender_b, vogati_kettle_b, ericsson_kettle_b]

for b in sheets['نوشیدنی ساز']:
    if b in special_bev:
        continue
    sec = b['section'] or ""
    brand = sec.split('◀')[-1].strip() if '◀' in sec else 'متفرقه'
    if brand not in target['نوشیدنی ساز']:
        target['نوشیدنی ساز'][brand] = []
    target['نوشیدنی ساز'][brand].append(b)

if 'گرنویک' not in target['نوشیدنی ساز']:
    target['نوشیدنی ساز']['گرنویک'] = []
if gronweg_samovar_b:
    target['نوشیدنی ساز']['گرنویک'].append(gronweg_samovar_b)
if gronweg_espresso_b:
    target['نوشیدنی ساز']['گرنویک'].append(gronweg_espresso_b)
if 'کورکماز' not in target['نوشیدنی ساز']:
    target['نوشیدنی ساز']['کورکماز'] = []
if korkmaz_tea_b:
    target['نوشیدنی ساز']['کورکماز'].append(korkmaz_tea_b)
if 'زامروتی' not in target['نوشیدنی ساز']:
    target['نوشیدنی ساز']['زامروتی'] = []
for zb in [zamroti_kettle_b, zamroti_samovar_b, zamroti_blender_b]:
    if zb:
        target['نوشیدنی ساز']['زامروتی'].append(zb)
if vogati_kettle_b:
    target['نوشیدنی ساز']['وگاتی'] = [vogati_kettle_b]
if ericsson_kettle_b:
    target['نوشیدنی ساز']['اریکسون'] = [ericsson_kettle_b]


# 5. سرمایش و گرمایش
target['سرمایش و گرمایش'] = OrderedDict()
for b in sheets['سرمایش و گرمایش']:
    sec = b['section'] or ""
    brand = sec.split('◀')[-1].strip() if '◀' in sec else 'متفرقه'
    if brand not in target['سرمایش و گرمایش']:
        target['سرمایش و گرمایش'][brand] = []
    target['سرمایش و گرمایش'][brand].append(b)
if pakshoma_ac_b:
    target['سرمایش و گرمایش']['پاکشوما'] = [pakshoma_ac_b]


# 6. تصفیه کننده آب
target['تصفیه کننده آب'] = OrderedDict()
for b in sheets['تصفیه کننده آب']:
    if b == clover_water_b:
        continue
    sec = b['section'] or ""
    brand = sec.split('◀')[-1].strip() if '◀' in sec else 'متفرقه'
    if brand not in target['تصفیه کننده آب']:
        target['تصفیه کننده آب'][brand] = []
    target['تصفیه کننده آب'][brand].append(b)


# 7. صوتی و تصویری
target['صوتی و تصویری'] = OrderedDict()
for b in sheets['صوتی و تصویری']:
    sec = b['section'] or ""
    brand = sec.split('◀')[-1].strip() if '◀' in sec else 'متفرقه'
    b['name'] = b['name'].replace('هاورسون', 'هاورسن')
    if brand not in target['صوتی و تصویری']:
        target['صوتی و تصویری'][brand] = []
    target['صوتی و تصویری'][brand].append(b)


# 8. زیبایی و سلامت فردی
target['زیبایی و سلامت فردی'] = OrderedDict()
for b in sheets['زیبایی و سلامت فردی']:
    sec = b['section'] or ""
    brand = sec.split('◀')[-1].strip() if '◀' in sec else 'متفرقه'
    if brand == 'پروامگا':
        brand = 'پرو امگا'
    if brand not in target['زیبایی و سلامت فردی']:
        target['زیبایی و سلامت فردی'][brand] = []
    target['زیبایی و سلامت فردی'][brand].append(b)

total_priced_target = 0
for sname, brands_dict in target.items():
    s_priced = sum(
        sum((1 if b['price_b'] else 0) + sum(1 if v['price_b'] else 0 for v in b['variations']) for b in blist)
        for blist in brands_dict.values()
    )
    total_priced_target += s_priced
    print(f"Target Sheet '{sname}': {s_priced} priced items.")

print(f"\nTotal priced items in target structure: {total_priced_target} (Expected: 195)")

with open('scratch/target_data.pkl', 'wb') as f:
    pickle.dump(target, f)
print("Saved target structure to scratch/target_data.pkl")

import openpyxl
from copy import copy
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

SOURCE_FILE = 'hosseiny_kala_catalog.xlsx'
wb = openpyxl.load_workbook(SOURCE_FILE)

# Function to extract all blocks
def extract_blocks_from_sheet(ws, sheet_name):
    blocks = []
    current_brand = "متفرقه"
    current_block = None
    
    for r in range(2, ws.max_row + 1):
        vA = ws.cell(row=r, column=1).value
        if not vA:
            continue
        vA_str = str(vA).strip()
        if '📂' in vA_str:
            parts = vA_str.split('◀')
            current_brand = parts[-1].strip() if len(parts) > 1 else vA_str
            continue
            
        row_vals = [ws.cell(row=r, column=c).value for c in range(1, 19)]
        
        if vA_str.startswith('↳'):
            if current_block:
                current_block['variations'].append(row_vals)
        else:
            current_block = {
                'sheet': sheet_name,
                'brand': current_brand,
                'parent': row_vals,
                'variations': []
            }
            blocks.append(current_block)
    return blocks

sheet_blocks = {}
for sname in wb.sheetnames:
    if sname in ['📊 خلاصه و داشبورد', '📖 راهنمای کاربری']:
        continue
    sheet_blocks[sname] = extract_blocks_from_sheet(wb[sname], sname)

print("Extraction completed.")

# Now let's reorganize blocks into new brand buckets for each sheet:
# We will create a dictionary: target_structure[sheet_name] = OrderedDict of {brand_name: [list of blocks]}

from collections import OrderedDict
target = OrderedDict()

# ----------------- 1. یخچال و فریزر -----------------
target['یخچال و فریزر'] = OrderedDict()
fridge_blocks = sheet_blocks['یخچال و فریزر']

# Identify blocks
electrosan_block = None
clover_36_block = None
clover_27_rnt_block = None

for b in fridge_blocks:
    name = str(b['parent'][0])
    if 'الکتروسان' in name:
        electrosan_block = b
    elif 'RNT101-FNT101' in name or '36 فوت' in name:
        clover_36_block = b
    elif 'FRNT101' in name:
        clover_27_rnt_block = b

# Also get clover fridge from water purifier sheet
clover_water_block = None
for b in sheet_blocks['تصفیه کننده آب']:
    name = str(b['parent'][0])
    if 'FRNT-70-GLORY PLUS' in name or 'GLORY PLUS-steel' in name:
        clover_water_block = b

# Group fridge blocks
for b in fridge_blocks:
    if b in [electrosan_block, clover_36_block, clover_27_rnt_block]:
        continue
    brand = b['brand']
    if brand not in target['یخچال و فریزر']:
        target['یخچال و فریزر'][brand] = []
    target['یخچال و فریزر'][brand].append(b)

# Add moved Clover blocks to کلور
if clover_36_block:
    clover_36_block['brand'] = 'کلور'
    clover_36_block['parent'][0] = clover_36_block['parent'][0].replace('کلوِر', 'کلور')
    clover_36_block['parent'][10] = 'کلور'
    clover_36_block['parent'][9] = 'یخچال فریزر کلور'
    target['یخچال و فریزر']['کلور'].append(clover_36_block)

if clover_27_rnt_block:
    clover_27_rnt_block['brand'] = 'کلور'
    clover_27_rnt_block['parent'][0] = clover_27_rnt_block['parent'][0].replace('کلوِر', 'کلور')
    clover_27_rnt_block['parent'][10] = 'کلور'
    clover_27_rnt_block['parent'][9] = 'یخچال فریزر کلور'
    target['یخچال و فریزر']['کلور'].append(clover_27_rnt_block)

if clover_water_block:
    clover_water_block['sheet'] = 'یخچال و فریزر'
    clover_water_block['brand'] = 'کلور'
    clover_water_block['parent'][8] = 'یخچال و فریزر'
    clover_water_block['parent'][9] = 'یخچال فریزر کلور'
    clover_water_block['parent'][10] = 'کلور'
    target['یخچال و فریزر']['کلور'].append(clover_water_block)

# Add Electrosan brand
if electrosan_block:
    electrosan_block['brand'] = 'الکتروسان'
    electrosan_block['parent'][10] = 'الکتروسان'
    target['یخچال و فریزر']['الکتروسان'] = [electrosan_block]

# Remove متفرقه if empty
if 'متفرقه' in target['یخچال و فریزر']:
    del target['یخچال و فریزر']['متفرقه']


# ----------------- 2. شستشو و نظافت -----------------
target['شستشو و نظافت'] = OrderedDict()
laundry_blocks = sheet_blocks['شستشو و نظافت']

dishwasher_16_block = None
pakizan_40_block = None

for b in laundry_blocks:
    name = str(b['parent'][0])
    if 'ماشین ظرفشویی ۱۶ نفره' in name or 'dishwasher-16-person' in str(b['parent'][15]):
        dishwasher_16_block = b
    elif 'پتوشور صنعتی و خانگی کد 40 تمام استیل پاکیزان' in name:
        pakizan_40_block = b

for b in laundry_blocks:
    if b in [dishwasher_16_block, pakizan_40_block]:
        continue
    brand = b['brand']
    if brand not in target['شستشو و نظافت']:
        target['شستشو و نظافت'][brand] = []
    target['شستشو و نظافت'][brand].append(b)

# Add dishwasher to کلور
if dishwasher_16_block:
    dishwasher_16_block['brand'] = 'کلور'
    dishwasher_16_block['parent'][0] = 'ماشین ظرفشویی ۱۶ نفره کلور مدل لمسی استیل ۳ سبد'
    dishwasher_16_block['parent'][9] = 'ماشین ظرفشویی کلور'
    dishwasher_16_block['parent'][10] = 'کلور'
    dishwasher_16_block['parent'][15] = 'https://hosseinykala.ir/product/clover-16-person-touch-inox-dishwasher/'
    target['شستشو و نظافت']['کلور'].append(dishwasher_16_block)

# Add pakizan 40 to پاکیزان
if pakizan_40_block:
    pakizan_40_block['brand'] = 'پاکیزان'
    pakizan_40_block['parent'][10] = 'پاکیزان'
    target['شستشو و نظافت']['پاکیزان'].append(pakizan_40_block)


# ----------------- 3. لوازم برقی و پخت و پز -----------------
target['لوازم برقی و پخت و پز'] = OrderedDict()
cooking_blocks = sheet_blocks['لوازم برقی و پخت و پز']

pakshoma_ac_block = None
gronweg_promar_block = None
delmonti_toaster_block = None
kenra_chopper_block = None
dasti_luxe_block = None

for b in cooking_blocks:
    name = str(b['parent'][0])
    if 'کولر گازی اسپلیت دیواری 18000 دور ثابت پاکشوما' in name:
        pakshoma_ac_block = b
    elif 'سرخ‌کن بدون روغن ۸ لیتری گرنویک مدل ProMar' in name:
        gronweg_promar_block = b
    elif 'آون توستر ۶۰ لیتری کانوکشن نان دلمونتی مدل DN-580' in name:
        delmonti_toaster_block = b
    elif 'سبزی خردکن KENRA' in name or 'سبزی خردکن کنرا' in name:
        kenra_chopper_block = b
    elif 'سرویس پخت و پز 10 پارچه مدل دستی لوکس' in name:
        dasti_luxe_block = b

for b in cooking_blocks:
    if b in [pakshoma_ac_block, gronweg_promar_block, delmonti_toaster_block, kenra_chopper_block, dasti_luxe_block]:
        continue
    brand = b['brand']
    # Merge اویزپلاس into اویز
    if brand == 'اویزپلاس':
        brand = 'اویز'
    if brand not in target['لوازم برقی و پخت و پز']:
        target['لوازم برقی و پخت و پز'][brand] = []
    target['لوازم برقی و پخت و پز'][brand].append(b)

# Move gronweg promar to گرنویک
if gronweg_promar_block:
    gronweg_promar_block['brand'] = 'گرنویک'
    gronweg_promar_block['parent'][10] = 'گرنویک'
    if 'گرنویک' not in target['لوازم برقی و پخت و پز']:
        target['لوازم برقی و پخت و پز']['گرنویک'] = []
    target['لوازم برقی و پخت و پز']['گرنویک'].append(gronweg_promar_block)

# Add Delmonti section
if delmonti_toaster_block:
    delmonti_toaster_block['brand'] = 'دلمونتی'
    delmonti_toaster_block['parent'][10] = 'دلمونتی'
    target['لوازم برقی و پخت و پز']['دلمونتی'] = [delmonti_toaster_block]

# Add Kenra section
if kenra_chopper_block:
    kenra_chopper_block['brand'] = 'کنرا'
    kenra_chopper_block['parent'][0] = 'سبزی خردکن خانگی کنرا مدل KENRA'
    kenra_chopper_block['parent'][10] = 'کنرا (KENRA)'
    target['لوازم برقی و پخت و پز']['کنرا'] = [kenra_chopper_block]

# Add Dasti Luxe section
if dasti_luxe_block:
    dasti_luxe_block['brand'] = 'دستی لوکس'
    dasti_luxe_block['parent'][10] = 'دستی لوکس'
    target['لوازم برقی و پخت و پز']['دستی لوکس'] = [dasti_luxe_block]


# ----------------- 4. نوشیدنی ساز -----------------
target['نوشیدنی ساز'] = OrderedDict()
beverage_blocks = sheet_blocks['نوشیدنی ساز']

gronweg_samovar_b = None
gronweg_espresso_b = None
korkmaz_tea_b = None
zamroti_kettle_b = None
zamroti_samovar_b = None
zamroti_blender_b = None
vogati_kettle_b = None
ericsson_kettle_b = None

for b in beverage_blocks:
    name = str(b['parent'][0])
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

for b in beverage_blocks:
    if b in special_bev:
        continue
    brand = b['brand']
    if brand not in target['نوشیدنی ساز']:
        target['نوشیدنی ساز'][brand] = []
    target['نوشیدنی ساز'][brand].append(b)

# Move gronweg items
if 'گرنویک' not in target['نوشیدنی ساز']: target['نوشیدنی ساز']['گرنویک'] = []
if gronweg_samovar_b:
    gronweg_samovar_b['brand'] = 'گرنویک'; gronweg_samovar_b['parent'][10] = 'گرنویک'
    target['نوشیدنی ساز']['گرنویک'].append(gronweg_samovar_b)
if gronweg_espresso_b:
    gronweg_espresso_b['brand'] = 'گرنویک'; gronweg_espresso_b['parent'][10] = 'گرنویک'
    target['نوشیدنی ساز']['گرنویک'].append(gronweg_espresso_b)

# Move korkmaz
if 'کورکماز' not in target['نوشیدنی ساز']: target['نوشیدنی ساز']['کورکماز'] = []
if korkmaz_tea_b:
    korkmaz_tea_b['brand'] = 'کورکماز'; korkmaz_tea_b['parent'][10] = 'کورکماز'
    target['نوشیدنی ساز']['کورکماز'].append(korkmaz_tea_b)

# Move zamroti
if 'زامروتی' not in target['نوشیدنی ساز']: target['نوشیدنی ساز']['زامروتی'] = []
for zb in [zamroti_kettle_b, zamroti_samovar_b, zamroti_blender_b]:
    if zb:
        zb['brand'] = 'زامروتی'; zb['parent'][10] = 'زامروتی'
        target['نوشیدنی ساز']['زامروتی'].append(zb)

# Add Vogati & Ericsson
if vogati_kettle_b:
    vogati_kettle_b['brand'] = 'وگاتی'; vogati_kettle_b['parent'][10] = 'وگاتی'
    target['نوشیدنی ساز']['وگاتی'] = [vogati_kettle_b]

if ericsson_kettle_b:
    ericsson_kettle_b['brand'] = 'اریکسون'; ericsson_kettle_b['parent'][10] = 'اریکسون'
    target['نوشیدنی ساز']['اریکسون'] = [ericsson_kettle_b]


# ----------------- 5. سرمایش و گرمایش -----------------
target['سرمایش و گرمایش'] = OrderedDict()
cooling_blocks = sheet_blocks['سرمایش و گرمایش']

for b in cooling_blocks:
    brand = b['brand']
    if brand not in target['سرمایش و گرمایش']:
        target['سرمایش و گرمایش'][brand] = []
    target['سرمایش و گرمایش'][brand].append(b)

# Add Pakshoma AC
if pakshoma_ac_block:
    pakshoma_ac_block['sheet'] = 'سرمایش و گرمایش'
    pakshoma_ac_block['brand'] = 'پاکشوما'
    pakshoma_ac_block['parent'][8] = 'سرمایش و گرمایش'
    pakshoma_ac_block['parent'][9] = 'کولر گازی پاکشوما'
    pakshoma_ac_block['parent'][10] = 'پاکشوما'
    target['سرمایش و گرمایش']['پاکشوما'] = [pakshoma_ac_block]


# ----------------- 6. تصفیه کننده آب -----------------
target['تصفیه کننده آب'] = OrderedDict()
water_blocks = sheet_blocks['تصفیه کننده آب']

for b in water_blocks:
    if b == clover_water_block:
        continue
    brand = b['brand']
    if brand not in target['تصفیه کننده آب']:
        target['تصفیه کننده آب'][brand] = []
    target['تصفیه کننده آب'][brand].append(b)


# ----------------- 7. صوتی و تصویری -----------------
target['صوتی و تصویری'] = OrderedDict()
av_blocks = sheet_blocks['صوتی و تصویری']

for b in av_blocks:
    brand = b['brand']
    # Standardize Haversen
    b['parent'][0] = b['parent'][0].replace('هاورسون', 'هاورسن')
    b['parent'][10] = 'هاورسن'
    if brand not in target['صوتی و تصویری']:
        target['صوتی و تصویری'][brand] = []
    target['صوتی و تصویری'][brand].append(b)


# ----------------- 8. زیبایی و سلامت فردی -----------------
target['زیبایی و سلامت فردی'] = OrderedDict()
beauty_blocks = sheet_blocks['زیبایی و سلامت فردی']

for b in beauty_blocks:
    brand = b['brand']
    # Merge پروامگا into پرو امگا
    if brand == 'پروامگا':
        brand = 'پرو امگا'
    if brand not in target['زیبایی و سلامت فردی']:
        target['زیبایی و سلامت فردی'][brand] = []
    target['زیبایی و سلامت فردی'][brand].append(b)

print("Target structure created successfully!")
for sname, brands_dict in target.items():
    print(f"Sheet '{sname}': {len(brands_dict)} brand sections, total blocks: {sum(len(v) for v in brands_dict.values())}")

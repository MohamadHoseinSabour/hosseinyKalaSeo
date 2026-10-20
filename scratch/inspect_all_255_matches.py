import sys
import json
import openpyxl
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('data/raw_parsed_new_list.json', 'r', encoding='utf-8') as f:
    raw_list = json.load(f)

wb = openpyxl.load_workbook('hosseiny_kala_catalog.xlsx', data_only=True)
catalog = []
for sname in wb.sheetnames:
    if sname.startswith('📊') or sname.startswith('📖'):
        continue
    ws = wb[sname]
    for r in range(1, ws.max_row + 1):
        v = ws.cell(r, 1).value
        if v:
            catalog.append({
                'sheet': sname,
                'row': r,
                'name': str(v).strip(),
                'brand': str(ws.cell(r, 11).value or '').strip(),
                'type': str(ws.cell(r, 12).value or '').strip(),
                'attr': str(ws.cell(r, 13).value or '').strip(),
                'status': str(ws.cell(r, 18).value or '').strip()
            })

def to_en(t):
    for f, e in zip('۰۱۲۳۴۵۶۷۸۹', '0123456789'):
        t = t.replace(f, e)
    return t

def norm(t):
    if not t: return ''
    t = to_en(str(t).lower())
    t = t.replace('ي', 'ی').replace('ك', 'ک').replace('‌', ' ').replace('-', ' ').replace('_', ' ')
    t = re.sub(r'[\(\)\[\]\.\,\/]', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()

def find_match(it):
    desc = it['desc']
    qty = it['qty']
    if 'کسرواضافات' in desc:
        return 'ACCOUNTING', None
        
    nd = norm(desc)
    
    # Daewoo TV 55
    if 'دوو' in nd and '7000' in nd:
        return 'NEW_PRODUCT', {
            'cat': 'صوتی و تصویری',
            'brand': 'دوو',
            'name': 'تلویزیون ال ای دی ۵۵ اینچ هوشمند دوو مدل 7000',
            'type': 'ساده',
            'qty': qty
        }
        
    # General Fit vacuums
    if 'جنرال فیت' in nd:
        m_code = '4500' if '4500' in nd else ('5300' if '5300' in nd else ('5500' if '5500' in nd else ('4800' if '4800' in nd else '4300')))
        m_name = 'اسکای پلاس 4500' if '4500' in nd else ('پرستو 5300' if '5300' in nd else ('پروانه 5500' if '5500' in nd else ('تاچ استار 4800' if '4800' in nd else 'کیوتی 4300')))
        return 'NEW_PRODUCT', {
            'cat': 'شستشو و نظافت',
            'brand': 'جنرال فیت',
            'name': f'جاروبرقی سطلی جنرال فیت مدل {m_name}',
            'type': 'ساده',
            'qty': qty
        }

    # Bach cordless vacuum
    if 'باخ' in nd and '1454' in nd:
        return 'NEW_PRODUCT', {
            'cat': 'شستشو و نظافت',
            'brand': 'باخ',
            'name': 'جارو شارژی باخ مدل 1454',
            'type': 'ساده',
            'qty': qty
        }

    # Clover 8vw1
    if 'کلور' in nd and '8vw1' in nd:
        return 'NEW_PRODUCT', {
            'cat': 'شستشو و نظافت',
            'brand': 'کلور',
            'name': 'ماشین لباسشویی 8 کیلویی کلور مدل 8vw1 سفید',
            'type': 'ساده',
            'qty': qty
        }

    # Kenwood citrus juicer
    if 'کنوود' in nd and 'مرکبات' in nd:
        return 'NEW_PRODUCT', {
            'cat': 'نوشیدنی ساز',
            'brand': 'کنوود',
            'name': 'آب مرکبات گیری برقی کنوود',
            'type': 'ساده',
            'qty': qty
        }

    # Iran Shargh water heaters
    if 'ایران شرق' in nd:
        if 'اتومات' in nd:
            return 'NEW_PRODUCT', {
                'cat': 'سرمایش و گرمایش',
                'brand': 'ایران شرق',
                'name': 'آبگرمکن دیواری اتوماتیک ایران شرق',
                'type': 'ساده',
                'qty': qty
            }
        else:
            return 'NEW_PRODUCT', {
                'cat': 'سرمایش و گرمایش',
                'brand': 'ایران شرق',
                'name': 'آبگرمکن دیواری شمعک دار ایران شرق مدل 3020',
                'type': 'ساده',
                'qty': qty
            }

    # Maier coffee grinder
    if 'مایر' in nd and 'آسیاب' in nd:
        return 'NEW_PRODUCT', {
            'cat': 'نوشیدنی ساز',
            'brand': 'مایر',
            'name': 'آسیاب قهوه مایر',
            'type': 'ساده',
            'qty': qty
        }

    # Maier food dehydrator 5959
    if 'مایر' in nd and '5959' in nd:
        return 'NEW_PRODUCT', {
            'cat': 'لوازم برقی و پخت و پز',
            'brand': 'مایر',
            'name': 'میوه خشک کن مایر مدل 5959',
            'type': 'ساده',
            'qty': qty
        }

    # Ziko products
    if 'زیکو' in nd:
        if '6501' in nd:
            return 'NEW_PRODUCT', {'cat': 'نوشیدنی ساز', 'brand': 'زیکو', 'name': 'آسیاب قهوه زیکو مدل 6501', 'type': 'ساده', 'qty': qty}
        elif '6502' in nd:
            return 'NEW_PRODUCT', {'cat': 'نوشیدنی ساز', 'brand': 'زیکو', 'name': 'آسیاب قهوه زیکو مدل 6502', 'type': 'ساده', 'qty': qty}
        elif '4038' in nd:
            return 'NEW_PRODUCT', {'cat': 'نوشیدنی ساز', 'brand': 'زیکو', 'name': 'آبمیوه گیری زیکو مدل 4038', 'type': 'ساده', 'qty': qty}
        elif '70028' in nd:
            return 'NEW_PRODUCT', {'cat': 'لوازم برقی و پخت و پز', 'brand': 'زیکو', 'name': 'خردکن برقی ۲ کاسه زیکو مدل 70028', 'type': 'ساده', 'qty': qty}
        elif '5020' in nd:
            return 'NEW_PRODUCT', {'cat': 'زیبایی و سلامت فردی', 'brand': 'زیکو', 'name': 'سشوار حرفه ای زیکو مدل 5020', 'type': 'ساده', 'qty': qty}

    # Bosch chopper
    if 'خردکن' in nd and 'بوش' in nd:
        return 'NEW_PRODUCT', {'cat': 'لوازم برقی و پخت و پز', 'brand': 'بوش', 'name': 'خردکن برقی بوش', 'type': 'ساده', 'qty': qty}

    # Welles chopper 6033
    if 'ویلز' in nd and '6033' in nd:
        return 'NEW_VARIATION', {'cat': 'لوازم برقی و پخت و پز', 'brand': 'ویلز', 'parent_row': 73, 'name': '↳ مدل: 6033 سه لیتری', 'type': 'تنوع', 'qty': qty}

    # Panasonic iron 650
    if 'پاناسونیک' in nd and '650' in nd:
        return 'NEW_PRODUCT', {'cat': 'شستشو و نظافت', 'brand': 'پاناسونیک', 'name': 'اتو بخار پاناسونیک مدل 650', 'type': 'ساده', 'qty': qty}

    # Mebashi espresso
    if 'مباشی' in nd:
        return 'NEW_PRODUCT', {'cat': 'نوشیدنی ساز', 'brand': 'مباشی', 'name': 'اسپرسوساز مباشی', 'type': 'ساده', 'qty': qty}

    # Westinghouse 1663 espresso
    if 'وستینگهوس' in nd and '1663' in nd:
        return 'NEW_PRODUCT', {'cat': 'نوشیدنی ساز', 'brand': 'وستینگهاوس', 'name': 'اسپرسوساز رترو وستینگهاوس مدل 1663', 'type': 'ساده', 'qty': qty}

    # BUVCK garment steamer
    if 'buvck' in nd or 'بخارگر' in nd:
        return 'NEW_PRODUCT', {'cat': 'شستشو و نظافت', 'brand': 'متفرقه', 'name': 'بخارگر دستی چندکاره مدل BUVCK-1266', 'type': 'ساده', 'qty': qty}

    # Polar stone heater
    if 'پلار' in nd and 'سنگ' in nd:
        return 'NEW_PRODUCT', {'cat': 'سرمایش و گرمایش', 'brand': 'پلار', 'name': 'بخاری گازی پلار طرح سنگ بدون دودکش', 'type': 'ساده', 'qty': qty}

    # Absal 405 heater
    if 'آبسال' in nd and '405' in nd:
        return 'NEW_PRODUCT', {'cat': 'سرمایش و گرمایش', 'brand': 'آبسال', 'name': 'بخاری گازی کابینتی آبسال مدل 405', 'type': 'ساده', 'qty': qty}

    # Alton hood 900
    if 'التون' in nd and '900' in nd:
        return 'NEW_PRODUCT', {'cat': 'لوازم برقی و پخت و پز', 'brand': 'آلتون', 'name': 'هود شومینه ای آلتون مدل 900', 'type': 'ساده', 'qty': qty}

    # Tefal 2.2L kettle
    if 'تفال' in nd and '2.2' in nd:
        return 'NEW_PRODUCT', {'cat': 'نوشیدنی ساز', 'brand': 'تفال', 'name': 'کتری برقی تفال 2.2 لیتر', 'type': 'ساده', 'qty': qty}

    # Westinghouse Red variations
    if 'وستینگهوس' in nd or 'وستینگ هوس' in nd:
        if 'کتری' in nd and 'قرمز' in nd:
            return 'NEW_VARIATION', {'cat': 'نوشیدنی ساز', 'brand': 'وستینگهاوس', 'parent_row': 18, 'name': '↳ رنگ: قرمز', 'type': 'تنوع', 'qty': qty}
        elif 'گوشت کوب' in nd and 'قرمز' in nd:
            return 'NEW_PRODUCT', {'cat': 'لوازم برقی و پخت و پز', 'brand': 'وستینگهاوس', 'name': 'گوشت کوب برقی رترو وستینگهاوس قرمز', 'type': 'ساده', 'qty': qty}

    # Depoint Explore twin
    if 'دیپونت' in nd and 'اکسپلور' in nd:
        return 'DEPOINT_EXPLORE', {'desc': desc, 'qty': qty}

    # Depoint Decent
    if 'دیپونت' in nd and 'دیسنت' in nd or 'dipoent' in nd and 'دیسنت' in nd:
        return 'DEPOINT_DECENT', {'desc': desc, 'qty': qty}

    # Electrosteel series 10
    if 'الکترواستیل' in nd and '10' in nd:
        return 'ELECTROSTEEL_SERIES_10', {'desc': desc, 'qty': qty}

    # Electrosteel 14 foot
    if 'الکتروسفید' in nd and '14' in nd or 'الکترواستیل' in nd and '14' in nd:
        return 'NEW_PRODUCT', {'cat': 'یخچال و فریزر', 'brand': 'الکترواستیل', 'name': 'یخچال و فریزر 14 فوت الکترواستیل سفید', 'type': 'ساده', 'qty': qty}

    # Electrosteel compact
    if 'الکتروسفید' in nd and 'کمپکت' in nd or 'الکترواستیل' in nd and 'کمپکت' in nd:
        return 'NEW_PRODUCT', {'cat': 'یخچال و فریزر', 'brand': 'الکترواستیل', 'name': 'یخچال و فریزر الکترواستیل مدل کمپکت سفید', 'type': 'ساده', 'qty': qty}

    # 34 foot white fridge
    if '34' in nd and 'سفید' in nd and 'یخچال' in nd:
        # Check Depoint Max 34 foot
        return 'EXISTING', {'matched': 'یخچال فریزر دوقلو 34 فوت دیپوینت مدل MAX.DU _ مکس (سفید)'}

    # 27 foot titanium
    if '27' in nd and 'تیتانیوم' in nd:
        return 'NEW_PRODUCT', {'cat': 'یخچال و فریزر', 'brand': 'متفرقه', 'name': 'یخچال و فریزر 27 فوت تیتانیوم', 'type': 'ساده', 'qty': qty}

    # 35 foot door bar white
    if '35' in nd and 'درب بار' in nd:
        return 'NEW_PRODUCT', {'cat': 'یخچال و فریزر', 'brand': 'متفرقه', 'name': 'یخچال و فریزر 35 فوت هوم بار سفید', 'type': 'ساده', 'qty': qty}

    # Oویز pot size 28
    if 'قابلمه' in nd and 'اویز' in nd and '28' in nd:
        return 'NEW_VARIATION', {'cat': 'لوازم برقی و پخت و پز', 'brand': 'اویز', 'parent_row': 12, 'name': '↳ سایز (سانتی‌متر): سایز ۲۸', 'type': 'تنوع', 'qty': qty}

    # Otherwise, it matches one of the existing items
    return 'EXISTING', None

categories_new = {}
counts = {'EXISTING': 0, 'NEW_PRODUCT': 0, 'NEW_VARIATION': 0, 'DEPOINT_EXPLORE': 0, 'DEPOINT_DECENT': 0, 'ELECTROSTEEL_SERIES_10': 0, 'ACCOUNTING': 0}

all_new_actions = []

for it in raw_list:
    m_type, data = find_match(it)
    counts[m_type] = counts.get(m_type, 0) + 1
    if m_type != 'EXISTING' and m_type != 'ACCOUNTING':
        all_new_actions.append((m_type, data, it))

print('Summary of classification:')
for k, v in counts.items():
    print(f'  {k}: {v}')

print(f'\nTotal new actions to take: {len(all_new_actions)}')

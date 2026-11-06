import os
import sys
import json
import re
import openpyxl

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"c:\Users\mmhhs\OneDrive\Documents\GitHub\hosseinyKalaSeo"

with open(os.path.join(PROJECT_DIR, 'scratch', 'parsed_incoming_rp_cu_5.json'), 'r', encoding='utf-8') as f:
    incoming = json.load(f)['incoming']

# Load catalog
wb = openpyxl.load_workbook(os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.xlsx'), data_only=True)
catalog = []
for sname in wb.sheetnames[1:9]:
    ws = wb[sname]
    for r in range(2, ws.max_row + 1):
        if type(ws.cell(r, 2)).__name__ == 'MergedCell' or type(ws.cell(r, 3)).__name__ == 'MergedCell':
            continue
        name = ws.cell(r, 1).value
        if not name or str(name).strip().startswith('📂') or str(name).strip().startswith('•') or str(name).strip() == '\\':
            continue
        catalog.append({
            'sheet': sname,
            'row': r,
            'name': str(name).strip(),
            'brand': str(ws.cell(r, 11).value or '').strip(),
            'type': str(ws.cell(r, 12).value or '').strip(),
            'variant': str(ws.cell(r, 13).value or '').strip(),
            'pid': ws.cell(r, 14).value,
            'vid': ws.cell(r, 15).value,
            'sku': str(ws.cell(r, 17).value or '').strip(),
            'status_r': str(ws.cell(r, 18).value or '').strip(),
            'stock': str(ws.cell(r, 8).value or '').strip()
        })

def normalize(text):
    if not text:
        return ""
    text = str(text).lower()
    text = text.replace('ي', 'ی').replace('ك', 'ک').replace('‌', ' ').replace('\xa0', ' ')
    text = text.replace('-', ' ').replace('_', ' ').replace('/', ' ')
    return re.sub(r'\s+', ' ', text).strip()

def extract_nums(text):
    return re.findall(r'[a-zA-Z0-9]+', normalize(text))

existing_list = []
discrepancies = []
new_products = []
accounting_rows = []

# Truly new brands that were never in the store before
NEW_BRANDS = ['کاخلر', 'ادمیلسون', 'تولیپس', 'ساتیا', 'ابکازو', 'بلانزو', 'وینسنت', 'شیمجه', 'واتک', 'گرین', 'آتمن', 'تفال', 'موناکو', 'ساینا', 'میکسی']

for it in incoming:
    idx = it['index']
    title = it['raw_title']
    qty = it['qty']
    norm = normalize(title)

    if 'کسرواضافات' in norm or 'کسورات' in norm:
        accounting_rows.append({
            'index': idx,
            'title': title,
            'qty': qty,
            'reason': 'ردیف تعدیل و کسر و اضافات حسابداری (غیرکالا)'
        })
        continue

    # Specific check for known items
    # 1. Westinghouse variations
    is_westinghouse_var = ('وستینگهوس' in norm or 'وستینگ هوس' in norm) and any(c in norm for c in ['آبی', 'کرم', 'قرمز'])
    # 2. Clever mini fridge variations
    is_clever_mini_var = ('کلورمینی' in norm or 'کلور مینی' in norm) and any(c in norm for c in ['آبی', 'سبز', 'سفید', 'مشکی', 'قرمز'])
    # 3. Depoint Explore twin fridge
    is_depoint_explore = 'اکسپلور' in norm
    # 4. Depoint Decent
    is_depoint_decent = 'دیسنت' in norm
    # 5. Depoint Boss / T7
    is_depoint_boss_t7 = ('دیپونت' in norm or 'دیپوینت' in norm) and any(m in norm for m in ['t7', 'boss', 'boos'])
    # 6. Clever 9TW1
    is_clever_9tw1 = '9tw1' in norm or '8vw1' in norm

    # Truly new check
    is_new = any(nb in norm for nb in NEW_BRANDS)
    if not is_new:
        if any(w in norm for w in ['خردکن بوش', 'سرخ کن دونالکس 6', 'سرخ کن دونالکس 8', 'سرخ کن دونالکس\xa0', 'همزن اوریکس', 'ساندویچ ساز\xa0', 'ساندویچ سازدونالکس 940مشکی', 'سالادساز150', 'پمپ آب', 'تصفیه اب افترون', 'چرخ گوشت ویلز']):
            is_new = True

    if is_new:
        # Detect brand
        b_detected = "نامشخص"
        for nb in NEW_BRANDS:
            if nb in norm:
                b_detected = nb
                break
        if b_detected == "نامشخص":
            for b in ['بوش', 'دونالکس', 'اوریکس', 'افترون', 'ویلز']:
                if b in norm:
                    b_detected = b
                    break

        # Suggest category
        cat = "نامشخص"
        if any(w in norm for w in ['آبگرمکن', 'بخاری', 'پنکه', 'کولر']):
            cat = "سرمایش و گرمایش"
        elif any(w in norm for w in ['اتو', 'بخارگر', 'جارو']):
            cat = "شستشو و نظافت"
        elif any(w in norm for w in ['خردکن', 'سرخ کن', 'زودپز', 'سالادساز', 'همزن', 'گاز', 'هود', 'فر', 'توستر', 'ساندویچ', 'چرخ گوشت']):
            cat = "لوازم برقی و پخت و پز"
        elif any(w in norm for w in ['اسپرسو', 'قهوه', 'آسیاب', 'چای', 'ابمیوه', 'کتری']):
            cat = "نوشیدنی ساز"
        elif any(w in norm for w in ['سشوار', 'اصلاح', 'تراش', 'ترازو']):
            cat = "زیبایی و سلامت فردی"
        elif any(w in norm for w in ['تصفیه', 'پمپ']):
            cat = "تصفیه کننده آب"
        elif any(w in norm for w in ['تلویزیون', 'ال ای دی', 'led']):
            cat = "صوتی و تصویری"

        new_products.append({
            'index': idx,
            'raw_title': title,
            'qty': qty,
            'brand': b_detected,
            'category': cat
        })
    else:
        # Existing Product
        # Detect discrepancies
        disc = []
        if 'aversen' in title.lower() or 'هاورسون' in title:
            disc.append(('برند', title, 'هاورسون / aversen', 'هاورسن', 'عدم رعایت املای صحیح و مصوب هاورسن طبق قانون پروژه'))
        if 'فلیپس' in title:
            disc.append(('برند', title, 'فلیپس', 'فیلیپس', 'اشتباه تایپی و حذف حرف ی'))
        if 'دیپونت' in title or 'dipoent' in title.lower():
            disc.append(('برند', title, 'دیپونت / Dipoent', 'دیپوینت', 'اشتباه در نگارش نام برند ایرانی دیپوینت'))
        if 'وستینگهوس' in title or 'وستینگ هوس' in title:
            disc.append(('برند', title, 'وستینگهوس / وستینگ هوس', 'وستینگهاوس', 'اشتباه املایی در درج حرف الف'))
        if 'x.visjon' in title.lower():
            disc.append(('برند', title, 'X.VISJON', 'ایکس ویژن (X-Vision)', 'اشتباه در درج برند به صورت مخفف انگلیسی'))
        if 'افریزر' in title:
            disc.append(('نام کالا', title, 'افریزر', 'فریزر', 'اشتباه املایی درج الف اضافی در ابتدای کلمه فریزر'))
        if 'ایخچال' in title:
            disc.append(('نام کالا', title, 'ایخچال', 'یخچال', 'اشتباه املایی درج الف اضافی در ابتدای کلمه یخچال'))
        if 'baby3383a' in title.lower():
            disc.append(('برند / کد مدل', title, 'baby3383a', 'بای بابلیس نانو (BaByliss) مدل 3383A', 'درج نامتعارف کد لاتین به جای نام برند و مدل رسمی'))
        if 'madl' in title.lower():
            disc.append(('نگارش', title, 'MADL', 'مدل', 'فینگلیش نوشتن واژه مدل'))
        if 'r)re01(' in title.lower():
            disc.append(('کد مدل', title, 'R)re01(', 'RE01 (قرمز)', 'به هم ریختگی پرانتز و حروف در کد مدل'))
        if 'اینج' in title:
            disc.append(('نگارش', title, 'اینج', 'اینچ', 'غلط املایی درج جیم به جای چ چسبان'))
        if 'boos' in title.lower():
            disc.append(('کد مدل', title, 'BOOS', 'Boss Pro', 'اشتباه تایپی در نوشتن نام مدل Boss Pro'))

        existing_record = {
            'index': idx,
            'raw_title': title,
            'qty': qty,
            'discrepancies': disc
        }
        existing_list.append(existing_record)
        if disc:
            discrepancies.append(existing_record)

print(f"Total Existing: {len(existing_list)}")
print(f"Total Existing with Errors/Discrepancies: {len(discrepancies)}")
print(f"Total New Products: {len(new_products)}")
print(f"Total Accounting Adjustments: {len(accounting_rows)}")
print(f"TOTAL CHECK: {len(existing_list) + len(new_products) + len(accounting_rows)} / {len(incoming)}")

summary_file = os.path.join(PROJECT_DIR, 'scratch', 'perfect_audit_summary.json')
with open(summary_file, 'w', encoding='utf-8') as f:
    json.dump({
        'existing_count': len(existing_list),
        'discrepancies_count': len(discrepancies),
        'new_products_count': len(new_products),
        'accounting_count': len(accounting_rows),
        'discrepancies': discrepancies,
        'new_products': new_products,
        'accounting_rows': accounting_rows
    }, f, ensure_ascii=False, indent=2)

print("Saved scratch/perfect_audit_summary.json")

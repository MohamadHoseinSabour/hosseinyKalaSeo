import os
import sys
import json
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"c:\Users\mmhhs\OneDrive\Documents\GitHub\hosseinyKalaSeo"

with open(os.path.join(PROJECT_DIR, 'scratch', 'parsed_incoming_rp_cu_5.json'), 'r', encoding='utf-8') as f:
    incoming = json.load(f)['incoming']

# Load catalog
import openpyxl
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

# Detailed classification of all 298 items
existing_items = []
new_items = []
accounting_adjustments = []

NEW_BRANDS = ['کاخلر', 'ادمیلسون', 'تولیپس', 'ساتیا', 'ابکازو', 'بلانزو', 'وینسنت', 'شیمجه', 'واتک', 'گرین', 'آتمن', 'تفال', 'موناکو', 'ساینا', 'میکسی']

for it in incoming:
    idx = it['index']
    title = it['raw_title']
    qty = it['qty']
    norm = normalize(title)

    if 'کسرواضافات' in norm or 'کسورات' in norm:
        accounting_adjustments.append(it)
        continue

    # Known new brands
    has_new_brand = any(nb in norm for nb in NEW_BRANDS)
    
    # Specific known new items without brand or with common brand
    specific_new = False
    if any(k in norm for k in ['خردکن بوش', 'سرخ کن دونالکس', 'همزن اوریکس', 'ساندویچ ساز', 'سالادساز150', 'پمپ آب', 'تصفیه اب افترون', 'چرخ گوشت ویلز']):
        specific_new = True

    if has_new_brand or specific_new:
        # Detected brand
        brand = "نامشخص"
        for nb in NEW_BRANDS:
            if nb in norm:
                brand = nb
                break
        if brand == "نامشخص":
            for b in ['بوش', 'دونالکس', 'اوریکس', 'افترون', 'ویلز']:
                if b in norm:
                    brand = b
                    break

        # Suggest category
        cat = "نامشخص"
        if any(w in norm for w in ['اتو', 'بخارگر', 'جارو', 'پتوشور']):
            cat = "شستشو و نظافت"
        elif any(w in norm for w in ['خردکن', 'سرخ کن', 'زودپز', 'سالادساز', 'همزن', 'گاز', 'هود', 'فر', 'توستر', 'ساندویچ']):
            cat = "لوازم برقی و پخت و پز"
        elif any(w in norm for w in ['اسپرسو', 'قهوه', 'آسیاب', 'چای', 'ابمیوه', 'کتری']):
            cat = "نوشیدنی ساز"
        elif any(w in norm for w in ['پنکه', 'بخاری', 'کولر', 'آبگرمکن']):
            cat = "سرمایش و گرمایش"
        elif any(w in norm for w in ['سشوار', 'اصلاح', 'تراش', 'اپیلیدی', 'ترازو']):
            cat = "زیبایی و سلامت فردی"
        elif any(w in norm for w in ['تصفیه', 'پمپ']):
            cat = "تصفیه کننده آب"
        elif any(w in norm for w in ['تلویزیون', 'ال ای دی', 'led']):
            cat = "صوتی و تصویری"

        new_items.append({
            'index': idx,
            'raw_title': title,
            'qty': qty,
            'brand': brand,
            'category': cat
        })
    else:
        # It's an existing item!
        # Check discrepancies
        discrepancies = []
        if 'aversen' in title.lower() or 'هاورسون' in title:
            discrepancies.append(('برند', 'هاورسون / aversen', 'هاورسن'))
        if 'فلیپس' in title:
            discrepancies.append(('برند', 'فلیپس', 'فیلیپس'))
        if 'دیپونت' in title or 'dipoent' in title.lower():
            discrepancies.append(('برند', 'دیپونت / Dipoent', 'دیپوینت'))
        if 'وستینگهوس' in title or 'وستینگ هوس' in title:
            discrepancies.append(('برند', 'وستینگهوس', 'وستینگهاوس'))
        if 'x.visjon' in title.lower():
            discrepancies.append(('برند', 'X.VISJON', 'ایکس ویژن (X-Vision)'))
        if 'افریزر' in title:
            discrepancies.append(('عنوان کالا', 'افریزر', 'فریزر'))
        if 'ایخچال' in title:
            discrepancies.append(('عنوان کالا', 'ایخچال', 'یخچال'))
        if 'baby3383a' in title.lower():
            discrepancies.append(('برند / مدل', 'baby3383a', 'بای بابلیس نانو (BaByliss) مدل 3383A'))
        if 'madl' in title.lower():
            discrepancies.append(('نگارش', 'MADL', 'مدل'))
        if 'r)re01(' in title.lower():
            discrepancies.append(('کد مدل', 'R)re01(', 'RE01 (قرمز)'))
        if 'اینج' in title:
            discrepancies.append(('نگارش', 'اینج', 'اینچ'))
        if 'boos' in title.lower():
            discrepancies.append(('کد مدل', 'BOOS', 'Boss Pro'))

        existing_items.append({
            'index': idx,
            'raw_title': title,
            'qty': qty,
            'discrepancies': discrepancies
        })

print(f"Total Existing: {len(existing_items)}")
print(f"Total Existing with Discrepancies: {sum(1 for e in existing_items if e['discrepancies'])}")
print(f"Total Truly New: {len(new_items)}")
print(f"Total Accounting Adjustments: {len(accounting_adjustments)}")

out_data = {
    'existing_count': len(existing_items),
    'existing_with_errors_count': sum(1 for e in existing_items if e['discrepancies']),
    'new_items_count': len(new_items),
    'accounting_count': len(accounting_adjustments),
    'existing_errors': [e for e in existing_items if e['discrepancies']],
    'new_items': new_items
}

with open(os.path.join(PROJECT_DIR, 'scratch', 'final_classified_audit.json'), 'w', encoding='utf-8') as f:
    json.dump(out_data, f, ensure_ascii=False, indent=2)

print("Saved scratch/final_classified_audit.json")

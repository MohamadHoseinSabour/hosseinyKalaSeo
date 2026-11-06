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

# Known brand list
KNOWN_BRANDS = [
    'کلور', 'دیپوینت', 'هیمالیا', 'الکترواستیل', 'ایستکول', 'بست', 'نیکسان', 'الکتروسان',
    'تکنوسان', 'ریگور', 'دوو', 'پاکشوما', 'دونالکس', 'پاناسونیک', 'فیلیپس', 'آلتون', 'کاخلر',
    'پارس خزر', 'سیماران', 'مباشی', 'کنوود', 'توشیبا', 'هایسنس', 'ایکس ویژن', 'هاورسن',
    'پرومارون', 'بای بابلیس نانو', 'امگا', 'زیکو', 'وستینگهاوس', 'مونزا', 'ساپر', 'سران',
    'آراز', 'ریتون', 'فریدولین', 'پاندا', 'پاکیزان', 'جنرال فیت', 'باخ', 'وگاترونیکس',
    'اویز', 'لاوان', 'نیاک', 'ویلز', 'کاستلو', 'کورکماز', 'ونتو', 'وولگا', 'پروکس',
    'ژمبو', 'وگاتی', 'اریکسون', 'مایر', 'الکترا', 'اوجنرال', 'اوناکس', 'بوتان', 'سانی',
    'پلار', 'گلدن لوکس', 'ایران شرق', 'آبسال', 'افترون', 'سافت واتر', 'سی سی کا', 'نیکایی',
    'هانو', 'هومگلد', 'وست واتر', 'ادمیلسون', 'تولیپس', 'بلانزو', 'ساتیا', 'ابکازو', 'وینسنت', 'شیمجه'
]

# Analysis of every incoming item
analysis_results = []

for it in incoming:
    raw_idx = it['index']
    raw_title = it['raw_title']
    qty = it['qty']
    
    # 1. Detect typos in raw_title
    typos = []
    if 'aversen' in raw_title.lower() or 'هاورسون' in raw_title:
        typos.append(('برند', 'هاورسون / aversen', 'هاورسن'))
    if 'فلیپس' in raw_title:
        typos.append(('برند', 'فلیپس', 'فیلیپس'))
    if 'دیپونت' in raw_title or 'dipoent' in raw_title.lower():
        typos.append(('برند', 'دیپونت / Dipoent', 'دیپوینت'))
    if 'وستینگهوس' in raw_title or 'وستینگ هوس' in raw_title:
        typos.append(('برند', 'وستینگهوس', 'وستینگهاوس'))
    if 'x.visjon' in raw_title.lower():
        typos.append(('برند', 'X.VISJON', 'ایکس ویژن (X-Vision)'))
    if 'افریزر' in raw_title:
        typos.append(('عنوان کالا', 'افریزر', 'فریزر'))
    if 'ایخچال' in raw_title:
        typos.append(('عنوان کالا', 'ایخچال', 'یخچال'))
    if 'baby3383a' in raw_title.lower():
        typos.append(('برند / مدل', 'baby3383a', 'بای بابلیس نانو مدل 3383A'))
    if 'madl' in raw_title.lower():
        typos.append(('نگارش', 'MADL', 'مدل'))
    if 'r)re01(' in raw_title.lower():
        typos.append(('کد مدل', 'R)re01(', 'RE01 (قرمز)'))
    if 'اینج' in raw_title:
        typos.append(('نگارش', 'اینج', 'اینچ'))

    analysis_results.append({
        'index': raw_idx,
        'raw_title': raw_title,
        'qty': qty,
        'typos': typos
    })

print(f"Items analyzed: {len(analysis_results)}")
print(f"Items with accounting text typos detected: {sum(1 for a in analysis_results if a['typos'])}")

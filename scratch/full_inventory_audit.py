import os
import sys
import json
import re
import openpyxl

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"c:\Users\mmhhs\OneDrive\Documents\GitHub\hosseinyKalaSeo"

# 1. Load incoming items
with open(os.path.join(PROJECT_DIR, 'scratch', 'parsed_incoming_rp_cu_5.json'), 'r', encoding='utf-8') as f:
    incoming = json.load(f)['incoming']

# 2. Load catalog
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

# 3. Load mapping standard
mapping_std = {}
if os.path.exists(os.path.join(PROJECT_DIR, 'data', 'inventory_mapping_standard.json')):
    with open(os.path.join(PROJECT_DIR, 'data', 'inventory_mapping_standard.json'), 'r', encoding='utf-8') as f:
        mapping_std = json.load(f)

def normalize_text(text):
    if not text:
        return ""
    text = str(text).lower()
    text = text.replace('ي', 'ی').replace('ك', 'ک').replace('‌', ' ').replace('\xa0', ' ')
    text = text.replace('-', ' ').replace('_', ' ').replace('/', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_model_numbers(text):
    norm = normalize_text(text)
    tokens = re.findall(r'[a-zA-Z0-9]+', norm)
    filtered = []
    for t in tokens:
        if t in ['led', 'smart', '4k', 'hd', 'full', 'fhd', 'madl', 'model']:
            continue
        filtered.append(t)
    return filtered

# Known brands dictionary
BRANDS_MAP = {
    'aversen': 'هاورسن',
    'هاورسون': 'هاورسن',
    'haversen': 'هاورسن',
    'فلیپس': 'فیلیپس',
    'philips': 'فیلیپس',
    'دیپونت': 'دیپوینت',
    'dipoent': 'دیپوینت',
    'depoint': 'دیپوینت',
    'وستینگهوس': 'وستینگهاوس',
    'وستینگ هوس': 'وستینگهاوس',
    'westinghouse': 'وستینگهاوس',
    'x.visjon': 'ایکس ویژن',
    'xvision': 'ایکس ویژن',
    'baby3383a': 'بای بابلیس نانو',
    'کاخلر': 'کاخلر',
    'ادمیلسون': 'ادمیلسون',
    'تولیپس': 'تولیپس',
    'ساتیا': 'ساتیا',
    'ابکازو': 'ابکازو',
    'بلانزو': 'بلانزو',
    'وینسنت': 'وینسنت',
    'شیمجه': 'شیمجه',
    'واتک': 'واتک',
    'گرین': 'گرین',
    'آتمن': 'آتمن',
    'تفال': 'تفال',
    'موناکو': 'موناکو',
    'ساینا': 'ساینا',
    'میکسی': 'میکسی',
}

# Perform comprehensive audit
existing_matched = []
discrepancies_list = []
new_products_list = []

for item in incoming:
    raw_idx = item['index']
    raw_title = item['raw_title']
    qty = item['qty']
    norm_title = normalize_text(raw_title)

    # 1. Match detection
    matched_cat = None
    best_score = 0
    raw_models = extract_model_numbers(raw_title)
    raw_tokens = set(norm_title.split())

    for c in catalog:
        cat_name = c['name']
        norm_cat = normalize_text(cat_name)
        cat_models = extract_model_numbers(cat_name + " " + c['sku'] + " " + c['variant'])
        cat_tokens = set(norm_cat.split())

        model_match = any(m in cat_models or m in norm_cat for m in raw_models if len(m) >= 3 or m.isdigit())
        brand_match = c['brand'] and normalize_text(c['brand']) in norm_title
        overlap = len(raw_tokens.intersection(cat_tokens))

        score = overlap + (15 if model_match else 0) + (8 if brand_match else 0)

        # Handle specific known pairs
        if 'دیسنت' in norm_title and 'دیسنت' in norm_cat:
            score += 25
        if 'اکسپلور' in norm_title and 'اکسپلور' in norm_cat:
            score += 25
        if 'کامپکت' in norm_cat and 'کمپکت' in norm_title:
            score += 25
        if '9tw1' in norm_title and '9tw1' in norm_cat:
            score += 25
        if 're01' in norm_title and 'قرمز' in norm_cat:
            score += 25

        if score > best_score and score >= 12:
            best_score = score
            matched_cat = c

    # Check known new items list
    is_truly_new = False
    new_brands = ['کاخلر', 'ادمیلسون', 'تولیپس', 'ساتیا', 'ابکازو', 'بلانزو', 'وینسنت', 'شیمجه', 'واتک', 'گرین', 'آتمن', 'تفال', 'موناکو', 'ساینا', 'میکسی']
    if any(nb in norm_title for nb in new_brands):
        # Unless it was already in catalog (none of these brands were in catalog!)
        is_truly_new = True

    if not matched_cat or is_truly_new:
        # Determine category and brand for new item
        detected_brand = "نامشخص"
        for nb in new_brands:
            if nb in norm_title:
                detected_brand = nb
                break

        # If brand still not found, search in BRANDS_MAP
        if detected_brand == "نامشخص":
            for k_b, v_b in BRANDS_MAP.items():
                if k_b in norm_title:
                    detected_brand = v_b
                    break

        # Suggest category
        suggested_cat = "نامشخص"
        if any(w in norm_title for w in ['اتو', 'لباسشویی', 'جارو', 'بخارگر', 'پتوشور']):
            suggested_cat = "شستشو و نظافت"
        elif any(w in norm_title for w in ['خردکن', 'پلوپز', 'سرخ کن', 'زودپز', 'سالادساز', 'همزن', 'گاز', 'هود', 'فر', 'توستر']):
            suggested_cat = "لوازم برقی و پخت و پز"
        elif any(w in norm_title for w in ['اسپرسو', 'قهوه', 'آسیاب', 'چای', 'ابمیوه', 'کتری']):
            suggested_cat = "نوشیدنی ساز"
        elif any(w in norm_title for w in ['یخچال', 'فریزر']):
            suggested_cat = "یخچال و فریزر"
        elif any(w in norm_title for w in ['پنکه', 'بخاری', 'کولر', 'پمپ']):
            suggested_cat = "سرمایش و گرمایش"
        elif any(w in norm_title for w in ['سشوار', 'اصلاح', 'تراش', 'اپیلیدی', 'ترازو']):
            suggested_cat = "زیبایی و سلامت فردی"
        elif any(w in norm_title for w in ['تصفیه', 'پمپ آب']):
            suggested_cat = "تصفیه کننده آب"
        elif any(w in norm_title for w in ['تلویزیون', 'ال ای دی', 'led']):
            suggested_cat = "صوتی و تصویری"

        new_products_list.append({
            'index': raw_idx,
            'raw_title': raw_title,
            'qty': qty,
            'detected_brand': detected_brand,
            'suggested_cat': suggested_cat,
            'models': raw_models
        })
    else:
        # Check discrepancies for matched existing items
        disc = []
        
        # 1. Brand name check
        cat_brand = matched_cat['brand']
        norm_brand = normalize_text(cat_brand)
        if 'aversen' in raw_title.lower() or 'هاورسون' in raw_title:
            disc.append(f"اشتباه املایی برند: در فاکتور '{raw_title}' خورده در حالی که برند استاندارد 'هاورسن' است.")
        elif 'فلیپس' in raw_title:
            disc.append(f"اشتباه املایی برند: در فاکتور 'فلیپس' خورده در حالی که املا صحیح 'فیلیپس' است.")
        elif 'دیپونت' in raw_title or 'dipoent' in raw_title.lower():
            disc.append(f"اشتباه املایی برند: در فاکتور 'دیپونت/Dipoent' خورده در حالی که املا صحیح 'دیپوینت' است.")
        elif 'وستینگهوس' in raw_title or 'وستینگ هوس' in raw_title:
            disc.append(f"اشتباه املایی برند: در فاکتور 'وستینگهوس' خورده در حالی که املا صحیح 'وستینگهاوس' است.")
        elif 'x.visjon' in raw_title.lower():
            disc.append(f"اشتباه املایی برند: در فاکتور 'X.VISJON' خورده در حالی که برند صحیح 'ایکس ویژن' است.")

        # 2. Product name typos
        if 'افریزر' in raw_title:
            disc.append(f"اشتباه تایپی عنوان: 'افریزر' به جای 'فریزر'.")
        if 'ایخچال' in raw_title:
            disc.append(f"اشتباه تایپی عنوان: 'ایخچال' به جای 'یخچال'.")
        if 'r)re01(' in raw_title.lower():
            disc.append(f"اشتباه در کد مدل و پرانتز: 'R)re01(' به جای کد مدل استاندارد 'RE01' (رنگ قرمز).")

        existing_matched.append({
            'index': raw_idx,
            'raw_title': raw_title,
            'qty': qty,
            'catalog_name': matched_cat['name'],
            'catalog_sheet': matched_cat['sheet'],
            'catalog_brand': matched_cat['brand'],
            'catalog_pid': matched_cat['pid'],
            'catalog_vid': matched_cat['vid'],
            'discrepancies': disc
        })
        if disc:
            discrepancies_list.append({
                'index': raw_idx,
                'raw_title': raw_title,
                'catalog_name': matched_cat['name'],
                'catalog_brand': matched_cat['brand'],
                'discrepancies': disc
            })

print(f"Total Existing Matched: {len(existing_matched)}")
print(f"Total Discrepancies/Typos in Existing Items: {len(discrepancies_list)}")
print(f"Total New Products Detected: {len(new_products_list)}")

with open(os.path.join(PROJECT_DIR, 'scratch', 'inventory_audit_summary.json'), 'w', encoding='utf-8') as f:
    json.dump({
        'existing_matched_count': len(existing_matched),
        'discrepancies_count': len(discrepancies_list),
        'new_products_count': len(new_products_list),
        'discrepancies': discrepancies_list,
        'new_products': new_products_list
    }, f, ensure_ascii=False, indent=2)

print("Saved scratch/inventory_audit_summary.json")

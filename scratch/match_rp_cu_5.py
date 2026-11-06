import os
import sys
import json
import re
import openpyxl

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"c:\Users\mmhhs\OneDrive\Documents\GitHub\hosseinyKalaSeo"

with open(os.path.join(PROJECT_DIR, 'scratch', 'parsed_incoming_rp_cu_5.json'), 'r', encoding='utf-8') as f:
    incoming_data = json.load(f)['incoming']

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

# Load site products
with open(os.path.join(PROJECT_DIR, 'data', 'products.json'), 'r', encoding='utf-8') as f:
    site_products = json.load(f)

# Load mapping standard
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
    # find all english/alphanumeric and digits >= 2 digits or model tokens
    tokens = re.findall(r'[a-zA-Z0-9]+', norm)
    # filter out common generic words like led, smart, 4k, etc.
    filtered = []
    for t in tokens:
        if t in ['led', 'smart', '4k', 'hd', 'full', 'fhd', 'madl', 'model']:
            continue
        filtered.append(t)
    return filtered

# Try to match each incoming item
matched = []
unmatched = []

for item in incoming_data:
    raw_idx = item['index']
    raw_title = item['raw_title']
    raw_qty = item['qty']
    norm_title = normalize_text(raw_title)

    # 1. Check previous mapping standard by sample_raw_desc or raw_index
    found_std = None
    for k, v in mapping_std.items():
        if isinstance(v, dict) and normalize_text(v.get('sample_raw_desc', '')) == norm_title:
            found_std = v
            break

    # 2. Match against catalog
    best_catalog_match = None
    best_score = 0
    raw_tokens = set(norm_title.split())
    raw_models = extract_model_numbers(raw_title)

    for cat_item in catalog:
        cat_name = cat_item['name']
        norm_cat = normalize_text(cat_name)
        cat_tokens = set(norm_cat.split())
        cat_models = extract_model_numbers(cat_name + " " + cat_item['sku'] + " " + cat_item['variant'])

        # Model code match is king
        model_match = False
        if raw_models:
            for rm in raw_models:
                if len(rm) >= 3 or rm.isdigit():
                    if rm in cat_models or rm in norm_cat:
                        model_match = True
                        break

        # Brand match
        brand_match = False
        cat_brand = normalize_text(cat_item['brand'])
        if cat_brand and (cat_brand in norm_title or any(b in norm_title for b in cat_brand.split())):
            brand_match = True

        # Common words overlap
        overlap = len(raw_tokens.intersection(cat_tokens))
        score = overlap

        if model_match:
            score += 15
        if brand_match:
            score += 8

        if score > best_score and score >= 10:
            best_score = score
            best_catalog_match = cat_item

    if best_catalog_match or found_std:
        matched.append({
            'incoming': item,
            'catalog_match': best_catalog_match,
            'std_match': found_std,
            'score': best_score
        })
    else:
        unmatched.append(item)

print(f"Matched count: {len(matched)}")
print(f"Unmatched count: {len(unmatched)}")

with open(os.path.join(PROJECT_DIR, 'scratch', 'matching_pass1.json'), 'w', encoding='utf-8') as f:
    json.dump({
        'matched_count': len(matched),
        'unmatched_count': len(unmatched),
        'matched': matched,
        'unmatched': unmatched
    }, f, ensure_ascii=False, indent=2)

print("Saved scratch/matching_pass1.json")

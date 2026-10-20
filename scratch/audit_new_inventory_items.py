import sys
import json
import openpyxl
import re
from collections import defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# 1. Load data
with open('data/raw_parsed_new_list.json', 'r', encoding='utf-8') as f:
    raw_list = json.load(f)

with open('data/inventory_mapping_standard.json', 'r', encoding='utf-8') as f:
    mapping_std = json.load(f)

wb = openpyxl.load_workbook('hosseiny_kala_catalog.xlsx', data_only=True)
cat_rows = []
for sname in wb.sheetnames:
    if sname.startswith('📊') or sname.startswith('📖'):
        continue
    ws = wb[sname]
    for r in range(1, ws.max_row + 1):
        v = ws.cell(r, 1).value
        if v:
            cat_rows.append({
                'sheet': sname,
                'row': r,
                'name': str(v).strip(),
                'brand': str(ws.cell(r, 11).value or '').strip(),
                'type': str(ws.cell(r, 12).value or '').strip(),
                'attr': str(ws.cell(r, 13).value or '').strip(),
                'status': str(ws.cell(r, 18).value or '').strip(),
                'price_b': ws.cell(r, 2).value,
                'price_d': ws.cell(r, 4).value,
                'pid': ws.cell(r, 14).value,
                'vid': ws.cell(r, 15).value
            })

def clean_text(t):
    if not t: return ''
    t = str(t).lower()
    t = t.replace('ي', 'ی').replace('ك', 'ک').replace('‌', ' ').replace('-', ' ').replace('_', ' ')
    t = re.sub(r'[\(\)\[\]\.\,\/]', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()

# Build index of catalog rows
catalog_by_clean = {}
for cr in cat_rows:
    cn = clean_text(cr['name'])
    if not cr['name'].startswith('📂'):
        catalog_by_clean[cn] = cr

# Also index by std mappings
std_by_clean_raw = {}
for k, v in mapping_std.items():
    raw_d = v.get('sample_raw_desc', '')
    if raw_d:
        std_by_clean_raw[clean_text(raw_d)] = v

audit_results = []
for idx, it in enumerate(raw_list, 1):
    desc = it['desc']
    qty = it['qty']
    c_desc = clean_text(desc)
    
    # 1. Accounting
    if 'کسرواضافات' in c_desc or 'کسورات' in c_desc:
        audit_results.append({
            'idx': idx,
            'qty': qty,
            'raw_desc': desc,
            'match_type': 'ACCOUNTING',
            'catalog_match': None,
            'note': 'ردیف تعدیل حسابداری - نباید به عنوان محصول وارد شود'
        })
        continue

    # 2. Check std mapping first
    std_info = std_by_clean_raw.get(c_desc)
    if not std_info:
        for sk, sv in std_by_clean_raw.items():
            if sk == c_desc or (len(c_desc) > 5 and (c_desc in sk or sk in c_desc)):
                std_info = sv
                break

    # 3. Try to find match in catalog
    matched_cat = None
    
    # If std_info has standard_name, try to match by that
    if std_info and std_info.get('standard_name'):
        c_std_name = clean_text(std_info['standard_name'])
        if c_std_name in catalog_by_clean:
            matched_cat = catalog_by_clean[c_std_name]
        else:
            for cn, cr in catalog_by_clean.items():
                if c_std_name in cn or cn in c_std_name:
                    matched_cat = cr
                    break

    # Try matching direct name or variation
    if not matched_cat:
        for cn, cr in catalog_by_clean.items():
            # if model number in desc matches
            pass

    audit_results.append({
        'idx': idx,
        'qty': qty,
        'raw_desc': desc,
        'std_info': std_info,
        'catalog_match': matched_cat
    })

print(f'Processed {len(audit_results)} items')

import sys
import os
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
    t = re.sub(r'[\(\)\[\]\.\,\/\+]', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()

# Check each item
results = []
for idx, it in enumerate(raw_list, start=1):
    desc = it['desc']
    qty = it['qty']
    if 'کسرواضافات' in desc:
        results.append({'idx': idx, 'status': 'ACCOUNTING', 'desc': desc, 'qty': qty})
        continue
    
    nd = norm(desc)
    
    # Let's find best candidate in catalog
    candidates = []
    for c in catalog:
        c_name = norm(c['name'])
        c_attr = norm(c['attr'])
        full_c = f"{c_name} {c_attr} {norm(c['brand'])}"
        
        # token overlap
        d_tokens = set(nd.split())
        c_tokens = set(full_c.split())
        common = d_tokens.intersection(c_tokens)
        
        # filter out very common words
        meaningful_common = [w for w in common if w not in ['مدل', 'برقی', 'و', 'فوت', 'لیتر', 'سفید', 'مشکی', 'استیل', 'طرح', 'سری', 'ها']]
        if len(meaningful_common) >= 2 or (len(meaningful_common) == 1 and any(ch.isdigit() for ch in list(meaningful_common)[0])):
            candidates.append((len(meaningful_common), c))
            
    candidates.sort(key=lambda x: x[0], reverse=True)
    results.append({
        'idx': idx,
        'desc': desc,
        'qty': qty,
        'top_candidates': [c[1] for c in candidates[:3]],
        'scores': [c[0] for c in candidates[:3]]
    })

# Print items with NO strong candidate (score < 2 and no number match)
print("=== ITEMS WITH WEAK OR NO MATCH ===")
unmatched = []
for r in results:
    if r.get('status') == 'ACCOUNTING':
        continue
    top_score = r['scores'][0] if r['scores'] else 0
    if top_score < 2:
        unmatched.append(r)
        print(f"#{r['idx']} (qty {r['qty']}): {r['desc']}")
        if r['top_candidates']:
            print(f"   Closest ({r['scores'][0]}): {r['top_candidates'][0]['sheet']} -> {r['top_candidates'][0]['name']}")
        else:
            print("   NO MATCH FOUND AT ALL")

print(f"\nTotal items with weak/no match: {len(unmatched)}")

import sys
import openpyxl
import json

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('hosseiny_kala_catalog.xlsx', data_only=False)

sheets_to_check = [
    'شستشو و نظافت',
    'نوشیدنی ساز',
    'سرمایش و گرمایش',
    'تصفیه کننده آب',
    'زیبایی و سلامت فردی',
    'لوازم برقی و پخت و پز'
]

sheet_brands = {}
for sname in sheets_to_check:
    ws = wb[sname]
    brands = []
    for r in range(1, ws.max_row + 1):
        v = ws.cell(r, 1).value
        if v and ('📂' in str(v)):
            # banner format: '  📂 {cat}  ◀  {brand}'
            parts = str(v).split('◀')
            if len(parts) > 1:
                b = parts[1].strip()
                brands.append((b, r))
    sheet_brands[sname] = brands

print("Existing Brands per sheet:")
for sname, b_list in sheet_brands.items():
    print(f"\n{sname}: {[b[0] for b in b_list]}")

with open('scratch/perfect_audit_summary.json', 'r', encoding='utf-8') as f:
    audit_data = json.load(f)

new_products = audit_data['new_products']

print("\n--- Mapping 44 New Products to Brands and Sheets ---")
for p in new_products:
    raw = p['raw_title']
    cat = p['category']
    b = p['brand']
    
    # check if brand exists in sheet
    existing = [x[0] for x in sheet_brands.get(cat, [])]
    status = "EXISTS" if b in existing else "NEW_BRAND"
    print(f"[{cat}] Brand: '{b}' ({status}) | Raw: '{raw}' | Qty: {p['qty']}")

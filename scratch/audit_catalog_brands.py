import openpyxl
import json

wb = openpyxl.load_workbook('hosseiny_kala_catalog.xlsx', data_only=True)

with open('data/products.json', 'r', encoding='utf-8') as f:
    site_products = json.load(f)

# Build a lookup of site products by id or normalized name
site_by_name = {p.get('name', '').strip(): p for p in site_products}

print("=== AUDIT OF SHEETS IN HOSSEINY_KALA_CATALOG.XLSX ===")
sheets_data = {}

for sheet_name in wb.sheetnames:
    ws = wb[sheet_name]
    current_brand = "UNKNOWN"
    current_section = ""
    rows_info = []
    
    for r in range(1, ws.max_row + 1):
        valA = ws.cell(row=r, column=1).value
        valB = ws.cell(row=r, column=2).value
        valR = ws.cell(row=r, column=18).value
        
        if valA is None:
            continue
        
        strA = str(valA).strip()
        if not strA:
            continue
            
        if '📂' in strA or '◀' in strA:
            # Section header
            current_section = strA
            parts = strA.split('◀')
            if len(parts) > 1:
                current_brand = parts[-1].strip()
            else:
                current_brand = strA.replace('📂', '').strip()
            continue
            
        if strA.startswith('↳'):
            # Variation row
            continue
            
        # Normal product row
        has_brand_in_title = current_brand.lower() in strA.lower() if current_brand != "UNKNOWN" else False
        rows_info.append({
            'row': r,
            'name': strA,
            'brand_section': current_brand,
            'section_raw': current_section,
            'price_rial': valB,
            'status_site': valR,
            'has_brand_in_title': has_brand_in_title
        })
    sheets_data[sheet_name] = rows_info

# Print summary
for sname, rlist in sheets_data.items():
    print(f"\n--- Sheet: {sname} (Total Products: {len(rlist)}) ---")
    brands = set(r['brand_section'] for r in rlist)
    print(f"Brands in sheet: {brands}")
    missing_brand_in_title = [r for r in rlist if not r['has_brand_in_title']]
    print(f"Products where brand '{rlist[0]['brand_section'] if rlist else ''}' is NOT in title: {len(missing_brand_in_title)}")
    for m in missing_brand_in_title:
        print(f"  Row {m['row']:2d} [Brand: {m['brand_section']}]: {m['name']}")

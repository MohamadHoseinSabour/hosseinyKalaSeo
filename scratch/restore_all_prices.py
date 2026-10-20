import openpyxl

# Parse catalog_full_dump.txt
dump_lines = open('scratch/catalog_full_dump.txt', encoding='utf-8').readlines()

prices_by_name = {}
current_sheet = ""

for line in dump_lines:
    if 'SHEET:' in line:
        current_sheet = line.split('SHEET:')[1].split()[0].strip()
        continue
    if '| A: ' in line and '| B: ' in line:
        parts = line.split('|')
        name = parts[1].replace('A:', '').strip()
        price_b = parts[2].replace('B:', '').strip()
        price_d = parts[3].replace('D:', '').strip()
        status_r = parts[4].replace('R:', '').strip()
        
        if price_b != 'None' and price_b != 'قیمت عادی (ریال)':
            try:
                b_val = int(price_b)
                d_val = int(price_d) if price_d != 'None' else b_val
                prices_by_name[(current_sheet, name)] = (b_val, d_val, status_r)
            except ValueError:
                pass

print(f"Extracted {len(prices_by_name)} priced items from dump.")

# Check current catalog
wb = openpyxl.load_workbook('hosseiny_kala_catalog.xlsx')
matched = 0
unmatched = []

for (sname, name), (b_val, d_val, st_r) in prices_by_name.items():
    # Find in wb
    found = False
    # Check sheet sname or all sheets
    for ws_name in wb.sheetnames:
        ws = wb[ws_name]
        for r in range(2, ws.max_row + 1):
            vA = ws.cell(row=r, column=1).value
            if not vA: continue
            vA_str = str(vA).strip()
            
            # Match directly or normalized
            if vA_str == name or (name.startswith('↳') and vA_str == name) or (not name.startswith('↳') and (name in vA_str or vA_str in name)):
                # Set price B, D, F
                ws.cell(row=r, column=2, value=b_val)
                ws.cell(row=r, column=4, value=d_val)
                sale_f = int(round(b_val * 0.95))
                ws.cell(row=r, column=6, value=sale_f)
                matched += 1
                found = True
                break
        if found:
            break
    if not found:
        unmatched.append((sname, name, b_val))

print(f"Matched and set prices for: {matched} items.")
print(f"Unmatched items: {len(unmatched)}")
for u in unmatched:
    print(f"  Unmatched: {u}")

wb.save('hosseiny_kala_catalog.xlsx')
print("Saved hosseiny_kala_catalog.xlsx")

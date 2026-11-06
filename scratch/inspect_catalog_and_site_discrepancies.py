import sys
import json
import openpyxl

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

keywords = ['515', '5040', '3383', 'اکونومی', 'توشیبا', 'وستینگهاوس', 'وستینگهوس', 'دیپوینت', 'دیپونت', 'dipoent', 're01', 'boos', 'boss', 'اینج', 'فلیپس', 'baby']

wb = openpyxl.load_workbook('hosseiny_kala_catalog.xlsx', data_only=True)
prods = json.load(open('data/products.json', encoding='utf-8'))

print('=== CATALOG SEARCH ===')
for s in wb.sheetnames[1:9]:
    ws = wb[s]
    for r in range(2, ws.max_row + 1):
        name = str(ws.cell(r, 1).value or '')
        brand = str(ws.cell(r, 11).value or '')
        sku = str(ws.cell(r, 17).value or '')
        pid = ws.cell(r, 14).value
        vid = ws.cell(r, 15).value
        combined = f'{name} {brand} {sku}'.lower()
        for kw in keywords:
            if kw in combined:
                print(f'{s} R{r}: name="{name}", brand="{brand}", PID={pid}, VID={vid}')
                break

print('\n=== SITE PRODUCTS SEARCH ===')
for p in prods:
    pname = p.get('name', '')
    pslug = p.get('slug', '')
    combined = f'{pname} {pslug}'.lower()
    for kw in keywords:
        if kw in combined:
            print(f'Site PID {p["id"]}: name="{pname}", slug="{pslug}"')
            break

import openpyxl, json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

# 1. Read existing divar products
divar_dirs = os.listdir('divar_organized') if os.path.exists('divar_organized') else []
existing_divar_names = []
existing_divar_folders = []

for d in divar_dirs:
    desc_p = os.path.join('divar_organized', d, 'description.txt')
    if os.path.exists(desc_p):
        existing_divar_folders.append(d)
        with open(desc_p, 'r', encoding='utf-8') as f:
            for line in f:
                if 'نام محصول:' in line or '📌' in line:
                    existing_divar_names.append(line.strip())

print(f"Total existing divar folders: {len(existing_divar_folders)}")

# 2. Read products from catalog
wb = openpyxl.load_workbook('hosseiny_kala_catalog.xlsx', data_only=True)
category_sheets = [s for s in wb.sheetnames if not s.startswith('📊') and not s.startswith('📖')]

with open('data/products.json', 'r', encoding='utf-8') as f:
    site_products = json.load(f)

site_dict = {p['id']: p for p in site_products}

catalog_items = []
for sheet in category_sheets:
    ws = wb[sheet]
    # find column headers
    cols = {}
    for col in range(1, ws.max_column + 1):
        h = str(ws.cell(1, col).value or '').strip()
        if 'نام محصول' in h: cols['name'] = col
        elif 'قیمت عادی (ریال)' in h: cols['price_reg_rial'] = col
        elif 'قیمت عادی (تومان)' in h: cols['price_reg_toman'] = col
        elif 'قیمت حراج (تومان)' in h: cols['price_sale_toman'] = col
        elif 'موجودی' in h: cols['stock'] = col
        elif 'نوع محصول' in h: cols['type'] = col
        elif 'شناسه محصول' in h: cols['pid'] = col
        elif 'شناسه تنوع' in h: cols['vid'] = col
        elif 'وضعیت در سایت' in h: cols['status_site'] = col

    for r in range(3, ws.max_row + 1):
        name = ws.cell(r, cols.get('name', 1)).value
        if not name or str(name).strip().startswith('---'):
            continue
        name = str(name).strip()
        status_site = str(ws.cell(r, cols.get('status_site', 18)).value or '').strip()
        pid = ws.cell(r, cols.get('pid', 16)).value
        vid = ws.cell(r, cols.get('vid', 17)).value
        ptype = str(ws.cell(r, cols.get('type', 12)).value or '').strip()
        stock = str(ws.cell(r, cols.get('stock', 8)).value or '').strip()
        price_reg_toman = ws.cell(r, cols.get('price_reg_toman', 3)).value
        price_sale_toman = ws.cell(r, cols.get('price_sale_toman', 7)).value

        # Only consider products defined in site
        if status_site == 'تعریف شده در سایت' or pid:
            catalog_items.append({
                'sheet': sheet,
                'row': r,
                'name': name,
                'status_site': status_site,
                'pid': pid,
                'vid': vid,
                'ptype': ptype,
                'stock': stock,
                'price_reg_toman': price_reg_toman,
                'price_sale_toman': price_sale_toman
            })

print(f"Total catalog items defined in site: {len(catalog_items)}")

# Check which items are new (created recently or not in divar)
with open('data/id_mappings.json', 'r', encoding='utf-8') as f:
    id_mappings = json.load(f)

# Find site products with ID >= 3400 (the newest additions) or not in divar
recent_site_products = [p for p in site_products if p.get('id', 0) >= 3400 and p.get('status') == 'publish']
print(f"Site products with ID >= 3400 (new batch): {len(recent_site_products)}")
for p in recent_site_products:
    print(f"ID {p['id']}: {p['name']} | slug: {p['slug']} | price: {p.get('price')} | sale: {p.get('sale_price')}")

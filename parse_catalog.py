import openpyxl
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('hosseiny_kala_catalog.xlsx', data_only=True)

catalog_items = []

for sheetname in wb.sheetnames:
    if sheetname in ['📊 خلاصه و داشبورد', '📖 راهنمای کاربری']:
        continue
    ws = wb[sheetname]
    header = None
    for row_idx, row in enumerate(ws.iter_rows(values_only=True)):
        if row_idx == 0:
            header = row
            continue
        if not row or not any(row):
            continue
        first_col = str(row[0]) if row[0] is not None else ""
        if first_col.startswith('📂'):
            continue
        
        name = row[0]
        price_toman = row[2]
        stock_status = row[7]
        main_cat = row[8]
        sub_cat = row[9]
        brand = row[10]
        product_type = row[11]
        product_id = row[13]
        direct_link = row[15]
        site_status = row[17] if len(row) > 17 else ""

        if name:
            catalog_items.append({
                "sheet": sheetname,
                "name": str(name).strip(),
                "price_toman": price_toman,
                "stock": stock_status,
                "main_cat": main_cat,
                "sub_cat": sub_cat,
                "brand": brand,
                "product_type": product_type,
                "product_id": product_id,
                "link": direct_link,
                "site_status": site_status
            })

print(f"Total catalog items loaded: {len(catalog_items)}")
from collections import Counter
print("By sheet:", Counter(x['sheet'] for x in catalog_items))
print("By brand:", Counter(x['brand'] for x in catalog_items).most_common(20))
print("By site_status:", Counter(x['site_status'] for x in catalog_items))

with open('data/catalog_extracted.json', 'w', encoding='utf-8') as f:
    json.dump(catalog_items, f, ensure_ascii=False, indent=2)
print("Saved data/catalog_extracted.json")

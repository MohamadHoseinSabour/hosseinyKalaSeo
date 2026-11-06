import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('hosseiny_kala_catalog.xlsx', data_only=True)
items = []
for sheet in wb.sheetnames:
    if sheet.startswith('📊'):
        continue
    ws = wb[sheet]
    for r_idx, row in enumerate(ws.iter_rows(values_only=True), start=1):
        if row and len(row) >= 18 and str(row[17]).strip() == 'در سایت تعریف نشده':
            items.append({
                'row': r_idx,
                'sheet': sheet,
                'name': str(row[0]).strip(),
                'price_rial': row[1],
                'price_toman': row[2],
                'sale_toman': row[5],
                'stock': row[6]
            })

print(f"Total undefined items found in catalog: {len(items)}")
for it in items[:10]:
    print(f"[{it['sheet']}] {it['name'][:35]} | Toman: {it['price_toman']} | Sale: {it['sale_toman']} | Stock: {it['stock']}")

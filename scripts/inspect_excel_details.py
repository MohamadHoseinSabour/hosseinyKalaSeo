import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('hosseiny_kala_catalog.xlsx', data_only=True)

for sheetname in wb.sheetnames:
    if sheetname in ['📊 خلاصه و داشبورد', '⚡ ویرایش گروهی', '📖 راهنمای کاربری']:
        continue
    ws = wb[sheetname]
    print(f"\n==================== SHEET: {sheetname} ({ws.max_row} rows) ====================")
    headers = [ws.cell(1, c).value for c in range(1, ws.max_column + 1)]
    # find rows with clover or pans or twin fridges
    for r in range(2, ws.max_row + 1):
        name = str(ws.cell(r, 1).value or '')
        stock = ws.cell(r, 6).value
        ptype = ws.cell(r, 10).value
        pid = ws.cell(r, 12).value
        vid = ws.cell(r, 13).value
        status_note = ws.cell(r, 16).value
        brand = ws.cell(r, 9).value
        attr = ws.cell(r, 11).value
        if any(k in name for k in ['کلور', 'تابه', 'مایتابه', 'ماهیتابه', 'روسو', 'فریزر تک', 'یخچال تک']):
            print(f"R{r:03d} | {name[:50]} | Br:{brand} | Attr:{attr} | PID:{pid} | VID:{vid} | Stock:{stock} | Note:{status_note}")

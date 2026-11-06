import sys
import json
import openpyxl
import requests
from requests.auth import HTTPBasicAuth

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('hosseiny_kala_catalog.xlsx', data_only=True)
sheets = ['یخچال و فریزر', 'شستشو و نظافت', 'لوازم برقی و پخت و پز', 'نوشیدنی ساز', 'سرمایش و گرمایش', 'تصفیه کننده آب', 'صوتی و تصویری', 'زیبایی و سلامت فردی']

cat_items = {}
for s in sheets:
    ws = wb[s]
    for r in range(2, ws.max_row+1):
        name = ws.cell(r, 1).value
        if not name or '📂' in str(name):
            continue
        pid = ws.cell(r, 14).value
        vid = ws.cell(r, 15).value
        b = ws.cell(r, 2).value
        f = ws.cell(r, 6).value
        ptype = str(ws.cell(r, 12).value or '').strip()
        if pid and b:
            cat_items[(int(pid), int(vid) if vid else None)] = {
                'reg_rial': b,
                'sale_rial': f,
                'reg_toman': b / 10 if b else None,
                'sale_toman': f / 10 if f else None,
                'name': name,
                'sheet': s,
                'row': r,
                'type': ptype
            }

print(f"Catalog items with price: {len(cat_items)}")

auth = HTTPBasicAuth('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
sample_ids = [4280, 4278, 4266, 4241, 4169]
for pid in sample_ids:
    res = requests.get(f'https://hosseinykala.ir/wp-json/wc/v3/products/{pid}', auth=auth, timeout=15)
    if res.status_code == 200:
        d = res.json()
        cat = cat_items.get((pid, None), {})
        print(f"PID {pid} ({d.get('name')[:25]}): Live reg={d.get('regular_price')}, sale={d.get('sale_price')} | Catalog reg={cat.get('reg_toman')}, sale={cat.get('sale_toman')}")

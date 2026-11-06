import sys
import json
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

# 1. Parse rp_cu_5.html completely
with open(r'c:\Users\mmhhs\Downloads\rp_cu_5.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

items_in_html = []
for tr in soup.find_all('tr'):
    txt = tr.get_text(strip=True)
    if txt and txt not in ['شرح', 'تعداد', 'ردیف', 'کد']:
        items_in_html.append(txt)

print(f"Total raw items in rp_cu_5.html: {len(items_in_html)}")

# Find all items mentioning LED, TV, Toshiba, Xvision, etc.
tv_items_html = []
for i, item in enumerate(items_in_html):
    if any(k in item.lower() for k in ['toshiba', 'x.visjon', 'xvision', 'توشیبا', 'ایکس', 'ال ای دی', 'led', 'aversen', 'هاورسون', 'هاورسن']):
        tv_items_html.append((i, item))

print(f"\nAll TV items found in rp_cu_5.html ({len(tv_items_html)} items):")
for idx, it in tv_items_html:
    print(f"  [{idx}]: {it}")

# 2. Check catalog sheet 'صوتی و تصویری'
import openpyxl
wb = openpyxl.load_workbook('hosseiny_kala_catalog.xlsx', data_only=True)
ws = wb['صوتی و تصویری']
print(f"\nCurrent rows in catalog sheet 'صوتی و تصویری' (max_row={ws.max_row}):")
for r in range(1, ws.max_row + 1):
    vals = [str(ws.cell(r, c).value or '') for c in [1, 8, 11, 14, 16, 18]]
    if any(vals):
        print(f"  Row {r:2d}: Name={vals[0]} | Stock={vals[1]} | Brand={vals[2]} | PID={vals[3]} | Status={vals[5]}")

# 3. Check products.json
with open('data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

print(f"\nProducts in data/products.json in audio-video / television category:")
for p in products:
    cats = [c.get('slug') for c in p.get('categories', [])]
    if any('audio' in c or 'video' in c or 'telev' in c for c in cats):
        print(f"  PID {p['id']}: {p['name']} ({p['slug']}) - stock: {p['stock_status']}")

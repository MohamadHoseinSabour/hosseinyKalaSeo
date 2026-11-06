import os
import sys
import json
import re
from bs4 import BeautifulSoup
import openpyxl

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"c:\Users\mmhhs\OneDrive\Documents\GitHub\hosseinyKalaSeo"
HTML_FILE = r"c:\Users\mmhhs\Downloads\rp_cu_5.html"
CATALOG_PATH = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.xlsx')
PRODUCTS_JSON = os.path.join(PROJECT_DIR, 'data', 'products.json')

def normalize(text):
    if not text:
        return ""
    text = str(text).lower()
    text = text.replace('ي', 'ی').replace('ك', 'ک').replace('‌', ' ').replace('\xa0', ' ')
    text = text.replace('-', ' ').replace('_', ' ').replace('/', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# 1. Parse HTML
with open(HTML_FILE, 'r', encoding='utf-8', errors='ignore') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

tables = soup.find_all('table')
incoming = []
i = 2
while i < len(tables) - 2:
    idx_text = tables[i].get_text(strip=True)
    title_text = tables[i+1].get_text(strip=True) if i+1 < len(tables) else ''
    qty_text = tables[i+2].get_text(strip=True) if i+2 < len(tables) else ''
    if idx_text.isdigit():
        incoming.append({
            'index': int(idx_text),
            'raw_title': title_text,
            'qty': int(qty_text) if qty_text.lstrip('-').isdigit() else 0
        })
        i += 3
    else:
        i += 1

print(f"Total incoming items parsed from HTML: {len(incoming)}")

# 2. Load catalog
wb = openpyxl.load_workbook(CATALOG_PATH, data_only=True)
catalog = []
for sname in wb.sheetnames[1:9]:
    ws = wb[sname]
    for r in range(2, ws.max_row + 1):
        if type(ws.cell(r, 2)).__name__ == 'MergedCell' or type(ws.cell(r, 3)).__name__ == 'MergedCell':
            continue
        name = ws.cell(r, 1).value
        if not name or str(name).strip().startswith('📂') or str(name).strip().startswith('•') or str(name).strip() == '\\':
            continue
        catalog.append({
            'sheet': sname,
            'row': r,
            'name': str(name).strip(),
            'brand': str(ws.cell(r, 11).value or '').strip(),
            'type': str(ws.cell(r, 12).value or '').strip(),
            'variant': str(ws.cell(r, 13).value or '').strip(),
            'pid': ws.cell(r, 14).value,
            'vid': ws.cell(r, 15).value,
            'sku': str(ws.cell(r, 17).value or '').strip(),
            'status_r': str(ws.cell(r, 18).value or '').strip()
        })

print(f"Total catalog items loaded: {len(catalog)}")

# 3. Load products.json
with open(PRODUCTS_JSON, 'r', encoding='utf-8') as f:
    site_products = json.load(f)

print(f"Total site products loaded: {len(site_products)}")

# Output summary to scratch
output_data = {
    'incoming_count': len(incoming),
    'catalog_count': len(catalog),
    'site_products_count': len(site_products),
    'incoming': incoming
}

with open(os.path.join(PROJECT_DIR, 'scratch', 'parsed_incoming_rp_cu_5.json'), 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print("Saved scratch/parsed_incoming_rp_cu_5.json")

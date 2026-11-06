import os
import sys
import json
import openpyxl

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAPSHOT_FILE = os.path.join(PROJECT_DIR, 'scratch', 'site_products_live.json')
CATALOG_PATH = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.xlsx')

with open(SNAPSHOT_FILE, 'r', encoding='utf-8') as f:
    site_data = json.load(f)

site_prods = {p['id']: p for p in site_data['products']}
site_vars = {}
for pid, vlist in site_data['variations'].items():
    for v in vlist:
        site_vars[v['id']] = v

wb = openpyxl.load_workbook(CATALOG_PATH, data_only=True)
SHEETS = [
    'یخچال و فریزر', 'شستشو و نظافت', 'لوازم برقی و پخت و پز', 'نوشیدنی ساز',
    'سرمایش و گرمایش', 'تصفیه کننده آب', 'صوتی و تصویری', 'زیبایی و سلامت فردی'
]

matched_pids = set()
matched_vids = set()

price_changes = []
stock_changes = []
sale_changes = []

for sname in SHEETS:
    ws = wb[sname]
    for r in range(2, ws.max_row + 1):
        name = ws.cell(r, 1).value
        if not name or str(name).strip().startswith('📂') or str(name).strip().startswith('•'):
            continue
        
        ptype = str(ws.cell(r, 12).value or '').strip()
        pid_val = ws.cell(r, 14).value
        vid_val = ws.cell(r, 15).value
        cat_b = ws.cell(r, 2).value # regular price rial
        cat_d = ws.cell(r, 4).value # last price rial
        cat_f = ws.cell(r, 6).value # sale price rial
        cat_h = str(ws.cell(r, 8).value or '').strip() # stock
        
        site_item = None
        item_id_str = ''
        if vid_val:
            try:
                vid = int(vid_val)
                if vid in site_vars:
                    site_item = site_vars[vid]
                    matched_vids.add(vid)
                    item_id_str = f'VID:{vid}'
            except ValueError:
                pass
        elif pid_val:
            try:
                pid = int(pid_val)
                if pid in site_prods:
                    site_item = site_prods[pid]
                    matched_pids.add(pid)
                    item_id_str = f'PID:{pid}'
            except ValueError:
                pass
                
        if site_item:
            # Check stock
            site_stock_code = site_item.get('stock_status')
            site_stock_str = '✓ موجود' if site_stock_code == 'instock' else '✗ ناموجود'
            if cat_h != site_stock_str:
                stock_changes.append((sname, r, name, item_id_str, cat_h, site_stock_str))
                
            # If variable parent, check its stock status, but skip prices
            if ptype == 'متغیر':
                continue
                
            # Check regular price (site IRT -> Rial = * 10)
            site_reg_str = str(site_item.get('regular_price') or '').strip()
            if site_reg_str:
                site_reg_rial = int(float(site_reg_str)) * 10
                if cat_b != site_reg_rial:
                    price_changes.append((sname, r, name, item_id_str, cat_b, site_reg_rial))
            else:
                if cat_b is not None:
                    price_changes.append((sname, r, name, item_id_str, cat_b, None))
                    
            # Check sale price
            site_sale_str = str(site_item.get('sale_price') or '').strip()
            if site_sale_str:
                site_sale_rial = int(float(site_sale_str)) * 10
                if cat_f != site_sale_rial:
                    sale_changes.append((sname, r, name, item_id_str, cat_f, site_sale_rial))
            else:
                if cat_f is not None and cat_f != '':
                    sale_changes.append((sname, r, name, item_id_str, cat_f, None))

print('=== MATCHING SUMMARY ===')
print(f'Matched Site Product IDs: {len(matched_pids)} / {len(site_prods)}')
print(f'Matched Site Variation IDs: {len(matched_vids)} / {len(site_vars)}')
print(f'Stock status changes detected: {len(stock_changes)}')
print(f'Regular price changes detected: {len(price_changes)}')
print(f'Sale price changes detected: {len(sale_changes)}')

if stock_changes:
    print(f'\nAll Stock Status Changes ({len(stock_changes)} items):')
    for sc in stock_changes:
        print(f'  [{sc[0]} R{sc[1]}] {sc[2][:35]} ({sc[3]}): Excel="{sc[4]}" -> Site="{sc[5]}"')

if price_changes:
    print(f'\nRegular Price Changes ({len(price_changes)} items):')
    for pc in price_changes[:20]:
        print(f'  [{pc[0]} R{pc[1]}] {pc[2][:35]} ({pc[3]}): Excel={pc[4]} -> Site={pc[5]}')

if sale_changes:
    print(f'\nSale Price Changes ({len(sale_changes)} items):')
    for sac in sale_changes[:20]:
        print(f'  [{sac[0]} R{sac[1]}] {sac[2][:35]} ({sac[3]}): Excel={sac[4]} -> Site={sac[5]}')

# Check unmatched site products
unmatched_pids = set(site_prods.keys()) - matched_pids
print(f'\nUnmatched Site Products in Catalog: {len(unmatched_pids)}')
for upid in unmatched_pids:
    up = site_prods[upid]
    print(f'  Site PID {upid}: {up.get("name")} (type: {up.get("type")})')

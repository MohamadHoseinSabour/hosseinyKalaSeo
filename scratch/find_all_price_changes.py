import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

USER_FILE = r'C:\Users\mmhhs\.gemini\antigravity\brain\1f248730-479c-4c28-869b-1c3bac549b81\.user_uploaded\media_1793650121277_127804a1.xlsx'
PRE_15_BACKUP = r'c:\Users\mmhhs\OneDrive\Documents\GitHub\hosseinyKalaSeo\hosseiny_kala_catalog.backup_before_15pct_sync_20261102_233158.xlsx'

wb_u = openpyxl.load_workbook(USER_FILE, data_only=True)
wb_p = openpyxl.load_workbook(PRE_15_BACKUP, data_only=True)

sheets = [
    'یخچال و فریزر', 'شستشو و نظافت', 'لوازم برقی و پخت و پز', 'نوشیدنی ساز',
    'سرمایش و گرمایش', 'تصفیه کننده آب', 'صوتی و تصویری', 'زیبایی و سلامت فردی'
]

# Let's inspect by PID/VID
all_u = []
for s in sheets:
    if s not in wb_u.sheetnames: continue
    ws = wb_u[s]
    for r in range(2, ws.max_row+1):
        name = ws.cell(r, 1).value
        if not name or str(name).startswith(('📂', '•')): continue
        pid = ws.cell(r, 14).value
        vid = ws.cell(r, 15).value
        b = ws.cell(r, 2).value
        d = ws.cell(r, 4).value
        f = ws.cell(r, 6).value
        stock = ws.cell(r, 8).value
        status = ws.cell(r, 18).value
        all_u.append({
            'sheet': s, 'row': r, 'name': str(name).strip(),
            'pid': int(pid) if pid else None, 'vid': int(vid) if vid else None,
            'b': b, 'd': d, 'f': f, 'stock': str(stock or '').strip(),
            'status': str(status or '').strip()
        })

all_p = []
for s in sheets:
    if s not in wb_p.sheetnames: continue
    ws = wb_p[s]
    for r in range(2, ws.max_row+1):
        name = ws.cell(r, 1).value
        if not name or str(name).startswith(('📂', '•')): continue
        pid = ws.cell(r, 14).value
        vid = ws.cell(r, 15).value
        b = ws.cell(r, 2).value
        d = ws.cell(r, 4).value
        f = ws.cell(r, 6).value
        stock = ws.cell(r, 8).value
        status = ws.cell(r, 18).value
        all_p.append({
            'sheet': s, 'row': r, 'name': str(name).strip(),
            'pid': int(pid) if pid else None, 'vid': int(vid) if vid else None,
            'b': b, 'd': d, 'f': f, 'stock': str(stock or '').strip(),
            'status': str(status or '').strip()
        })

# Check items in all_u where Column E (percentage change) != 0 or Column B != Column D
print("--- Items in user sheet where B != D ---")
for u in all_u:
    b = u['b']
    d = u['d']
    if b and d and b != d:
        print(f"Sheet {u['sheet']} | {u['name']} (PID {u['pid']}): B={b:,} vs D={d:,} (Diff: {(b-d)/d*100:+.1f}%)")

print("\n--- Check all items where user has B > 0 but D is empty ---")
for u in all_u:
    b = u['b']
    d = u['d']
    if b and not d:
        print(f"Sheet {u['sheet']} | {u['name']} (PID {u['pid']}): B={b:,} (D is empty)")


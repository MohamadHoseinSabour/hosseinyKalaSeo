import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

USER_FILE = r'C:\Users\mmhhs\.gemini\antigravity\brain\1f248730-479c-4c28-869b-1c3bac549b81\.user_uploaded\media_1793650121277_127804a1.xlsx'
PRE_15_BACKUP = r'c:\Users\mmhhs\OneDrive\Documents\GitHub\hosseinyKalaSeo\hosseiny_kala_catalog.backup_before_15pct_sync_20261102_233158.xlsx'

wb_user = openpyxl.load_workbook(USER_FILE, data_only=True)
wb_pre = openpyxl.load_workbook(PRE_15_BACKUP, data_only=True)

sheets = [
    'یخچال و فریزر', 'شستشو و نظافت', 'لوازم برقی و پخت و پز', 'نوشیدنی ساز',
    'سرمایش و گرمایش', 'تصفیه کننده آب', 'صوتی و تصویری', 'زیبایی و سلامت فردی'
]

def load_items(wb):
    res = {}
    for s in sheets:
        if s not in wb.sheetnames:
            continue
        ws = wb[s]
        for r in range(2, ws.max_row + 1):
            name = ws.cell(r, 1).value
            if not name or str(name).startswith(('📂', '•')):
                continue
            pid = ws.cell(r, 14).value
            vid = ws.cell(r, 15).value
            stock = str(ws.cell(r, 8).value or '').strip()
            res[(int(pid) if pid else None, int(vid) if vid else None, str(name).strip())] = {
                'sheet': s, 'row': r, 'name': str(name).strip(),
                'pid': int(pid) if pid else None, 'vid': int(vid) if vid else None,
                'stock': stock, 'b': ws.cell(r, 2).value, 'd': ws.cell(r, 4).value,
                'f': ws.cell(r, 6).value, 'status': str(ws.cell(r, 18).value or '').strip()
            }
    return res

u_items = load_items(wb_user)
p_items = load_items(wb_pre)

to_out = []
to_in = []

for k, u in u_items.items():
    p = p_items.get(k)
    if not p:
        matches = [v for k2, v in p_items.items() if k2[0] == k[0] and k2[1] == k[1] and k[0] is not None]
        if matches:
            p = matches[0]
    if not p:
        continue

    u_stk = u['stock']
    p_stk = p['stock']

    u_is_out = ('ناموجود' in u_stk)
    p_is_out = ('ناموجود' in p_stk)

    if u_is_out and not p_is_out:
        to_out.append((u, p))
    elif not u_is_out and p_is_out:
        to_in.append((u, p))

print(f"Total items changed to OUT OF STOCK (ناموجود): {len(to_out)}")
for u, p in to_out:
    print(f"  • {u['name']} (PID {u['pid']}, VID {u['vid']}) in {u['sheet']}: before='{p['stock']}' -> user='{u['stock']}'")

print(f"\nTotal items changed to IN STOCK (موجود): {len(to_in)}")
for u, p in to_in:
    print(f"  • {u['name']} (PID {u['pid']}, VID {u['vid']}) in {u['sheet']}: before='{p['stock']}' -> user='{u['stock']}'")

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

# Map by (sheet, row) and also by (pid, vid)
# Let's inspect every single row in wb_u compared to wb_p

price_diffs = []
stock_diffs = []
status_diffs = []
new_prices = []

for s in sheets:
    if s not in wb_u.sheetnames or s not in wb_p.sheetnames:
        continue
    ws_u = wb_u[s]
    ws_p = wb_p[s]

    # Map wb_p items by (pid, vid) and by name
    p_by_id = {}
    p_by_name = {}
    for r in range(2, ws_p.max_row + 1):
        name = ws_p.cell(r, 1).value
        if not name or str(name).startswith(('📂', '•')):
            continue
        pid = ws_p.cell(r, 14).value
        vid = ws_p.cell(r, 15).value
        p_data = {
            'row': r, 'name': str(name).strip(),
            'pid': int(pid) if pid else None, 'vid': int(vid) if vid else None,
            'b': ws_p.cell(r, 2).value, 'd': ws_p.cell(r, 4).value,
            'f': ws_p.cell(r, 6).value, 'stock': str(ws_p.cell(r, 8).value or '').strip(),
            'status': str(ws_p.cell(r, 18).value or '').strip()
        }
        if pid:
            p_by_id[(int(pid), int(vid) if vid else None)] = p_data
        p_by_name[str(name).strip()] = p_data

    for r in range(2, ws_u.max_row + 1):
        name = ws_u.cell(r, 1).value
        if not name or str(name).startswith(('📂', '•')):
            continue
        name_str = str(name).strip()
        pid = ws_u.cell(r, 14).value
        vid = ws_u.cell(r, 15).value
        pid_int = int(pid) if pid else None
        vid_int = int(vid) if vid else None

        u_b = ws_u.cell(r, 2).value
        u_d = ws_u.cell(r, 4).value
        u_f = ws_u.cell(r, 6).value
        u_stock = str(ws_u.cell(r, 8).value or '').strip()
        u_status = str(ws_u.cell(r, 18).value or '').strip()

        # Find matching item in p
        p = None
        if pid_int:
            p = p_by_id.get((pid_int, vid_int))
        if not p:
            p = p_by_name.get(name_str)

        if not p:
            # Item only in user sheet?
            print(f"[ONLY IN USER] {s} R{r}: {name_str} (PID {pid_int}, VID {vid_int})")
            continue

        # Check status
        if u_status != p['status']:
            status_diffs.append((s, name_str, pid_int, vid_int, p['status'], u_status))

        # Check stock
        if u_stock != p['stock']:
            stock_diffs.append((s, name_str, pid_int, vid_int, p['stock'], u_stock))

        # Check prices
        p_b = p['b']
        u_b_valid = (u_b is not None and isinstance(u_b, (int, float)) and u_b > 0)
        p_b_valid = (p_b is not None and isinstance(p_b, (int, float)) and p_b > 0)

        if u_b_valid and not p_b_valid:
            new_prices.append((s, name_str, pid_int, vid_int, u_b, u_f))
        elif u_b_valid and p_b_valid and u_b != p_b:
            price_diffs.append((s, name_str, pid_int, vid_int, p_b, u_b, p['f'], u_f))

print(f"\n--- STATUS DIFFS (Column R) [{len(status_diffs)}] ---")
for x in status_diffs:
    print(f"  • {x[0]} | {x[1]} (PID {x[2]}): {x[4]} -> {x[5]}")

print(f"\n--- STOCK DIFFS (Column H) [{len(stock_diffs)}] ---")
for x in stock_diffs:
    print(f"  • {x[0]} | {x[1]} (PID {x[2]}): {x[4]} -> {x[5]}")

print(f"\n--- NEWLY PRICED ITEMS [{len(new_prices)}] ---")
for x in new_prices:
    print(f"  • {x[0]} | {x[1]} (PID {x[2]}): Reg={x[4]/10:,.0f} Toman ({x[4]:,} Rial) | Sale={x[5]/10 if x[5] else 0:,.0f} Toman")

print(f"\n--- PRICE DIFFS (MANUAL CHANGES BY USER) [{len(price_diffs)}] ---")
for x in price_diffs:
    print(f"  • {x[0]} | {x[1]} (PID {x[2]}): Reg {x[4]/10:,.0f} -> {x[5]/10:,.0f} Toman ({x[5]:,} Rial) | OldSale={x[6]/10 if x[6] else 0:,.0f} -> NewSale={x[7]/10 if x[7] else 0:,.0f}")

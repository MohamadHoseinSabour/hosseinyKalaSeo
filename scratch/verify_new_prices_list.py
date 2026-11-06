import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

USER_FILE = r'C:\Users\mmhhs\.gemini\antigravity\brain\1f248730-479c-4c28-869b-1c3bac549b81\.user_uploaded\media_1793650121277_127804a1.xlsx'
CURRENT = r'c:\Users\mmhhs\OneDrive\Documents\GitHub\hosseinyKalaSeo\hosseiny_kala_catalog.xlsx'

wb_u = openpyxl.load_workbook(USER_FILE, data_only=True)
wb_c = openpyxl.load_workbook(CURRENT, data_only=True)

sheets = [
    'یخچال و فریزر', 'شستشو و نظافت', 'لوازم برقی و پخت و پز', 'نوشیدنی ساز',
    'سرمایش و گرمایش', 'تصفیه کننده آب', 'صوتی و تصویری', 'زیبایی و سلامت فردی'
]

# Let's verify mapping between wb_u and wb_c for the 31 items + Korkmaz + 2 out-of-stock + 5 status changes
target_pids = {
    # 2 out of stock
    3026, 4112,
    # 1 manual price change
    3673,
    # 5 status changes
    4085, 4402, 4127, 4442
}

# Add 31 newly priced pids
# We will collect all pids where u_b > 0 but c_b was 0/None (before our 15% increase, or currently)
# Let's list all items from wb_u where u_b > 0 and in wb_c the old baseline was None
c_pre_15 = openpyxl.load_workbook(r'c:\Users\mmhhs\OneDrive\Documents\GitHub\hosseinyKalaSeo\hosseiny_kala_catalog.backup_before_15pct_sync_20261102_233158.xlsx', data_only=True)

newly_priced = []
for s in sheets:
    ws_u = wb_u[s]
    ws_p = c_pre_15[s]
    p_by_id = {}
    for r in range(2, ws_p.max_row+1):
        pid = ws_p.cell(r, 14).value
        vid = ws_p.cell(r, 15).value
        if pid:
            p_by_id[(int(pid), int(vid) if vid else None)] = ws_p.cell(r, 2).value

    for r in range(2, ws_u.max_row+1):
        pid = ws_u.cell(r, 14).value
        vid = ws_u.cell(r, 15).value
        if not pid: continue
        key = (int(pid), int(vid) if vid else None)
        u_b = ws_u.cell(r, 2).value
        p_b = p_by_id.get(key)
        if u_b and not p_b:
            newly_priced.append({
                'sheet': s,
                'pid': int(pid),
                'vid': int(vid) if vid else None,
                'name': str(ws_u.cell(r, 1).value).strip(),
                'price_rial': u_b,
                'price_toman': int(u_b / 10),
                'stock': str(ws_u.cell(r, 8).value or '').strip(),
                'status': str(ws_u.cell(r, 18).value or '').strip()
            })

print(f"Total newly priced items: {len(newly_priced)}")
for it in newly_priced:
    print(f"  • {it['sheet']} | {it['name'][:30]} | PID: {it['pid']} | {it['price_toman']:,} Toman | Stock: {it['stock']}")

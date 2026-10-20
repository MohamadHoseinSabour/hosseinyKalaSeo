import os, sys, openpyxl

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('hosseiny_kala_catalog.xlsx', data_only=True)

# Let's inspect sheets and print all rows with status 'در سایت تعریف نشده' and their parents/children
for sheetname in wb.sheetnames:
    ws = wb[sheetname]
    found = False
    for r in range(2, ws.max_row + 1):
        status_r = ws.cell(r, 18).value
        if status_r == 'در سایت تعریف نشده':
            found = True
            break
    if not found:
        continue
    
    print(f"\n==================== SHEET: {sheetname} ====================")
    for r in range(2, ws.max_row + 1):
        status_r = ws.cell(r, 18).value
        name = ws.cell(r, 1).value
        if not name:
            continue
        # If this row or adjacent rows have 'در سایت تعریف نشده', print context
        # Actually print all rows where status_r is 'در سایت تعریف نشده' along with row-1 and row+1
        if status_r == 'در سایت تعریف نشده':
            parent_info = ""
            # look up upwards for parent if this is a variation (starts with ↳)
            if str(name).strip().startswith('↳'):
                for pr in range(r - 1, 1, -1):
                    pname = str(ws.cell(pr, 1).value or '')
                    if not pname.startswith('↳') and not pname.startswith('📂'):
                        parent_info = f" [PARENT: Row {pr} '{pname}' PID: {ws.cell(pr, 15).value} Status: {ws.cell(pr, 18).value}]"
                        break
            print(f"Row {r:3d} | Status: {status_r:18s} | PID: {str(ws.cell(r, 15).value):6s} | Price: {str(ws.cell(r, 2).value):10s} | Stock: {str(ws.cell(r, 8).value):10s} | Name: {name}{parent_info}")

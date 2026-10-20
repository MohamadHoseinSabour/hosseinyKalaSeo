import openpyxl, os, sys, shutil
from datetime import datetime
from openpyxl.styles import PatternFill

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.xlsx')

def fix_colors():
    print("=== FIXING CATALOG ROW COLORS & DYNAMIC FORMATTING ===")
    
    # 1. Backup catalog
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(PROJECT_DIR, f'hosseiny_kala_catalog.backup_colors_{ts}.xlsx')
    shutil.copy2(CATALOG_PATH, backup_path)
    print(f"✓ Backup created: {os.path.basename(backup_path)}")

    wb = openpyxl.load_workbook(CATALOG_PATH)
    
    total_fixed_white = 0
    total_hold_fixed = 0

    no_fill = PatternFill(fill_type=None)

    for sheetname in wb.sheetnames:
        if sheetname in ['📖 راهنمای کاربری', '📊 خلاصه و داشبورد']:
            continue
            
        ws = wb[sheetname]
        fixed_in_sheet = []
        
        for r in range(2, ws.max_row + 1):
            name = str(ws.cell(r, 1).value or '')
            # Skip brand category header rows
            if name.startswith('  📂'):
                continue
                
            st = ws.cell(r, 18).value
            
            # Check if this row is 'ثبت‌شده در سایت' and has yellow direct fill
            f1 = ws.cell(r, 1).fill
            fg1 = f1.fgColor.rgb if f1 and f1.fgColor else 'None'
            
            if st == 'ثبت‌شده در سایت' and fg1 in ['FFFFF2CC', 'FFF2CC']:
                # Reset all 18 cells in this row to no_fill (white)
                for c in range(1, 19):
                    ws.cell(r, c).fill = no_fill
                fixed_in_sheet.append((r, name[:30]))
                total_fixed_white += 1
                
        if fixed_in_sheet:
            print(f"\nSheet [{sheetname}]: Fixed {len(fixed_in_sheet)} rows to pure white:")
            for row_num, row_name in fixed_in_sheet:
                print(f"  - Row {row_num:3d}: {row_name}")

    wb.save(CATALOG_PATH)
    print(f"\n✓ Successfully updated {total_fixed_white} rows to white in {CATALOG_PATH}")

if __name__ == '__main__':
    fix_colors()

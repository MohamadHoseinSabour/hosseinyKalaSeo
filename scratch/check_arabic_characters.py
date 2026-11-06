import sys
import openpyxl

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('hosseiny_kala_catalog.xlsx', data_only=True)

arabic_issues = []
for s in wb.sheetnames[1:9]:
    ws = wb[s]
    for r in range(2, ws.max_row + 1):
        if type(ws.cell(r, 2)).__name__ == 'MergedCell' or type(ws.cell(r, 3)).__name__ == 'MergedCell':
            continue
        name = str(ws.cell(r, 1).value or '')
        brand = str(ws.cell(r, 11).value or '')
        if 'ي' in name or 'ك' in name or 'ي' in brand or 'ك' in brand:
            arabic_issues.append((s, r, name, brand))

print(f"Rows with Arabic kaf or ya: {len(arabic_issues)}")
for ai in arabic_issues:
    print(f"[{ai[0]} R{ai[1]}] name=\"{ai[2][:45]}\", brand=\"{ai[3]}\"")

import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('hosseiny_kala_catalog_latest.xlsx', data_only=True)
ws = wb['جاروبرقی']
print("=== Products in Sheet 'جاروبرقی' ===")
for r in ws.iter_rows(values_only=True):
    if r[0] and not r[0].startswith('•') and not r[0].startswith('نام'):
        # Check if it has a product ID or is a subcategory header
        if r[9]:
            print(f"  PID: {r[9]} | Name: {r[0]} | Price: {r[1]} | Cat: {r[6]}")
        elif r[0].startswith('■'):
            print(f"{r[0]}")

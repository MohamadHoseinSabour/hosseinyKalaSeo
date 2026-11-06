import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('scratch/test_rebuilt_catalog_out.xlsx', data_only=False)
ws = wb['لوازم برقی و پخت و پز']

print("--- Inspecting Donalex section in لوازم برقی و پخت و پز ---")
for r in range(1, ws.max_row + 1):
    val_k = str(ws.cell(r, 11).value or '')
    val_a = str(ws.cell(r, 1).value or '')
    if 'دونالکس' in val_k or 'دونالکس' in val_a:
        print(f"Row {r:3d}: Name='{val_a[:35]}' | Col 3={ws.cell(r, 3).value} | Stock={ws.cell(r, 8).value} | Status={ws.cell(r, 18).value}")

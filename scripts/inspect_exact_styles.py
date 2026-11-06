import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('hosseiny_kala_catalog.xlsx', data_only=False)
ws = wb['شستشو و نظافت']

# Banner row 2
b_cell = ws.cell(2, 1)
print("Banner fill:", b_cell.fill.fill_type, b_cell.fill.start_color.rgb if b_cell.fill else None)
print("Banner font:", b_cell.font.name, b_cell.font.size, b_cell.font.bold, b_cell.font.color.rgb if b_cell.font.color else None)
print("Banner align:", b_cell.alignment.horizontal, b_cell.alignment.vertical)

# Data row 3
for col in [1, 2, 3, 8, 11, 12, 18]:
    c = ws.cell(3, col)
    print(f"Col {col} ({ws.cell(1, col).value}):")
    print(f"  val={c.value}")
    print(f"  font={c.font.name if c.font else None}, size={c.font.size if c.font else None}, bold={c.font.bold if c.font else None}")
    print(f"  fill={c.fill.fill_type if c.fill else None}, color={c.fill.start_color.rgb if c.fill and c.fill.start_color else None}")
    print(f"  align={c.alignment.horizontal if c.alignment else None}, {c.alignment.vertical if c.alignment else None}")
    print(f"  num_format={c.number_format}")

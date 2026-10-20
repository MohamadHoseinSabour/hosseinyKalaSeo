import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/inventory_normalized.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

print(f"Total normalized items: {len(items)}")

print("\n=== FREEZERS (Index 110 to 135) ===")
for it in items:
    if 110 <= it['raw_index'] <= 135:
        print(f"Index: {it['raw_index']:03d} | Qty: {it['raw_quantity']} | Stock: {it['in_stock']} | Desc: {it['cleaned_raw_desc']} | Brand: {it['brand']} | Model: {it.get('model_code')}")

import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/inventory_normalized.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

for it in items:
    desc = it['cleaned_raw_desc']
    if any(k in desc for k in ['اکونومی', 'افریزر', 'ایخچال', '101']):
        print(f"Index: {it['raw_index']:03d} | Qty: {it['raw_quantity']} | Stock: {it['in_stock']} | Desc: {desc} | Brand: {it['brand']} | Model: {it.get('model_code')}")

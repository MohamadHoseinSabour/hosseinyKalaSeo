import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/perfect_audit_summary.json', 'r', encoding='utf-8') as f:
    audit_data = json.load(f)

new_products = audit_data['new_products']
print(f"Total new products: {len(new_products)}")

for i, p in enumerate(new_products):
    print(f"{i+1:2d}. [Index {p['index']}] Raw: '{p['raw_title']}' | Qty: {p['qty']} | Brand: '{p['brand']}' | Cat: '{p['category']}'")

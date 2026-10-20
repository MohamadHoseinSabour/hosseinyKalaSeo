import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/missing_products.json', encoding='utf-8') as f:
    items = json.load(f)

for i, it in enumerate(items[:20]):
    print(f"Row {it.get('row')}: is_var={it.get('is_variation')} | parent={it.get('parent_name')} | name={it.get('name')}")

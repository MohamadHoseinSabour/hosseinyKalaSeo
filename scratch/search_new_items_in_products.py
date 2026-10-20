import json
import sys
import os
sys.path.insert(0, os.path.abspath('.'))
sys.stdout.reconfigure(encoding='utf-8')

with open('data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

with open('data/id_mappings.json', 'r', encoding='utf-8') as f:
    id_mappings = json.load(f)

from scratch.verify_all_255_coverage import NEW_ITEM_INDICES

for idx, (sheet, brand, name, ptype, stock) in NEW_ITEM_INDICES.items():
    # search products
    found_p = []
    for p in products:
        p_name = p.get('name', '')
        if any(term in p_name for term in [brand, name.split()[-1]] if len(term) > 3):
            if brand in p_name:
                found_p.append(p)
    # search id_mappings
    found_id = []
    for k, v in id_mappings.items():
        v_name = v.get('name', '')
        if brand in v_name:
            found_id.append((k, v_name))
            
    print(f"#{idx} [{sheet} - {brand}] {name}")
    matching_prod = [p for p in products if name in p.get('name', '') or p.get('name', '') in name]
    if matching_prod:
        print(f"   MATCH IN products.json: ID={matching_prod[0].get('id')} Price={matching_prod[0].get('regular_price')}")
    else:
        print("   Not on site.")

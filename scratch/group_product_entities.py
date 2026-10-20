import json
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/catalog_current_rows.json', encoding='utf-8') as f:
    rows = json.load(f)

# Group rows into product entities
# A product entity is defined by the parent row (or standalone row if not a variation)
# All variation rows belonging to that parent are grouped together.

product_entities = []
current_entity = None

for r in rows:
    if not r['is_variation']:
        # This is a standalone product or a parent of a variable product
        current_entity = {
            'sheet': r['sheet'],
            'folder': r['folder'],
            'parent_row': r['row'],
            'name': r['name'],
            'brand': r['brand'],
            'ptype': r['ptype'],
            'status': r['status'],
            'variations': []
        }
        product_entities.append(current_entity)
    else:
        # This is a variation row belonging to current_entity
        if current_entity:
            current_entity['variations'].append(r)

print(f"Total distinct product entities (families): {len(product_entities)}")

# Analyze status distribution of product entities
# An entity might be:
# - all 'ثبت‌شده در سایت'
# - all 'فعلا دست نگه دار'
# - all 'در سایت تعریف نشده'
# - mixed statuses
for p in product_entities:
    all_statuses = set([p['status']] + [v['status'] for v in p['variations']])
    p['all_statuses'] = list(all_statuses)
    
print("\nProduct entities with 'فعلا دست نگه دار':")
hold_entities = [p for p in product_entities if 'فعلا دست نگه دار' in p['all_statuses']]
for p in hold_entities:
    print(f"[{p['sheet']} | Row {p['parent_row']}] {p['name']} (Brand: {p['brand']}, Vars: {len(p['variations'])}) - Statuses: {p['all_statuses']}")

print(f"\nTotal entities with 'فعلا دست نگه دار': {len(hold_entities)}")

# Entities that are to be registered (i.e. have 'در سایت تعریف نشده' and NOT hold)
unlisted_entities = [p for p in product_entities if 'در سایت تعریف نشده' in p['all_statuses']]
print(f"Total entities with 'در سایت تعریف نشده': {len(unlisted_entities)}")

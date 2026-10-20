import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/catalog_current_rows.json', encoding='utf-8') as f:
    rows = json.load(f)

entities = []
curr = None
for r in rows:
    if not r['is_variation']:
        curr = {
            'sheet': r['sheet'],
            'folder': r['folder'],
            'parent_row': r['row'],
            'name': r['name'],
            'brand': r['brand'],
            'ptype': r['ptype'],
            'status': r['status'],
            'variations': []
        }
        entities.append(curr)
    else:
        if curr:
            curr['variations'].append(r)

registered = [e for e in entities if e['status'] == 'ثبت‌شده در سایت']
hold = [e for e in entities if e['status'] == 'فعلا دست نگه دار']
unlisted = [e for e in entities if e['status'] == 'در سایت تعریف نشده']

print("="*60)
print(f"Total product entities: {len(entities)}")
print(f"  * Registered entities ('ثبت‌شده در سایت'): {len(registered)}")
print(f"  * Hold entities ('فعلا دست نگه دار'): {len(hold)}")
print(f"  * Active unlisted entities ('در سایت تعریف نشده'): {len(unlisted)}")
print("="*60)

# Check among active unlisted entities (should be exactly 21 + 40 = 61!):
# 21 from previous automated search + 40 that the user added images for!
print(f"\nActive Unlisted Entities Count: {len(unlisted)}")
print("Let's check if all 61 active unlisted entities have images:")
for i, e in enumerate(unlisted, 1):
    vc = len(e['variations'])
    v_info = f" ({vc} تنوع)" if vc > 0 else ""
    print(f"{i:2d}. [{e['sheet']} | Row {e['parent_row']}] [{e['brand']}] {e['name']}{v_info}")

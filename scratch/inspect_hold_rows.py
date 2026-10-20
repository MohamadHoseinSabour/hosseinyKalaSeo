import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/catalog_current_rows.json', encoding='utf-8') as f:
    rows = json.load(f)

with open('scratch/user_changes_audit.json', encoding='utf-8') as f:
    audit = json.load(f)

hold_candidates = audit['hold_candidates']

print('Checking 23 hold items and their variations:')
total_rows_to_update = []
for h in hold_candidates:
    sheet = h['sheet']
    prow = h['row']
    # find all rows with this parent_row or row == prow
    matching_rows = [r for r in rows if r['sheet'] == sheet and (r['row'] == prow or r['parent_row'] == prow)]
    total_rows_to_update.extend(matching_rows)
    fname = h['folder_name']
    print(f"[{sheet} | Row {prow}] {fname}: {len(matching_rows)} rows")
    for mr in matching_rows:
        if mr['is_variation']:
            r_num = mr['row']
            r_name = mr['name']
            r_stat = mr['status']
            print(f"   -> Var Row {r_num}: {r_name} (current status: {r_stat})")

print(f"\nTotal Excel rows to update: {len(total_rows_to_update)}")

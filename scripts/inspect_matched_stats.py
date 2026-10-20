import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/inventory_matched_results.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

print(f"Total results in inventory_matched_results.json: {len(results)}")

match_types = {}
site_statuses = {}
for r in results:
    mt = r.get('match_type')
    st = r.get('site_status')
    match_types[mt] = match_types.get(mt, 0) + 1
    site_statuses[st] = site_statuses.get(st, 0) + 1

print("\nMatch Types:")
for k, v in match_types.items():
    print(f"  {k}: {v}")

print("\nSite Statuses:")
for k, v in site_statuses.items():
    print(f"  {k}: {v}")

print("\nItems marked as 'در سایت تعریف نشده' (New Offline):")
new_offline = [r for r in results if r.get('site_status') == 'در سایت تعریف نشده']
print(f"Count: {len(new_offline)}")
for it in new_offline[:25]:
    print(f"  Raw: {it['raw_desc']} | Brand: {it['brand']} | Model: {it['model_code']} | Cat: {it['category']}")

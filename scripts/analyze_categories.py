import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('data/categories.json', 'r', encoding='utf-8') as f:
    cats = json.load(f)

print(f"Total categories: {len(cats)}\n")

# Map parents
cat_map = {c['id']: c for c in cats}
parents = [c for c in cats if c.get('parent', 0) == 0]
children = [c for c in cats if c.get('parent', 0) != 0]

print("=== MAIN (PARENT) CATEGORIES ===")
for p in sorted(parents, key=lambda x: x.get('count', 0), reverse=True):
    subcats = [c for c in cats if c.get('parent') == p['id']]
    sub_count_sum = sum(c.get('count', 0) for c in subcats)
    print(f"[{p['id']}] {p['name']} | Direct Products: {p.get('count', 0)} | Subcats: {len(subcats)} (Sum: {sub_count_sum})")
    print(f"     URL: {p.get('url')}")
    for sc in subcats:
        print(f"       -> [{sc['id']}] {sc['name']} (Products: {sc.get('count', 0)}) | Slug: {sc.get('slug')}")
        print(f"          URL: {sc.get('url')}")
    print()

print("\n=== ORPHAN / OTHER SUB-CATEGORIES (Parent not 0 and parent not in parents) ===")
parent_ids = {p['id'] for p in parents}
other_subs = [c for c in cats if c.get('parent', 0) not in parent_ids and c.get('parent', 0) != 0]
for sc in other_subs:
    print(f"[{sc['id']}] {sc['name']} | Parent ID: {sc.get('parent')} | Count: {sc.get('count', 0)} | URL: {sc.get('url')}")

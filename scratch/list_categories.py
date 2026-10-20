import json, sys
if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')

with open('data/categories.json', 'r', encoding='utf-8') as f:
    cats = json.load(f)

cat_dict = {c['id']: c for c in cats}

print("--- MAIN CATEGORIES (Parent = 0) ---")
for c in cats:
    if c.get('parent') == 0:
        print(f"ID: {c['id']:4d} | Name: {c['name']} | URL: {c['url']}")

print("\n--- ALL CATEGORIES HIERARCHY ---")
for c in sorted(cats, key=lambda x: x['id']):
    parent_id = c.get('parent', 0)
    parent_name = cat_dict.get(parent_id, {}).get('name', 'ROOT') if parent_id else 'ROOT'
    print(f"ID: {c['id']:4d} | Parent: {parent_id:4d} ({parent_name}) | Name: {c['name']}")

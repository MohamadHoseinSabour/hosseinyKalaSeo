import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/categories.json', 'r', encoding='utf-8') as f:
    cats = json.load(f)

print(f"Total categories: {len(cats)}")

roots = [c for c in cats if c.get('parent', 0) == 0]
print(f"Root categories: {len(roots)}")

for r in sorted(roots, key=lambda x: x['name']):
    print(f"\n📂 [{r['id']}] {r['name']} (URL: {r['url']}) - Total products: {r.get('count', 0)}")
    
    # Children of this root
    children = [c for c in cats if c.get('parent') == r['id']]
    for ch in sorted(children, key=lambda x: x['name']):
        print(f"   ├── 📁 [{ch['id']}] {ch['name']} (Count: {ch.get('count', 0)}) -> {ch['url']}")
        
        # Sub-children (Level 3)
        sub_children = [c for c in cats if c.get('parent') == ch['id']]
        for sc in sorted(sub_children, key=lambda x: x['name']):
            print(f"   │     └── 📄 [{sc['id']}] {sc['name']} (Count: {sc.get('count', 0)}) -> {sc['url']}")

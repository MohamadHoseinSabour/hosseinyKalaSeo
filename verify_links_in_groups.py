import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/proposed_ad_groups.json', 'r', encoding='utf-8') as f:
    groups = json.load(f)

with open('data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

# Build a mapping from name to canonical url
name_to_url = {}
for p in products:
    name_to_url[p['name'].strip()] = p.get('permalink') or f"https://hosseinykala.ir/product/{p.get('slug')}/"

for g_key, g_val in groups.items():
    print(f"\n### {g_val['title']} ({g_val['count']} کالا)")
    print(f"لینک دسته‌بندی در سایت: {g_val['category_link']}")
    for item in g_val['items']:
        name = item['name']
        link = item.get('link') or name_to_url.get(name, '')
        print(f"  - {name} -> {link}")

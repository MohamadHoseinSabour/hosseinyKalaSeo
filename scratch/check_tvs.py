import json

with open('scratch/live_wp_products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

for p in products:
    title = p.get('title', {}).get('raw', '') or p.get('title', {}).get('rendered', '')
    if 'تلویزیون' in title:
        print(f"ID {p['id']}: {title} | Slug: {p['slug']}")

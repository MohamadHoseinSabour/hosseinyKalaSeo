import json

with open('scratch/live_wp_products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

for pid in [3546, 3662, 4099, 4101, 3354]:
    p = next((x for x in products if x['id'] == pid), None)
    if p:
        print(f"\n==================== PRODUCT {pid}: {p.get('title', {}).get('raw')} ====================")
        print("Slug:", p.get('slug'))
        print("Excerpt:", p.get('excerpt', {}).get('raw'))
        content = p.get('content', {}).get('raw', '')
        print("Content lines mentioning brand or متفرقه:")
        for line in content.splitlines():
            if 'برند' in line or 'متفرقه' in line or 'مدل' in line:
                print("  ", line.strip()[:150])

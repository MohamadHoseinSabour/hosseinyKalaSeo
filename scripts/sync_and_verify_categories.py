import requests
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Content-Type': 'application/json'
}

print("=== 1. Fetching all categories from WooCommerce ===")
r = requests.get('https://hosseinykala.ir/wp-json/wp/v2/product_cat?per_page=100', auth=AUTH, headers=HEADERS, timeout=30)
if r.status_code != 200:
    print(f"Failed to fetch categories: {r.status_code}")
    sys.exit(1)

cats = r.json()
print(f"Fetched {len(cats)} categories from WooCommerce.")

# Format data for data/categories.json
clean_cats = []
for c in cats:
    clean_cats.append({
        'id': c['id'],
        'name': c['name'],
        'slug': c['slug'],
        'url': c['link'],
        'parent': c.get('parent', 0),
        'count': c.get('count', 0),
        'description': c.get('description', '')
    })

# Sort clean_cats by id
clean_cats = sorted(clean_cats, key=lambda x: x['id'])

with open('data/categories.json', 'w', encoding='utf-8') as f:
    json.dump(clean_cats, f, ensure_ascii=False, indent=2)

print(f"Saved {len(clean_cats)} categories to data/categories.json.")

# Analyze hierarchy
roots = [c for c in clean_cats if c['parent'] == 0]
level2 = [c for c in clean_cats if c['parent'] in [r['id'] for r in roots]]
level3 = [c for c in clean_cats if c['parent'] in [l['id'] for l in level2]]

print(f"\n--- Hierarchy Summary ---")
print(f"Root categories (Level 1): {len(roots)}")
print(f"Level 2 categories: {len(level2)}")
print(f"Level 3 categories: {len(level3)}")
print(f"Total categories: {len(clean_cats)}")

print("\n--- The 7 Main Root Categories ---")
for rc in sorted(roots, key=lambda x: x['name']):
    print(f"ID: {rc['id']:<4} | Name: {rc['name']:<28} | Count: {rc['count']:<3} | URL: {rc['url']}")

print("\n=== 2. Testing HTTP status of category URLs ===")
failed_urls = []
for c in clean_cats:
    url = c['url']
    try:
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        if res.status_code != 200:
            print(f"  [ERROR] ID {c['id']} ({c['name']}): HTTP {res.status_code} -> {url}")
            failed_urls.append((c['id'], c['name'], url, res.status_code))
        else:
            print(f"  [OK 200] ID {c['id']:<4} | {c['name']:<25} | Parent: {c['parent']}")
    except Exception as e:
        print(f"  [EXC] ID {c['id']} ({c['name']}): {e}")
        failed_urls.append((c['id'], c['name'], url, str(e)))

print(f"\nVerification Results: {len(clean_cats) - len(failed_urls)} / {len(clean_cats)} URLs OK.")
if failed_urls:
    print(f"Failed URLs ({len(failed_urls)}):", failed_urls)
else:
    print("ALL CATEGORY URLS RETURNED HTTP 200! ZERO BROKEN LINKS!")

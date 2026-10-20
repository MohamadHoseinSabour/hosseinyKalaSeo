import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# 1. Fetch menus
r = requests.get('https://hosseinykala.ir/wp-json/wp/v2/menus', auth=AUTH, headers=headers)
menus = r.json()
print("=== Menus ===")
for m in menus:
    print(f"Menu {m['id']}: {m['name']} (slug: {m['slug']})")

# 2. Fetch menu items
for m in menus:
    mid = m['id']
    r_items = requests.get(f"https://hosseinykala.ir/wp-json/wp/v2/menu-items?menus={mid}&per_page=100", auth=AUTH, headers=headers)
    items = r_items.json()
    print(f"\n=== Menu {mid}: {m['name']} ({len(items)} items) ===")
    items_sorted = sorted(items, key=lambda x: x.get('menu_order', 0))
    for it in items_sorted:
        title = it.get('title', {}).get('rendered', '')
        parent = it.get('parent', 0)
        url = it.get('url', '')
        order = it.get('menu_order', 0)
        print(f"  ID: {it['id']:<5} | Parent: {parent:<5} | Order: {order:<3} | Title: {title:<28} | URL: {url}")

import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/id_mappings.json', 'r', encoding='utf-8') as f:
    id_map = json.load(f)

with open('data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

# Name to slug mapping
name_to_slug = {}
id_to_slug = {}

for pid, info in id_map.items():
    if isinstance(info, dict) and 'slug' in info:
        id_to_slug[str(pid)] = info['slug']
        name_to_slug[info.get('name', '').strip()] = info['slug']

for p in products:
    pid = str(p.get('id', ''))
    slug = p.get('slug', '')
    name = p.get('name', '').strip()
    if pid and slug:
        id_to_slug[pid] = slug
    if name and slug:
        name_to_slug[name] = slug

def get_canonical_product_url(name, fallback_link=""):
    name = name.strip()
    if name in name_to_slug:
        return f"https://hosseinykala.ir/product/{name_to_slug[name]}/"
    if '?p=' in fallback_link:
        pid = fallback_link.split('?p=')[-1].split('&')[0]
        if pid in id_to_slug:
            return f"https://hosseinykala.ir/product/{id_to_slug[pid]}/"
    if '/product/' in fallback_link:
        return fallback_link
    return fallback_link

# Test
print("Resolved Glory Plus:", get_canonical_product_url("یخچال فریزر دوقلو 54 فوت کلور مدل گلوری پلاس", "https://hosseinykala.ir/?p=2972"))
print("Resolved Glory 60:", get_canonical_product_url("یخچال فریزر دوقلو 40 فوت کلور مدل گلوری عرض 60", "https://hosseinykala.ir/?p=2471"))
print("Resolved T7:", get_canonical_product_url("یخچال و فریزر 28 فوت دیپوینت مدل T7 بدون برفک", "https://hosseinykala.ir/?p=2585"))

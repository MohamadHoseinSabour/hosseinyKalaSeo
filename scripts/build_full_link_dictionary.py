import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. Load categories
with open('data/categories.json', encoding='utf-8') as f:
    cats = json.load(f)

replacements = {}

# Categories
for c in cats:
    cid = str(c['id'])
    url = c['url']
    replacements[f"https://hosseinykala.ir/?product_cat={cid}"] = url
    replacements[f"http://hosseinykala.ir/?product_cat={cid}"] = url
    replacements[f"/?product_cat={cid}"] = url

# Fix known category typos:
# ID 94 was typed for کولر آبی (real ID is 95)
air_cooler_url = "https://hosseinykala.ir/product-category/%da%a9%d9%88%d9%84%d8%b1-%d8%a2%d8%a8%db%8c/"
replacements["https://hosseinykala.ir/?product_cat=94"] = air_cooler_url
replacements["/?product_cat=94"] = air_cooler_url

# 2. Load products from id_mappings.json
with open('data/id_mappings.json', encoding='utf-8') as f:
    mappings = json.load(f)

for pid, info in mappings.items():
    slug = info.get('slug')
    ptype = info.get('type')
    if slug and ptype in ('simple', 'variable'):
        prod_canonical = f"https://hosseinykala.ir/product/{slug}/"
        replacements[f"https://hosseinykala.ir/?p={pid}"] = prod_canonical
        replacements[f"http://hosseinykala.ir/?p={pid}"] = prod_canonical

# 3. Post mappings (cluster posts)
post_slugs = {
    3851: "home-appliances-installment-buying-guide",
    3853: "refah-bank-beta-installment-guide",
    3855: "bajet-tejarat-refah-300m-appliances",
    3857: "mellat-bank-200m-appliances-loan-guide",
    3859: "sayadi-cheque-installment-buying-guide",
    3861: "mehr-iran-kalacard-bnpl-appliances-guide"
}

for pid, slug in post_slugs.items():
    post_canonical = f"https://hosseinykala.ir/{slug}/"
    replacements[f"https://hosseinykala.ir/?p={pid}"] = post_canonical
    replacements[f"http://hosseinykala.ir/?p={pid}"] = post_canonical

print(f"Total link replacement rules created: {len(replacements)}")

with open('data/all_link_replacements.json', 'w', encoding='utf-8') as f:
    json.dump(replacements, f, ensure_ascii=False, indent=2)
print("Saved to data/all_link_replacements.json")

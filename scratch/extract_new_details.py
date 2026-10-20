import json, openpyxl, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data/products.json', 'r', encoding='utf-8') as f:
    site_products = json.load(f)

site_dict = {p['id']: p for p in site_products}

new_ids = [
    4302, 4297, 4294, 4292, 4290, 4288, 4286, 4284, 4282, 4280,
    4278, 4276, 4274, 4272, 4270, 4268, 4266, 4264, 4262, 4258,
    4257, 4255, 4253, 4251, 4249, 4245, 4241, 4239, 4237, 4235
]

print(f"Total new IDs to process: {len(new_ids)}")

extracted_new_products = []
for pid in new_ids:
    p = site_dict.get(pid, {})
    name = p.get('name', '')
    slug = p.get('slug', '')
    price = p.get('price', '')
    regular_price = p.get('regular_price', '')
    sale_price = p.get('sale_price', '')
    categories = [c.get('name') for c in p.get('categories', [])]
    short_desc = p.get('short_description', '')
    desc = p.get('description', '')
    
    extracted_new_products.append({
        'id': pid,
        'name': name,
        'slug': slug,
        'price': price,
        'regular_price': regular_price,
        'sale_price': sale_price,
        'categories': categories,
        'short_description': short_desc,
        'description': desc
    })
    print(f"[{pid}] {name} | Cat: {categories} | Price: {price}")

with open('scratch/new_30_products_details.json', 'w', encoding='utf-8') as f:
    json.dump(extracted_new_products, f, ensure_ascii=False, indent=2)

print("\nSaved details to scratch/new_30_products_details.json")

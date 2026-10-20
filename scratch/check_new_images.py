import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data/products.json', 'r', encoding='utf-8') as f:
    site_products = json.load(f)

prods_by_id = {p['id']: p for p in site_products}

new_ids = [
    4302, 4297, 4294, 4292, 4290, 4288, 4286, 4284, 4282, 4280,
    4278, 4276, 4274, 4272, 4270, 4268, 4266, 4264, 4262, 4258,
    4257, 4255, 4253, 4251, 4249, 4245, 4241, 4239, 4237, 4235
]

print("Checking images for the 30 new products:")
for pid in new_ids:
    p = prods_by_id.get(pid)
    if p:
        imgs = [img.get('src') for img in p.get('images', [])]
        print(f"ID {pid}: {p['name'][:35]} -> images count: {len(imgs)} | first: {imgs[0] if imgs else 'None'}")
    else:
        print(f"ID {pid}: Not found in products.json")

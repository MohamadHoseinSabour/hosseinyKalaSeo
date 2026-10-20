import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data/products.json', 'r', encoding='utf-8') as f:
    site_products = json.load(f)

divar_dirs = os.listdir('divar_organized') if os.path.exists('divar_organized') else []

# Extract slugs or keywords from divar folders
divar_slugs = []
for d in divar_dirs:
    # d is like P-01_clever-combi-rosso
    parts = d.split('_', 1)
    if len(parts) > 1:
        divar_slugs.append(parts[1].lower())

print(f"Total divar folders: {len(divar_dirs)}")

# Match site products to divar
matched_in_divar = []
missing_from_divar = []

for p in site_products:
    if p.get('status') != 'publish':
        continue
    pslug = p.get('slug', '').lower()
    pname = p.get('name', '')
    pid = p.get('id')
    
    # Check if slug or name is already in divar
    found = False
    for ds in divar_slugs:
        # direct substring or token overlap
        d_tokens = set(ds.split('-'))
        s_tokens = set(pslug.split('-'))
        common = d_tokens.intersection(s_tokens)
        if len(common) >= 3 or ds in pslug or pslug in ds:
            found = True
            matched_in_divar.append((pid, pname, ds))
            break
            
    if not found:
        missing_from_divar.append(p)

print(f"Matched in Divar: {len(matched_in_divar)}")
print(f"Missing from Divar: {len(missing_from_divar)}")
print("\n=== Missing Products List ===")
for idx, p in enumerate(missing_from_divar, 1):
    price = p.get('price') or p.get('regular_price') or 'بدون قیمت'
    sale = p.get('sale_price')
    print(f"{idx}. ID: {p['id']} | {p['name']} | Price: {price} | Sale: {sale} | Slug: {p['slug']}")

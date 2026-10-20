import json

with open('data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

print(f"Total products in products.json: {len(products)}")

# Known brands
known_brands = [
    'کلور', 'کلوِر', 'ایستکول', 'دیپوینت', 'بست', 'اسنوا', 'دوو', 'هیمالیا', 'الکترواستیل',
    'پاکشوما', 'ریتون', 'آراز', 'رانکو', 'ساپر', 'سران', 'سیماران', 'فریدولین', 'فیلیپس',
    'مونزا', 'هیتاچی', 'پاناسونیک', 'پاندا', 'پاکیزان', 'وگاترونیکس', 'دونالکس', 'گرنویک',
    'وستینگهاوس', 'پارس خزر', 'آلتون', 'لاوان', 'نیاک', 'ویلز', 'کنوود', 'تفال', 'کورکماز',
    'زامروتی', 'وگاتی', 'اریکسون', 'جنرال', 'کاستلو', 'وولگا', 'ژمبو', 'پروکس', 'اوریکس',
    'ونتو', 'سانی', 'هاورسن', 'هاورسون', 'پرومارون', 'پروامگا', 'امگا', 'الکتروسان',
    'تکنوسان', 'نیکسان', 'ریگور', 'هومگلد', 'هانو', 'وست واتر', 'نیکایی', 'افترون',
    'سی سی کا', 'سافت واتر', 'دلمونتی', 'بوتان', 'پلار', 'الکترا', 'اوجنرال', 'گلدن لوکس'
]

no_brand_found = []
has_motafareghe = []

for p in products:
    name = p.get('name', '')
    desc = p.get('description', '')
    short_desc = p.get('short_description', '')
    p_id = p.get('id')
    slug = p.get('slug')
    cats = [c.get('name') if isinstance(c, dict) else str(c) for c in p.get('categories', [])]
    
    # Check if brand in name
    found_brand = None
    for b in known_brands:
        if b.lower() in name.lower():
            found_brand = b
            break
            
    if not found_brand:
        no_brand_found.append({'id': p_id, 'name': name, 'slug': slug, 'cats': cats})
        
    if 'متفرقه' in desc or 'متفرقه' in short_desc or any('متفرقه' in str(c) for c in cats):
        has_motafareghe.append({'id': p_id, 'name': name, 'slug': slug, 'found_brand': found_brand, 'cats': cats})

print(f"\n--- Site products without any recognized brand in title: {len(no_brand_found)} ---")
for p in no_brand_found:
    print(f"ID {p['id']}: {p['name']} | Slug: {p['slug']} | Cats: {p['cats']}")

print(f"\n--- Site products mentioning 'متفرقه' in desc or cats: {len(has_motafareghe)} ---")
for p in has_motafareghe:
    print(f"ID {p['id']}: {p['name']} (Brand detected: {p['found_brand']}) | Slug: {p['slug']}")

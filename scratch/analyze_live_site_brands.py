import json

with open('scratch/live_wp_products.json', 'r', encoding='utf-8') as f:
    products = f.read()
    products = json.loads(products)

with open('data/categories.json', 'r', encoding='utf-8') as f:
    categories = json.load(f)

cat_by_id = {c['id']: c for c in categories}

known_brands = [
    'کلور', 'کلوِر', 'ایستکول', 'دیپوینت', 'بست', 'اسنوا', 'دوو', 'هیمالیا', 'الکترواستیل',
    'پاکشوما', 'ریتون', 'آراز', 'رانکو', 'ساپر', 'سران', 'سیماران', 'فریدولین', 'فیلیپس',
    'مونزا', 'هیتاچی', 'پاناسونیک', 'پاندا', 'پاکیزان', 'وگاترونیکس', 'دونالکس', 'گرنویک',
    'وستینگهاوس', 'پارس خزر', 'آلتون', 'لاوان', 'نیاک', 'ویلز', 'کنوود', 'تفال', 'کورکماز',
    'زامروتی', 'وگاتی', 'اریکسون', 'جنرال', 'کاستلو', 'وولگا', 'ژمبو', 'پروکس', 'اوریکس',
    'ونتو', 'سانی', 'هاورسن', 'هاورسون', 'پرومارون', 'پروامگا', 'امگا', 'الکتروسان',
    'تکنوسان', 'نیکسان', 'ریگور', 'هومگلد', 'هانو', 'وست واتر', 'نیکایی', 'افترون',
    'سی سی کا', 'سافت واتر', 'دلمونتی', 'بوتان', 'پلار', 'الکترا', 'اوجنرال', 'گلدن لوکس',
    'اویژ', 'اویز', 'اویزپلاس', 'آویز', 'آویزپلاس', 'دستی لوکس', 'دستی', 'کنرا', 'KENRA', 'Averson'
]

print(f"Loaded {len(products)} live products.")

has_motafareghe = []
no_brand_in_title = []

for p in products:
    p_id = p.get('id')
    raw_title = p.get('title', {}).get('raw', '') or p.get('title', {}).get('rendered', '')
    slug = p.get('slug', '')
    content_raw = p.get('content', {}).get('raw', '') or p.get('content', {}).get('rendered', '')
    excerpt_raw = p.get('excerpt', {}).get('raw', '') or p.get('excerpt', {}).get('rendered', '')
    cat_ids = p.get('categories', []) or p.get('product_cat', [])
    cat_names = [cat_by_id.get(cid, {}).get('name', str(cid)) for cid in cat_ids]
    
    # Check for motafareghe
    if 'متفرقه' in content_raw or 'متفرقه' in excerpt_raw or 'متفرقه' in raw_title:
        has_motafareghe.append({
            'id': p_id,
            'title': raw_title,
            'slug': slug,
            'categories': cat_names,
            'excerpt_motafareghe': 'متفرقه' in excerpt_raw,
            'content_motafareghe': 'متفرقه' in content_raw
        })
        
    # Check if any known brand in title
    found_brand = None
    for b in known_brands:
        if b.lower() in raw_title.lower():
            found_brand = b
            break
            
    if not found_brand:
        no_brand_in_title.append({
            'id': p_id,
            'title': raw_title,
            'slug': slug,
            'categories': cat_names
        })

print(f"\n================ PRODUCTS WITH 'متفرقه' ON SITE: {len(has_motafareghe)} ================")
for item in has_motafareghe:
    print(f"ID {item['id']}: {item['title']}")
    print(f"   Slug: {item['slug']}")
    print(f"   Categories: {item['categories']}")
    print()

print(f"\n================ PRODUCTS WITHOUT KNOWN BRAND IN TITLE: {len(no_brand_in_title)} ================")
for item in no_brand_in_title:
    print(f"ID {item['id']}: {item['title']}")
    print(f"   Slug: {item['slug']}")
    print(f"   Categories: {item['categories']}")
    print()

import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/live_products_check.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

with open('data/categories.json', 'r', encoding='utf-8') as f:
    cats = json.load(f)

cat_map = {c['id']: c for c in cats}

# Brand categories mapping:
# 153: یخچال فریزر کلور (parent: 92)
# 154: یخچال فریزر دیپوینت (parent: 92)
# 155: یخچال فریزر ایستکول (parent: 92)
# 156: یخچال فریزر الکترواستیل (parent: 92)
# 157: ماشین لباسشویی کلور (parent: 93)
# 158: ماشین لباسشویی دوو (parent: 93)
# 159: ماشین ظرفشویی کلور (parent: 97)
# 160: جاروبرقی بست (parent: 21)
# 161: جاروبرقی پاناسونیک (parent: 21)
# 162: جاروبرقی هیتاچی (parent: 21)
# 163: کولر آبی ریتون (parent: 95)
# 164: تصفیه آب سافت واتر (parent: 96)
# 165: آبمیوه گیری دونالکس (parent: 120)
# 166: اتو بخار دونالکس (parent: 118)
# 167: اسپرسو ساز دونالکس (parent: 119)
# 168: سرخ کن دونالکس (parent: 121)
# 169: گوشت کوب برقی دونالکس (parent: 122)
# 170: مخلوط کن دونالکس (parent: 123)
# 171: ماشین اصلاح سر پرو امگا (parent: 126)
# 174: سشوار پرو امگا (parent: 124)

brand_rules = [
    ('کلور', 92, 153, 'یخچال'),
    ('دیپوینت', 92, 154, 'یخچال'),
    ('ایستکول', 92, 155, 'یخچال'),
    ('الکترواستیل', 92, 156, 'یخچال'),
    ('کلور', 93, 157, 'لباسشویی'),
    ('دوو', 93, 158, 'لباسشویی'),
    ('کلور', 97, 159, 'ظرفشویی'),
    ('بست', 21, 160, 'جاروبرقی'),
    ('پاناسونیک', 21, 161, 'جاروبرقی'),
    ('هیتاچی', 21, 162, 'جاروبرقی'),
    ('ریتون', 95, 163, 'کولر'),
    ('سافت واتر', 96, 164, 'تصفیه'),
    ('دونالکس', 120, 165, 'آبمیوه'),
    ('دونالکس', 118, 166, 'اتو'),
    ('دونالکس', 119, 167, 'اسپرسو'),
    ('دونالکس', 121, 168, 'سرخ'),
    ('دونالکس', 122, 169, 'گوشت'),
    ('دونالکس', 123, 170, 'مخلوط'),
    ('پرو امگا', 126, 171, 'اصلاح'),
    ('پرو امگا', 124, 174, 'سشوار'),
]

updates = {}

for p in products:
    pid = p['id']
    title = p['title']['rendered']
    p_cats = set(p.get('product_cat', []))
    new_cats = set(p_cats)
    
    # 1. Fix misclassified products
    if pid == 2972: # Refrigerator in Vacuum
        new_cats.discard(21)
        new_cats.add(92)
        new_cats.add(153)
    if pid == 3551: # Washing Machine in Vacuum
        new_cats.discard(21)
        new_cats.add(93)
        
    # 2. Check brand rules
    for brand_kw, parent_id, sub_id, prod_kw in brand_rules:
        if brand_kw in title and prod_kw in title:
            new_cats.add(parent_id)
            new_cats.add(sub_id)
            
    if new_cats != p_cats:
        updates[pid] = {
            'title': title,
            'old': sorted(list(p_cats)),
            'new': sorted(list(new_cats)),
            'old_names': [cat_map.get(cid, {}).get('name', str(cid)) for cid in sorted(list(p_cats))],
            'new_names': [cat_map.get(cid, {}).get('name', str(cid)) for cid in sorted(list(new_cats))],
        }

print(f"Total products to update: {len(updates)}\n")
for pid, d in updates.items():
    print(f"Product {pid}: {d['title']}")
    print(f"  Old: {d['old']} -> {d['old_names']}")
    print(f"  New: {d['new']} -> {d['new_names']}\n")

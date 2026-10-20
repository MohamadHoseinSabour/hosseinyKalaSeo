import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/live_products_check.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

with open('data/categories.json', 'r', encoding='utf-8') as f:
    cats = json.load(f)

cat_map = {c['id']: c for c in cats}

print(f"Total products: {len(products)}\n")

# Products in category 21 (جاروبرقی)
print("=== Products in category 21 (جاروبرقی) or subcats (160, 161, 162) ===")
vac_cats = {21, 160, 161, 162}
for p in products:
    p_cats = set(p.get('product_cat', []))
    if p_cats.intersection(vac_cats):
        names = [cat_map.get(cid, {}).get('name', str(cid)) for cid in p_cats]
        print(f"ID: {p['id']:<5} | Title: {p['title']['rendered']} | Cats: {names}")

print("\n=== Checking ALL products for potential category mismatches ===")
mismatches = []
for p in products:
    pid = p['id']
    title = p['title']['rendered']
    p_cats = p.get('product_cat', [])
    cat_names = [cat_map.get(cid, {}).get('name', str(cid)) for cid in p_cats]
    
    # Heuristics based on title
    title_lower = title.lower()
    
    expected_type = None
    if 'یخچال' in title or 'فریزر' in title:
        expected_type = 'یخچال فریزر'
    elif 'لباسشویی' in title or 'پتوشور' in title or 'کهنه‌شور' in title:
        expected_type = 'ماشین لباسشویی'
    elif 'ظرفشویی' in title:
        expected_type = 'ماشین ظرفشویی'
    elif 'جارو' in title:
        expected_type = 'جاروبرقی'
    elif 'کولر' in title:
        if 'گازی' in title or 'اسپلیت' in title:
            expected_type = 'کولر گازی'
        else:
            expected_type = 'کولر آبی'
    elif 'تصفیه' in title:
        expected_type = 'تصفیه کننده آب'
    elif 'تلویزیون' in title or 'پنکه' in title:
        expected_type = 'صوتی، تصویری و گرمایشی'
    elif 'اتو' in title and 'اتومو' not in title:
        expected_type = 'اتو'
    elif 'اتومو' in title or 'اپیلاتور' in title or 'سشوار' in title or 'اصلاح' in title or 'برس حرارتی' in title:
        expected_type = 'زیبایی و سلامت فردی'
    elif 'اسپرسو' in title or 'قهوه' in title:
        expected_type = 'اسپرسو ساز'
    elif 'چای' in title or 'سماور' in title or 'کتری' in title:
        expected_type = 'چای ساز'
    elif 'آبمیوه' in title:
        expected_type = 'آبمیوه گیری'
    elif 'مخلوط' in title:
        expected_type = 'مخلوط کن'
    elif 'سرخ' in title:
        expected_type = 'سرخ کن'
    elif 'گوشت' in title and 'کوب' in title:
        expected_type = 'گوشت کوب برقی'
    elif 'اجاق' in title or 'گاز' in title:
        if 'صفحه' in title:
            expected_type = 'گاز صفحه ای'
        else:
            expected_type = 'اجاق گاز'
    elif any(x in title for x in ['قابلمه', 'تابه', 'سرویس پخت', 'زودپز', 'شیرجوش', 'سرویس گرانیتی']):
        expected_type = 'ظروف و پخت و پز'
    elif any(x in title for x in ['ساندویچ', 'توستر', 'همزن', 'غذاساز']):
        expected_type = 'لوازم برقی و پخت و پز'

    # Check if expected_type matches any of the assigned cat_names or their ancestors
    if expected_type:
        has_match = any(expected_type in cn for cn in cat_names)
        # Check parent match
        if not has_match:
            mismatches.append({
                'id': pid,
                'title': title,
                'current_cats': cat_names,
                'cat_ids': p_cats,
                'expected': expected_type
            })

print(f"\nFound {len(mismatches)} potential mismatches:")
for m in mismatches:
    print(f"ID: {m['id']:<5} | Expected: {m['expected']:<20} | Current: {m['current_cats']} | Title: {m['title']}")

import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_NEW_PRODS = os.path.join(PROJECT_DIR, 'data', 'new_products')

MASTER_PATH = os.path.join(PROJECT_DIR, 'scratch', 'products_44_master_data.json')
with open(MASTER_PATH, 'r', encoding='utf-8') as f:
    products = {p['slug']: p for p in json.load(f)}

SUMMARY_PATH = os.path.join(PROJECT_DIR, 'scratch', 'image_search_summary_pass1.json')
with open(SUMMARY_PATH, 'r', encoding='utf-8') as f:
    results = json.load(f)

exact_matches = []
mismatches = []

for r in results:
    slug = r['slug']
    p = products.get(slug, {})
    brand_fa = p.get('brand_fa', '')
    brand_en = p.get('brand_en', '')
    model = p.get('model', '')
    source_title = r.get('source_title', '')
    
    # Check if brand_fa or brand_en is in source_title
    has_brand = (brand_fa.lower() in source_title.lower()) or (brand_en.lower() in source_title.lower())
    has_model = (model.lower() in source_title.lower()) if len(model) > 2 else True

    item_report = {
        'slug': slug,
        'expected_name': p.get('name'),
        'brand': brand_fa,
        'model': model,
        'source_title': source_title,
        'img_url': r.get('img_url'),
        'status': r.get('status')
    }

    if has_brand:
        exact_matches.append(item_report)
    else:
        mismatches.append(item_report)

print(f"=== نتایج ممیزی تطابق تصاویر (PASS 1) ===")
print(f"✓ تصاویر کاملاً منطبق با برند: {len(exact_matches)}")
print(f"⚠️ تصاویر مغایر / برند نامرتبط: {len(mismatches)}")

print("\n--- لیست تصاویر نامرتبط که باید فوراً اصلاح و از منبع واقعی جایگزین شوند ---")
for i, m in enumerate(mismatches):
    print(f"{i+1:2d}. [{m['brand']}] {m['expected_name']}")
    print(f"    ❌ عنوان عکس پیدا شده: '{m['source_title']}'")
    print(f"    URL: {m['img_url']}\n")

with open(os.path.join(PROJECT_DIR, 'scratch', 'image_audit_mismatches.json'), 'w', encoding='utf-8') as f_out:
    json.dump({
        'exact_matches': exact_matches,
        'mismatches': mismatches
    }, f_out, ensure_ascii=False, indent=2)

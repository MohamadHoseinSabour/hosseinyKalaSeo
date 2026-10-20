import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/catalog_current_rows.json', encoding='utf-8') as f:
    rows = json.load(f)

# Load entities
entities = []
curr = None
for r in rows:
    if not r['is_variation']:
        curr = {
            'sheet': r['sheet'],
            'folder': r['folder'],
            'parent_row': r['row'],
            'name': r['name'],
            'brand': r['brand'],
            'ptype': r['ptype'],
            'status': r['status'],
            'variations': []
        }
        entities.append(curr)
    else:
        if curr:
            curr['variations'].append(r)

# Map of active entities with image (21 entities)
# Note: Par Khazar Row 90 is hold. Row 89 (model 361) has NO image.
active_with_image_keys = {
    ('زیبایی و سلامت فردی', 24), # پرومارون 731
    ('نوشیدنی ساز', 66),         # کنوود HM430
    ('نوشیدنی ساز', 68),         # کورکماز A331
    ('نوشیدنی ساز', 54),         # کتری وولگا F1-64
    ('لوازم برقی و پخت و پز', 58),# فر آلتون 7303
    ('لوازم برقی و پخت و پز', 25),# تابه گرانیتی اویز
    ('لوازم برقی و پخت و پز', 83),# خردکن ویلز
    ('سرمایش و گرمایش', 25),     # پنکه پایه بلند پارس خزر
    ('سرمایش و گرمایش', 24),     # فن هیتر پارس خزر FH-2000P
    ('سرمایش و گرمایش', 29),     # بخاری پلار 3PN-NEW
    ('یخچال و فریزر', 57),       # مینی یخچال فانتزی کلور
    ('یخچال و فریزر', 54),       # کلور روسو هوم بار
    ('یخچال و فریزر', 51),       # کلور روسو آبریزدار
    ('یخچال و فریزر', 22),       # هیمالیا آیس پول 60MW
    ('یخچال و فریزر', 87),       # نیکسان کمبی RF8410
    ('شستشو و نظافت', 67),       # مینی واش فریدولین تک درب SW35
    ('شستشو و نظافت', 88),       # پتوشور پاکیزان
    ('شستشو و نظافت', 25),       # لباسشویی دوقلو پاکشوما
    ('شستشو و نظافت', 86),       # جاروبرقی پاندا 80 لیتر
    ('شستشو و نظافت', 58),       # اتو بخار ساپر 4025
    ('شستشو و نظافت', 59),       # اتو بخار ساپر 4035
}

# Filter exactly the 63 entities
unlisted_active = [e for e in entities if e['status'] == 'در سایت تعریف نشده']
missing_63 = [e for e in unlisted_active if (e['sheet'], e['parent_row']) not in active_with_image_keys]

print(f"Total missing products to create folders for: {len(missing_63)}")

def sanitize(name):
    for c in '<>:"/\\|?*':
        name = name.replace(c, '-')
    return name.strip(' .')

base_dir = 'product_images_2026-10-05'

created_folders = []

for e in missing_63:
    brand = e['brand'].strip()
    pname = e['name'].strip()
    category_folder = e['folder']
    
    # Format folder name
    if brand and (brand.lower() not in pname.lower()) and brand != 'متفرقه':
        folder_title = f"{brand} - {pname}"
    else:
        folder_title = pname
    
    folder_title = sanitize(folder_title)
    
    target_path = os.path.join(base_dir, category_folder, folder_title)
    os.makedirs(target_path, exist_ok=True)
    
    # Create info.txt inside folder
    info_file = os.path.join(target_path, 'مشخصات_محصول.txt')
    
    lines = [
        f"نام محصول: {pname}",
        f"برند: {brand if brand else 'نامشخص'}",
        f"دسته‌بندی در کاتالوگ: {e['sheet']}",
        f"شماره سطر در کاتالوگ: {e['parent_row']}",
        f"نوع محصول: {e['ptype']}",
        f"وضعیت در کاتالوگ: {e['status']}",
    ]
    
    if e['variations']:
        lines.append("\nتنوع‌های این محصول در کاتالوگ:")
        for v in e['variations']:
            lines.append(f"  - سطر {v['row']}: {v['name']} (وضعیت: {v['status']})")
    else:
        lines.append("\nاین محصول تک‌مدل (ساده) است و تنوع ندارد.")
        
    lines.extend([
        "\n" + "="*50,
        "راهنمای استاندارد تصاویر حسینی کالا:",
        "1. عکس محصول بدون هیچ‌گونه واترمارک، لوگوی سایت‌ها (دیجی‌کالا، ترب و...) یا برچسب‌های تبلیغاتی باشد.",
        "2. پس‌زمینه تصویر کاملاً سفید یکدست و استودیویی (#FFFFFF) باشد.",
        "3. ابعاد ترجیحی: حداقل 1000 در 1000 پیکسل (مربعی).",
        "4. تطابق ۱۰۰٪ مدل، رنگ، ویژگی‌ها و دستگیره/درب با مشخصات فوق الزامی است.",
        "="*50
    ])
    
    with open(info_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
        
    created_folders.append({
        'category': category_folder,
        'sheet': e['sheet'],
        'row': e['parent_row'],
        'folder_name': folder_title,
        'path': target_path
    })

print(f"Successfully created {len(created_folders)} product folders!")

from collections import Counter
cat_counts = Counter([cf['sheet'] for cf in created_folders])
print("\nBreakdown by category sheet:")
for sname, cnt in cat_counts.items():
    print(f"  * {sname}: {cnt} پوشه")

with open('scratch/created_product_folders.json', 'w', encoding='utf-8') as f:
    json.dump(created_folders, f, ensure_ascii=False, indent=2)

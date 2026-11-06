import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Load files
with open('data/divar_current_ads.json', 'r', encoding='utf-8') as f:
    divar_ads = json.load(f)

with open('data/catalog_extracted.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

with open('data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

with open('data/categories.json', 'r', encoding='utf-8') as f:
    categories = json.load(f)

print(f"Loaded: {len(divar_ads)} Divar ads, {len(catalog)} catalog items, {len(products)} products, {len(categories)} categories.")

# Analyze current Divar ads:
# Classify each Divar ad
single_model_keywords = ['مدل', '815', 'dn-950', 'dn-475', '950f', '2919', '2835', 't7', 't8', 'max', 'روسو پلاس', 'رسوپلاس', 'گلوری', '101', 'boss']
divar_analysis = []

for ad in divar_ads:
    title = ad['title']
    price = ad['price']
    token = ad['token']
    url = ad['url']
    
    # Identify category & brand
    cat = "سایر"
    brand = "متفرقه"
    is_single = False
    
    # Brand detection
    for b in ['کلور', 'دیپوینت', 'پاکشوما', 'هیمالیا', 'الکترواستیل', 'دونالکس', 'دوو', 'بست', 'ایستکول', 'ریتون', 'یاسان', 'سافت واتر', 'وست واتر', 'هوم گلد', 'پرو امگا', 'پاناسونیک', 'هیتاچی', 'تیوا', 'کسری', 'نیکای', 'یونوا', 'افترون', 'پاکیزان', 'لمروتی']:
        if b in title:
            brand = b
            break
            
    # Category detection
    if 'یخچال' in title:
        cat = 'یخچال و فریزر'
    elif 'لباسشویی' in title or 'پتوشور' in title:
        cat = 'ماشین لباسشویی و پتوشور'
    elif 'ظرفشویی' in title:
        cat = 'ماشین ظرفشویی'
    elif 'کولر' in title:
        cat = 'سرمایش و گرمایش'
    elif 'تصفیه آب' in title:
        cat = 'تصفیه کننده آب'
    elif 'جاروبرقی' in title:
        cat = 'جاروبرقی'
    elif 'آبسردکن' in title:
        cat = 'آبسردکن'
    elif any(k in title for k in ['اتو', 'سرخ‌کن', 'سرخ کن', 'اسپرسوساز', 'صبحانه', 'خردکن']):
        cat = 'لوازم خانگی کوچک و پخت و پز'
    elif 'اصلاح' in title:
        cat = 'زیبایی و سلامت فردی'
        
    # Check if single or grouped
    t_lower = title.lower()
    if any(k in t_lower for k in ['مدل t7', 'مدل روسو', 'مدل dn', 'مدل 815', 'مدل 475', 'مدل t8', 'مدل max', 'مدل boss', 'مدل 2919', 'مدل 2835', '950f', 'مدل 101']):
        ad_type = "مدل اختصاصی (تک مدل)"
    elif 'دوقلو' in title and ('کلور' in title or 'هیمالیا' in title or 'الکترواستیل' in title or 'دیپوینت' in title):
        if any(m in t_lower for m in ['روسو', 'گلوری', '101', 'max']):
            ad_type = "مدل اختصاصی (تک مدل)"
        else:
            ad_type = "دسته‌ای / چند مدلی"
    elif any(k in title for k in ['انواع', '8 و 9', 'سلولزی', 'سافت واتر', 'هوم گلد', 'وست واتر', 'دوقلو پاکشوما']):
        ad_type = "دسته‌ای / چند مدلی"
    else:
        ad_type = "تک محصول / نیمه دسته‌ای"
        
    divar_analysis.append({
        "index": ad['index'],
        "title": title,
        "price": price,
        "token": token,
        "url": url,
        "category": cat,
        "brand": brand,
        "ad_type": ad_type
    })

with open('data/divar_analysis.json', 'w', encoding='utf-8') as f:
    json.dump(divar_analysis, f, ensure_ascii=False, indent=2)

print("Saved divar_analysis.json")
from collections import Counter
print("Ads by Category:", Counter(x['category'] for x in divar_analysis))
print("Ads by Brand:", Counter(x['brand'] for x in divar_analysis).most_common(10))
print("Ads by Type:", Counter(x['ad_type'] for x in divar_analysis))

import json
import urllib.parse
import csv
import sys
import requests

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

raw_urls = [
    'https://hosseinykala.ir/product-category/اصلاح-موی-صورت/',
    'https://hosseinykala.ir/product-category/اصلاح-موی-صورت/?stock_status=instock,onsale',
    'https://hosseinykala.ir/product-category/اصلاح-موی-صورت/?stock_status=instock',
    'https://hosseinykala.ir/product-category/اصلاح-موی-صورت/?stock_status=onsale',
    'https://hosseinykala.ir/?product_cat=157',
    'https://hosseinykala.ir/?product_cat=154',
    'https://hosseinykala.ir/?product_cat=161',
    'https://hosseinykala.ir/?product_cat=162',
    'https://hosseinykala.ir/?product_cat=160',
    'https://hosseinykala.ir/?product_cat=164',
    'https://hosseinykala.ir/?product_cat=159',
    'https://hosseinykala.ir/"https:////hosseinykala.ir//product//کولر-آبی-سلولزی-16000-ریتون-مدل-کولر-پرتابل///"',
    'https://hosseinykala.ir/"https:////hosseinykala.ir//product//یخچال-و-فریزر-27-فوت-کلور-مدل-كمبي-فريزر-پ///"',
    'https://hosseinykala.ir/"https:////hosseinykala.ir//product//ماشین-لباسشویی-8-کیلوگرم-اتوماتیک-کلور///"',
    'https://hosseinykala.ir/wp-content/uploads/*',
    'https://hosseinykala.ir/?product_cat=158',
    'https://hosseinykala.ir/?product_cat=155',
    'https://hosseinykala.ir/?product_cat=156',
    'https://hosseinykala.ir/?product_cat=153',
    'https://hosseinykala.ir/?product_cat=163',
    'https://hosseinykala.ir/"https:////hosseinykala.ir//product//یخچال-و-فریزر-28-فوت-دیپوینت-مدل-t7،-بدون-بر///"',
    'https://hosseinykala.ir/"https:////hosseinykala.ir//product//کولر-آبی-سلولزی-7000-ریتون-مدل-vento-7000///"',
    'https://hosseinykala.ir/"https:////hosseinykala.ir/"',
    'https://hosseinykala.ir/"https:////hosseinykala.ir//product//یخچال-فریزر-دوقلو-40-فوت-کلور-مدل-رسوپلا///"',
    'https://hosseinykala.ir/"https:////hosseinykala.ir//product//یخچال-فریزر-دوقلو-44-فوت-کلور-مدل-54-فوت-glory-plus-lm70///"',
    'https://hosseinykala.ir/"https:////hosseinykala.ir//product//یخچال-و-فریزر-27-فوت-کلور-مدل-كمبي-هوم-بار///"',
    'https://hosseinykala.ir/"https:////hosseinykala.ir//product//یخچال-فریزر-دوقلو-40-فوت-کلور-مدل-گلوری-ع///"',
    'https://hosseinykala.ir/"https:////hosseinykala.ir//shop///"',
    'https://hosseinykala.ir/"https:////hosseinykala.ir//علاقه-مندی-ها///"',
    'https://hosseinykala.ir/"https:////hosseinykala.ir//product//یخچال-فریزر-دوقلو-40-فوت-کلور-مدل-گلوری-پ///"',
    'https://hosseinykala.ir/"https:////hosseinykala.ir//product//یخچال-10-فوت-کلور-مدل-mini-refrigerator///"',
    'https://hosseinykala.ir/"https:////hosseinykala.ir//product//یخچال-و-فریزر-27-فوت-کلوِر-مدل-frnt101///"',
    'https://hosseinykala.ir/?product_cat=93',
    'https://hosseinykala.ir/?product_cat=21',
    'https://hosseinykala.ir/?product_cat=97',
    'https://hosseinykala.ir/?product_cat=96',
    'https://hosseinykala.ir/?product_cat=95',
    'https://hosseinykala.ir/wp-*.php',
    'https://hosseinykala.ir/?product_cat=92',
    'https://hosseinykala.ir/*',
    'https://hosseinykala.ir/"https:////hosseinykala.ir//product//جاروبرقی-سطلی-هیتاچی-مدل-cv-950f///"',
    'https://hosseinykala.ir/"https:////hosseinykala.ir//product//ماشین-لباسشویی-9-کیلوگرم-اتوماتیک-کلور///"',
    'https://hosseinykala.ir/"https:////hosseinykala.ir//product//یخچال-و-فریزر-دوقلو-36-فوت-کلوِر-مدل-rnt101-fnt101///"',
    'https://hosseinykala.ir/"https:////hosseinykala.ir//product//یخچال-فریزر-30-فوت-دیپوینت-مدل-boss-pro///"',
    'https://hosseinykala.ir/"https:////hosseinykala.ir//product//ماشین-لباسشویی-هوشمند-9-کیلوگرم-اتومات///"',
    'https://hosseinykala.ir/wp-content/*'
]

print(f"Total raw URLs loaded: {len(raw_urls)}")

# Category Mapping from categories.json
CAT_MAP = {
    '157': 'https://hosseinykala.ir/product-category/washing-cleaning/%d9%85%d8%a7%d8%b4%db%8c%d9%86-%d9%84%d8%a8%d8%a7%d8%b3%d8%b4%d9%88%db%8c%db%8c/clover-washing-machines/',
    '154': 'https://hosseinykala.ir/product-category/%db%8c%d8%ae%da%86%d8%a7%d9%84-%d9%81%d8%b1%db%8c%d8%b2%d8%b1/depoint-refrigerators/',
    '161': 'https://hosseinykala.ir/product-category/washing-cleaning/%d8%ac%d8%a7%d8%b1%d9%88%d8%a8%d8%b1%d9%82%db%8c/panasonic-vacuum-cleaners/',
    '162': 'https://hosseinykala.ir/product-category/washing-cleaning/%d8%ac%d8%a7%d8%b1%d9%88%d8%a8%d8%b1%d9%82%db%8c/hitachi-vacuum-cleaners/',
    '160': 'https://hosseinykala.ir/product-category/washing-cleaning/%d8%ac%d8%a7%d8%b1%d9%88%d8%a8%d8%b1%d9%82%db%8c/bost-vacuum-cleaners/',
    '164': 'https://hosseinykala.ir/product-category/%d8%aa%d8%b5%d9%81%db%8c%d9%87-%da%a9%d9%86%d9%86%d8%af%d9%87-%d8%a2%d8%a8/softwater-purifiers/',
    '159': 'https://hosseinykala.ir/product-category/washing-cleaning/%d9%85%d8%a7%d8%b4%db%8c%d9%86-%d8%b8%d8%b1%d9%81%d8%b4%d9%88%db%8c%db%8c/clover-dishwashers/',
    '158': 'https://hosseinykala.ir/product-category/washing-cleaning/%d9%85%d8%a7%d8%b4%db%8c%d9%86-%d9%84%d8%a8%d8%a7%d8%b3%d8%b4%d9%88%db%8c%db%8c/daewoo-washing-machines/',
    '155': 'https://hosseinykala.ir/product-category/%db%8c%d8%ae%da%86%d8%a7%d9%84-%d9%81%d8%b1%db%8c%d8%b2%d8%b1/eastcool-refrigerators/',
    '156': 'https://hosseinykala.ir/product-category/%db%8c%d8%ae%da%86%d8%a7%d9%84-%d9%81%d8%b1%db%8c%d8%b2%d8%b1/electrosteel-refrigerators/',
    '153': 'https://hosseinykala.ir/product-category/%db%8c%d8%ae%da%86%d8%a7%d9%84-%d9%81%d8%b1%db%8c%d8%b2%d8%b1/clover-refrigerators/',
    '163': 'https://hosseinykala.ir/product-category/heating-cooling/%da%a9%d9%88%d9%84%d8%b1-%d8%a2%d8%a8%db%8c/rayton-water-coolers/',
    '93': 'https://hosseinykala.ir/product-category/washing-cleaning/%d9%85%d8%a7%d8%b4%db%8c%d9%86-%d9%84%d8%a8%d8%a7%d8%b3%d8%b4%d9%88%db%8c%db%8c/',
    '21': 'https://hosseinykala.ir/product-category/washing-cleaning/%d8%ac%d8%a7%d8%b1%d9%88%d8%a8%d8%b1%d9%82%db%8c/',
    '97': 'https://hosseinykala.ir/product-category/washing-cleaning/%d9%85%d8%a7%d8%b4%db%8c%d9%86-%d8%b8%d8%b1%d9%81%d8%b4%d9%88%db%8c%db%8c/',
    '96': 'https://hosseinykala.ir/product-category/%d8%aa%d8%b5%d9%81%db%8c%d9%87-%da%a9%d9%86%d9%86%d8%af%d9%87-%d8%a2%d8%a8/',
    '95': 'https://hosseinykala.ir/product-category/heating-cooling/%da%a9%d9%88%d9%84%d8%b1-%d8%a2%d8%a8%db%8c/',
    '92': 'https://hosseinykala.ir/product-category/%db%8c%d8%ae%da%86%d8%a7%d9%84-%d9%81%d8%b1%db%8c%d8%b2%d8%b1/'
}

# Explicit mapping table for all 46
mappings = []

for u in raw_urls:
    target = None
    note = ""
    
    # 1. Category query parameters
    if '?product_cat=' in u:
        cid = u.split('?product_cat=')[1].strip()
        target = CAT_MAP.get(cid)
        note = f"Category ID {cid} query param"
    
    # 2. اصلاح موی صورت
    elif 'اصلاح-موی-صورت' in u:
        target = 'https://hosseinykala.ir/product-category/%d8%a7%d8%b5%d9%84%d8%a7%d8%ad-%d9%88-%d8%b2%db%8c%d8%a8%d8%a7%db%8c%db%8c/%d8%a7%d8%b5%d9%84%d8%a7%d8%ad-%d9%85%d9%88%db%8c-%d8%b3%d8%b1/'
        note = "Deleted subcategory -> Main hair clipper category"
        
    # 3. Double-quote / Malformed URLs
    elif 'کولر-آبی-سلولزی-16000-ریتون' in u:
        target = 'https://hosseinykala.ir/product/reyton-vento-16000-portable-air-cooler/'
        note = "Product: Rayton 16000 air cooler"
    elif 'یخچال-و-فریزر-27-فوت-کلور-مدل-كمبي-فريزر-پ' in u:
        target = 'https://hosseinykala.ir/product/clover-frnt-70-glory-plus/'
        note = "Product: Clover FRNT-70 Glory Plus"
    elif 'ماشین-لباسشویی-8-کیلوگرم-اتوماتیک-کلور' in u:
        target = 'https://hosseinykala.ir/product/clover-bmw-t3-washing-machine-8kg/'
        note = "Product: Clover BMW T3 8kg"
    elif 'یخچال-و-فریزر-28-فوت-دیپوینت-مدل-t7' in u:
        target = 'https://hosseinykala.ir/product/depoint-t7-refrigerator-28ft/'
        note = "Product: Depoint T7 28ft"
    elif 'کولر-آبی-سلولزی-7000-ریتون' in u:
        target = 'https://hosseinykala.ir/product/reyton-vento-7000-air-cooler/'
        note = "Product: Rayton Vento 7000"
    elif 'یخچال-فریزر-دوقلو-40-فوت-کلور-مدل-رسوپلا' in u:
        target = 'https://hosseinykala.ir/product/clover-rosso-plus-w60-twin-refrigerator-40ft/'
        note = "Product: Clover Rosso Plus 40ft"
    elif 'یخچال-فریزر-دوقلو-44-فوت-کلور-مدل-54-فوت-glory-plus-lm70' in u:
        target = 'https://hosseinykala.ir/product/clover-glory-plus-lm70-twin-refrigerator/'
        note = "Product: Clover Glory Plus LM70 44ft"
    elif 'یخچال-و-فریزر-27-فوت-کلور-مدل-كمبي-هوم-بار' in u:
        target = 'https://hosseinykala.ir/product/clover-rosso-homebar-refrigerator-27ft/'
        note = "Product: Clover Rosso Homebar 27ft"
    elif 'یخچال-فریزر-دوقلو-40-فوت-کلور-مدل-گلوری-ع' in u:
        target = 'https://hosseinykala.ir/product/clover-glory-w60-twin-refrigerator-40ft/'
        note = "Product: Clover Glory W60 40ft"
    elif 'یخچال-فریزر-دوقلو-40-فوت-کلور-مدل-گلوری-پ' in u:
        target = 'https://hosseinykala.ir/product/clover-glory-plus-54ft-twin-refrigerator/'
        note = "Product: Clover Glory Plus 54ft"
    elif 'یخچال-10-فوت-کلور-مدل-mini-refrigerator' in u:
        target = 'https://hosseinykala.ir/product/clover-mini-refrigerator-10ft/'
        note = "Product: Clover Mini Refrigerator 10ft"
    elif 'یخچال-و-فریزر-27-فوت-کلوِر-مدل-frnt101' in u:
        target = 'https://hosseinykala.ir/product/clover-frnt101-refrigerator-27ft/'
        note = "Product: Clover FRNT101 27ft"
    elif 'جاروبرقی-سطلی-هیتاچی-مدل-cv-950f' in u:
        target = 'https://hosseinykala.ir/product/hitachi-cv-950f-vacuum-cleaner/'
        note = "Product: Hitachi CV-950F"
    elif 'ماشین-لباسشویی-9-کیلوگرم-اتوماتیک-کلور' in u:
        target = 'https://hosseinykala.ir/product/clover-bmw-t2-washing-machine-9kg/'
        note = "Product: Clover BMW T2 9kg"
    elif 'یخچال-و-فریزر-دوقلو-36-فوت-کلوِر-مدل-rnt101-fnt101' in u:
        target = 'https://hosseinykala.ir/product/clover-rnt101-fnt101-twin-refrigerator-36ft/'
        note = "Product: Clover RNT101-FNT101 36ft"
    elif 'یخچال-فریزر-30-فوت-دیپوینت-مدل-boss-pro' in u:
        target = 'https://hosseinykala.ir/product/depoint-boss-pro-refrigerator-30ft/'
        note = "Product: Depoint Boss Pro 30ft"
    elif 'ماشین-لباسشویی-هوشمند-9-کیلوگرم-اتومات' in u:
        target = 'https://hosseinykala.ir/product/daewoo-lm-9170-washing-machine-9kg/'
        note = "Product: Daewoo LM-9170 9kg"
    elif 'shop' in u:
        target = 'https://hosseinykala.ir/shop/'
        note = "Shop page"
    elif 'علاقه-مندی-ها' in u:
        target = 'https://hosseinykala.ir/'
        note = "Wishlist relative link -> Homepage"
    elif u == 'https://hosseinykala.ir/"https:////hosseinykala.ir/"':
        target = 'https://hosseinykala.ir/'
        note = "Malformed homepage link -> Homepage"
        
    # 4. Wildcards / System
    elif any(k in u for k in ['wp-content/uploads/*', 'wp-*.php', 'wp-content/*', 'https://hosseinykala.ir/*']):
        target = 'https://hosseinykala.ir/'
        note = "Wildcard crawler artifact -> Homepage"
    else:
        target = 'https://hosseinykala.ir/'
        note = "Fallback -> Homepage"

    mappings.append({
        'source_url': u,
        'target_url': target,
        'note': note
    })

print(f"Total mapped: {len(mappings)}")
for idx, m in enumerate(mappings, 1):
    print(f"{idx:02d}. {m['source_url'][:40]} -> {m['target_url'][:45]} ({m['note']})")

with open('data/404_redirect_mappings.json', 'w', encoding='utf-8') as f:
    json.dump(mappings, f, ensure_ascii=False, indent=2)

print("\nSaved to data/404_redirect_mappings.json successfully!")

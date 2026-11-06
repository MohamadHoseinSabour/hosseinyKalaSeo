import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_NEW_PRODS = os.path.join(PROJECT_DIR, 'data', 'new_products')

# Map each slug to exact WC category IDs and canonical category info
CATEGORY_MAP = {
    # Donalex
    'donalex-dn-150-salad-maker-white': {'cat_ids': [216], 'cat_name': 'لوازم برقی و پخت و پز', 'cat_url': 'https://hosseinykala.ir/product-category/%d9%84%d9%88%d8%a7%d8%b2%d9%85-%d8%a8%d8%b1%d9%82%db%8c-%d8%a2%d8%b4%d9%be%d8%b2%d8%ae%d8%a7%d9%86%d9%87/'},
    'donalex-dn-150-salad-maker-black': {'cat_ids': [216], 'cat_name': 'لوازم برقی و پخت و پز', 'cat_url': 'https://hosseinykala.ir/product-category/%d9%84%d9%88%d8%a7%d8%b2%d9%85-%d8%a8%d8%b1%d9%82%db%8c-%d8%a2%d8%b4%d9%be%d8%b2%d8%ae%d8%a7%d9%86%d9%87/'},
    'donalex-dn-940-sandwich-maker-black': {'cat_ids': [216], 'cat_name': 'لوازم برقی و پخت و پز', 'cat_url': 'https://hosseinykala.ir/product-category/%d9%84%d9%88%d8%a7%d8%b2%d9%85-%d8%a8%d8%b1%d9%82%db%8c-%d8%a2%d8%b4%d9%be%d8%b2%d8%ae%d8%a7%d9%86%d9%87/'},
    'donalex-dn-965-air-fryer-6l': {'cat_ids': [121, 168, 216], 'cat_name': 'سرخ کن دونالکس', 'cat_url': 'https://hosseinykala.ir/product-category/%d9%84%d9%88%d8%a7%d8%b2%d9%85-%d8%a8%d8%b1%d9%82%db%8c-%d8%a2%d8%b4%d9%be%d8%b2%d8%ae%d8%a7%d9%86%d9%87/donallex-air-fryers/'},
    'donalex-dn-955-air-fryer-8l': {'cat_ids': [121, 168, 216], 'cat_name': 'سرخ کن دونالکس', 'cat_url': 'https://hosseinykala.ir/product-category/%d9%84%d9%88%d8%a7%d8%b2%d9%85-%d8%a8%d8%b1%d9%82%db%8c-%d8%a2%d8%b4%d9%be%d8%b2%d8%ae%d8%a7%d9%86%d9%87/donallex-air-fryers/'},

    # Choppers & Meat Grinders
    'willz-heavy-duty-meat-grinder': {'cat_ids': [216], 'cat_name': 'لوازم برقی و پخت و پز', 'cat_url': 'https://hosseinykala.ir/product-category/%d9%84%d9%88%d8%a7%d8%b2%d9%85-%d8%a8%d8%b1%d9%82%db%8c-%d8%a2%d8%b4%d9%be%d8%b2%d8%ae%d8%a7%d9%86%d9%87/'},
    'bosch-electric-bowl-chopper': {'cat_ids': [216], 'cat_name': 'لوازم برقی و پخت و پز', 'cat_url': 'https://hosseinykala.ir/product-category/%d9%84%d9%88%d8%a7%d8%b2%d9%85-%d8%a8%d8%b1%d9%82%db%8c-%d8%a2%d8%b4%d9%be%d8%b2%d8%ae%d8%a7%d9%86%d9%87/'},
    'bellanzo-1136-electric-chopper': {'cat_ids': [216], 'cat_name': 'لوازم برقی و پخت و پز', 'cat_url': 'https://hosseinykala.ir/product-category/%d9%84%d9%88%d8%a7%d8%b2%d9%85-%d8%a8%d8%b1%d9%82%db%8c-%d8%a2%d8%b4%d9%be%d8%b2%d8%ae%d8%a7%d9%86%d9%87/'},

    # Toasters & Cooking
    'edmilson-ot-820-toaster-oven': {'cat_ids': [216], 'cat_name': 'لوازم برقی و پخت و پز', 'cat_url': 'https://hosseinykala.ir/product-category/%d9%84%d9%88%d8%a7%d8%b2%d9%85-%d8%a8%d8%b1%d9%82%db%8c-%d8%a2%d8%b4%d9%be%d8%b2%d8%ae%d8%a7%d9%86%d9%87/'},
    'edmilson-ot-827-solar-toaster-oven': {'cat_ids': [216], 'cat_name': 'لوازم برقی و پخت و پز', 'cat_url': 'https://hosseinykala.ir/product-category/%d9%84%d9%88%d8%a7%d8%b2%d9%85-%d8%a8%d8%b1%d9%82%db%8c-%d8%a2%d8%b4%d9%be%d8%b2%d8%ae%d8%a7%d9%86%d9%87/'},
    'kahler-kh-5512-multi-cooker-black': {'cat_ids': [216], 'cat_name': 'لوازم برقی و پخت و پز', 'cat_url': 'https://hosseinykala.ir/product-category/%d9%84%d9%88%d8%a7%d8%b2%d9%85-%d8%a8%d8%b1%d9%82%db%8c-%d8%a2%d8%b4%d9%be%d8%b2%d8%ae%d8%a7%d9%86%d9%87/'},
    'kahler-kh-134-w-stand-mixer-white': {'cat_ids': [216], 'cat_name': 'لوازم برقی و پخت و پز', 'cat_url': 'https://hosseinykala.ir/product-category/%d9%84%d9%88%d8%a7%d8%b2%d9%85-%d8%a8%d8%b1%d9%82%db%8c-%d8%a2%d8%b4%d9%be%d8%b2%d8%ae%d8%a7%d9%86%d9%87/'},
    'oryx-rotating-bowl-stand-mixer': {'cat_ids': [216], 'cat_name': 'لوازم برقی و پخت و پز', 'cat_url': 'https://hosseinykala.ir/product-category/%d9%84%d9%88%d8%a7%d8%b2%d9%85-%d8%a8%d8%b1%d9%82%db%8c-%d8%a2%d8%b4%d9%be%d8%b2%d8%ae%d8%a7%d9%86%d9%87/'},

    # Air fryers
    'satia-st-9015-digital-air-fryer': {'cat_ids': [121, 216], 'cat_name': 'سرخ کن', 'cat_url': 'https://hosseinykala.ir/product-category/%d9%84%d9%88%d8%a7%d8%b2%d9%85-%d8%a8%d8%b1%d9%82%db%8c-%d8%a2%d8%b4%d9%be%d8%b2%d8%ae%d8%a7%d9%86%d9%87/%d8%b3%d8%b1%d8%ae-%da%a9%d9%86/'},
    'satia-st-9025-digital-air-fryer': {'cat_ids': [121, 216], 'cat_name': 'سرخ کن', 'cat_url': 'https://hosseinykala.ir/product-category/%d9%84%d9%88%d8%a7%d8%b2%d9%85-%d8%a8%d8%b1%d9%82%db%8c-%d8%a2%d8%b4%d9%be%d8%b2%d8%ae%d8%a7%d9%86%d9%87/%d8%b3%d8%b1%d8%ae-%da%a9%d9%86/'},
    'tefal-easy-fry-healthy-air-fryer': {'cat_ids': [121, 216], 'cat_name': 'سرخ کن', 'cat_url': 'https://hosseinykala.ir/product-category/%d9%84%d9%88%d8%a7%d8%b2%d9%85-%d8%a8%d8%b1%d9%82%db%8c-%d8%a2%d8%b4%d9%be%d8%b2%d8%ae%d8%a7%d9%86%d9%87/%d8%b3%d8%b1%d8%ae-%da%a9%d9%86/'},

    # Water heaters & Climate
    'pars-green-120l-electric-water-heater': {'cat_ids': [241], 'cat_name': 'سرمایش و گرمایش', 'cat_url': 'https://hosseinykala.ir/product-category/heating-cooling/'},
    'pars-green-160l-electric-water-heater': {'cat_ids': [241], 'cat_name': 'سرمایش و گرمایش', 'cat_url': 'https://hosseinykala.ir/product-category/heating-cooling/'},
    'pars-green-30-gallon-gas-water-heater': {'cat_ids': [241], 'cat_name': 'سرمایش و گرمایش', 'cat_url': 'https://hosseinykala.ir/product-category/heating-cooling/'},
    'pars-green-40-gallon-gas-water-heater': {'cat_ids': [241], 'cat_name': 'سرمایش و گرمایش', 'cat_url': 'https://hosseinykala.ir/product-category/heating-cooling/'},
    'pars-green-50-gallon-gas-water-heater': {'cat_ids': [241], 'cat_name': 'سرمایش و گرمایش', 'cat_url': 'https://hosseinykala.ir/product-category/heating-cooling/'},
    'pars-green-60-gallon-gas-water-heater': {'cat_ids': [241], 'cat_name': 'سرمایش و گرمایش', 'cat_url': 'https://hosseinykala.ir/product-category/heating-cooling/'},
    'green-20l-instant-electric-water-heater': {'cat_ids': [241], 'cat_name': 'سرمایش و گرمایش', 'cat_url': 'https://hosseinykala.ir/product-category/heating-cooling/'},
    'green-30-gallon-dual-fuel-water-heater': {'cat_ids': [241], 'cat_name': 'سرمایش و گرمایش', 'cat_url': 'https://hosseinykala.ir/product-category/heating-cooling/'},
    'green-60-gallon-dual-fuel-water-heater': {'cat_ids': [241], 'cat_name': 'سرمایش و گرمایش', 'cat_url': 'https://hosseinykala.ir/product-category/heating-cooling/'},
    'green-70l-electric-wall-water-heater': {'cat_ids': [241], 'cat_name': 'سرمایش و گرمایش', 'cat_url': 'https://hosseinykala.ir/product-category/heating-cooling/'},
    'green-gas-heater-with-fan': {'cat_ids': [241, 214], 'cat_name': 'پنکه و گرمایشی', 'cat_url': 'https://hosseinykala.ir/product-category/heating-cooling/%d8%b5%d9%88%d8%aa%db%8c%d8%8c-%d8%aa%d8%b5%d9%88%db%8c%d8%b1%db%8c-%d9%88-%da%af%d8%b1%d9%85%d8%a7%db%8c%d8%b4%db%8c/'},

    # Fans
    'satia-1215-stand-fan': {'cat_ids': [241, 214], 'cat_name': 'پنکه و گرمایشی', 'cat_url': 'https://hosseinykala.ir/product-category/heating-cooling/%d8%b5%d9%88%d8%aa%db%8c%d8%8c-%d8%aa%d8%b5%d9%88%db%8c%d8%b1%db%8c-%d9%88-%da%af%d8%b1%d9%85%d8%a7%db%8c%d8%b4%db%8c/'},
    'sayna-kalia-stand-fan': {'cat_ids': [241, 214], 'cat_name': 'پنکه و گرمایشی', 'cat_url': 'https://hosseinykala.ir/product-category/heating-cooling/%d8%b5%d9%88%d8%aa%db%8c%d8%8c-%d8%aa%d8%b5%d9%88%db%8c%d8%b1%db%8c-%d9%88-%da%af%d8%b1%d9%85%d8%a7%db%8c%d8%b4%db%8c/'},

    # Irons
    'kahler-kh-812-steam-iron-white': {'cat_ids': [118, 239], 'cat_name': 'اتو', 'cat_url': 'https://hosseinykala.ir/product-category/washing-cleaning/%d8%a7%d8%aa%d9%88/'},
    'kahler-kh-813-steam-iron-black-silver': {'cat_ids': [118, 239], 'cat_name': 'اتو', 'cat_url': 'https://hosseinykala.ir/product-category/washing-cleaning/%d8%a7%d8%aa%d9%88/'},
    'kahler-kh-814-steam-iron-black-rosegold': {'cat_ids': [118, 239], 'cat_name': 'اتو', 'cat_url': 'https://hosseinykala.ir/product-category/washing-cleaning/%d8%a7%d8%aa%d9%88/'},
    'ebkazo-2139-garment-steamer': {'cat_ids': [118, 239], 'cat_name': 'اتو', 'cat_url': 'https://hosseinykala.ir/product-category/washing-cleaning/%d8%a7%d8%aa%d9%88/'},

    # Vacuums
    'tulips-vc-625-vacuum-cleaner-black': {'cat_ids': [21, 239], 'cat_name': 'جاروبرقی', 'cat_url': 'https://hosseinykala.ir/product-category/washing-cleaning/%d8%ac%d8%a7%d8%b1%d9%88%d8%a8%d8%b1%d9%82%db%8c/'},
    'edmilson-811-cordless-vacuum-cleaner-black': {'cat_ids': [21, 239], 'cat_name': 'جاروبرقی', 'cat_url': 'https://hosseinykala.ir/product-category/washing-cleaning/%d8%ac%d8%a7%d8%b1%d9%88%d8%a8%d8%b1%d9%82%db%8c/'},

    # Beverage
    'tefal-2-2l-stainless-steel-electric-kettle': {'cat_ids': [211, 240], 'cat_name': 'چای ساز', 'cat_url': 'https://hosseinykala.ir/product-category/drink-makers/%da%86%d8%a7%db%8c-%d8%b3%d8%a7%d8%b2/'},
    'monaco-20-bar-espresso-coffee-machine': {'cat_ids': [119, 240], 'cat_name': 'اسپرسو ساز', 'cat_url': 'https://hosseinykala.ir/product-category/drink-makers/%d8%a7%d8%b3%d9%be%d8%b1%d8%b3%d9%88-%d8%b3%d8%a7%d8%b2/'},
    'tulips-cg-473-coffee-and-spice-grinder': {'cat_ids': [240], 'cat_name': 'نوشیدنی ساز', 'cat_url': 'https://hosseinykala.ir/product-category/drink-makers/'},

    # Water Purifiers & Pumps
    'aftron-6-stage-ro-water-purifier': {'cat_ids': [96], 'cat_name': 'تصفیه کننده آب', 'cat_url': 'https://hosseinykala.ir/product-category/%d8%aa%d8%b5%d9%81%db%8c%d9%87-%da%a9%d9%86%d9%86%d8%af%d9%87-%d8%a2%d8%a8/'},
    'shimge-1hp-cpm158-water-pump': {'cat_ids': [241], 'cat_name': 'سرمایش و گرمایش', 'cat_url': 'https://hosseinykala.ir/product-category/heating-cooling/'},
    'vatek-1hp-jet-water-pump': {'cat_ids': [241], 'cat_name': 'سرمایش و گرمایش', 'cat_url': 'https://hosseinykala.ir/product-category/heating-cooling/'},

    # Beauty & Personal Health
    'mixi-digital-body-scale-tempered-glass': {'cat_ids': [212], 'cat_name': 'زیبایی و سلامت فردی', 'cat_url': 'https://hosseinykala.ir/product-category/%d8%a7%d8%b5%d9%84%d8%a7%d8%ad-%d9%88-%d8%b2%db%8c%d8%a8%d8%a7%db%8c%db%8c/'},
    'atman-powerful-538-professional-hair-dryer': {'cat_ids': [124, 212], 'cat_name': 'سشوار', 'cat_url': 'https://hosseinykala.ir/product-category/%d8%a7%d8%b5%d9%84%d8%a7%d8%ad-%d9%88-%d8%b2%db%8c%d8%a8%d8%a7%db%8c%db%8c/%d8%b3%d8%b4%d9%88%d8%a7%d8%b1/'},
    'vincent-hc3321-cordless-hair-clipper': {'cat_ids': [126, 212], 'cat_name': 'اصلاح موی سر و صورت', 'cat_url': 'https://hosseinykala.ir/product-category/%d8%a7%d8%b5%d9%84%d8%a7%d8%ad-%d9%88-%d8%b2%db%8c%d8%a8%d8%a7%db%8c%db%8c/%d8%a7%d8%b5%d9%84%d8%a7%d8%ad-%d9%85%d9%88%db%8c-%d8%b3%d8%b1/'}
}

updated_count = 0
for folder in sorted(os.listdir(DATA_NEW_PRODS)):
    info_path = os.path.join(DATA_NEW_PRODS, folder, 'info.json')
    if os.path.exists(info_path):
        with open(info_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        mapping = CATEGORY_MAP.get(folder)
        if mapping:
            data['wc_category_ids'] = mapping['cat_ids']
            data['wc_category_name'] = mapping['cat_name']
            data['wc_canonical_url'] = mapping['cat_url']
            
            with open(info_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            updated_count += 1

print(f"✓ {updated_count} از 44 محصول با دسته‌بندی‌های رسمی و لینک کاننیکال همگام شدند.")

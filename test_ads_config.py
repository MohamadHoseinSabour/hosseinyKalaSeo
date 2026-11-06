import json
import os
import re
import urllib.request
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Load products and catalog
with open('data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

with open('data/catalog_extracted.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

# Helper for slug and image lookup
prod_lookup = {}
for p in products:
    name_clean = p['name'].strip()
    prod_lookup[name_clean] = p
    # also by slug
    prod_lookup[p['slug']] = p

# Let's define the 20 ads with their concise Divar title and filter criteria
ads_config = [
    {
        "id": "01_refrig_clever_twin",
        "folder": "01_یخچال_دوقلو_کلور",
        "title": "یخچال فریزر دوقلو کلور در اهواز - اقساطی",
        "divar_cat": "وسایل برقی > یخچال و فریزر",
        "cat_link": "https://hosseinykala.ir/product-category/refrigerator-freezer/clever-refrigerator/",
        "filter": lambda p: 'یخچال' in p['name'] and 'کلور' in p['name'] and any(k in p['name'] for k in ['دوقلو', 'روسو پلاس', 'رسوپلاس', 'گلوری', '101', 'اکونومی']) and not any(k in p['name'] for k in ['کمبی', '10 فوت', 'مینی'])
    },
    {
        "id": "02_refrig_clever_combi",
        "folder": "02_یخچال_کمبی_کلور",
        "title": "یخچال فریزر کمبی کلور در اهواز - اقساط",
        "divar_cat": "وسایل برقی > یخچال و فریزر",
        "cat_link": "https://hosseinykala.ir/product-category/refrigerator-freezer/clever-refrigerator/",
        "filter": lambda p: 'یخچال' in p['name'] and 'کلور' in p['name'] and any(k in p['name'] for k in ['کمبی', 'بالا پایین', 'پایین بالا', '10 فوت', 'مینی'])
    },
    {
        "id": "03_refrig_himalia_twin",
        "folder": "03_یخچال_دوقلو_هیمالیا",
        "title": "یخچال فریزر دوقلو هیمالیا در اهواز - اقساط",
        "divar_cat": "وسایل برقی > یخچال و فریزر",
        "cat_link": "https://hosseinykala.ir/product-category/refrigerator-freezer/himalia-refrigerator/",
        "filter": lambda p: 'یخچال' in p['name'] and 'هیمالیا' in p['name'] and 'دوقلو' in p['name']
    },
    {
        "id": "04_refrig_depoint",
        "folder": "04_یخچال_فریزر_دیپوینت",
        "title": "یخچال فریزر دیپوینت دوقلو و کمبی اهواز",
        "divar_cat": "وسایل برقی > یخچال و فریزر",
        "cat_link": "https://hosseinykala.ir/product-category/refrigerator-freezer/depoint-refrigerator/",
        "filter": lambda p: 'یخچال' in p['name'] and 'دیپوینت' in p['name']
    },
    {
        "id": "05_refrig_electrosteel",
        "folder": "05_یخچال_فریزر_الکترواستیل",
        "title": "یخچال فریزر الکترواستیل در اهواز - اقساط",
        "divar_cat": "وسایل برقی > یخچال و فریزر",
        "cat_link": "https://hosseinykala.ir/product-category/refrigerator-freezer/electrosteel-refrigerator/",
        "filter": lambda p: 'یخچال' in p['name'] and 'الکترواستیل' in p['name']
    },
    {
        "id": "06_refrig_mini_hotel",
        "folder": "06_یخچال_مینی_و_هتلی",
        "title": "یخچال هتلی و مینی ۵ و ۹ فوت در اهواز",
        "divar_cat": "وسایل برقی > یخچال و فریزر",
        "cat_link": "https://hosseinykala.ir/product-category/refrigerator-freezer/eastcool-refrigerator/",
        "filter": lambda p: ('ایستکول' in p['name'] or 'مینی' in p['name'] or 'هتلی' in p['name'] or '5 فوت' in p['name'] or '۹ فوت' in p['name'] or '9 فوت' in p['name'] or '10 فوت' in p['name']) and 'یخچال' in p['name']
    },
    {
        "id": "07_refrig_bost",
        "folder": "07_یخچال_فریزر_بست",
        "title": "یخچال فریزر بست (BOST) در اهواز - اقساط",
        "divar_cat": "وسایل برقی > یخچال و فریزر",
        "cat_link": "https://hosseinykala.ir/product-category/refrigerator-freezer/",
        "filter": lambda p: 'یخچال' in p['name'] and 'بست' in p['name']
    },
    {
        "id": "08_wm_pakshoma_auto",
        "folder": "08_لباسشویی_اتوماتیک_پاکشوما",
        "title": "لباسشویی اتوماتیک پاکشوما اهواز - اقساط",
        "divar_cat": "وسایل برقی > ماشین لباسشویی و خشک‌کن",
        "cat_link": "https://hosseinykala.ir/product-category/washing-machine-and-dryer/pakshoma-washing-machine/",
        "filter": lambda p: 'لباسشویی' in p['name'] and 'پاکشوما' in p['name'] and 'دوقلو' not in p['name'] and 'ظرفشویی' not in p['name']
    },
    {
        "id": "09_wm_pakshoma_twin",
        "folder": "09_لباسشویی_دوقلو_پاکشوما",
        "title": "لباسشویی دوقلو پاکشوما در اهواز - اقساط",
        "divar_cat": "وسایل برقی > ماشین لباسشویی و خشک‌کن",
        "cat_link": "https://hosseinykala.ir/product-category/washing-machine-and-dryer/pakshoma-washing-machine/",
        "filter": lambda p: 'لباسشویی' in p['name'] and 'پاکشوما' in p['name'] and 'دوقلو' in p['name']
    },
    {
        "id": "10_wm_daewoo_auto",
        "folder": "10_لباسشویی_اتوماتیک_دوو",
        "title": "لباسشویی اتوماتیک دوو در اهواز - اقساطی",
        "divar_cat": "وسایل برقی > ماشین لباسشویی و خشک‌کن",
        "cat_link": "https://hosseinykala.ir/product-category/washing-machine-and-dryer/daewoo-washing-machine/",
        "filter": lambda p: 'لباسشویی' in p['name'] and 'دوو' in p['name'] and 'ظرفشویی' not in p['name']
    },
    {
        "id": "11_wm_clever_auto",
        "folder": "11_لباسشویی_اینورتر_کلور",
        "title": "لباسشویی اینورتر کلور در اهواز - اقساطی",
        "divar_cat": "وسایل برقی > ماشین لباسشویی و خشک‌کن",
        "cat_link": "https://hosseinykala.ir/product-category/washing-machine-and-dryer/clever-washing-machine/",
        "filter": lambda p: 'لباسشویی' in p['name'] and 'کلور' in p['name'] and 'ظرفشویی' not in p['name']
    },
    {
        "id": "12_dishwasher_and_blanket",
        "folder": "12_ظرفشویی_و_پتوشور",
        "title": "ماشین ظرفشویی و پتوشور در اهواز - اقساط",
        "divar_cat": "وسایل برقی > ماشین ظرفشویی",
        "cat_link": "https://hosseinykala.ir/product-category/washing-machine-and-dryer/dishwasher/",
        "filter": lambda p: any(k in p['name'] for k in ['ظرفشویی', 'پتوشور', 'پاکیزان', 'ریتون']) and 'کولر' not in p['name']
    },
    {
        "id": "13_water_purifier",
        "folder": "13_دستگاه_تصفیه_آب",
        "title": "دستگاه تصفیه آب خانگی تایوانی در اهواز",
        "divar_cat": "لوازم خانگی > سایر",
        "cat_link": "https://hosseinykala.ir/product-category/water-purifier/",
        "filter": lambda p: any(k in p['name'] for k in ['تصفیه آب', 'سافت واتر', 'هوم گلد', 'وست واتر'])
    },
    {
        "id": "14_water_dispenser",
        "folder": "14_آبسردکن",
        "title": "آبسردکن ایستاده و رومیزی در اهواز - اقساط",
        "divar_cat": "وسایل برقی > سایر وسایل برقی",
        "cat_link": "https://hosseinykala.ir/product-category/water-dispenser/",
        "filter": lambda p: 'آبسردکن' in p['name'] or 'آب سردکن' in p['name']
    },
    {
        "id": "15_evap_cooler",
        "folder": "15_کولر_آبی",
        "title": "کولر آبی سلولزی یاسان و ریتون اهواز",
        "divar_cat": "سرمایش و گرمایش > کولر آبی",
        "cat_link": "https://hosseinykala.ir/product-category/cooling-and-heating/evaporative-cooler/",
        "filter": lambda p: any(k in p['name'] for k in ['کولر آبی', 'سلولزی', 'یاسان', 'ریتون']) and 'گازی' not in p['name'] and 'لباسشویی' not in p['name']
    },
    {
        "id": "16_ac_split",
        "folder": "16_کولر_گازی_اسپلیت",
        "title": "کولر گازی اسپلیت پاکشوما در اهواز - اقساط",
        "divar_cat": "سرمایش و گرمایش > کولر گازی",
        "cat_link": "https://hosseinykala.ir/product-category/cooling-and-heating/air-conditioner/",
        "filter": lambda p: any(k in p['name'] for k in ['کولر گازی', 'اسپلیت'])
    },
    {
        "id": "17_vacuum_cleaner_canister",
        "folder": "17_جاروبرقی_کیسه_ای",
        "title": "جاروبرقی کیسه‌ای خانگی در اهواز - اقساط",
        "divar_cat": "وسایل برقی > جاروبرقی و نظافت",
        "cat_link": "https://hosseinykala.ir/product-category/vacuum-cleaner/",
        "filter": lambda p: ('جاروبرقی' in p['name'] or 'جارو برقی' in p['name']) and not any(k in p['name'] for k in ['سطلی', 'صنعتی', 'تیوا', 'کسری', 'هیتاچی'])
    },
    {
        "id": "18_vacuum_cleaner_bucket",
        "folder": "18_جاروبرقی_سطلی_و_صنعتی",
        "title": "جاروبرقی سطلی و صنعتی در اهواز - اقساط",
        "divar_cat": "وسایل برقی > جاروبرقی و نظافت",
        "cat_link": "https://hosseinykala.ir/product-category/vacuum-cleaner/",
        "filter": lambda p: ('جاروبرقی' in p['name'] or 'جارو برقی' in p['name']) and any(k in p['name'] for k in ['سطلی', 'صنعتی', 'تیوا', 'کسری', 'هیتاچی'])
    },
    {
        "id": "19_kitchen_fryer_toaster",
        "folder": "19_سرخ_کن_و_لوازم_پخت_و_پز",
        "title": "سرخ کن بدون روغن و توستر در اهواز",
        "divar_cat": "وسایل برقی > سرخ‌کن و پخت‌وپز",
        "cat_link": "https://hosseinykala.ir/product-category/electrical-and-cooking-appliances/fryer/",
        "filter": lambda p: any(k in p['name'] for k in ['سرخ‌کن', 'سرخ کن', 'آون توستر', 'توستر', 'اسپرسوساز', 'اسپرسو ساز', 'خردکن'])
    },
    {
        "id": "20_grooming_shaver",
        "folder": "20_ماشین_اصلاح_و_ریش_تراش",
        "title": "ماشین اصلاح و خط زن پرو امگا اهواز",
        "divar_cat": "زیبایی و سلامت > اصلاح و پیرایش",
        "cat_link": "https://hosseinykala.ir/product-category/personal-health-and-beauty/hair-clipper/",
        "filter": lambda p: any(k in p['name'] for k in ['اصلاح', 'ریش تراش', 'شیور', 'خط زن'])
    }
]

print("Ads config defined. Checking matches in products.json...")
for ac in ads_config:
    matched = [p for p in products if ac['filter'](p)]
    print(f"[{ac['folder']}] Matched {len(matched)} products in products.json | Title len: {len(ac['title'])} chars")

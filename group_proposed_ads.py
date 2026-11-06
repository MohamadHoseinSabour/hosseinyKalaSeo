import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/catalog_extracted.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

with open('data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

with open('data/categories.json', 'r', encoding='utf-8') as f:
    categories = json.load(f)

# Helper to find canonical link
prod_by_name = {}
for p in products:
    prod_by_name[p['name'].strip()] = p.get('permalink') or f"https://hosseinykala.ir/product/{p.get('slug')}/"

cat_by_slug = {c['slug']: c.get('url', f"https://hosseinykala.ir/product-category/{c['slug']}/") for c in categories}

# Let's inspect catalog items grouped by logic
buckets = {
    "refrig_clever_twin": {
        "title": "انواع یخچال و فریزر دوقلو کلور (Clever)",
        "category_link": "https://hosseinykala.ir/product-category/refrigerator-freezer/clever-refrigerator/",
        "filter": lambda x: x['sheet'] == 'یخچال و فریزر' and x['brand'] == 'کلور' and any(k in x['name'] for k in ['دوقلو', 'روسو پلاس', 'رسوپلاس', 'گلوری', '101', 'glory', 'rosso']) and not any(k in x['name'] for k in ['کمبی', '10 فوت', 'مینی'])
    },
    "refrig_clever_combi": {
        "title": "انواع یخچال و فریزر کمبی کلور (Clever)",
        "category_link": "https://hosseinykala.ir/product-category/refrigerator-freezer/clever-refrigerator/",
        "filter": lambda x: x['sheet'] == 'یخچال و فریزر' and x['brand'] == 'کلور' and any(k in x['name'] for k in ['کمبی', 'بالا پایین', 'پایین بالا', '10 فوت', 'مینی'])
    },
    "refrig_himalia_twin": {
        "title": "انواع یخچال و فریزر دوقلو هیمالیا (Himalia)",
        "category_link": "https://hosseinykala.ir/product-category/refrigerator-freezer/himalia-refrigerator/",
        "filter": lambda x: x['sheet'] == 'یخچال و فریزر' and x['brand'] == 'هیمالیا' and 'دوقلو' in x['name']
    },
    "refrig_depoint": {
        "title": "انواع یخچال و فریزر دیپوینت (دوقلو و کمبی Depoint)",
        "category_link": "https://hosseinykala.ir/product-category/refrigerator-freezer/depoint-refrigerator/",
        "filter": lambda x: x['sheet'] == 'یخچال و فریزر' and x['brand'] == 'دیپوینت'
    },
    "refrig_electrosteel": {
        "title": "انواع یخچال و فریزر الکترواستیل (دوقلو و کمبی Electrosteel)",
        "category_link": "https://hosseinykala.ir/product-category/refrigerator-freezer/electrosteel-refrigerator/",
        "filter": lambda x: x['sheet'] == 'یخچال و فریزر' and x['brand'] == 'الکترواستیل'
    },
    "refrig_eastcool_mini": {
        "title": "انواع یخچال و فریزر هتلی و کوچک (ایستکول و کلور)",
        "category_link": "https://hosseinykala.ir/product-category/refrigerator-freezer/eastcool-refrigerator/",
        "filter": lambda x: x['sheet'] == 'یخچال و فریزر' and (x['brand'] == 'ایستکول' or any(k in x['name'] for k in ['کوچک', 'هتلی', '5 فوت', '9 فوت', 'مینی', '10 فوت']))
    },
    "refrig_bost": {
        "title": "انواع یخچال و فریزر بست (کمبی و دوقلو BOST)",
        "category_link": "https://hosseinykala.ir/product-category/refrigerator-freezer/",
        "filter": lambda x: x['sheet'] == 'یخچال و فریزر' and x['brand'] == 'بست'
    },
    "wm_pakshoma_auto": {
        "title": "انواع ماشین لباسشویی اتوماتیک پاکشوما (Pakshoma)",
        "category_link": "https://hosseinykala.ir/product-category/washing-machine-and-dryer/pakshoma-washing-machine/",
        "filter": lambda x: x['sheet'] == 'شستشو و نظافت' and x['brand'] == 'پاکشوما' and 'دوقلو' not in x['name'] and 'ظرفشویی' not in x['name']
    },
    "wm_pakshoma_semi": {
        "title": "انواع ماشین لباسشویی دوقلو و نیمه‌اتوماتیک پاکشوما",
        "category_link": "https://hosseinykala.ir/product-category/washing-machine-and-dryer/pakshoma-washing-machine/",
        "filter": lambda x: x['sheet'] == 'شستشو و نظافت' and x['brand'] == 'پاکشوما' and 'دوقلو' in x['name']
    },
    "wm_daewoo": {
        "title": "انواع ماشین لباسشویی اتوماتیک دوو (Daewoo)",
        "category_link": "https://hosseinykala.ir/product-category/washing-machine-and-dryer/daewoo-washing-machine/",
        "filter": lambda x: x['sheet'] == 'شستشو و نظافت' and x['brand'] == 'دوو' and 'ظرفشویی' not in x['name']
    },
    "wm_clever": {
        "title": "انواع ماشین لباسشویی اتوماتیک اینورتر کلور (Clever)",
        "category_link": "https://hosseinykala.ir/product-category/washing-machine-and-dryer/clever-washing-machine/",
        "filter": lambda x: x['sheet'] == 'شستشو و نظافت' and x['brand'] == 'کلور' and 'ظرفشویی' not in x['name']
    },
    "dishwasher": {
        "title": "انواع ماشین ظرفشویی مبله (کلور، پاکشوما و...)",
        "category_link": "https://hosseinykala.ir/product-category/washing-machine-and-dryer/dishwasher/",
        "filter": lambda x: x['sheet'] == 'شستشو و نظافت' and any(k in x['name'] for k in ['ظرفشویی', 'ظرف شویی'])
    },
    "wm_twin_blanket": {
        "title": "انواع لباسشویی دوقلو و پتوشور (ریتون، پاکیزان و...)",
        "category_link": "https://hosseinykala.ir/product-category/washing-machine-and-dryer/",
        "filter": lambda x: x['sheet'] == 'شستشو و نظافت' and any(k in x['name'] for k in ['پتوشور', 'پاکیزان', 'ریتون', 'سطلی'])
    },
    "water_purifier": {
        "title": "انواع دستگاه تصفیه آب خانگی (سافت واتر، هوم گلد، وست واتر و...)",
        "category_link": "https://hosseinykala.ir/product-category/water-purifier/",
        "filter": lambda x: x['sheet'] == 'تصفیه کننده آب'
    },
    "evap_cooler": {
        "title": "انواع کولر آبی سلولزی و معمولی (یاسان، ریتون و...)",
        "category_link": "https://hosseinykala.ir/product-category/cooling-and-heating/evaporative-cooler/",
        "filter": lambda x: x['sheet'] == 'سرمایش و گرمایش' and any(k in x['name'] for k in ['کولر آبی', 'سلولزی', 'یاسان', 'ریتون'])
    },
    "ac_split": {
        "title": "انواع کولر گازی و اسپلیت (پاکشوما، گرین، وستینگهاوس)",
        "category_link": "https://hosseinykala.ir/product-category/cooling-and-heating/air-conditioner/",
        "filter": lambda x: x['sheet'] == 'سرمایش و گرمایش' and any(k in x['name'] for k in ['کولر گازی', 'اسپلیت'])
    },
    "vacuum_cleaner": {
        "title": "انواع جاروبرقی خانگی و سطلی (بست، پاناسونیک، دونالکس، تیوا، هیتاچی)",
        "category_link": "https://hosseinykala.ir/product-category/vacuum-cleaner/",
        "filter": lambda x: any(k in x['name'] for k in ['جاروبرقی', 'جارو برقی'])
    },
    "water_dispenser": {
        "title": "انواع آبسردکن ایستاده و رومیزی (نیکای، یونوا، افترون)",
        "category_link": "https://hosseinykala.ir/product-category/water-dispenser/",
        "filter": lambda x: 'آبسردکن' in x['name'] or 'آب سردکن' in x['name']
    },
    "cooking_fryer": {
        "title": "انواع سرخ‌کن بدون روغن و آون توستر (دونالکس و...)",
        "category_link": "https://hosseinykala.ir/product-category/electrical-and-cooking-appliances/fryer/",
        "filter": lambda x: any(k in x['name'] for k in ['سرخ‌کن', 'سرخ کن', 'آون توستر', 'توستر'])
    },
    "coffee_tea": {
        "title": "انواع اسپرسوساز و نوشیدنی‌ساز (دونالکس و...)",
        "category_link": "https://hosseinykala.ir/product-category/beverage-maker/espresso-maker/",
        "filter": lambda x: x['sheet'] == 'نوشیدنی ساز' and any(k in x['name'] for k in ['اسپرسوساز', 'اسپرسو ساز', 'قهوه ساز'])
    },
    "grooming": {
        "title": "انواع ست ماشین اصلاح مو و ریش‌تراش (پرو امگا، پرومارون)",
        "category_link": "https://hosseinykala.ir/product-category/personal-health-and-beauty/hair-clipper/",
        "filter": lambda x: x['sheet'] == 'زیبایی و سلامت فردی' and any(k in x['name'] for k in ['اصلاح', 'ریش تراش'])
    }
}

result_groups = {}
for k, conf in buckets.items():
    matched = []
    for item in catalog:
        try:
            if conf['filter'](item):
                matched.append(item)
        except Exception:
            pass
    result_groups[k] = {
        "title": conf['title'],
        "category_link": conf['category_link'],
        "count": len(matched),
        "items": matched
    }
    print(f"- {conf['title']}: {len(matched)} items")

with open('data/proposed_ad_groups.json', 'w', encoding='utf-8') as f:
    json.dump(result_groups, f, ensure_ascii=False, indent=2)
print("Saved data/proposed_ad_groups.json")

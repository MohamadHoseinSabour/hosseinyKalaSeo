import os
import sys
import json
import urllib.request
import re
import socket

sys.stdout.reconfigure(encoding='utf-8')
socket.setdefaulttimeout(15)

# 1. Load data
with open('data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

with open('data/catalog_extracted.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

base_dir = "divar_ads"
os.makedirs(base_dir, exist_ok=True)

# Helper to download image safely
def download_image(url, save_path):
    if os.path.exists(save_path) and os.path.getsize(save_path) > 1000:
        return True
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
        )
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
            if len(data) > 500:
                with open(save_path, 'wb') as f:
                    f.write(data)
                return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    return False

# 2. Ads configuration with concise titles (<50 chars) and targeted models
ads_config = [
    {
        "id": "01_refrig_clever_twin",
        "folder": "01_یخچال_دوقلو_کلور",
        "title": "یخچال فریزر دوقلو کلور در اهواز - اقساطی",
        "divar_cat": "وسایل برقی > یخچال و فریزر",
        "canonical_cat": "https://hosseinykala.ir/product-category/refrigerator-freezer/clever-refrigerator/",
        "filter": lambda p: 'یخچال' in p['name'] and 'کلور' in p['name'] and any(k in p['name'] for k in ['دوقلو', 'روسو پلاس', 'رسوپلاس', 'گلوری', '101', 'اکونومی']) and not any(k in p['name'] for k in ['کمبی', '10 فوت', 'مینی']),
        "headline": "فروش اقساطی انواع یخچال و فریزر دوقلو کلور (Clever)",
        "models_summary": [
            "دوقلو ۵۴ فوت کلور مدل گلوری پلاس (عرض ۷۰ جادارترین مدل)",
            "دوقلو ۴۰ فوت کلور مدل گلوری (عرض ۶۰ استاندارد)",
            "دوقلو ۴۰ فوت کلور مدل روسوپلاس آبریزدار هوشمند",
            "دوقلو کلور مدل ۱۰۱ (موتور اینورتر کم‌مصرف A+)",
            "دوقلو ۲۷ فوت کلور مدل اکونومی اقتصادی"
        ],
        "specs": [
            "موتور اینورتر دیجیتال کم‌صدا و کم‌مصرف",
            "سیستم بدون برفک نوفراست (No Frost)",
            "دارای بوگیر هوشمند با نانو سیلور و گردش هوای چندگانه",
            "۳۰ ماه ضمانت تعویض و گارانتی معتبر شرکتی"
        ]
    },
    {
        "id": "02_refrig_clever_combi",
        "folder": "02_یخچال_کمبی_کلور",
        "title": "یخچال فریزر کمبی کلور در اهواز - اقساط",
        "divar_cat": "وسایل برقی > یخچال و فریزر",
        "canonical_cat": "https://hosseinykala.ir/product-category/refrigerator-freezer/clever-refrigerator/",
        "filter": lambda p: 'یخچال' in p['name'] and 'کلور' in p['name'] and any(k in p['name'] for k in ['کمبی', 'بالا پایین', 'پایین بالا', '10 فوت', 'مینی']),
        "headline": "انواع یخچال فریزر کمبی کلور (بالا و پایین Clever)",
        "models_summary": [
            "کمبی ۲۷ فوت کلور مدل روسو (فریزر پایین با هوم‌بار و آبریز)",
            "کمبی کلور مدل گلوری پلاس فریزر پایین عرض ۷۰",
            "کمبی ۲۷ فوت کلور مدل ۱۰۱ (بدون برفک اقتصادی)",
            "یخچال ۱۰ فوت مینی فانتزی و طرح‌دار رنگی کلور"
        ],
        "specs": [
            "طراحی بسیار شیک مناسب آشپزخانه‌های مدرن و کم‌جا",
            "سیستم انجماد سریع Super Freezing",
            "طبقات شیشه‌ای نشکن مقاوم در برابر شوک حرارتی",
            "گارانتی رسمی و پشتیبانی سراسری"
        ]
    },
    {
        "id": "03_refrig_himalia_twin",
        "folder": "03_یخچال_دوقلو_هیمالیا",
        "title": "یخچال فریزر دوقلو هیمالیا در اهواز - اقساط",
        "divar_cat": "وسایل برقی > یخچال و فریزر",
        "canonical_cat": "https://hosseinykala.ir/product-category/refrigerator-freezer/himalia-refrigerator/",
        "filter": lambda p: 'یخچال' in p['name'] and 'هیمالیا' in p['name'] and 'دوقلو' in p['name'],
        "headline": "فروش انواع یخچال فریزر دوقلو هیمالیا (Himalia) اهواز",
        "models_summary": [
            "دوقلو هیمالیا مدل آلفا پلاس (Alpha هوم‌بار و یخساز اتومات)",
            "دوقلو هیمالیا مدل آیس پول (Ice Pool 60MW دیجیتال)",
            "دوقلو هیمالیا مدل پانوراما (Panorama لوکس و جادار)"
        ],
        "specs": [
            "مجهز به یخساز اتوماتیک و اتصال مستقیم به آب شهری",
            "کمپرسور مخصوص مناطق گرمسیری (تروپیکال مناسب اهواز)",
            "کندانسور مخفی و طراحی بدون برفک ۱۰۰٪",
            "گارانتی معتبر شرکتی هیمالیا"
        ]
    },
    {
        "id": "04_refrig_depoint",
        "folder": "04_یخچال_فریزر_دیپوینت",
        "title": "یخچال فریزر دیپوینت دوقلو و کمبی اهواز",
        "divar_cat": "وسایل برقی > یخچال و فریزر",
        "canonical_cat": "https://hosseinykala.ir/product-category/refrigerator-freezer/depoint-refrigerator/",
        "filter": lambda p: 'یخچال' in p['name'] and 'دیپوینت' in p['name'],
        "headline": "انواع یخچال فریزر دوقلو و کمبی دیپوینت (Depoint)",
        "models_summary": [
            "دوقلو ۳۴ فوت دیپوینت مدل مکس (MAX جادارترین دوقلو)",
            "دوقلو دیپوینت مدل اکسپلور (Explore دارای دو درب مجزا)",
            "کمبی ۳۰ فوت دیپوینت مدل Boss Pro (فریزر بالا بسیار عریض)",
            "کمبی ۲۸ فوت دیپوینت مدل T7 (محبوب‌ترین کمبی بازار)",
            "کمبی دیپوینت مدل دیسنت (Decent مجهز به یخساز)"
        ],
        "specs": [
            "سیستم گردش هوای سه‌بعدی و کنترل رطوبت محفظه میوه",
            "مصرف انرژی فوق‌العاده بهینه با اینورتر هوشمند",
            "پنل لمسی دیجیتال و یخساز دستی و اتوماتیک",
            "خدمات پس از فروش گسترده در خوزستان"
        ]
    },
    {
        "id": "05_refrig_electrosteel",
        "folder": "05_یخچال_فریزر_الکترواستیل",
        "title": "یخچال فریزر الکترواستیل در اهواز - اقساط",
        "divar_cat": "وسایل برقی > یخچال و فریزر",
        "canonical_cat": "https://hosseinykala.ir/product-category/refrigerator-freezer/electrosteel-refrigerator/",
        "filter": lambda p: 'یخچال' in p['name'] and 'الکترواستیل' in p['name'],
        "headline": "انواع یخچال و فریزر الکترواستیل (Electrosteel) در اهواز",
        "models_summary": [
            "دوقلو الکترواستیل مدل فیوچر (Future ES23)",
            "دوقلو الکترواستیل مدل پرایم (Prime با آبسردکن و یخساز اتومات)",
            "کمبی الکترواستیل مدل استار (Star ES35 بدون برفک)",
            "فریزر تک و یخچال تک الکترواستیل سری ۱۰ نوفراست"
        ],
        "specs": [
            "کمپرسور با کیفیت ساخت ایتالیا/اروپا فوق‌العاده بی‌صدا",
            "فیلتر آنتی‌باکتریال و ضد بو",
            "۴۰ ماه گارانتی قطعات کمپرسور",
            "بدنه مقاوم در برابر رطوبت و شرجی اهواز"
        ]
    },
    {
        "id": "06_refrig_mini_hotel",
        "folder": "06_یخچال_مینی_و_هتلی",
        "title": "یخچال هتلی و مینی ۵ و ۹ فوت در اهواز",
        "divar_cat": "وسایل برقی > یخچال و فریزر",
        "canonical_cat": "https://hosseinykala.ir/product-category/refrigerator-freezer/eastcool-refrigerator/",
        "filter": lambda p: ('ایستکول' in p['name'] or 'مینی' in p['name'] or 'هتلی' in p['name'] or '5 فوت' in p['name'] or '۹ فوت' in p['name'] or '9 فوت' in p['name'] or '10 فوت' in p['name']) and 'یخچال' in p['name'],
        "headline": "انواع یخچال کوچک، مینی و هتلی (ایستکول و کلور)",
        "models_summary": [
            "یخچال ۵ فوت ایستکول مدل TM-2835 (سفید، مشکی و نقره‌ای)",
            "یخچال فریزر ۹ فوت ایستکول مدل TM-2919 جادار",
            "مینی یخچال ۱۰ فوت فانتزی و طرح‌دار رنگی کلور",
            "یخچال ۷ فوت کامپکت کم‌مصرف"
        ],
        "specs": [
            "بسیار کم‌صدا و کم‌مصرف مناسب اتاق خواب، هتل و محل کار",
            "دارای جایخی و محفظه میوه با گاز مبرد سازگار با محیط زیست",
            "ابعاد جمع و جور و حمل آسان",
            "گارانتی معتبر ۲۴ ماهه شرکتی"
        ]
    },
    {
        "id": "07_refrig_bost",
        "folder": "07_یخچال_فریزر_بست",
        "title": "یخچال فریزر بست (BOST) در اهواز - اقساط",
        "divar_cat": "وسایل برقی > یخچال و فریزر",
        "canonical_cat": "https://hosseinykala.ir/product-category/refrigerator-freezer/",
        "filter": lambda p: 'یخچال' in p['name'] and 'بست' in p['name'],
        "headline": "انواع یخچال فریزر کمبی و اقتصادی بست (BOST)",
        "models_summary": [
            "یخچال فریزر کمبی بست مدل BRB240 بدون برفک",
            "یخچال و فریزر دوقلو بست مدل BLR200 اقتصادی"
        ],
        "specs": [
            "محصول کارخانجات گروه صنعتی انتخاب (تولیدکننده دوو و اسنوا)",
            "قیمت بسیار مناسب و اقتصادی با کیفیت ساخت بالا",
            "طراحی ارگونومیک با نوار درزگیر آنتی‌باکتریال",
            "پشتیبانی و گارانتی رسمی انتخاب سرویس"
        ]
    },
    {
        "id": "08_wm_pakshoma_auto",
        "folder": "08_لباسشویی_اتوماتیک_پاکشوما",
        "title": "لباسشویی اتوماتیک پاکشوما اهواز - اقساط",
        "divar_cat": "وسایل برقی > ماشین لباسشویی و خشک‌کن",
        "canonical_cat": "https://hosseinykala.ir/product-category/washing-machine-and-dryer/pakshoma-washing-machine/",
        "filter": lambda p: 'لباسشویی' in p['name'] and 'پاکشوما' in p['name'] and 'دوقلو' not in p['name'] and 'ظرفشویی' not in p['name'],
        "headline": "انواع ماشین لباسشویی اتوماتیک پاکشوما (۷، ۸ و ۹ کیلو)",
        "models_summary": [
            "لباسشویی ۹ کیلویی اتوماتیک اینورتر مدل BWF-40901",
            "لباسشویی ۸ کیلویی پاکشوما مدل BWF-40801 سیلور و سفید",
            "لباسشویی ۷ کیلویی پاکشوما سری اقتصادی ۴۰۷۰۱"
        ],
        "specs": [
            "موتور پیشرفته BLDC اینورتر با دور خشک‌کن ۱۴۰۰ دور",
            "۱۶ برنامه شستشوی اصلی + ۸ برنامه کمکی",
            "قابلیت اضافه کردن لباس حین کار (Add Garment)",
            "۲۴ ماه گارانتی و ۱۴۴ ماه پشتیبانی موتور پاکشوما"
        ]
    },
    {
        "id": "09_wm_pakshoma_twin",
        "folder": "09_لباسشویی_دوقلو_پاکشوما",
        "title": "لباسشویی دوقلو پاکشوما در اهواز - اقساط",
        "divar_cat": "وسایل برقی > ماشین لباسشویی و خشک‌کن",
        "canonical_cat": "https://hosseinykala.ir/product-category/washing-machine-and-dryer/pakshoma-washing-machine/",
        "filter": lambda p: 'لباسشویی' in p['name'] and 'پاکشوما' in p['name'] and 'دوقلو' in p['name'],
        "headline": "انواع لباسشویی دوقلو و نیمه‌اتوماتیک پاکشوما",
        "models_summary": [
            "لباسشویی دوقلو ۱۵.۵ کیلوگرم مدل PWT-1554NJ (مخصوص پتو و پرده)",
            "لباسشویی دوقلو ۹.۶ کیلوگرم مدل PWT-9654AJ پرفروش‌ترین سایز",
            "لباسشویی دوقلو ۶.۵ کیلوگرم مدل PWT-6523AJ جمع‌وجور"
        ],
        "specs": [
            "بدنه دولایه پلاستیکی ضدزنگ و مقاوم در برابر رطوبت شرجی",
            "پروانه قدرتمند با شستشوی گردابی بدون آسیب به بافت لباس",
            "خشک‌کن با قدرت چرخش بالا و تخلیه سریع آب",
            "گارانتی و خدمات رسمی پاک سرویس"
        ]
    },
    {
        "id": "10_wm_daewoo_auto",
        "folder": "10_لباسشویی_اتوماتیک_دوو",
        "title": "لباسشویی اتوماتیک دوو در اهواز - اقساطی",
        "divar_cat": "وسایل برقی > ماشین لباسشویی و خشک‌کن",
        "canonical_cat": "https://hosseinykala.ir/product-category/washing-machine-and-dryer/daewoo-washing-machine/",
        "filter": lambda p: 'لباسشویی' in p['name'] and 'دوو' in p['name'] and 'ظرفشویی' not in p['name'],
        "headline": "انواع ماشین لباسشویی اتوماتیک دوو (Daewoo)",
        "models_summary": [
            "لباسشویی دوو سری لایف ۹ کیلوگرم (Life دایرکت درایو بدون تسمه)",
            "لباسشویی دوو سری کاریزما ۸ و ۹ کیلوگرم (Charisma پرفروش)",
            "لباسشویی دوو سری پرو ۸ کیلوگرم (Pro هوشمند)"
        ],
        "specs": [
            "موتور دایرکت درایو ۱۴۰۰ دور بدون لرزش و صدا",
            "سیستم حباب‌ساز نانو برای شستشوی عمیق با آب سرد (Air Bubble)",
            "شستشوی سریع ۱۹ دقیقه‌ای و شستشو با بخار Steam Care",
            "۱۳۰ ماه ضمانت تعویض موتور از انتخاب سرویس"
        ]
    },
    {
        "id": "11_wm_clever_auto",
        "folder": "11_لباسشویی_اینورتر_کلور",
        "title": "لباسشویی اینورتر کلور در اهواز - اقساطی",
        "divar_cat": "وسایل برقی > ماشین لباسشویی و خشک‌کن",
        "canonical_cat": "https://hosseinykala.ir/product-category/washing-machine-and-dryer/clever-washing-machine/",
        "filter": lambda p: 'لباسشویی' in p['name'] and 'کلور' in p['name'] and 'ظرفشویی' not in p['name'],
        "headline": "انواع ماشین لباسشویی تمام اتوماتیک کلور (Clever)",
        "models_summary": [
            "لباسشویی ۹ کیلوگرم کلور مدل تاچ اینورتر (سفید، سیلور، تیتانیوم)",
            "لباسشویی ۸ کیلوگرم کلور مدل تاچ اینورتر پنل لمسی مدرن",
            "لباسشویی کلور سری میراژ (Mirage با دیگ الماسه)"
        ],
        "specs": [
            "موتور اینورتر BLDC کم‌مصرف رده انرژی A+++",
            "دیگ الماسه ضدسایش با شستشوی ضدچروک",
            "کنترل پنل تمام لمسی فول تاچ ضدآب",
            "۳۰ ماه گارانتی قطعات و تعویض شرکت کلور"
        ]
    },
    {
        "id": "12_dishwasher_and_blanket",
        "folder": "12_ظرفشویی_و_پتوشور",
        "title": "ماشین ظرفشویی و پتوشور در اهواز - اقساط",
        "divar_cat": "وسایل برقی > ماشین ظرفشویی",
        "canonical_cat": "https://hosseinykala.ir/product-category/washing-machine-and-dryer/dishwasher/",
        "filter": lambda p: any(k in p['name'] for k in ['ظرفشویی', 'پتوشور', 'پاکیزان', 'ریتون']) and 'کولر' not in p['name'],
        "headline": "انواع ماشین ظرفشویی مبله و پتوشورهای خانگی و نیمه‌صنعتی",
        "models_summary": [
            "ماشین ظرفشویی ۱۵ و ۱۶ نفره مبله کلور (سه سبد اینورتر)",
            "پتوشور خانگی و صنعتی پاکیزان ۳۰، ۴۵ و ۶۰ کیلوگیربکسی",
            "لباسشویی دوقلو و پتوشور ریتون با موتور پرقدرت"
        ],
        "specs": [
            "شستشوی پرقدرت با کمترین مصرف آب و شوینده",
            "موتورهای گیربکسی سفارشی مقاوم در برابر بارهای سنگین",
            "بدنه استیل ضدزنگ با دوام طولانی در هوای اهواز",
            "گارانتی و ضمانت‌نامه کتبی اصالت کالا"
        ]
    },
    {
        "id": "13_water_purifier",
        "folder": "13_دستگاه_تصفیه_آب",
        "title": "دستگاه تصفیه آب خانگی تایوانی در اهواز",
        "divar_cat": "لوازم خانگی > سایر",
        "canonical_cat": "https://hosseinykala.ir/product-category/water-purifier/",
        "filter": lambda p: any(k in p['name'] for k in ['تصفیه آب', 'سافت واتر', 'هوم گلد', 'وست واتر']),
        "headline": "انواع دستگاه تصفیه آب ۶، ۷ و ۸ مرحله‌ای (سافت واتر، هوم گلد، وست واتر)",
        "models_summary": [
            "دستگاه تصفیه آب سافت واتر (Soft Water RO تایوانی اصلی)",
            "دستگاه تصفیه آب هوم گلد اولترا (Home Gold با پمپ پرقدرت)",
            "دستگاه تصفیه آب وست واتر (West Water قلیایی‌ساز و مینرال)"
        ],
        "specs": [
            "فیلتراسیون اسمز معکوس (RO) جهت حذف کامل گچ، نمک و املاح آب اهواز",
            "مخزن آنتی‌باکتریال ۴ گالن با شیر برداشت اهرمی لوکس",
            "دارای هوزینگ‌های دابل اورینگ ضد نشتی و بو",
            "نصب و راه‌اندازی با پشتیبانی تعویض فیلتر دوره‌ای"
        ]
    },
    {
        "id": "14_water_dispenser",
        "folder": "14_آبسردکن",
        "title": "آبسردکن ایستاده و رومیزی در اهواز - اقساط",
        "divar_cat": "وسایل برقی > سایر وسایل برقی",
        "canonical_cat": "https://hosseinykala.ir/product-category/water-dispenser/",
        "filter": lambda p: 'آبسردکن' in p['name'] or 'آب سردکن' in p['name'],
        "headline": "انواع آبسردکن ایستاده یخچال‌دار و رومیزی (نیکای، یونوا، افترون)",
        "models_summary": [
            "آبسردکن ایستاده ۳ شیر نیکای مدل NWD-1400R با یخچال مجزا",
            "آبسردکن ایستاده یونوا سوپرکول (Super Cool خنک‌کنندگی فوری)",
            "آبسردکن رومیزی و اداری افترون (Aftron اصل کم‌صدا)"
        ],
        "specs": [
            "ارائه آب سرد، گرم و ولرم با شیر قفل کودک برای ایمنی آب داغ",
            "کمپرسور قدرتمند و رادیاتور تقویت‌شده برای تابستان خوزستان",
            "طراحی بسیار شکیل مناسب منازل، مطب‌ها و دفاتر کار",
            "گارانتی و ضمانت کارکرد طولانی‌مدت"
        ]
    },
    {
        "id": "15_evap_cooler",
        "folder": "15_کولر_آبی",
        "title": "کولر آبی سلولزی یاسان و ریتون اهواز",
        "divar_cat": "سرمایش و گرمایش > کولر آبی",
        "canonical_cat": "https://hosseinykala.ir/product-category/cooling-and-heating/evaporative-cooler/",
        "filter": lambda p: any(k in p['name'] for k in ['کولر آبی', 'سلولزی', 'یاسان', 'ریتون']) and 'گازی' not in p['name'] and 'لباسشویی' not in p['name'],
        "headline": "انواع کولر آبی سلولزی کانال‌دار و پرتابل (یاسان و ریتون)",
        "models_summary": [
            "کولر آبی سلولزی کانال‌دار یاسان (بالاترین سرمایش با پد فنلاندی)",
            "کولر آبی سلولزی ۱۶۰۰۰ ریتون (مخصوص سالن‌های بزرگ و کارگاهی)",
            "کولر آبی پرتابل چرخ‌دار ۷۰۰۰ ریتون (قابل جابجایی آسان)"
        ],
        "specs": [
            "پدهای ضخیم سلولزی با سرمادهی ۳۰٪ بیشتر نسبت به پوشال معمولی",
            "موتور الکتروژن و موتوژن مسی ضدسوختگی و کم‌مصرف",
            "بدنه گالوانیزه ضخیم با رنگ پودری الکترواستاتیک مقاوم در برابر شرجی",
            "پمپ آب غوطه‌ور کم‌مصرف و بی‌صدا"
        ]
    },
    {
        "id": "16_ac_split",
        "folder": "16_کولر_گازی_اسپلیت",
        "title": "کولر گازی اسپلیت پاکشوما در اهواز - اقساط",
        "divar_cat": "سرمایش و گرمایش > کولر گازی",
        "canonical_cat": "https://hosseinykala.ir/product-category/cooling-and-heating/air-conditioner/",
        "filter": lambda p: any(k in p['name'] for k in ['کولر گازی', 'اسپلیت']),
        "headline": "انواع کولر گازی اسپلیت پاکشوما و گرین (مخصوص خوزستان)",
        "models_summary": [
            "کولر گازی پاکشوما ظرفیت‌های ۱۲، ۱۸، ۲۴ و ۳۰ هزار تروپیکال T3",
            "کولر گازی اینورتر گرین (Green سرد و گرم فوق‌العاده کم‌مصرف)"
        ],
        "specs": [
            "کمپرسور روتاری و پیستونی T3 پرقدرت ویژه دمای بالای ۶۰ درجه اهواز",
            "پوشش محافظ فین طلایی (Gold Fin) ضدخوردگی و فرسایش",
            "پرتاب باد ۴ جهته هوشمند با فیلتر هوای تصفیه‌کننده ویتامین C",
            "۶۰ ماه ضمانت کمپرسور و ۱۸ ماه سایر قطعات پاک سرویس"
        ]
    },
    {
        "id": "17_vacuum_cleaner_canister",
        "folder": "17_جاروبرقی_کیسه_ای",
        "title": "جاروبرقی کیسه‌ای خانگی در اهواز - اقساط",
        "divar_cat": "وسایل برقی > جاروبرقی و نظافت",
        "canonical_cat": "https://hosseinykala.ir/product-category/vacuum-cleaner/",
        "filter": lambda p: ('جاروبرقی' in p['name'] or 'جارو برقی' in p['name']) and not any(k in p['name'] for k in ['سطلی', 'صنعتی', 'تیوا', 'کسری', 'هیتاچی']),
        "headline": "انواع جاروبرقی کیسه‌ای خانگی سایلنت (بست، پاناسونیک، دونالکس)",
        "models_summary": [
            "جاروبرقی بست مدل BVC (سایلنت، کم‌صدا و پرقدرت با فیلتر هپا)",
            "جاروبرقی ۲۰۰۰ وات پاناسونیک موتور ژاپن (سفید، مشکی و قرمز)",
            "جاروبرقی ۲۲۰۰ وات سوپر سایلنت دونالکس دیجیتال"
        ],
        "specs": [
            "موتورهای نسل جدید با مکش بسیار قوی و مصرف برق استاندارد",
            "فیلتر بهداشتی HEPA جهت جلوگیری از خروج گرد و غبار به محیط",
            "سیم‌جمع‌کن خودکار سریع با لوله تلسکوپی آلومینیومی ارگونومیک",
            "گارانتی معتبر و موجودی همیشگی پاکت و فیلتر"
        ]
    },
    {
        "id": "18_vacuum_cleaner_bucket",
        "folder": "18_جاروبرقی_سطلی_و_صنعتی",
        "title": "جاروبرقی سطلی و صنعتی در اهواز - اقساط",
        "divar_cat": "وسایل برقی > جاروبرقی و نظافت",
        "canonical_cat": "https://hosseinykala.ir/product-category/vacuum-cleaner/",
        "filter": lambda p: ('جاروبرقی' in p['name'] or 'جارو برقی' in p['name']) and any(k in p['name'] for k in ['سطلی', 'صنعتی', 'تیوا', 'کسری', 'هیتاچی']),
        "headline": "انواع جاروبرقی سطلی، هتلی و صنعتی کالسکه دار (تیوا، کسری، هیتاچی)",
        "models_summary": [
            "جاروبرقی سطلی تیوا مدل ۳۲۰۰ و ۳۶۰۰ پرقدرت خانگی و مساجد",
            "جاروبرقی صنعتی کالسکه دار دو و سه موتوره کسری (آب و خاک)",
            "جاروبرقی سطلی ۲۱۰۰ وات هیتاچی مدل 950F بدنه فلزی بادوام"
        ],
        "specs": [
            "مخزن‌های بزرگ فلزی و پلاستیک فشرده مقاوم در برابر ضربه",
            "مناسب مساجد، حسینیه‌ها، رستوران‌ها، هتل‌ها و منازل بزرگ",
            "قابلیت مکش آب و خاک با فیلترهای قابل شستشو",
            "گارانتی قطعات و تامین مداوم برس و اتصالات"
        ]
    },
    {
        "id": "19_kitchen_fryer_toaster",
        "folder": "19_سرخ_کن_و_لوازم_پخت_و_پز",
        "title": "سرخ کن بدون روغن و توستر در اهواز",
        "divar_cat": "وسایل برقی > سرخ‌کن و پخت‌وپز",
        "canonical_cat": "https://hosseinykala.ir/product-category/electrical-and-cooking-appliances/fryer/",
        "filter": lambda p: any(k in p['name'] for k in ['سرخ‌کن', 'سرخ کن', 'آون توستر', 'توستر', 'اسپرسوساز', 'اسپرسو ساز', 'خردکن']),
        "headline": "انواع سرخ‌کن بدون روغن، آون توستر و اسپرسوساز (دونالکس و لمروتی)",
        "models_summary": [
            "سرخ‌کن بدون روغن ۸ لیتری دونالکس مدل DN-950 و DN-955 دیجیتال",
            "سرخ‌کن ۶ لیتری دونالکس مدل DN-965 با سبد نچسب تفلون",
            "اسپرسوساز ۲۰ بار دونالکس مدل DN-475 و DN-480 پمپ ایتالیایی",
            "ست صبحانه و خردکن پیرکس لمروتی (Lamroti)"
        ],
        "specs": [
            "پخت سالم و رژیمی با کاهش ۹۰ درصدی مصرف روغن",
            "المنت‌های حرارتی پیشرفته با قابلیت تنظیم حرارت و تایمر هوشمند",
            "طراحی بسیار مدرن استیل و مشکی برای دکوراسیون آشپزخانه",
            "گارانتی و تضمین کیفیت کالا"
        ]
    },
    {
        "id": "20_grooming_shaver",
        "folder": "20_ماشین_اصلاح_و_ریش_تراش",
        "title": "ماشین اصلاح و خط زن پرو امگا اهواز",
        "divar_cat": "زیبایی و سلامت > اصلاح و پیرایش",
        "canonical_cat": "https://hosseinykala.ir/product-category/personal-health-and-beauty/hair-clipper/",
        "filter": lambda p: any(k in p['name'] for k in ['اصلاح', 'ریش تراش', 'شیور', 'خط زن']),
        "headline": "انواع ست ماشین اصلاح مو و خط‌زن شارژی (پرو امگا و پرومارون)",
        "models_summary": [
            "ست ماشین اصلاح ۵ کاره پرو امگا مدل T8 بدنه تمام فلزی",
            "ماشین اصلاح و خط‌زن صفرزن پرو امگا مدل T7 با تیغه تیتانیوم",
            "شیور چندکاره پرومارون ضدآب مدل RL-614"
        ],
        "specs": [
            "باتری لیتیومی پرقدرت با شارژ سریع و نگهداری شارژ طولانی‌مدت",
            "تیغه‌های خودتیزشونده از جنس استیل ضدزنگ و تیتانیوم",
            "مناسب استفاده شخصی و سالن‌های آرایشگاهی",
            "گارانتی اصالت و مهلت تست"
        ]
    }
]

print(f"Starting extraction for {len(ads_config)} ad folders...")

stats = []

for idx, ac in enumerate(ads_config):
    folder_path = os.path.join(base_dir, ac['folder'])
    images_dir = os.path.join(folder_path, "images")
    os.makedirs(images_dir, exist_ok=True)
    
    # Find matching products
    matched_prods = [p for p in products if ac['filter'](p)]
    
    # Download images
    downloaded_imgs = []
    for p in matched_prods:
        img_url = p.get('featured_image')
        if img_url:
            slug = p.get('slug', 'product')
            ext = os.path.splitext(img_url.split('?')[0])[-1]
            if not ext or len(ext) > 5:
                ext = ".jpg"
            img_filename = f"{slug}{ext}"
            img_dest = os.path.join(images_dir, img_filename)
            ok = download_image(img_url, img_dest)
            if ok:
                downloaded_imgs.append(img_filename)
                
    # Build models bullet points with site URLs
    models_text_lines = []
    for m in ac['models_summary']:
        models_text_lines.append(f"• {m}")
        
    specs_text_lines = []
    for s in ac['specs']:
        specs_text_lines.append(f"✓ {s}")
        
    site_product_links = []
    for p in matched_prods[:6]:
        p_name = p['name']
        p_link = f"https://hosseinykala.ir/product/{p['slug']}/"
        site_product_links.append(f"- {p_name}: {p_link}")

    # Generate ad copy text strictly following user constraints:
    # 1. Price fluctuation warning
    # 2. Short, punchy, humanized
    # 3. No exact fixed price
    # 4. Under title char limit
    
    ad_copy = f"""═══════════════════════════════════════════════════════════════
📌 راهنمای ثبت آگهی در دیوار: {ac['title']}
═══════════════════════════════════════════════════════════════

【 عنوان آگهی دیوار (تعداد کاراکتر: {len(ac['title'])} کاراکتر) 】
{ac['title']}

【 دسته‌بندی پیشنهادی دیوار 】
{ac['divar_cat']}

【 فیلد قیمت در دیوار 】
توافقی (یا درج قیمت کف دسته)

───────────────────────────────────────────────────────────────
📝 متن کامل آگهی جهت کپی در دیوار:
───────────────────────────────────────────────────────────────

⭐ {ac['headline']} - فروش نقد و اقساطی در اهواز ⭐

اگر به دنبال خرید مطمئن با گارانتی معتبر شرکتی و اصالت کالا هستید، در فروشگاه لوازم خانگی حسینی تمامی مدل‌های روز آماده تحویل به مشتریان عزیز می‌باشد.

⚠️ توجه مهم:
به دلیل نوسانات روزانه بازار، قیمت‌ها متغیر بوده و قیمت قطعی محسوب نمی‌شود؛ لطفاً جهت استعلام قیمت دقیق روز و اطلاع از موجودی لحظه‌ای کالاها حتماً تماس بگیرید یا در چت دیوار پیام دهید.

🔹 مدل‌های موجود و قابل سفارش:
{chr(10).join(models_text_lines)}

✨ ویژگی‌ها و مشخصات فنی برجسته:
{chr(10).join(specs_text_lines)}

🎁 مزایای خرید از فروشگاه لوازم خانگی حسینی:
✅ شرایط ویژه فروش اقساطی (با چک صیادی یا بدون ضامن در اهواز)
✅ گارانتی رسمی و معتبر شرکتی با ضمانت سلامت و اصالت کالا
✅ امکان مراجعه و بازدید حضوری در شووروم فروشگاه اهواز
✅ ارسال سریع و امن به سراسر استان خوزستان

📍 آدرس مراجعه حضوری:
اهواز، خیابان نادری، فروشگاه لوازم خانگی حسینی

🌐 مشاهده کاتالوگ آنلاین و بررسی مشخصات در سایت:
دسته‌بندی اصلی: {ac['canonical_cat']}

📞 جهت مشاوره رایگان، استعلام موجودی و شرایط اقساط تماس بگیرید یا پیام دهید.
"""

    # Save to ad_content.txt and README.md
    with open(os.path.join(folder_path, "ad_content.txt"), 'w', encoding='utf-8') as f:
        f.write(ad_copy)
        
    with open(os.path.join(folder_path, "README.md"), 'w', encoding='utf-8') as f:
        f.write(ad_copy)
        
    stats.append({
        "folder": ac['folder'],
        "title": ac['title'],
        "title_len": len(ac['title']),
        "images_count": len(downloaded_imgs),
        "products_matched": len(matched_prods)
    })
    print(f"[{idx+1:02d}/20] {ac['folder']}: {len(downloaded_imgs)} images downloaded, ad copy saved.")

with open(os.path.join(base_dir, "summary.json"), 'w', encoding='utf-8') as f:
    json.dump(stats, f, ensure_ascii=False, indent=2)

print("\nAll 20 ad folders and assets generated successfully!")

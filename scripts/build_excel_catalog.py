"""
build_excel_catalog.py
======================
مرحله ۱: Crawler - واکشی اطلاعات کامل محصولات از سایت hosseinykala.ir
مرحله ۲: Matcher - تطابق لیست ۱۸۰ محصول کاربر با داده‌های سایت
مرحله ۳: Excel Builder - ایجاد فایل اکسل با شیت‌های جداگانه برای هر دسته‌بندی

ویژگی‌ها:
- شناسایی محصولات متغیر (variable products) در مقابل ساده (simple)
- هر variation در یک ردیف جداگانه
- قابلیت به‌روزرسانی دوطرفه قیمت‌ها
- استفاده از شناسه عددی ?p=ID برای جلوگیری از 404 فارسی
"""

import os
import sys
import json
import time
import re
import urllib.parse
import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from difflib import SequenceMatcher
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# =========================================================
# تنظیمات کلی
# =========================================================
BASE_URL = "https://hosseinykala.ir"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'fa-IR,fa;q=0.9,en-US;q=0.8',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
OUTPUT_DIR = os.path.dirname(os.path.dirname(__file__))
RAW_DATA_FILE = os.path.join(DATA_DIR, 'products_raw.json')
MATCHED_FILE = os.path.join(DATA_DIR, 'products_matched.json')
EXCEL_OUTPUT = os.path.join(OUTPUT_DIR, 'hosseiny_kala_catalog.xlsx')

# =========================================================
# لیست ۱۸۰ محصول کاربر
# =========================================================
USER_PRODUCT_LIST = [
    "ال ای دی هاورسون ۷۵ اینچ",
    "لباسشویی کلور مدل 9771 سفید",
    "Panasonic MC CG715 2100W",
    "آب سردکن افترون رومیزی",
    "آبسردکن هانو",
    "آبسردکن نیکایی مدل ۱۱۲۰۶ ایستاده",
    "آبگرمکن الکترواستیل مخزندار دیواری",
    "آبمیوهگیری جنرال ۶۰۷ غذاساز",
    "آسیاب کاستلو ۲۷۰",
    "آبمیوهگیر دونالکس ۴ کاره ۱۲۰",
    "آبمیوهگیر دونالکس ۴ کاره ۱۱۰",
    "اپیلاتور پرومارون ۵ کاره ۶۱۴",
    "اتو دونالکس ۸۱۵",
    "اتو فیلیپس ۵۰۴۰",
    "اتو مو Baby3383A",
    "اتو مو پاناسونیک HV11",
    "اتوماتیک دوو کینو ۹۰۵ سینیور",
    "اتومو پرومارون ۱۱۱۵",
    "اتومو پرومارون ۱۱۱۶",
    "اسپرسوساز دونالکس ۳۸۰",
    "اسپرسوساز دونالکس ۳۷۵",
    "اسپرسوساز نارنجی گرنویک",
    "اسپایپ ونتو",
    "ال ای دی ۳۲ Averson",
    "ال ای دی ۸۵ Averson",
    "ال ای دی ۶۵ اینچ هاورسون",
    "ال ای دی هاورسون ۵۵ پنرست",
    "بخاری گلدن لوکس",
    "بخاری پارس خزر فندار FH-2000P",
    "بخاری پلار 32-067 شیشه‌ای",
    "پتوشور پاکیزان ۲۰ کیلو",
    "پتوشور پاکیزان ۴۰ کیلو",
    "پرومارون برس حرارتی ۱۱۳",
    "پلوپز پارس خزر ۸ نقره",
    "پلوپز پارس خزر مدل ۳۶۱",
    "پنکه پایه‌بلند 1455",
    "پنکه پارس خزر پایه‌بلند",
    "پنکه پاناسونیک ۲ حالته",
    "پنکه سانی ۷۶۰۰",
    "پنکه سانی مدل ۲۰۱۳ ساده",
    "تابه اویز سایز ۳۰",
    "تابه اویز سایز ۲۲ مشکی",
    "تابه اویز سایز ۲۲ فوم مشکی دربدار",
    "تابه اویز سایز ۲۶",
    "تصفیه آب سافت واتر ۶ مرحله",
    "تصفیه آب وست 5515",
    "تصفیه آب هومگلد",
    "تصفیه آب C.C.K",
    "توستر ۶۰ لیتر",
    "توستر ناندلمونتی ۵۸",
    "توستر وستینگهاوس ۲۷",
    "توستر وستینگهاوس کرم",
    "جاروبرقی آراز ۲۰ لیتر",
    "جاروبرقی هیتاچی سطلی ۱۲۰۰",
    "جاروبرقی دونالکس ۷۵۰ سورمه‌ای",
    "جاروبرقی دونالکس ۷۷۰",
    "جاروبرقی کلور سطلی",
    "جاروبرقی BOST سطلی",
    "چایساز دونالکس ۱۸۵ مشکی",
    "چایساز زامروتی",
    "چایساز ساورر گرنویک",
    "چایساز کُرکماز A331",
    "دستگاه پیرایش سیمی صورت ۷۲۱",
    "ریشتراش پرومارون ۷۰۶",
    "زودپز اویزپلاس تک‌قلو مشکی رزگلد",
    "زودپز اویزپلاس دوقلو مشکی رزگلد",
    "ساندویچ‌ساز دونالکس ۴۰۹ سفید",
    "ساندویچ‌ساز دونالکس ۴۹۰ مشکی",
    "سبزی خردکن KENRA",
    "سبزی خردکن نیکا ۲ کیلویی",
    "سرخکن دونالکس",
    "سرخکن ایرفرایر خاکستری گرنویک",
    "سرخکن دونالکس ۱۹۵۰ استیل",
    "سرویس خمره قابلمه اویز کرم‌سلین",
    "سرویس قابلمه استیل ۱۰ پارچه",
    "سرویس قابلمه اویز ۱۰ پارچه سرمه‌ای",
    "سرویس قابلمه اویزپلاس ۱۰ پارچه اناری",
    "سرویس قابلمه اویزپلاس ۱۲ پارچه مشکی",
    "سرویس قابلمه اویزپلاس ۱۲ پارچه سبز",
    "سرویس قابلمه اویزپلاس ویولا ۱۱ پارچه",
    "سشوار امگا ۲۰۰۰ وات",
    "سشوار پروامگا ۲۲۰۰ وات",
    "شیرجوش مشکی اویزپلاس",
    "ظرفشویی انفره استیل",
    "ظرفشویی انفره لمسی استیل",
    "غذاساز فیلیپس ۷۷۷۸",
    "فر الکترواستیل تیتانیوم ۱۱",
    "فر الکترواستیل عرض ۶۰ چرمی ۲۱",
    "فر توکار آلتون ۷۳۰۳",
    "فرکننده مو پرومارون ۴+",
    "فرگاز آلتون MPS",
    "فرگاز آلتون MD5W",
    "فریزر صندوقی الکتروسان ۳۴۵",
    "فریزر کلور ۶۰ روسوپلاس سفید",
    "فریزر کلور ۶۰ روسوپلاس استیل",
    "فریزر کلور ۶۰ گلوریا استیل",
    "فریزر کلور ۷۰ روسو آبریزا استیل",
    "فریزر کلور ۷۰ گلوریاپلاس سفید",
    "فریزر کلور ۲۷ سفید کره‌ای ۱۰۱",
    "فریزر هیمالیا آیسپول استیل 60MW",
    "فریزر هیمالیا آیسپول چرم 60MW",
    "قابلمه اویز سایز ۲۰ مشکی",
    "قابلمه اویز سایز ۲۰ مشکی",
    "قابلمه اویز سایز ۲۲ مشکی",
    "قابلمه اویز سایز ۲۲ مشکی",
    "قابلمه اویز سایز ۲۴ مشکی",
    "قابلمه اویز سایز ۱۶ مشکی",
    "قابلمه اویز سایز ۲۶ مشکی",
    "قابلمه اویز سایز ۱۸ مشکی",
    "قابلمه مرغخوری اویزپلاس مشکی",
    "کتری برقی اریکسون",
    "کتری برقی تک زامروتی کرم",
    "کتری برقی سانی ۱.۵ لیتر",
    "کتری برقی وگاتی توپی",
    "کتری برقی وستینگهاوس آبی",
    "کتری برقی وستینگهاوس کرم",
    "کتری برقی پروکس",
    "کتری و قوری زامروتی دسته استیل ۲۰۲۲",
    "کتری و قوری زامروتی دسته چوب ۲۰۲۲",
    "کتری و قوری مدل هرمی تمام‌طلا ۶۰۴",
    "کسورات اضافات کالا",
    "کولر آبی مدل ۴۵۰۰",
    "کولر آبی اوناکس 150L",
    "کولر آبی اوناکس B35",
    "کولر پنجره‌ای اوجنرال ۱۸ هزار",
    "کولر آبی ریتون",
    "کولر وستینگهاوس ۲۰ کوپلند",
    "گاز صفحه‌ای آلتون استیل S517",
    "گاز صفحه‌ای آلتون استیل SG518",
    "گوشتکوب دونالکس ۲۷۵",
    "گوشتکوب و غذاساز دونالکس ۱۹۹۰",
    "لباسشویی ۱۷ دوقلو ریتون",
    "لباسشویی دوقلو پاکشوما هاک",
    "لباسشویی ۸ کلور لمسی سفید 8TW1",
    "لباسشویی ۹ کلور لمسی سفید 9TW1",
    "لباسشویی اتوماتیک دوو 991S",
    "لباسشویی درب بالا پاکشوما ۱۲",
    "لباسشویی دوقلو ۲۱ کیلو پاکشوما",
    "لباسشویی کلور ۹ لمسی اینوکس 9TI1",
    "لباسشویی کلور ۹ کیلویی کرمی",
    "لباسشویی کلور ۹ کیلویی لمسی اینوکس",
    "لباسشویی کلور ۹ کیلویی سفید ویوا",
    "ماشین اصلاح پروامگا تک",
    "ماشین اصلاح پروامگا ۴ کاره",
    "ماشین اصلاح پروامگا شارژی و برقی",
    "مخلوطکن زامروتی کرم",
    "مخلوطکن و آسیاب دونالکس ۲۰۵",
    "مخلوطکن وستینگهاوس آبی",
    "مخلوطکن وستینگهاوس کرم",
    "همزن اوریکس کاسه چرخدار",
    "همزن کنوود ۴۳۰",
    "همزن دستی دونالکس ۳۵۵",
    "همزن وستینگهاوس آبی",
    "همزن وستینگهاوس کرم",
    "هود آلتون H312",
    "هود آلتون H315B",
    "یخچال فریزر BOST",
    "یخچال فریزر ۳۲ دیپوینت استیل T7",
    "یخچال فریزر دیپوینت سفید T7",
    "یخچال فریزر دیپوینت استیل Dipoent",
    "یخچال کلور مینی سبز پاستیلی",
    "یخچال الکترواستیل سفید ES21-FUTUR",
    "یخچال الکترواستیل یخساز تیتانیوم",
    "یخچال ایستکول فوت سفید",
    "یخچال ایستکول فوت نوک مدادی",
    "یخچال ایستکول فوت سفید",
    "یخچال ایستکول فوت نوک مدادی",
    "یخچال فریزر کلور روسو سفید",
    "یخچال فریزر کلور گلوریاپلاس سفید",
    "یخچال فریزر کلور ۱۰۱ کمبی سفید ساده",
    "یخچال فریزر کلور روسو مومبارا استیل",
    "یخچال کلور ۶۰ روسوپلاس استیل",
    "یخچال کلور ۶۰ روسوپلاس سفید",
    "یخچال کلور ۶۰ گلوریا استیل",
    "یخچال کلور روسوپلاس استیل",
    "یخچال کلور گلوریاپلاس سفید",
    "یخچال کلور ۲۷ سفید کره‌ای ۱۰۱",
    "یخچال فریزر R(re01)",
    "یخچال هیمالیا آیسپول استیل 60MW",
    "یخچال هیمالیا آیسپول چرم 60MW",
]

# =========================================================
# نقشه دسته‌بندی محصولات - بر اساس شیت‌های اکسل
# =========================================================
SHEET_CATEGORIES = {
    "یخچال و فریزر": {
        "keywords": ["یخچال", "فریزر", "refrigerator", "freezer"],
        "subcats": {
            "کلور": ["کلور"],
            "دیپوینت": ["دیپوینت", "depoint"],
            "ایستکول": ["ایستکول", "eastcool"],
            "الکترواستیل": ["الکترواستیل", "electrosteel"],
            "هیمالیا": ["هیمالیا", "himalaya"],
            "BOST": ["bost", "بست"],
            "الکتروسان": ["الکتروسان"],
        }
    },
    "ماشین لباسشویی": {
        "keywords": ["لباسشویی", "پتوشور", "washing machine"],
        "subcats": {
            "کلور": ["کلور"],
            "دوو": ["دوو", "daewoo"],
            "پاکشوما": ["پاکشوما"],
            "ریتون": ["ریتون", "rayton"],
        }
    },
    "جاروبرقی": {
        "keywords": ["جاروبرقی", "vacuum"],
        "subcats": {
            "کلور": ["کلور"],
            "BOST": ["bost", "بست"],
            "هیتاچی": ["هیتاچی", "hitachi"],
            "دونالکس": ["دونالکس"],
            "آراز": ["آراز"],
        }
    },
    "کولر آبی": {
        "keywords": ["کولر آبی", "کولر گازی", "کولر پنجره", "water cooler", "air cooler"],
        "subcats": {
            "ریتون": ["ریتون"],
            "اوناکس": ["اوناکس"],
            "وستینگهاوس": ["وستینگهاوس"],
            "اوجنرال": ["اوجنرال"],
        }
    },
    "ماشین ظرفشویی": {
        "keywords": ["ظرفشویی", "dishwasher"],
        "subcats": {
            "انفره": ["انفره"],
            "کلور": ["کلور"],
        }
    },
    "تصفیه آب": {
        "keywords": ["تصفیه آب", "water purifier"],
        "subcats": {
            "سافت واتر": ["سافت واتر"],
            "وست": ["وست"],
            "هومگلد": ["هومگلد"],
            "CCK": ["c.c.k", "cck"],
        }
    },
    "لوازم آشپزخانه": {
        "keywords": ["اسپرسوساز", "توستر", "پلوپز", "ساندویچ‌ساز", "ساندویچساز",
                     "سرخکن", "غذاساز", "آبمیوه", "مخلوطکن", "همزن", "گوشتکوب",
                     "چایساز", "کتری", "کتری برقی", "شیرجوش", "زودپز", "سبزی خردکن",
                     "آسیاب", "espresso", "toaster", "blender", "mixer"],
        "subcats": {
            "دونالکس": ["دونالکس"],
            "گرنویک": ["گرنویک"],
            "وستینگهاوس": ["وستینگهاوس"],
            "زامروتی": ["زامروتی"],
            "سانی": ["سانی"],
            "اویزپلاس": ["اویزپلاس"],
            "فیلیپس": ["فیلیپس"],
            "کرکماز": ["کرکماز"],
            "کنوود": ["کنوود"],
            "اوریکس": ["اوریکس"],
        }
    },
    "ظروف": {
        "keywords": ["قابلمه", "تابه", "سرویس قابلمه", "سرویس خمره", "cookware"],
        "subcats": {
            "اویز": ["اویز"],
            "اویزپلاس": ["اویزپلاس"],
            "استیل": ["استیل ۱۰ پارچه"],
        }
    },
    "لوازم شخصی": {
        "keywords": ["سشوار", "اتو مو", "فرکننده مو", "برس حرارتی", "ماشین اصلاح",
                     "اپیلاتور", "ریشتراش", "دستگاه پیرایش", "hair dryer"],
        "subcats": {
            "پروامگا": ["پروامگا"],
            "پرومارون": ["پرومارون"],
            "امگا": ["امگا"],
        }
    },
    "گاز و هود": {
        "keywords": ["گاز صفحه‌ای", "گاز صفحهای", "فرگاز", "فر توکار", "فر الکترواستیل", "هود", "gas", "hood"],
        "subcats": {
            "آلتون": ["آلتون"],
            "الکترواستیل": ["الکترواستیل"],
        }
    },
    "سایر": {
        "keywords": [],  # پیش‌فرض
        "subcats": {}
    }
}

# =========================================================
# مرحله ۱: واکشی اطلاعات محصولات از سایت
# =========================================================

def fetch_url(url, retries=3, delay=2):
    """واکشی URL با retry"""
    for i in range(retries):
        try:
            r = requests.get(url, headers=HEADERS, timeout=30)
            if r.status_code == 200:
                return r
            elif r.status_code == 429:
                time.sleep(delay * 2)
        except Exception as e:
            if i == retries - 1:
                print(f"  [FAIL] {url}: {e}", flush=True)
            time.sleep(delay)
    return None


def crawl_category_page(url):
    """واکشی URLهای محصول از یک صفحه دسته‌بندی (تمام صفحات)"""
    found_urls = set()
    page = 1
    while True:
        page_url = f"{url}page/{page}/" if page > 1 else url
        r = fetch_url(page_url)
        if not r:
            break
        soup = BeautifulSoup(r.text, 'html.parser')
        found = 0
        for a in soup.find_all('a', href=True):
            href = a['href']
            if '/product/' in href:
                clean_href = href.split('?')[0].rstrip('/') + '/'
                if '/product-category/' not in clean_href and clean_href not in found_urls:
                    found_urls.add(clean_href)
                    found += 1
        if found == 0:
            break
        page += 1
    return found_urls


def get_all_product_urls():
    """دریافت تمام URLهای محصولات از sitemap و صفحات دسته‌بندی (موازی)"""
    print("\n[STEP 1] Collecting all product URLs...", flush=True)
    product_urls = set()

    # از sitemap
    r = fetch_url(f"{BASE_URL}/product-sitemap.xml")
    if r:
        root = ET.fromstring(r.content)
        for child in root:
            for elem in child:
                if elem.tag.endswith('loc') and '/product/' in elem.text:
                    product_urls.add(elem.text.rstrip('/') + '/')
    print(f"  Sitemap: {len(product_urls)} products", flush=True)

    # لیست صفحات دسته‌بندی
    cat_urls = [
        f"{BASE_URL}/shop/",
        f"{BASE_URL}/product-category/%db%8c%d8%ae%da%86%d8%a7%d9%84-%d9%81%d8%b1%db%8c%d8%b2%d8%b1/",
        f"{BASE_URL}/product-category/%d9%85%d8%a7%d8%b4%db%8c%d9%86-%d9%84%d8%a8%d8%a7%d8%b3%d8%b4%d9%88%db%8c%db%8c/",
        f"{BASE_URL}/product-category/%d8%ac%d8%a7%d8%b1%d9%88%d8%a8%d8%b1%d9%82%db%8c/",
        f"{BASE_URL}/product-category/%da%a9%d9%88%d9%84%d8%b1-%d8%a2%d8%a8%db%8c/",
        f"{BASE_URL}/product-category/%d9%85%d8%a7%d8%b4%db%8c%d9%86-%d8%b8%d8%b1%d9%81%d8%b4%d9%88%db%8c%db%8c/",
        f"{BASE_URL}/product-category/%d8%aa%d8%b5%d9%81%db%8c%d9%87-%da%a9%d9%86%d9%86%d8%af%d9%87-%d8%a2%d8%a8/",
        f"{BASE_URL}/product-category/%d8%a7%d8%b3%d9%be%d8%b1%d8%b3%d9%88-%d8%b3%d8%a7%d8%b2/",
        f"{BASE_URL}/product-category/%d8%a7%d8%aa%d9%88/",
        f"{BASE_URL}/product-category/%d8%b3%d8%b1%d8%ae-%da%a9%d9%86/",
        f"{BASE_URL}/product-category/%d8%b3%d8%b4%d9%88%d8%a7%d8%b1/",
        f"{BASE_URL}/product-category/%d9%85%d8%ae%d9%84%d9%88%d8%b7-%da%a9%d9%86/",
        f"{BASE_URL}/product-category/%da%af%d9%88%d8%b4%d8%aa-%da%a9%d9%88%d8%a8-%d8%a8%d8%b1%d9%82%db%8c/",
        f"{BASE_URL}/product-category/%d8%a2%d8%a8%d9%85%db%8c%d9%88%d9%87-%da%af%db%8c%d8%b1%db%8c/",
        f"{BASE_URL}/product-category/%d8%a7%d8%b5%d9%84%d8%a7%d8%ad-%d9%85%d9%88%db%8c-%d8%b3%d8%b1/",
        f"{BASE_URL}/product-category/%d8%a7%d8%b5%d9%84%d8%a7%d8%ad-%d9%85%d9%88%db%8c-%d8%b5%d9%88%d8%b1%d8%aa/",
    ]

    # crawl موازی
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(crawl_category_page, url): url for url in cat_urls}
        for future in as_completed(futures):
            url = futures[future]
            try:
                found = future.result()
                added = len(found - product_urls)
                product_urls.update(found)
                short_url = url.split('product-category/')[-1].rstrip('/')[:30] if 'product-category' in url else 'shop'
                print(f"  Category {short_url}: +{added} products", flush=True)
            except Exception as e:
                print(f"  [WARN] Failed: {e}", flush=True)

    print(f"  Total unique product URLs: {len(product_urls)}", flush=True)
    return list(product_urls)


def parse_price(price_str):
    """تبدیل قیمت متنی به عدد"""
    if not price_str:
        return None
    # حذف کاراکترهای غیر عددی (نگه‌داشتن اعداد فارسی و انگلیسی)
    cleaned = re.sub(r'[^\d۰-۹]', '', str(price_str))
    # تبدیل اعداد فارسی
    fa_to_en = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
    cleaned = cleaned.translate(fa_to_en)
    try:
        return int(cleaned) if cleaned else None
    except:
        return None


def extract_product_data(url):
    """استخراج اطلاعات کامل محصول از صفحه"""
    r = fetch_url(url)
    if not r:
        return None

    soup = BeautifulSoup(r.text, 'html.parser')

    data = {
        'url': url,
        'product_id': None,
        'shortlink': None,
        'name': '',
        'type': 'simple',  # simple | variable
        'categories': [],
        'price_regular': None,
        'price_sale': None,
        'in_stock': True,
        'sku': '',
        'variations': [],
        'attributes': {}
    }

    # استخراج product ID از body class
    body = soup.find('body')
    if body:
        for cls in body.get('class', []):
            m = re.search(r'postid-(\d+)', cls)
            if m:
                data['product_id'] = int(m.group(1))
                data['shortlink'] = f"https://hosseinykala.ir/?p={m.group(1)}"
                break

    # نام محصول
    h1 = soup.find('h1', class_='product_title') or soup.find('h1')
    if h1:
        data['name'] = h1.get_text(strip=True)

    # دسته‌بندی
    cat_elem = soup.find('span', class_='posted_in')
    if cat_elem:
        for a in cat_elem.find_all('a'):
            data['categories'].append(a.get_text(strip=True))

    # SKU
    sku_elem = soup.find('span', class_='sku')
    if sku_elem:
        data['sku'] = sku_elem.get_text(strip=True)

    # بررسی محصول متغیر
    variation_form = soup.find('form', class_='variations_form')
    if variation_form:
        data['type'] = 'variable'

        # واریاسیون‌ها از JSON داخل صفحه
        product_variations_json = variation_form.get('data-product_variations')
        if product_variations_json:
            try:
                variations_data = json.loads(product_variations_json)
                for v in variations_data:
                    var = {
                        'variation_id': v.get('variation_id'),
                        'attributes': v.get('attributes', {}),
                        'price_regular': parse_price(v.get('display_price')),
                        'price_sale': parse_price(v.get('display_regular_price')) if v.get('display_regular_price') != v.get('display_price') else None,
                        'in_stock': v.get('is_in_stock', True),
                        'sku': v.get('sku', ''),
                        'shortlink': f"https://hosseinykala.ir/?p={v.get('variation_id')}" if v.get('variation_id') else None,
                    }
                    # پاکسازی attribute keys
                    clean_attrs = {}
                    for k, val in var['attributes'].items():
                        clean_key = k.replace('attribute_', '').replace('pa_', '')
                        clean_attrs[clean_key] = val
                    var['attributes'] = clean_attrs
                    data['variations'].append(var)
            except Exception as e:
                print(f"  [WARN] Could not parse variations for {url}: {e}", flush=True)

    # قیمت برای محصولات ساده
    price_elem = soup.find('p', class_='price')
    if price_elem:
        ins_elem = price_elem.find('ins')
        del_elem = price_elem.find('del')
        if ins_elem:
            data['price_sale'] = parse_price(ins_elem.get_text(strip=True))
            if del_elem:
                data['price_regular'] = parse_price(del_elem.get_text(strip=True))
        else:
            amount = price_elem.find('span', class_='woocommerce-Price-amount')
            if amount:
                data['price_regular'] = parse_price(amount.get_text(strip=True))

    # موجودی
    stock_elem = soup.find('p', class_='stock')
    if stock_elem and 'out-of-stock' in stock_elem.get('class', []):
        data['in_stock'] = False

    # JSON-LD برای اطلاعات بیشتر
    for script in soup.find_all('script', type='application/ld+json'):
        try:
            ld = json.loads(script.string or '{}')
            graph = ld.get('@graph', [ld]) if isinstance(ld, dict) else ld
            for item in graph:
                if isinstance(item, dict) and item.get('@type') == 'Product':
                    if not data['name'] and item.get('name'):
                        data['name'] = item['name']
                    if not data['sku'] and item.get('sku'):
                        data['sku'] = str(item['sku'])
                    offers = item.get('offers')
                    if offers and data['type'] == 'simple':
                        if isinstance(offers, list):
                            offers = offers[0]
                        if isinstance(offers, dict):
                            if not data['price_regular']:
                                data['price_regular'] = parse_price(offers.get('price'))
                            avail = offers.get('availability', '')
                            if 'OutOfStock' in avail:
                                data['in_stock'] = False
        except:
            pass

    return data


def fetch_all_products(urls):
    """واکشی موازی اطلاعات محصولات"""
    print(f"\n[STEP 2] Fetching data for {len(urls)} product pages...", flush=True)
    products = []
    total = len(urls)

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(extract_product_data, url): url for url in urls}
        done = 0
        for future in as_completed(futures):
            done += 1
            result = future.result()
            if result:
                products.append(result)
            if done % 10 == 0 or done == total:
                print(f"  Progress: {done}/{total} ({len(products)} successful)", flush=True)
            time.sleep(0.2)

    return products


# =========================================================
# مرحله ۲: تطابق محصولات
# =========================================================

def normalize_text(text):
    """نرمال‌سازی متن فارسی برای مقایسه"""
    text = text.strip()
    # یکپارچه‌سازی کاراکترهای فارسی
    text = text.replace('ي', 'ی').replace('ك', 'ک').replace('ة', 'ه')
    # حذف نشانه‌گذاری‌های مازاد
    text = re.sub(r'[\u200c\u200d]', '', text)  # Zero-width chars
    text = re.sub(r'\s+', ' ', text)
    # تبدیل اعداد فارسی به انگلیسی
    fa_to_en = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
    text = text.translate(fa_to_en)
    return text.lower()


def similarity_score(a, b):
    """محاسبه شباهت دو رشته"""
    return SequenceMatcher(None, normalize_text(a), normalize_text(b)).ratio()


def match_product(user_name, site_products):
    """تطابق محصول کاربر با محصولات سایت"""
    best_match = None
    best_score = 0

    for prod in site_products:
        score = similarity_score(user_name, prod['name'])
        if score > best_score:
            best_score = score
            best_match = prod

    return best_match, best_score


def determine_sheet_and_subcat(product_name, categories):
    """تعیین شیت و زیردسته‌بندی"""
    name_lower = normalize_text(product_name)
    cats_lower = [normalize_text(c) for c in categories]
    all_text = name_lower + ' ' + ' '.join(cats_lower)

    for sheet_name, sheet_info in SHEET_CATEGORIES.items():
        if sheet_name == "سایر":
            continue
        for kw in sheet_info['keywords']:
            if normalize_text(kw) in all_text:
                # تعیین زیردسته
                for subcat, subkws in sheet_info['subcats'].items():
                    for skw in subkws:
                        if normalize_text(skw) in all_text:
                            return sheet_name, subcat

                return sheet_name, ""

    return "سایر", ""


def build_matched_products(user_list, site_products):
    """ساخت لیست محصولات تطابق یافته"""
    print(f"\n[STEP 3] Matching {len(user_list)} user products with {len(site_products)} site products...", flush=True)

    matched = []
    unmatched = []
    MATCH_THRESHOLD = 0.45

    for idx, user_name in enumerate(user_list):
        # محصولاتی که در لیست کاربر کلا محصول نیستند
        if user_name in ["کسورات اضافات کالا"]:
            matched.append({
                'user_name': user_name,
                'matched': False,
                'note': 'سطر غیر محصول',
                'sheet': 'سایر',
                'category_path': 'سایر',
            })
            continue

        best_match, score = match_product(user_name, site_products)

        if best_match and score >= MATCH_THRESHOLD:
            sheet, subcat = determine_sheet_and_subcat(
                user_name,
                best_match.get('categories', [])
            )
            cat_path = f"{sheet}/{subcat}" if subcat else sheet

            entry = {
                'user_name': user_name,
                'matched': True,
                'match_score': round(score, 2),
                'product_id': best_match.get('product_id'),
                'shortlink': best_match.get('shortlink') or best_match.get('url'),
                'name': best_match.get('name'),
                'type': best_match.get('type', 'simple'),
                'sku': best_match.get('sku', ''),
                'categories': best_match.get('categories', []),
                'sheet': sheet,
                'subcategory': subcat,
                'category_path': cat_path,
                'price_regular': best_match.get('price_regular'),
                'price_sale': best_match.get('price_sale'),
                'in_stock': best_match.get('in_stock', True),
                'variations': best_match.get('variations', []),
            }
            matched.append(entry)
        else:
            sheet, subcat = determine_sheet_and_subcat(user_name, [])
            cat_path = f"{sheet}/{subcat}" if subcat else sheet
            matched.append({
                'user_name': user_name,
                'matched': False,
                'match_score': round(score, 2) if best_match else 0,
                'sheet': sheet,
                'category_path': cat_path,
                'note': f'یافت نشد (score={score:.2f})'
            })
            unmatched.append(user_name)

    print(f"  Matched: {len([m for m in matched if m.get('matched')])}", flush=True)
    print(f"  Unmatched: {len(unmatched)}", flush=True)
    if unmatched:
        print("  Unmatched products:", flush=True)
        for u in unmatched:
            print(f"    - {u}", flush=True)

    return matched


# =========================================================
# مرحله ۳: ایجاد فایل اکسل
# =========================================================

# رنگ‌های استایل
COLORS = {
    'header_bg': 'FF2C3E50',
    'header_font': 'FFFFFFFF',
    'variable_bg': 'FFEAF4FB',
    'variation_bg': 'FFDBEAFE',
    'simple_bg': 'FFFFFFFF',
    'unmatched_bg': 'FFFFF3CD',
    'in_stock': 'FF27AE60',
    'out_of_stock': 'FFE74C3C',
    'alt_row': 'FFF8F9FA',
    'subcat_bg': 'FFD5E8D4',
    'subcat_font': 'FF1E8449',
}

COLUMNS = [
    ('product_id', 'شناسه محصول (ID)', 15),
    ('variation_id', 'شناسه واریاسیون', 15),
    ('user_name', 'نام در لیست', 35),
    ('name', 'نام در سایت', 40),
    ('type', 'نوع محصول', 12),
    ('attribute_name', 'ویژگی متغیر', 18),
    ('attribute_value', 'مقدار ویژگی', 18),
    ('category_path', 'دسته‌بندی', 25),
    ('shortlink', 'لینک محصول', 40),
    ('price_regular', 'قیمت عادی', 18),
    ('price_sale', 'قیمت حراج', 18),
    ('in_stock', 'وضعیت موجودی', 15),
    ('sku', 'کد SKU', 18),
    ('match_score', 'دقت تطابق', 12),
    ('notes', 'یادداشت', 25),
]


def make_header_style():
    return {
        'font': Font(bold=True, color=COLORS['header_font'], size=11, name='Calibri'),
        'fill': PatternFill(fill_type='solid', fgColor=COLORS['header_bg']),
        'alignment': Alignment(horizontal='center', vertical='center', wrap_text=True),
        'border': Border(
            bottom=Side(style='thin', color='FFAAAAAA')
        )
    }


def apply_style(cell, style_dict):
    for attr, val in style_dict.items():
        setattr(cell, attr, val)


def write_header(ws, col_defs):
    header_style = make_header_style()
    ws.row_dimensions[1].height = 35
    for col_idx, (field, header, width) in enumerate(col_defs, 1):
        cell = ws.cell(row=1, column=col_idx, value=header)
        apply_style(cell, header_style)
        ws.column_dimensions[get_column_letter(col_idx)].width = width


def format_price(price):
    if price is None:
        return ''
    try:
        return int(price)
    except:
        return price


def write_product_row(ws, row_num, product, col_defs, variation=None, is_alt=False):
    """نوشتن یک ردیف محصول یا واریاسیون"""
    is_variation = variation is not None
    is_variable_parent = product.get('type') == 'variable' and not is_variation

    # تعیین رنگ ردیف
    if not product.get('matched', True):
        bg_color = COLORS['unmatched_bg']
    elif is_variation:
        bg_color = COLORS['variation_bg']
    elif is_variable_parent:
        bg_color = COLORS['variable_bg']
    elif is_alt:
        bg_color = COLORS['alt_row']
    else:
        bg_color = COLORS['simple_bg']

    fill = PatternFill(fill_type='solid', fgColor=bg_color)
    align = Alignment(horizontal='right', vertical='center', wrap_text=False)
    align_center = Alignment(horizontal='center', vertical='center')
    align_left = Alignment(horizontal='left', vertical='center')


    # ساخت داده ردیف
    row_data = {}
    if is_variation:
        attrs = variation.get('attributes', {})
        first_attr_key = list(attrs.keys())[0] if attrs else ''
        first_attr_val = list(attrs.values())[0] if attrs else ''
        row_data = {
            'product_id': product.get('product_id', ''),
            'variation_id': variation.get('variation_id', ''),
            'user_name': '',
            'name': f"  ↳ {product.get('name', '')} [{', '.join(f'{k}={v}' for k, v in attrs.items())}]",
            'type': 'variation',
            'attribute_name': first_attr_key,
            'attribute_value': first_attr_val,
            'category_path': product.get('category_path', ''),
            'shortlink': variation.get('shortlink') or product.get('shortlink', ''),
            'price_regular': format_price(variation.get('price_regular')),
            'price_sale': format_price(variation.get('price_sale')),
            'in_stock': '✓ موجود' if variation.get('in_stock', True) else '✗ ناموجود',
            'sku': variation.get('sku', ''),
            'match_score': '',
            'notes': '',
        }
    else:
        stock_status = '✓ موجود' if product.get('in_stock', True) else '✗ ناموجود'
        type_label = {'simple': 'ساده', 'variable': 'متغیر', 'variation': 'واریاسیون'}.get(
            product.get('type', 'simple'), product.get('type', 'simple')
        )
        row_data = {
            'product_id': product.get('product_id', ''),
            'variation_id': '',
            'user_name': product.get('user_name', ''),
            'name': product.get('name', product.get('user_name', '')),
            'type': type_label,
            'attribute_name': '',
            'attribute_value': '',
            'category_path': product.get('category_path', ''),
            'shortlink': product.get('shortlink', ''),
            'price_regular': format_price(product.get('price_regular')),
            'price_sale': format_price(product.get('price_sale')),
            'in_stock': stock_status if product.get('matched', True) else '',
            'sku': product.get('sku', ''),
            'match_score': product.get('match_score', '') if product.get('matched') else '---',
            'notes': product.get('note', '') if not product.get('matched', True) else '',
        }

    ws.row_dimensions[row_num].height = 20

    for col_idx, (field, header, width) in enumerate(col_defs, 1):
        cell = ws.cell(row=row_num, column=col_idx, value=row_data.get(field, ''))
        cell.fill = fill
        cell.alignment = align_center if field in ('type', 'in_stock', 'match_score', 'product_id', 'variation_id', 'price_regular', 'price_sale') else align
        if field == 'shortlink' and row_data.get('shortlink'):
            cell.hyperlink = row_data['shortlink']
            cell.style = 'Hyperlink'
            cell.fill = fill
        if field == 'in_stock':
            if '✓' in str(row_data.get('in_stock', '')):
                cell.font = Font(color=COLORS['in_stock'], bold=True)
            elif '✗' in str(row_data.get('in_stock', '')):
                cell.font = Font(color=COLORS['out_of_stock'], bold=True)
        if field in ('price_regular', 'price_sale') and row_data.get(field):
            try:
                cell.number_format = '#,##0'
            except:
                pass


def build_excel(matched_products):
    """ایجاد فایل اکسل"""
    print(f"\n[STEP 4] Building Excel file...", flush=True)

    wb = openpyxl.Workbook()
    wb.remove(wb.active)  # حذف شیت پیش‌فرض

    # گروه‌بندی محصولات بر اساس شیت
    sheet_groups = {}
    for prod in matched_products:
        sheet = prod.get('sheet', 'سایر')
        if sheet not in sheet_groups:
            sheet_groups[sheet] = []
        sheet_groups[sheet].append(prod)

    # ترتیب شیت‌ها
    sheet_order = [
        "یخچال و فریزر",
        "ماشین لباسشویی",
        "جاروبرقی",
        "کولر آبی",
        "ماشین ظرفشویی",
        "تصفیه آب",
        "لوازم آشپزخانه",
        "ظروف",
        "لوازم شخصی",
        "گاز و هود",
        "سایر",
    ]

    col_defs = COLUMNS
    total_rows_written = 0

    for sheet_name in sheet_order:
        if sheet_name not in sheet_groups:
            continue

        products_in_sheet = sheet_groups[sheet_name]
        ws = wb.create_sheet(title=sheet_name[:31])  # Excel max 31 chars
        ws.sheet_view.rightToLeft = True  # راست به چپ

        # هدر
        write_header(ws, col_defs)

        row_num = 2
        is_alt = False

        # مرتب‌سازی بر اساس زیردسته، سپس نام
        products_in_sheet.sort(key=lambda p: (p.get('subcategory', ''), p.get('user_name', '')))

        current_subcat = None
        for prod in products_in_sheet:
            subcat = prod.get('subcategory', '')

            # جداکننده زیردسته
            if subcat and subcat != current_subcat:
                current_subcat = subcat
                # ردیف عنوان زیردسته
                ws.row_dimensions[row_num].height = 22
                ws.merge_cells(start_row=row_num, start_column=1, end_row=row_num, end_column=len(col_defs))
                title_cell = ws.cell(row=row_num, column=1, value=f"  ▶ {sheet_name} / {subcat}")
                title_cell.font = Font(bold=True, color=COLORS['subcat_font'], size=11)
                title_cell.fill = PatternFill(fill_type='solid', fgColor=COLORS['subcat_bg'])
                title_cell.alignment = Alignment(horizontal='right', vertical='center')
                row_num += 1
                is_alt = False

            # ردیف اصلی محصول
            write_product_row(ws, row_num, prod, col_defs, is_alt=is_alt)
            row_num += 1
            total_rows_written += 1

            # ردیف‌های واریاسیون (برای محصولات متغیر)
            if prod.get('type') == 'variable' and prod.get('variations'):
                for var in prod['variations']:
                    write_product_row(ws, row_num, prod, col_defs, variation=var)
                    row_num += 1
                    total_rows_written += 1

            is_alt = not is_alt

        # فریز ردیف اول
        ws.freeze_panes = 'A2'

        # فیلتر خودکار
        ws.auto_filter.ref = f"A1:{get_column_letter(len(col_defs))}1"

        print(f"  Sheet '{sheet_name}': {row_num - 2} rows", flush=True)

    # شیت راهنما
    ws_guide = wb.create_sheet(title="راهنما", index=0)
    ws_guide.sheet_view.rightToLeft = True
    guide_data = [
        ("راهنمای استفاده از فایل اکسل حسینی کالا", "", ""),
        ("", "", ""),
        ("نوع محصول", "توضیح", ""),
        ("ساده", "محصول با یک قیمت ثابت - بدون واریاسیون", ""),
        ("متغیر", "محصول با چند رنگ/مدل/سایز - قیمت‌ها در ردیف‌های زیرین", ""),
        ("واریاسیون", "یک حالت از محصول متغیر (مثلاً رنگ سفید)", ""),
        ("", "", ""),
        ("ستون‌ها", "توضیح", ""),
        ("شناسه محصول (ID)", "شناسه عددی یکتا در وردپرس - برای به‌روزرسانی قیمت استفاده کنید", ""),
        ("شناسه واریاسیون", "شناسه یکتای واریاسیون (برای محصولات متغیر)", ""),
        ("لینک محصول", "لینک مستقیم به صفحه محصول در سایت (قابل کلیک)", ""),
        ("قیمت عادی", "قیمت بدون تخفیف (عدد خالص - تومان)", ""),
        ("قیمت حراج", "قیمت با تخفیف در صورت وجود (عدد خالص - تومان)", ""),
        ("دقت تطابق", "میزان مطابقت نام محصول لیست با نام در سایت (0 تا 1)", ""),
        ("", "", ""),
        ("نحوه به‌روزرسانی قیمت‌ها:", "", ""),
        ("۱. قیمت‌های مورد نظر را در ستون‌های قیمت عادی یا قیمت حراج ویرایش کنید", "", ""),
        ("۲. اسکریپت update_prices.py را اجرا کنید", "", ""),
        ("۳. اسکریپت از شناسه‌های ID/variation_id برای تشخیص محصول استفاده می‌کند", "", ""),
    ]
    for r_idx, row in enumerate(guide_data, 1):
        for c_idx, val in enumerate(row, 1):
            ws_guide.cell(row=r_idx, column=c_idx, value=val)
        if r_idx == 1:
            ws_guide.cell(r_idx, 1).font = Font(bold=True, size=14)

    wb.save(EXCEL_OUTPUT)
    print(f"\n[DONE] Excel saved to: {EXCEL_OUTPUT}", flush=True)
    print(f"  Total product rows: {total_rows_written}", flush=True)
    return EXCEL_OUTPUT


# =========================================================
# واکشی محصولات از WP REST API (منبع اصلی)
# =========================================================

import base64

WP_USER = "agent"
WP_APP_PASSWORD = "Mlwg pHHX NQ64 drrz 7ca2 IVto"
AUTH_B64 = base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode('utf-8')).decode()
API_HEADERS = {
    'Authorization': f'Basic {AUTH_B64}',
    'User-Agent': 'HosseinyKala-Catalog/1.0',
    'Accept': 'application/json',
}


def fetch_wp_api_products():
    """دریافت همه محصولات از WP REST API (wp/v2/product)"""
    print("\n[API] Fetching products from WP REST API...", flush=True)
    all_products = []
    page = 1
    per_page = 100

    while True:
        url = f"{BASE_URL}/wp-json/wp/v2/product?per_page={per_page}&page={page}&status=publish"
        try:
            r = requests.get(url, headers=API_HEADERS, timeout=30)
            if r.status_code == 400:
                break  # no more pages
            if r.status_code != 200:
                print(f"  [API WARN] status {r.status_code} on page {page}", flush=True)
                break
            data = r.json()
            if not data:
                break
            all_products.extend(data)
            total_pages = int(r.headers.get('X-WP-TotalPages', 1))
            total_items = int(r.headers.get('X-WP-Total', len(data)))
            print(f"  API page {page}/{total_pages}: got {len(data)} products (total so far: {len(all_products)}/{total_items})", flush=True)
            if page >= total_pages:
                break
            page += 1
            time.sleep(0.5)
        except Exception as e:
            print(f"  [API ERROR] {e}", flush=True)
            break

    print(f"  Total products from API: {len(all_products)}", flush=True)
    return all_products


def convert_api_product(wp_item):
    """تبدیل آیتم API وردپرس به فرمت استاندارد ما"""
    pid = wp_item.get('id')
    name_raw = wp_item.get('title', {})
    name = name_raw.get('rendered', '') if isinstance(name_raw, dict) else str(name_raw)
    # HTML entity decode
    import html
    name = html.unescape(name).strip()

    link = wp_item.get('link', '')
    slug = wp_item.get('slug', '')

    # دسته‌بندی‌ها از product_cat terms
    categories = []
    product_cats = wp_item.get('product_cat', [])

    # قیمت و وضعیت موجودی از meta یا excerpt
    meta = wp_item.get('meta', {}) or {}
    price_regular = None
    price_sale = None
    sku = ''
    product_type = 'simple'

    # برخی سایت‌ها قیمت را در فیلد excerpt یا content میگذارند
    # اما بهتر است از صفحه مستقیم parse کنیم — اینجا فقط ساختار پایه
    if isinstance(meta, dict):
        price_regular = parse_price(meta.get('_regular_price') or meta.get('_price'))
        price_sale = parse_price(meta.get('_sale_price'))
        sku = str(meta.get('_sku', ''))
        if meta.get('_virtual') == 'no':
            product_type = 'simple'

    return {
        'url': link,
        'product_id': pid,
        'shortlink': f"https://hosseinykala.ir/?p={pid}",
        'name': name,
        'slug': slug,
        'type': product_type,
        'categories': categories,
        'price_regular': price_regular,
        'price_sale': price_sale,
        'in_stock': True,
        'sku': sku,
        'variations': [],
        '_needs_detail': True,  # نیاز به واکشی صفحه محصول برای قیمت
    }


def enrich_with_page_data(api_products, scraped_products):
    """ترکیب داده‌های API با داده‌های scrape شده"""
    # ایجاد فهرست بر اساس URL
    scraped_by_url = {}
    for p in scraped_products:
        url_clean = p.get('url', '').rstrip('/') + '/'
        scraped_by_url[url_clean] = p

    enriched = []
    for ap in api_products:
        link_clean = ap.get('url', '').rstrip('/') + '/'
        if link_clean in scraped_by_url:
            scraped = scraped_by_url[link_clean]
            # ترکیب: اطلاعات scrape شده برای قیمت و variation، API برای ID و نام
            merged = {**scraped}
            merged['product_id'] = ap['product_id']
            merged['shortlink'] = ap['shortlink']
            if not merged.get('name'):
                merged['name'] = ap['name']
            enriched.append(merged)
        else:
            # محصولی که فقط در API هست (صفحه‌اش crawl نشده)
            ap['_needs_detail'] = True
            enriched.append(ap)

    return enriched


# =========================================================
# تابع اصلی
# =========================================================

def main():
    print("=" * 60, flush=True)
    print("هوسینی کالا - ساخت کاتالوگ اکسل محصولات", flush=True)
    print("=" * 60, flush=True)

    # ── مرحله ۱: واکشی از WP REST API (منبع اصلی) ──
    api_products_raw = fetch_wp_api_products()

    # تبدیل به فرمت استاندارد
    api_products = [convert_api_product(p) for p in api_products_raw]

    # ── مرحله ۲: جمع‌آوری URLها از sitemap و category pages ──
    product_urls = get_all_product_urls()

    # اضافه کردن URLهای API که در sitemap نبودن
    api_urls = set()
    for ap in api_products:
        if ap.get('url'):
            api_urls.add(ap['url'].rstrip('/') + '/')

    extra_urls = list(api_urls - set(u.rstrip('/') + '/' for u in product_urls))
    all_urls = list(set(product_urls) | api_urls)
    print(f"\n  Total URLs to scrape (sitemap + API): {len(all_urls)}", flush=True)
    if extra_urls:
        print(f"  Extra URLs from API (not in sitemap): {len(extra_urls)}", flush=True)

    # ── مرحله ۳: واکشی صفحات محصول برای اطلاعات کامل (قیمت، variation) ──
    site_products = fetch_all_products(all_urls)

    # ── مرحله ۴: ترکیب داده‌های API + scrape ──
    # برای محصولاتی که در API هستند ولی scrape نشدن، از داده‌های API استفاده می‌کنیم
    scraped_urls = set(p.get('url', '').rstrip('/') + '/' for p in site_products)
    for ap in api_products:
        ap_url = ap.get('url', '').rstrip('/') + '/'
        if ap_url not in scraped_urls:
            site_products.append(ap)

    # حذف تکراری‌ها بر اساس URL
    seen_urls = set()
    unique_products = []
    for p in site_products:
        url_key = p.get('url', '').rstrip('/') + '/'
        if url_key not in seen_urls:
            seen_urls.add(url_key)
            unique_products.append(p)
    site_products = unique_products

    print(f"\n  Final unique products: {len(site_products)}", flush=True)

    # ذخیره داده خام
    with open(RAW_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(site_products, f, ensure_ascii=False, indent=2)
    print(f"  Raw data saved: {RAW_DATA_FILE}", flush=True)

    # ── مرحله ۵: تطابق ──
    matched = build_matched_products(USER_PRODUCT_LIST, site_products)

    with open(MATCHED_FILE, 'w', encoding='utf-8') as f:
        json.dump(matched, f, ensure_ascii=False, indent=2)
    print(f"  Matched data saved: {MATCHED_FILE}", flush=True)

    # ── مرحله ۶: ایجاد اکسل ──
    output_path = build_excel(matched)

    print("\n" + "=" * 60, flush=True)
    print(f"✓ کامل شد! فایل اکسل در مسیر زیر ذخیره شده:", flush=True)
    print(f"  {output_path}", flush=True)
    print("=" * 60, flush=True)


if __name__ == '__main__':
    main()

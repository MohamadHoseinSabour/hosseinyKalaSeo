"""
build_simple_catalog.py
=======================
ساخت فایل اکسل ساده و قابل ویرایش برای کاتالوگ محصولات حسینی کالا

اصول طراحی:
- سمت راست شیت (RTL) = مهم‌ترین اطلاعات: نام محصول + قیمت
- مچ‌کردن فقط با اطمینان بالا (threshold >= 0.80)
- محصولات بدون قیمت در سایت → قیمت خالی (نه قیمت اشتباه)
- هیچ cross-category matching نمی‌شه (آبگرمکن با یخچال match نمیشه)
- ساختار ساده، تمیز و قابل ویرایش
"""

import os
import sys
import json
import re
import base64
import time
import html
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from difflib import SequenceMatcher
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# ─── مسیرها ───────────────────────────────────────────────
BASE_URL = "https://hosseinykala.ir"
SCRIPT_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
EXCEL_OUT = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.xlsx')
RAW_FILE = os.path.join(DATA_DIR, 'products_raw.json')

# ─── Auth ─────────────────────────────────────────────────
WP_USER = "agent"
WP_PASS = "Mlwg pHHX NQ64 drrz 7ca2 IVto"
AUTH = base64.b64encode(f"{WP_USER}:{WP_PASS}".encode()).decode()
API_H = {'Authorization': f'Basic {AUTH}', 'Accept': 'application/json'}
WEB_H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# ─── لیست ۱۸۰ محصول کاربر + دسته‌بندی دستی ──────────────
#   فرمت: (نام محصول, شیت, زیردسته)
USER_PRODUCTS = [
    # ── یخچال و فریزر ─────────────────────────────────────
    ("یخچال فریزر BOST",                           "یخچال و فریزر", "BOST"),
    ("یخچال فریزر ۳۲ دیپوینت استیل T7",            "یخچال و فریزر", "دیپوینت"),
    ("یخچال فریزر دیپوینت سفید T7",                "یخچال و فریزر", "دیپوینت"),
    ("یخچال فریزر دیپوینت استیل Dipoent",          "یخچال و فریزر", "دیپوینت"),
    ("یخچال کلور مینی سبز پاستیلی",               "یخچال و فریزر", "کلور"),
    ("یخچال الکترواستیل سفید ES21-FUTUR",          "یخچال و فریزر", "الکترواستیل"),
    ("یخچال الکترواستیل یخساز تیتانیوم",           "یخچال و فریزر", "الکترواستیل"),
    ("یخچال ایستکول فوت سفید",                     "یخچال و فریزر", "ایستکول"),
    ("یخچال ایستکول فوت نوک مدادی",               "یخچال و فریزر", "ایستکول"),
    ("یخچال ایستکول فوت سفید",                     "یخچال و فریزر", "ایستکول"),
    ("یخچال ایستکول فوت نوک مدادی",               "یخچال و فریزر", "ایستکول"),
    ("یخچال فریزر کلور روسو سفید",                "یخچال و فریزر", "کلور"),
    ("یخچال فریزر کلور گلوریاپلاس سفید",          "یخچال و فریزر", "کلور"),
    ("یخچال فریزر کلور ۱۰۱ کمبی سفید ساده",       "یخچال و فریزر", "کلور"),
    ("یخچال فریزر کلور روسو مومبارا استیل",       "یخچال و فریزر", "کلور"),
    ("یخچال کلور ۶۰ روسوپلاس استیل",              "یخچال و فریزر", "کلور"),
    ("یخچال کلور ۶۰ روسوپلاس سفید",               "یخچال و فریزر", "کلور"),
    ("یخچال کلور ۶۰ گلوریا استیل",                "یخچال و فریزر", "کلور"),
    ("یخچال کلور روسوپلاس استیل",                  "یخچال و فریزر", "کلور"),
    ("یخچال کلور گلوریاپلاس سفید",                "یخچال و فریزر", "کلور"),
    ("یخچال کلور ۲۷ سفید کره‌ای ۱۰۱",             "یخچال و فریزر", "کلور"),
    ("یخچال فریزر R(re01)",                        "یخچال و فریزر", "سایر"),
    ("یخچال هیمالیا آیسپول استیل 60MW",           "یخچال و فریزر", "هیمالیا"),
    ("یخچال هیمالیا آیسپول چرم 60MW",             "یخچال و فریزر", "هیمالیا"),
    ("فریزر صندوقی الکتروسان ۳۴۵",               "یخچال و فریزر", "الکتروسان"),
    ("فریزر کلور ۶۰ روسوپلاس سفید",               "یخچال و فریزر", "کلور"),
    ("فریزر کلور ۶۰ روسوپلاس استیل",              "یخچال و فریزر", "کلور"),
    ("فریزر کلور ۶۰ گلوریا استیل",                "یخچال و فریزر", "کلور"),
    ("فریزر کلور ۷۰ روسو آبریزا استیل",           "یخچال و فریزر", "کلور"),
    ("فریزر کلور ۷۰ گلوریاپلاس سفید",             "یخچال و فریزر", "کلور"),
    ("فریزر کلور ۲۷ سفید کره‌ای ۱۰۱",             "یخچال و فریزر", "کلور"),
    ("فریزر هیمالیا آیسپول استیل 60MW",           "یخچال و فریزر", "هیمالیا"),
    ("فریزر هیمالیا آیسپول چرم 60MW",             "یخچال و فریزر", "هیمالیا"),

    # ── ماشین لباسشویی ────────────────────────────────────
    ("لباسشویی کلور مدل 9771 سفید",               "ماشین لباسشویی", "کلور"),
    ("لباسشویی ۱۷ دوقلو ریتون",                   "ماشین لباسشویی", "ریتون"),
    ("لباسشویی دوقلو پاکشوما هاک",                "ماشین لباسشویی", "پاکشوما"),
    ("لباسشویی ۸ کلور لمسی سفید 8TW1",            "ماشین لباسشویی", "کلور"),
    ("لباسشویی ۹ کلور لمسی سفید 9TW1",            "ماشین لباسشویی", "کلور"),
    ("لباسشویی اتوماتیک دوو 991S",                "ماشین لباسشویی", "دوو"),
    ("لباسشویی درب بالا پاکشوما ۱۲",              "ماشین لباسشویی", "پاکشوما"),
    ("لباسشویی دوقلو ۲۱ کیلو پاکشوما",            "ماشین لباسشویی", "پاکشوما"),
    ("لباسشویی کلور ۹ لمسی اینوکس 9TI1",          "ماشین لباسشویی", "کلور"),
    ("لباسشویی کلور ۹ کیلویی کرمی",               "ماشین لباسشویی", "کلور"),
    ("لباسشویی کلور ۹ کیلویی لمسی اینوکس",        "ماشین لباسشویی", "کلور"),
    ("لباسشویی کلور ۹ کیلویی سفید ویوا",          "ماشین لباسشویی", "کلور"),
    ("اتوماتیک دوو کینو ۹۰۵ سینیور",              "ماشین لباسشویی", "دوو"),
    ("پتوشور پاکیزان ۲۰ کیلو",                    "ماشین لباسشویی", "پاکیزان"),
    ("پتوشور پاکیزان ۴۰ کیلو",                    "ماشین لباسشویی", "پاکیزان"),

    # ── جاروبرقی ──────────────────────────────────────────
    ("جاروبرقی آراز ۲۰ لیتر",                     "جاروبرقی", "آراز"),
    ("جاروبرقی هیتاچی سطلی ۱۲۰۰",                "جاروبرقی", "هیتاچی"),
    ("جاروبرقی دونالکس ۷۵۰ سورمه‌ای",             "جاروبرقی", "دونالکس"),
    ("جاروبرقی دونالکس ۷۷۰",                      "جاروبرقی", "دونالکس"),
    ("جاروبرقی کلور سطلی",                        "جاروبرقی", "کلور"),
    ("جاروبرقی BOST سطلی",                        "جاروبرقی", "BOST"),
    ("Panasonic MC CG715 2100W",                  "جاروبرقی", "پاناسونیک"),

    # ── کولر آبی ──────────────────────────────────────────
    ("کولر آبی مدل ۴۵۰۰",                         "کولر آبی", "سایر"),
    ("کولر آبی اوناکس 150L",                       "کولر آبی", "اوناکس"),
    ("کولر آبی اوناکس B35",                        "کولر آبی", "اوناکس"),
    ("کولر پنجره‌ای اوجنرال ۱۸ هزار",              "کولر آبی", "اوجنرال"),
    ("کولر آبی ریتون",                             "کولر آبی", "ریتون"),
    ("کولر وستینگهاوس ۲۰ کوپلند",                 "کولر آبی", "وستینگهاوس"),
    ("اسپایپ ونتو",                                "کولر آبی", "اسپایپ"),

    # ── ماشین ظرفشویی ─────────────────────────────────────
    ("ظرفشویی انفره استیل",                        "ماشین ظرفشویی", "انفره"),
    ("ظرفشویی انفره لمسی استیل",                   "ماشین ظرفشویی", "انفره"),

    # ── تصفیه آب ──────────────────────────────────────────
    ("تصفیه آب سافت واتر ۶ مرحله",                "تصفیه آب", "سافت واتر"),
    ("تصفیه آب وست 5515",                          "تصفیه آب", "وست"),
    ("تصفیه آب هومگلد",                            "تصفیه آب", "هومگلد"),
    ("تصفیه آب C.C.K",                             "تصفیه آب", "CCK"),
    ("آبسردکن نیکایی مدل ۱۱۲۰۶ ایستاده",           "تصفیه آب", "نیکایی"),
    ("آبسردکن هانو",                               "تصفیه آب", "هانو"),
    ("آب سردکن افترون رومیزی",                     "تصفیه آب", "افترون"),
    ("آبگرمکن الکترواستیل مخزندار دیواری",          "تصفیه آب", "الکترواستیل"),

    # ── لوازم آشپزخانه ────────────────────────────────────
    # اسپرسوساز
    ("اسپرسوساز دونالکس ۳۸۰",                     "لوازم آشپزخانه", "اسپرسوساز"),
    ("اسپرسوساز دونالکس ۳۷۵",                     "لوازم آشپزخانه", "اسپرسوساز"),
    ("اسپرسوساز نارنجی گرنویک",                   "لوازم آشپزخانه", "اسپرسوساز"),
    # چایساز
    ("چایساز دونالکس ۱۸۵ مشکی",                   "لوازم آشپزخانه", "چایساز"),
    ("چایساز زامروتی",                             "لوازم آشپزخانه", "چایساز"),
    ("چایساز ساورر گرنویک",                        "لوازم آشپزخانه", "چایساز"),
    ("چایساز کُرکماز A331",                        "لوازم آشپزخانه", "چایساز"),
    # کتری
    ("کتری برقی اریکسون",                         "لوازم آشپزخانه", "کتری برقی"),
    ("کتری برقی تک زامروتی کرم",                  "لوازم آشپزخانه", "کتری برقی"),
    ("کتری برقی سانی ۱.۵ لیتر",                   "لوازم آشپزخانه", "کتری برقی"),
    ("کتری برقی وگاتی توپی",                      "لوازم آشپزخانه", "کتری برقی"),
    ("کتری برقی وستینگهاوس آبی",                  "لوازم آشپزخانه", "کتری برقی"),
    ("کتری برقی وستینگهاوس کرم",                  "لوازم آشپزخانه", "کتری برقی"),
    ("کتری برقی پروکس",                           "لوازم آشپزخانه", "کتری برقی"),
    ("کتری و قوری زامروتی دسته استیل ۲۰۲۲",       "لوازم آشپزخانه", "کتری برقی"),
    ("کتری و قوری زامروتی دسته چوب ۲۰۲۲",        "لوازم آشپزخانه", "کتری برقی"),
    ("کتری و قوری مدل هرمی تمام‌طلا ۶۰۴",         "لوازم آشپزخانه", "کتری برقی"),
    # توستر
    ("توستر ۶۰ لیتر",                             "لوازم آشپزخانه", "توستر"),
    ("توستر ناندلمونتی ۵۸",                        "لوازم آشپزخانه", "توستر"),
    ("توستر وستینگهاوس ۲۷",                       "لوازم آشپزخانه", "توستر"),
    ("توستر وستینگهاوس کرم",                      "لوازم آشپزخانه", "توستر"),
    # سرخکن
    ("سرخکن دونالکس",                             "لوازم آشپزخانه", "سرخکن"),
    ("سرخکن ایرفرایر خاکستری گرنویک",             "لوازم آشپزخانه", "سرخکن"),
    ("سرخکن دونالکس ۱۹۵۰ استیل",                 "لوازم آشپزخانه", "سرخکن"),
    # ساندویچ‌ساز
    ("ساندویچ‌ساز دونالکس ۴۰۹ سفید",              "لوازم آشپزخانه", "ساندویچ‌ساز"),
    ("ساندویچ‌ساز دونالکس ۴۹۰ مشکی",             "لوازم آشپزخانه", "ساندویچ‌ساز"),
    # پلوپز
    ("پلوپز پارس خزر ۸ نقره",                     "لوازم آشپزخانه", "پلوپز"),
    ("پلوپز پارس خزر مدل ۳۶۱",                    "لوازم آشپزخانه", "پلوپز"),
    # آبمیوه‌گیری
    ("آبمیوهگیری جنرال ۶۰۷ غذاساز",               "لوازم آشپزخانه", "آبمیوه‌گیری"),
    ("آبمیوهگیر دونالکس ۴ کاره ۱۲۰",              "لوازم آشپزخانه", "آبمیوه‌گیری"),
    ("آبمیوهگیر دونالکس ۴ کاره ۱۱۰",              "لوازم آشپزخانه", "آبمیوه‌گیری"),
    # مخلوط‌کن
    ("مخلوطکن زامروتی کرم",                       "لوازم آشپزخانه", "مخلوط‌کن"),
    ("مخلوطکن و آسیاب دونالکس ۲۰۵",              "لوازم آشپزخانه", "مخلوط‌کن"),
    ("مخلوطکن وستینگهاوس آبی",                   "لوازم آشپزخانه", "مخلوط‌کن"),
    ("مخلوطکن وستینگهاوس کرم",                   "لوازم آشپزخانه", "مخلوط‌کن"),
    # گوشت‌کوب
    ("گوشتکوب دونالکس ۲۷۵",                      "لوازم آشپزخانه", "گوشت‌کوب"),
    ("گوشتکوب و غذاساز دونالکس ۱۹۹۰",            "لوازم آشپزخانه", "گوشت‌کوب"),
    # همزن
    ("همزن اوریکس کاسه چرخدار",                  "لوازم آشپزخانه", "همزن"),
    ("همزن کنوود ۴۳۰",                            "لوازم آشپزخانه", "همزن"),
    ("همزن دستی دونالکس ۳۵۵",                    "لوازم آشپزخانه", "همزن"),
    ("همزن وستینگهاوس آبی",                       "لوازم آشپزخانه", "همزن"),
    ("همزن وستینگهاوس کرم",                       "لوازم آشپزخانه", "همزن"),
    # غذاساز
    ("غذاساز فیلیپس ۷۷۷۸",                       "لوازم آشپزخانه", "غذاساز"),
    ("آسیاب کاستلو ۲۷۰",                          "لوازم آشپزخانه", "غذاساز"),
    ("سبزی خردکن KENRA",                          "لوازم آشپزخانه", "غذاساز"),
    ("سبزی خردکن نیکا ۲ کیلویی",                 "لوازم آشپزخانه", "غذاساز"),
    # زودپز
    ("زودپز اویزپلاس تک‌قلو مشکی رزگلد",          "لوازم آشپزخانه", "زودپز"),
    ("زودپز اویزپلاس دوقلو مشکی رزگلد",           "لوازم آشپزخانه", "زودپز"),

    # ── ظروف ──────────────────────────────────────────────
    ("تابه اویز سایز ۳۰",                         "ظروف", "تابه"),
    ("تابه اویز سایز ۲۲ مشکی",                   "ظروف", "تابه"),
    ("تابه اویز سایز ۲۲ فوم مشکی دربدار",         "ظروف", "تابه"),
    ("تابه اویز سایز ۲۶",                         "ظروف", "تابه"),
    ("قابلمه اویز سایز ۲۰ مشکی",                 "ظروف", "قابلمه"),
    ("قابلمه اویز سایز ۲۰ مشکی",                 "ظروف", "قابلمه"),
    ("قابلمه اویز سایز ۲۲ مشکی",                 "ظروف", "قابلمه"),
    ("قابلمه اویز سایز ۲۲ مشکی",                 "ظروف", "قابلمه"),
    ("قابلمه اویز سایز ۲۴ مشکی",                 "ظروف", "قابلمه"),
    ("قابلمه اویز سایز ۱۶ مشکی",                 "ظروف", "قابلمه"),
    ("قابلمه اویز سایز ۲۶ مشکی",                 "ظروف", "قابلمه"),
    ("قابلمه اویز سایز ۱۸ مشکی",                 "ظروف", "قابلمه"),
    ("قابلمه مرغخوری اویزپلاس مشکی",              "ظروف", "قابلمه"),
    ("سرویس خمره قابلمه اویز کرم‌سلین",           "ظروف", "سرویس"),
    ("سرویس قابلمه استیل ۱۰ پارچه",              "ظروف", "سرویس"),
    ("سرویس قابلمه اویز ۱۰ پارچه سرمه‌ای",        "ظروف", "سرویس"),
    ("سرویس قابلمه اویزپلاس ۱۰ پارچه اناری",      "ظروف", "سرویس"),
    ("سرویس قابلمه اویزپلاس ۱۲ پارچه مشکی",      "ظروف", "سرویس"),
    ("سرویس قابلمه اویزپلاس ۱۲ پارچه سبز",       "ظروف", "سرویس"),
    ("سرویس قابلمه اویزپلاس ویولا ۱۱ پارچه",      "ظروف", "سرویس"),
    ("شیرجوش مشکی اویزپلاس",                      "ظروف", "سرویس"),

    # ── لوازم شخصی ────────────────────────────────────────
    ("سشوار امگا ۲۰۰۰ وات",                       "لوازم شخصی", "سشوار"),
    ("سشوار پروامگا ۲۲۰۰ وات",                    "لوازم شخصی", "سشوار"),
    ("ماشین اصلاح پروامگا تک",                    "لوازم شخصی", "ماشین اصلاح"),
    ("ماشین اصلاح پروامگا ۴ کاره",                "لوازم شخصی", "ماشین اصلاح"),
    ("ماشین اصلاح پروامگا شارژی و برقی",          "لوازم شخصی", "ماشین اصلاح"),
    ("فرکننده مو پرومارون ۴+",                    "لوازم شخصی", "فرکننده مو"),
    ("پرومارون برس حرارتی ۱۱۳",                   "لوازم شخصی", "فرکننده مو"),
    ("اتو مو Baby3383A",                           "لوازم شخصی", "اتو مو"),
    ("اتو مو پاناسونیک HV11",                     "لوازم شخصی", "اتو مو"),
    ("اتومو پرومارون ۱۱۱۵",                       "لوازم شخصی", "اتو مو"),
    ("اتومو پرومارون ۱۱۱۶",                       "لوازم شخصی", "اتو مو"),
    ("اپیلاتور پرومارون ۵ کاره ۶۱۴",              "لوازم شخصی", "اپیلاتور"),
    ("ریشتراش پرومارون ۷۰۶",                      "لوازم شخصی", "ریشتراش"),
    ("دستگاه پیرایش سیمی صورت ۷۲۱",              "لوازم شخصی", "ریشتراش"),

    # ── اتو ───────────────────────────────────────────────
    ("اتو دونالکس ۸۱۵",                           "اتو", "دونالکس"),
    ("اتو فیلیپس ۵۰۴۰",                           "اتو", "فیلیپس"),

    # ── گاز و هود ─────────────────────────────────────────
    ("گاز صفحه‌ای آلتون استیل S517",               "گاز و هود", "آلتون"),
    ("گاز صفحه‌ای آلتون استیل SG518",              "گاز و هود", "آلتون"),
    ("فر الکترواستیل تیتانیوم ۱۱",                "گاز و هود", "الکترواستیل"),
    ("فر الکترواستیل عرض ۶۰ چرمی ۲۱",             "گاز و هود", "الکترواستیل"),
    ("فر توکار آلتون ۷۳۰۳",                       "گاز و هود", "آلتون"),
    ("فرگاز آلتون MPS",                           "گاز و هود", "آلتون"),
    ("فرگاز آلتون MD5W",                           "گاز و هود", "آلتون"),
    ("هود آلتون H312",                             "گاز و هود", "آلتون"),
    ("هود آلتون H315B",                            "گاز و هود", "آلتون"),

    # ── سایر ──────────────────────────────────────────────
    ("ال ای دی هاورسون ۷۵ اینچ",                  "سایر", "تلویزیون"),
    ("ال ای دی ۳۲ Averson",                       "سایر", "تلویزیون"),
    ("ال ای دی ۸۵ Averson",                       "سایر", "تلویزیون"),
    ("ال ای دی ۶۵ اینچ هاورسون",                  "سایر", "تلویزیون"),
    ("ال ای دی هاورسون ۵۵ پنرست",                "سایر", "تلویزیون"),
    ("بخاری گلدن لوکس",                           "سایر", "بخاری"),
    ("بخاری پارس خزر فندار FH-2000P",             "سایر", "بخاری"),
    ("بخاری پلار 32-067 شیشه‌ای",                  "سایر", "بخاری"),
    ("پنکه پایه‌بلند 1455",                        "سایر", "پنکه"),
    ("پنکه پارس خزر پایه‌بلند",                    "سایر", "پنکه"),
    ("پنکه پاناسونیک ۲ حالته",                    "سایر", "پنکه"),
    ("پنکه سانی ۷۶۰۰",                            "سایر", "پنکه"),
    ("پنکه سانی مدل ۲۰۱۳ ساده",                   "سایر", "پنکه"),
    ("کسورات اضافات کالا",                        "سایر", "متفرقه"),
]

# ─── ستون‌ها (در اکسل RTL، ستون A سمت راست ظاهر می‌شه) ───
# پس مهم‌ترین اطلاعات = ستون A و B (نام + قیمت)
COLUMNS = [
    # (field_key,         header_fa,              width)
    ("name",             "نام محصول",              40),
    ("price_regular",    "قیمت عادی",              16),
    ("price_sale",       "قیمت حراج",              16),
    ("type",             "نوع",                   10),
    ("attr_name",        "ویژگی",                  14),
    ("attr_value",       "مقدار ویژگی",             16),
    ("category_path",    "دسته‌بندی",              24),
    ("link",             "لینک محصول",             38),
    ("product_id",       "شناسه (ID)",              12),
    ("variation_id",     "شناسه واریاسیون",        15),
    ("in_stock",         "موجودی",                 11),
    ("sku",              "کد SKU",                 14),
    ("note",             "یادداشت",                22),
]

# ─── رنگ‌ها ───────────────────────────────────────────────
C = {
    'hdr_bg':    '2C3E50',  # header background
    'hdr_fg':    'FFFFFF',  # header text
    'var_bg':    'EAF4FB',  # محصول متغیر (parent)
    'vrn_bg':    'D6EAF8',  # واریاسیون (child)
    'sub_bg':    'D5F5E3',  # عنوان زیردسته
    'sub_fg':    '1E8449',
    'miss_bg':   'FFF9C4',  # محصول بدون داده سایت
    'row1_bg':   'FFFFFF',
    'row2_bg':   'F8F9FA',
    'green':     '27AE60',
    'red':       'E74C3C',
}


# ─── توابع کمکی ───────────────────────────────────────────

def parse_price(s):
    if not s:
        return None
    s = str(s)
    s = s.translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789'))
    digits = re.sub(r'[^\d]', '', s)
    return int(digits) if digits else None


def normalize(text):
    text = str(text).strip()
    text = text.replace('ي', 'ی').replace('ك', 'ک').replace('ة', 'ه')
    text = re.sub(r'[\u200c\u200d\s]+', ' ', text)
    text = text.translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789'))
    return text.lower().strip()


def sim(a, b):
    return SequenceMatcher(None, normalize(a), normalize(b)).ratio()


# ─── واکشی محصولات از سایت ────────────────────────────────

def fetch_url(url, retries=2):
    for i in range(retries):
        try:
            r = requests.get(url, headers=WEB_H, timeout=25)
            if r.status_code == 200:
                return r
        except Exception:
            if i < retries - 1:
                time.sleep(1)
    return None


def get_site_products():
    """واکشی محصولات از WP REST API"""
    print("[1] Fetching products from API...", flush=True)

    # از WP REST API
    products = []
    page = 1
    while True:
        url = f"{BASE_URL}/wp-json/wp/v2/product?per_page=100&page={page}&status=publish"
        r = requests.get(url, headers=API_H, timeout=25)
        if r.status_code != 200:
            break
        data = r.json()
        if not data:
            break
        products.extend(data)
        total = int(r.headers.get('X-WP-TotalPages', 1))
        print(f"  page {page}/{total}: {len(data)} products", flush=True)
        if page >= total:
            break
        page += 1
        time.sleep(0.3)

    print(f"  Total from API: {len(products)}", flush=True)
    return products


def scrape_product_page(url):
    """استخراج اطلاعات کامل از صفحه محصول"""
    r = fetch_url(url)
    if not r:
        return None
    soup = BeautifulSoup(r.text, 'html.parser')

    data = {
        'url': url,
        'product_id': None,
        'shortlink': None,
        'name': '',
        'type': 'simple',
        'categories': [],
        'price_regular': None,
        'price_sale': None,
        'in_stock': True,
        'sku': '',
        'variations': [],
    }

    # product_id از body class
    body = soup.find('body')
    if body:
        for cls in body.get('class', []):
            m = re.search(r'postid-(\d+)', cls)
            if m:
                data['product_id'] = int(m.group(1))
                data['shortlink'] = f"{BASE_URL}/?p={m.group(1)}"
                break

    # نام
    h1 = soup.find('h1', class_='product_title') or soup.find('h1')
    if h1:
        data['name'] = h1.get_text(strip=True)

    # دسته‌بندی
    cat_elem = soup.find('span', class_='posted_in')
    if cat_elem:
        data['categories'] = [a.get_text(strip=True) for a in cat_elem.find_all('a')]

    # SKU
    sku_el = soup.find('span', class_='sku')
    if sku_el:
        data['sku'] = sku_el.get_text(strip=True)

    # محصول متغیر
    vform = soup.find('form', class_='variations_form')
    if vform:
        data['type'] = 'variable'
        vdata = vform.get('data-product_variations')
        if vdata:
            try:
                for v in json.loads(vdata):
                    attrs = {}
                    for k, val in v.get('attributes', {}).items():
                        attrs[k.replace('attribute_', '').replace('pa_', '')] = val
                    vid = v.get('variation_id')
                    data['variations'].append({
                        'variation_id': vid,
                        'shortlink': f"{BASE_URL}/?p={vid}" if vid else None,
                        'attributes': attrs,
                        'price_regular': parse_price(v.get('display_price')),
                        'price_sale': None,
                        'in_stock': v.get('is_in_stock', True),
                        'sku': v.get('sku', ''),
                    })
            except Exception:
                pass

    # قیمت محصول ساده
    price_el = soup.find('p', class_='price')
    if price_el:
        ins = price_el.find('ins')
        del_ = price_el.find('del')
        if ins:
            data['price_sale'] = parse_price(ins.get_text())
            if del_:
                data['price_regular'] = parse_price(del_.get_text())
        else:
            amt = price_el.find('span', class_='woocommerce-Price-amount')
            if amt:
                data['price_regular'] = parse_price(amt.get_text())

    # موجودی
    stock_el = soup.find('p', class_='stock')
    if stock_el and 'out-of-stock' in ' '.join(stock_el.get('class', [])):
        data['in_stock'] = False

    return data


def load_or_fetch_site_products():
    """بارگذاری از کش یا fetch مجدد"""
    if os.path.exists(RAW_FILE):
        print(f"[1] Loading cached data from {RAW_FILE}", flush=True)
        with open(RAW_FILE, encoding='utf-8') as f:
            return json.load(f)

    api_items = get_site_products()

    # scrape هر صفحه برای قیمت کامل و variations
    urls = [item.get('link', '') for item in api_items if item.get('link')]
    print(f"[2] Scraping {len(urls)} product pages...", flush=True)

    products = []
    with ThreadPoolExecutor(max_workers=3) as ex:
        futs = {ex.submit(scrape_product_page, u): u for u in urls}
        done = 0
        for fut in as_completed(futs):
            done += 1
            res = fut.result()
            if res:
                # merge: product_id از API
                for api in api_items:
                    if api.get('link', '').rstrip('/') == res['url'].rstrip('/'):
                        res['product_id'] = api['id']
                        res['shortlink'] = f"{BASE_URL}/?p={api['id']}"
                        if not res['name']:
                            res['name'] = html.unescape(
                                api.get('title', {}).get('rendered', '') if isinstance(api.get('title'), dict)
                                else str(api.get('title', ''))
                            )
                        break
                products.append(res)
            if done % 5 == 0:
                print(f"  scraped {done}/{len(urls)}", flush=True)

    with open(RAW_FILE, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    print(f"  Saved {len(products)} products to {RAW_FILE}", flush=True)
    return products


# ─── مچ‌کردن دقیق ─────────────────────────────────────────

# کلمات کلیدی دسته‌بندی برای جلوگیری از cross-category match
CATEGORY_KEYWORDS = {
    'یخچال و فریزر': ['یخچال', 'فریزر', 'refrigerator', 'freezer'],
    'ماشین لباسشویی': ['لباسشوی', 'washing', 'پتوشور', 'اتوماتیک دوو'],
    'جاروبرقی': ['جاروبرقی', 'vacuum', 'جارو برقی'],
    'کولر آبی': ['کولر', 'cooler', 'اسپایپ'],
    'ماشین ظرفشویی': ['ظرفشوی', 'dishwasher'],
    'تصفیه آب': ['تصفیه', 'آبسردکن', 'آبگرمکن', 'آب سردکن', 'water purifier'],
    'لوازم آشپزخانه': ['اسپرسو', 'چایساز', 'کتری', 'توستر', 'سرخکن',
                       'ساندویچ', 'پلوپز', 'آبمیوه', 'مخلوطکن', 'مخلوط‌کن',
                       'گوشتکوب', 'همزن', 'غذاساز', 'آسیاب', 'سبزی خردکن',
                       'زودپز', 'شیرجوش'],
    'ظروف': ['قابلمه', 'تابه', 'سرویس', 'ظروف'],
    'لوازم شخصی': ['سشوار', 'اتو مو', 'اتومو', 'ماشین اصلاح', 'اپیلاتور',
                   'ریشتراش', 'فرکننده', 'برس حرارتی', 'پیرایش'],
    'اتو': ['اتو دونالکس', 'اتو فیلیپس'],
    'گاز و هود': ['گاز', 'هود', 'فر', 'فرگاز'],
    'سایر': ['ال ای دی', 'تلویزیون', 'بخاری', 'پنکه', 'کسورات'],
}


def get_user_category(user_name, sheet):
    return sheet  # دسته‌بندی دستی مشخص شده


def products_same_category(user_name, user_sheet, site_product_name, site_cats):
    """بررسی می‌کنه که آیا محصول سایت در همون دسته کاربر هست"""
    user_kws = CATEGORY_KEYWORDS.get(user_sheet, [])
    site_text = normalize(site_product_name) + ' ' + normalize(' '.join(site_cats))
    for kw in user_kws:
        if normalize(kw) in site_text:
            return True
    return False


def match_product(user_name, user_sheet, site_products, threshold=0.72):
    """
    مچ‌کردن با شرایط سخت‌گیرانه:
    1. threshold بالا (0.72)
    2. cross-category مچ نمی‌شه
    """
    best, best_score = None, 0

    for sp in site_products:
        site_name = sp.get('name', '')
        site_cats = sp.get('categories', [])

        # بررسی هم‌دسته بودن
        if not products_same_category(user_name, user_sheet, site_name, site_cats):
            continue

        score = sim(user_name, site_name)
        if score > best_score:
            best_score = score
            best = sp

    if best and best_score >= threshold:
        return best, best_score
    return None, 0


# ─── ساخت اکسل ────────────────────────────────────────────

def st(bold=False, color=None, size=10):
    return Font(bold=bold, color=color or '000000', size=size, name='Calibri')

def fill(color):
    return PatternFill(fill_type='solid', fgColor=color)

def aln(h='right', v='center', wrap=False):
    return Alignment(horizontal=h, vertical=v, wrap_text=wrap)

def thin_border():
    s = Side(style='thin', color='CCCCCC')
    return Border(bottom=s)


def write_header(ws, cols):
    ws.row_dimensions[1].height = 30
    hf = Font(bold=True, color=C['hdr_fg'], size=10, name='Calibri')
    hfill = fill(C['hdr_bg'])
    halign = aln('center')
    for ci, (_, hdr, w) in enumerate(cols, 1):
        cell = ws.cell(row=1, column=ci, value=hdr)
        cell.font = hf
        cell.fill = hfill
        cell.alignment = halign
        ws.column_dimensions[get_column_letter(ci)].width = w
    ws.freeze_panes = 'A2'
    ws.auto_filter.ref = f"A1:{get_column_letter(len(cols))}1"


def write_row(ws, row_num, row_data, cols, bg):
    f = fill(bg)
    for ci, (fk, _, _) in enumerate(cols, 1):
        val = row_data.get(fk, '')
        cell = ws.cell(row=row_num, column=ci, value=val)
        cell.fill = f
        # سمت راست = نام و قیمت → align right
        if fk in ('name', 'note', 'category_path'):
            cell.alignment = aln('right')
        elif fk == 'link' and val:
            cell.hyperlink = str(val)
            cell.style = 'Hyperlink'
            cell.fill = f
            cell.alignment = aln('left')
        else:
            cell.alignment = aln('center')
        # رنگ موجودی
        if fk == 'in_stock':
            if val == '✓':
                cell.font = Font(color=C['green'], bold=True, name='Calibri')
            elif val == '✗':
                cell.font = Font(color=C['red'], bold=True, name='Calibri')
        # فرمت قیمت
        if fk in ('price_regular', 'price_sale') and isinstance(val, int):
            cell.number_format = '#,##0'
    ws.row_dimensions[row_num].height = 18


def write_subcat_header(ws, row_num, text, num_cols, bg, fg):
    ws.merge_cells(start_row=row_num, start_column=1,
                   end_row=row_num, end_column=num_cols)
    c = ws.cell(row=row_num, column=1, value=f"  ► {text}")
    c.font = Font(bold=True, color=fg, size=10, name='Calibri')
    c.fill = fill(bg)
    c.alignment = aln('right')
    ws.row_dimensions[row_num].height = 20


def build_row_data(user_name, user_sheet, subcat, site_match, variation=None):
    """ساخت داده یک ردیف"""
    cat_path = f"{user_sheet} / {subcat}" if subcat else user_sheet

    # محصول در سایت پیدا نشد
    if site_match is None:
        return {
            'name': user_name,
            'price_regular': '',
            'price_sale': '',
            'type': '',
            'attr_name': '',
            'attr_value': '',
            'category_path': cat_path,
            'link': '',
            'product_id': '',
            'variation_id': '',
            'in_stock': '',
            'sku': '',
            'note': 'در سایت موجود نیست',
        }, 'miss'

    # واریاسیون
    if variation:
        attrs = variation.get('attributes', {})
        first_key = list(attrs.keys())[0] if attrs else ''
        first_val = list(attrs.values())[0] if attrs else ''
        vid = variation.get('variation_id')
        return {
            'name': f"  ↳ {site_match.get('name', user_name)}",
            'price_regular': variation.get('price_regular') or '',
            'price_sale': variation.get('price_sale') or '',
            'type': 'واریاسیون',
            'attr_name': first_key,
            'attr_value': first_val,
            'category_path': cat_path,
            'link': variation.get('shortlink') or site_match.get('shortlink', ''),
            'product_id': site_match.get('product_id', ''),
            'variation_id': vid or '',
            'in_stock': '✓' if variation.get('in_stock', True) else '✗',
            'sku': variation.get('sku', ''),
            'note': '',
        }, 'variation'

    # محصول اصلی (ساده یا parent متغیر)
    ptype = {'simple': 'ساده', 'variable': 'متغیر'}.get(
        site_match.get('type', 'simple'), site_match.get('type', ''))
    reg = site_match.get('price_regular')
    sale = site_match.get('price_sale')
    return {
        'name': user_name,
        'price_regular': reg if reg else '',
        'price_sale': sale if sale else '',
        'type': ptype,
        'attr_name': '',
        'attr_value': '',
        'category_path': cat_path,
        'link': site_match.get('shortlink', ''),
        'product_id': site_match.get('product_id', ''),
        'variation_id': '',
        'in_stock': '✓' if site_match.get('in_stock', True) else '✗',
        'sku': site_match.get('sku', ''),
        'note': '',
    }, 'simple' if site_match.get('type') == 'simple' else 'variable'


def build_excel(grouped, site_products):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    # شیت راهنما
    wg = wb.create_sheet('راهنما', 0)
    wg.sheet_view.rightToLeft = True
    guide = [
        ("فایل کاتالوگ محصولات — حسینی کالا", "", ""),
        ("", "", ""),
        ("ستون", "توضیح", ""),
        ("نام محصول", "نام از لیست کاربر (ستون اول = سمت راست)", ""),
        ("قیمت عادی", "عدد خالص بدون واحد — قابل ویرایش", ""),
        ("قیمت حراج", "قیمت با تخفیف — قابل ویرایش", ""),
        ("نوع", "ساده / متغیر / واریاسیون", ""),
        ("لینک محصول", "لینک مستقیم با فرمت ?p=ID", ""),
        ("شناسه (ID)", "کلید اصلی برای آپدیت قیمت از اکسل به سایت", ""),
        ("", "", ""),
        ("رنگ‌ها", "معنی", ""),
        ("زرد روشن", "محصول هنوز در سایت ثبت نشده", ""),
        ("آبی روشن", "محصول متغیر (چند رنگ/مدل)", ""),
        ("آبی تیره‌تر", "واریاسیون (یک رنگ/مدل از محصول متغیر)", ""),
        ("سبز روشن", "عنوان زیردسته‌بندی", ""),
        ("", "", ""),
        ("به‌روزرسانی قیمت", "python scripts/update_prices.py --apply", ""),
    ]
    for ri, row in enumerate(guide, 1):
        for ci, v in enumerate(row, 1):
            c = wg.cell(row=ri, column=ci, value=v)
            if ri == 1:
                c.font = Font(bold=True, size=12, name='Calibri')
            elif ri == 3 or ri == 11:
                c.font = Font(bold=True, name='Calibri')
    wg.column_dimensions['A'].width = 24
    wg.column_dimensions['B'].width = 42

    # ترتیب شیت‌ها
    sheet_order = [
        "یخچال و فریزر", "ماشین لباسشویی", "جاروبرقی",
        "کولر آبی", "ماشین ظرفشویی", "تصفیه آب",
        "لوازم آشپزخانه", "ظروف", "لوازم شخصی",
        "اتو", "گاز و هود", "سایر",
    ]

    cols = COLUMNS
    total_rows = 0

    for sheet_name in sheet_order:
        if sheet_name not in grouped:
            continue
        items = grouped[sheet_name]  # list of (user_name, subcat, site_match)

        ws = wb.create_sheet(sheet_name[:31])
        ws.sheet_view.rightToLeft = True
        write_header(ws, cols)

        row_num = 2
        alt = False
        current_sub = None

        # مرتب‌سازی بر اساس زیردسته
        items.sort(key=lambda x: (x[1], x[0]))

        for user_name, subcat, site_match in items:
            # عنوان زیردسته
            if subcat != current_sub:
                current_sub = subcat
                if subcat:
                    write_subcat_header(ws, row_num,
                                        f"{sheet_name}  /  {subcat}",
                                        len(cols), C['sub_bg'], C['sub_fg'])
                    row_num += 1
                    alt = False

            # ردیف اصلی
            rd, rtype = build_row_data(user_name, sheet_name, subcat, site_match)
            if rtype == 'miss':
                bg = C['miss_bg']
            elif rtype == 'variable':
                bg = C['var_bg']
            else:
                bg = C['row1_bg'] if alt else C['row2_bg']
            write_row(ws, row_num, rd, cols, bg)
            row_num += 1
            total_rows += 1

            # واریاسیون‌ها
            if site_match and site_match.get('type') == 'variable':
                for v in site_match.get('variations', []):
                    vrd, _ = build_row_data(user_name, sheet_name, subcat, site_match, variation=v)
                    write_row(ws, row_num, vrd, cols, C['vrn_bg'])
                    row_num += 1
                    total_rows += 1

            alt = not alt

        print(f"  Sheet '{sheet_name}': {row_num - 2} rows", flush=True)

    wb.save(EXCEL_OUT)
    print(f"\n✓ Excel saved: {EXCEL_OUT}", flush=True)
    print(f"  Total rows: {total_rows}", flush=True)
    return EXCEL_OUT


# ─── اجرای اصلی ───────────────────────────────────────────

def main():
    print("=" * 55, flush=True)
    print("ساخت کاتالوگ اکسل — حسینی کالا", flush=True)
    print("=" * 55, flush=True)

    # بارگذاری داده‌های خام واکشی‌شده
    site_products = load_or_fetch_site_products()

    print(f"\n[3] Matching {len(USER_PRODUCTS)} user products with {len(site_products)} site products...", flush=True)

    matched_count = 0
    unmatched_count = 0

    # گروه‌بندی بر اساس شیت
    grouped = {}
    for user_name, sheet, subcat in USER_PRODUCTS:
        if sheet not in grouped:
            grouped[sheet] = []

        # کسورات = هیچ match انجام نمی‌شه
        if user_name == "کسورات اضافات کالا":
            grouped[sheet].append((user_name, subcat, None))
            continue

        site_match, score = match_product(user_name, sheet, site_products)

        if site_match:
            matched_count += 1
        else:
            unmatched_count += 1

        grouped[sheet].append((user_name, subcat, site_match))

    print(f"  Matched: {matched_count}", flush=True)
    print(f"  Not in site: {unmatched_count}", flush=True)

    print("\n[4] Building Excel file...", flush=True)
    build_excel(grouped, site_products)
    print("\n" + "=" * 55, flush=True)


if __name__ == '__main__':
    import json
    main()

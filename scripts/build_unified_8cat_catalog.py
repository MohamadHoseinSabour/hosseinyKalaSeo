"""
build_unified_8cat_catalog.py
=============================
اسکریپت نهایی و جامع ساخت کاتالوگ اکسل محصولات حسینی کالا:
- انطباق ۱۰۰٪ با ۸ دسته‌بندی اصلی و مادر وب‌سایت (جلوگیری از شلوغی و تعدد شیت‌ها)
- واکشی و درج تمامی ۹۷ محصول لایو سایت + ۷۸ واریاسیون و تنوع رنگ/مدل/ظرفیت
- پوشش اقلام تکمیلی لیست کاربر با برچسب مشخص
- ستون‌های قیمت ریال و محاسبه خودکار قیمت تومان با فرمول اکسل
- منوی کشویی وضعیت موجودی (✓ موجود / ✗ ناموجود) با فرمت رنگی خودکار
- لینک‌های مستقیم و کاننیکال
- طراحی شیک و اداری RTL، فریز هدر، استایل والد و تنوع درختی
- داشبورد آماری و تحلیلی KPI و شیت راهنمای استفاده
"""

import os
import sys
import json
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.chart import BarChart, Reference

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"c:\Users\mmhhs\OneDrive\Documents\GitHub\hosseinyKalaSeo"
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
RAW_FILE = os.path.join(DATA_DIR, 'products_raw.json')
EXCEL_OUT_LATEST = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog_latest.xlsx')
EXCEL_OUT_MAIN = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.xlsx')

with open(RAW_FILE, encoding='utf-8') as f:
    live_products = json.load(f)

live_by_id = {p['id']: p for p in live_products}

# ستون‌های استاندارد در شیت‌های محصولات
COLUMNS = [
    # (key,              header_text,                 width,  align,   is_price,  is_formula)
    ("name",             "نام محصول",                  44,     "right",   False,     False),
    ("price_regular",    "قیمت عادی (ریال)",          18,     "center",  True,      False),
    ("price_reg_toman",  "قیمت عادی (تومان)",          18,     "center",  True,      True),
    ("price_sale",       "قیمت حراج (ریال)",          18,     "center",  True,      False),
    ("price_sale_toman", "قیمت حراج (تومان)",          18,     "center",  True,      True),
    ("in_stock",         "وضعیت موجودی",               15,     "center",  False,     False),
    ("main_cat",         "دسته‌بندی اصلی سایت",        22,     "center",  False,     False),
    ("subcat",           "زیردسته / گروه کالا",       22,     "center",  False,     False),
    ("brand",            "برند",                       16,     "center",  False,     False),
    ("type",             "نوع محصول",                  14,     "center",  False,     False),
    ("variant_attr",     "مشخصه تنوع / متغیر",         22,     "center",  False,     False),
    ("product_id",       "شناسه محصول (ID)",           16,     "center",  False,     False),
    ("variation_id",     "شناسه تنوع",                 15,     "center",  False,     False),
    ("link",             "لینک مستقیم در سایت",        36,     "left",    False,     False),
    ("sku",              "کد SKU",                     15,     "center",  False,     False),
    ("status_note",      "وضعیت در سایت",              22,     "center",  False,     False),
]

# پالت رنگ‌های حرفه‌ای
COLOR_HEADER_BG = "1F4E79"        # سرمه‌ای تیره رسمی
COLOR_HEADER_TEXT = "FFFFFF"      # سفید
COLOR_BANNER_BG = "D9E1F2"        # آبی ملایم بخش‌ها
COLOR_BANNER_TEXT = "1F4E79"      # سرمه‌ای متن بخش
COLOR_VAR_PARENT_BG = "EBF1F5"    # زمینه سطر والد محصول متغیر
COLOR_VARIATION_BG = "F8F9FA"     # خاکستری روشن ملایم تنوع‌ها
COLOR_OFFLINE_BG = "FFF9E6"       # زرد بسیار ملایم برای اقلام تعریف‌نشده
COLOR_IN_STOCK = "27AE60"         # سبز
COLOR_OUT_OF_STOCK = "C00000"     # قرمز
COLOR_BORDER = "D9D9D9"           # خاکستری خطوط جدول

def get_border():
    s = Side(style='thin', color=COLOR_BORDER)
    return Border(top=s, bottom=s, left=s, right=s)

# =========================================================
# معماری دقیق ۸ دسته‌بندی اصلی مطابق وب‌سایت حسینی کالا
# =========================================================
CATALOG_STRUCTURE = {
    "یخچال و فریزر": {
        "کلور": [
            2972, # یخچال فریزر گلوری پلاس دوقلو کلور 54 فوت
            2464, # یخچال فریزر دوقلو 44 فوت کلور مدل 54 فوت glory plus-lm70
            2471, # یخچال فریزر دوقلو 40 فوت کلور مدل گلوری عرض 60
            2457, # یخچال فریزر دوقلو 40 فوت کلور مدل رسوپلاس عرض 60
            2637, # یخچال و فریزر دوقلو 36 فوت کلوِر مدل RNT101-FNT101
            2497, # یخچال و فریزر 27 فوت کلور مدل كمبي FRNT-70 GLORY PLUS
            2408, # یخچال و فریزر 27 فوت کلوِر مدل FRNT101
            2484, # یخچال و فریزر 27 فوت کلور مدل كمبي هوم بار روسو
            2431, # یخچال 10 فوت کلور مدل Mini Refrigerator
        ],
        "دیپوینت": [
            2745, # یخچال فریزر دوقلو 34 فوت دیپوینت مدل MAX.DU _ مکس
            2594, # یخچال فریزر 30 فوت دیپوینت مدل Boss Pro
            2585, # یخچال و فریزر 28 فوت دیپوینت مدل T7
        ],
        "هیمالیا": [
            3395, # یخچال و فریزر دوقلو 28 فوت هیمالیا مدل آلفا
            {"name": "یخچال هیمالیا آیسپول استیل 60MW", "brand": "هیمالیا", "type": "simple", "site_id": None},
            {"name": "فریزر هیمالیا آیسپول استیل 60MW", "brand": "هیمالیا", "type": "simple", "site_id": None},
        ],
        "الکترواستیل": [
            3453, # یخچال فریزر دوقلو 21 فوت الکترواستیل مدل فیوچر
            {"name": "یخچال الکترواستیل یخساز تیتانیوم", "brand": "الکترواستیل", "type": "simple", "site_id": None},
        ],
        "ایستکول": [
            2691, # یخچال فریزر 9 فوت ایستکول مدل هتلی 2919
            2704, # یخچال 5 فوت ایستکول مدل 2835
        ],
        "الکتروسان": [
            3513, # فریزر صندوقی الکتروسان مدل کم‌مصرف سوپر سایلنت
        ],
        "بست (BOST)": [
            3389, # یخچال و فریزر 24 فوت بست مدل BRB241-10
        ],
        "سایر برندها": [
            {"name": "یخچال فریزر R(re01)", "brand": "متفرقه", "type": "simple", "site_id": None},
        ],
    },

    "شستشو و نظافت": {
        "ماشین لباسشویی": [
            3573, # ماشین لباسشویی ۱۰ کیلوگرم اینورتر کلور دایرکت درایو
            2505, # ماشین لباسشویی 9 کیلوگرم اتوماتیک کلور BMWT2
            2510, # ماشین لباسشویی 8 کیلوگرم اتوماتیک کلور BMW T3
            2579, # ماشین لباسشویی هوشمند 9 کیلوگرم اتوماتیک دوو LM-9170
            3707, # ماشین لباسشویی دوقلو ۲۱ کیلوگرم پاکشوما
            3563, # ماشین لباسشویی دوقلو ۱۵ کیلوگرم پاکشوما
            3557, # ماشین لباسشویی ۱۲ کیلوگرم درب از بالا پاکشوما
            3551, # ماشین لباسشویی ۱۷ کیلوگرم دوقلو ریتون
            3709, # پتوشور صنعتی و خانگی ۴۰ کیلوگرم تمام استیل پاکیزان
            {"name": "پتوشور صنعتی و خانگی ۲۰ کیلوگرم پاکیزان", "brand": "پاکیزان", "type": "simple", "site_id": None},
            {"name": "لباسشویی دوقلو پاکشوما هاک", "brand": "پاکشوما", "type": "simple", "site_id": None},
            {"name": "لباسشویی کلور ۹ کیلویی سفید ویوا", "brand": "کلور", "type": "simple", "site_id": None},
            {"name": "لباسشویی کلور مدل 9771 سفید", "brand": "کلور", "type": "simple", "site_id": None},
            {"name": "اتوماتیک دوو کینو ۹۰۵ سینیور", "brand": "دوو", "type": "simple", "site_id": None},
        ],
        "ماشین ظرفشویی": [
            2871, # ماشین ظرفشویی 15 نفره کلور CDW-H15V
            3546, # ماشین ظرفشویی ۱۶ نفره استیل لمسی ۳ سبد
            {"name": "ظرفشویی انفره استیل", "brand": "انفره", "type": "simple", "site_id": None},
        ],
        "جاروبرقی": [
            2519, # جاروبرقی سطلی هیتاچی CV-950F
            2661, # جاروبرقی پاناسونیک MC-CG715
            2885, # جاروبرقی بست BVC-PC18B
            3510, # جاروبرقی ۲۴۰۰ وات دونالکس DN-750
            3840, # این محصول در سایت شما تعریف نشده است (باسلام)
            {"name": "جاروبرقی کلور سطلی", "brand": "کلور", "type": "simple", "site_id": None},
            {"name": "جاروبرقی آراز ۲۰ لیتر", "brand": "آراز", "type": "simple", "site_id": None},
            {"name": "جاروبرقی دونالکس ۷۷۰", "brand": "دونالکس", "type": "simple", "site_id": None},
            {"name": "جاروبرقی هیتاچی سطلی ۱۲۰۰", "brand": "هیتاچی", "type": "simple", "site_id": None},
        ],
        "اتو و بخارگر": [
            3271, # اتو بخار فیلیپس مدل DST5040
            3007, # اتو بخار ۲۵۰۰ وات دونالکس مدل 815
        ],
    },

    "لوازم برقی و پخت و پز": {
        "سرخ‌کن بدون روغن": [
            3026, # سرخ‌کن 8 لیتر دونالکس مدل DN-950
            3647, # سرخ‌کن بدون روغن ۸ لیتری گرنویک مدل ProMar
            {"name": "سرخکن دونالکس ۱۹۵۰ استیل", "brand": "دونالکس", "type": "simple", "site_id": None},
        ],
        "گوشت‌کوب و غذاساز": [
            3032, # گوشت کوب برقی دونالکس مدل DN-275
            3626, # گوشت‌کوب و غذاساز چندکاره ۸۰۰ وات دونالکس مدل DN-290
            3629, # غذاساز حرفه‌ای ۱۳۰۰ وات فیلیپس مدل HR7778
            {"name": "سبزی خردکن KENRA", "brand": "KENRA", "type": "simple", "site_id": None},
            {"name": "سبزی خردکن نیکا ۲ کیلویی", "brand": "نیکا", "type": "simple", "site_id": None},
        ],
        "اجاق گاز و فر": [
            3380, # اجاق گاز 5 شعله آلتون مدل MD5S
            3383, # اجاق گاز صفحه ای آلتون مدل S517N
            {"name": "گاز صفحه‌ای آلتون استیل SG518", "brand": "آلتون", "type": "simple", "site_id": None},
            {"name": "فر توکار آلتون ۷۳۰۳", "brand": "آلتون", "type": "simple", "site_id": None},
            {"name": "فرگاز آلتون MPS", "brand": "آلتون", "type": "simple", "site_id": None},
            {"name": "فرگاز آلتون MD5W", "brand": "آلتون", "type": "simple", "site_id": None},
            {"name": "هود آلتون H312", "brand": "آلتون", "type": "simple", "site_id": None},
            {"name": "هود آلتون H315B", "brand": "آلتون", "type": "simple", "site_id": None},
            {"name": "فر الکترواستیل تیتانیوم ۱۱", "brand": "الکترواستیل", "type": "simple", "site_id": None},
            {"name": "فر الکترواستیل عرض ۶۰ چرمی ۲۱", "brand": "الکترواستیل", "type": "simple", "site_id": None},
        ],
        "ظروف پخت و پز": [
            3612, # شیرجوش گرانیتی ۱۴ سانتی‌متر اویزپلاس
            3610, # سرویس قابلمه ۱۲ پارچه گرانیتی اویزپلاس
            3608, # سرویس قابلمه ۲۴ پارچه گرانیتی اویزپلاس
            3606, # سرویس زودپز دوقلو ۵ و ۷ لیتری کلیپسی اویزپلاس
            3602, # زودپز کلیپسی ۷ لیتری اویزپلاس
            3596, # قابلمه گرانیتی مشکی اویز
            3592, # سرویس قابلمه ۱۰ پارچه خمره‌ای اویز مدل سلین
            3357, # سرویس پخت و پز 10 پارچه اویز مدل سلین
            3318, # سرویس پخت و پز 11 پارچه اویز پلاس مدل ویولا
            3354, # سرویس پخت و پز 10 پارچه مدل دستی لوکس
            {"name": "سرویس قابلمه استیل ۱۰ پارچه", "brand": "متفرقه", "type": "simple", "site_id": None},
            {"name": "سرویس قابلمه اویزپلاس ۱۰ پارچه اناری", "brand": "اویزپلاس", "type": "simple", "site_id": None},
            {"name": "تابه اویز سایز ۳۰", "brand": "اویز", "type": "simple", "site_id": None},
            {"name": "تابه اویز سایز ۲۲ مشکی", "brand": "اویز", "type": "simple", "site_id": None},
            {"name": "تابه اویز سایز ۲۶", "brand": "اویز", "type": "simple", "site_id": None},
            {"name": "قابلمه مرغخوری اویزپلاس مشکی", "brand": "اویزپلاس", "type": "simple", "site_id": None},
        ],
        "توستر و ساندویچ‌ساز": [
            3617, # ساندویچ‌ساز و گریل ۱۴۰۰ وات دونالکس مدل DN-940
            3637, # توستر نان ۲ شیار رترو وستینگهاوس
            3631, # آون توستر ۶۰ لیتری کانوکشن نان دلمونتی مدل DN-580
            {"name": "توستر ۶۰ لیتر", "brand": "متفرقه", "type": "simple", "site_id": None},
            {"name": "ساندویچ‌ساز دونالکس ۴۰۹ سفید", "brand": "دونالکس", "type": "simple", "site_id": None},
        ],
        "پلوپز": [
            {"name": "پلوپز پارس خزر ۸ نقره", "brand": "پارس خزر", "type": "simple", "site_id": None},
            {"name": "پلوپز پارس خزر مدل ۳۶۱", "brand": "پارس خزر", "type": "simple", "site_id": None},
        ]
    },

    "نوشیدنی ساز": {
        "اسپرسوساز": [
            3013, # اسپرسو ساز ۱۲ میلی لیتر دونالکس مدل DN480
            3016, # اسپرسو ساز ۱۸ میلی لیتر دونالکس مدل DN475
            3679, # اسپرسوساز ۲۰ بار گرنویک مدل رترو آنالوگ
            {"name": "اسپرسوساز دونالکس ۳۸۰", "brand": "دونالکس", "type": "simple", "site_id": None},
            {"name": "اسپرسوساز دونالکس ۳۷۵", "brand": "دونالکس", "type": "simple", "site_id": None},
        ],
        "چای‌ساز و سماور برقی": [
            3673, # چای‌ساز تمام استیل کورکماز مدل A331 چای‌تما
            3457, # چای ساز دونالکس مدل DN-185
            3681, # سماور برقی پیرکس ۳.۲ لیتری گرنویک مدل GST-883
            3657, # سماور برقی ۳ لیتری دیجیتال پیرکس زامروتی
            {"name": "چایساز زامروتی", "brand": "زامروتی", "type": "simple", "site_id": None},
            {"name": "چایساز ساورر گرنویک", "brand": "گرنویک", "type": "simple", "site_id": None},
        ],
        "کتری برقی و قوری": [
            3664, # کتری برقی رترو ۲۲۰۰ وات وستینگهاوس مدل WKKE210
            3660, # کتری برقی رترو ۱.۷ لیتری زامروتی مدل عقربه‌ای
            3668, # کتری برقی ۱.۸ لیتری وگاتی مدل توپی
            3653, # کتری برقی استیل ۲۰۰۰ وات اریکسون مدل ۱.۸ لیتری
            3662, # کتری و قوری روگازی هرمی ۵ لیتری استیل طلا مدل 604
            {"name": "کتری برقی سانی ۱.۵ لیتر", "brand": "سانی", "type": "simple", "site_id": None},
            {"name": "کتری برقی پروکس", "brand": "پروکس", "type": "simple", "site_id": None},
            {"name": "کتری و قوری زامروتی دسته استیل ۲۰۲۲", "brand": "زامروتی", "type": "simple", "site_id": None},
            {"name": "کتری و قوری زامروتی دسته چوب ۲۰۲۲", "brand": "زامروتی", "type": "simple", "site_id": None},
        ],
        "آبمیوه‌گیری": [
            3711, # آبمیوه‌گیری تک‌کاره ۸۰۰ وات دونالکس مدل DN-120
            3019, # آبمیوه‌گیری ۴ کاره ۱۰۰۰ وات دونالکس مدل DN-110
            {"name": "آبمیوهگیری جنرال ۶۰۷ غذاساز", "brand": "جنرال", "type": "simple", "site_id": None},
        ],
        "مخلوط‌کن و آسیاب": [
            3035, # مخلوط کن و آسیاب کن 1.5 لیتری دونالکس مدل DN-205
            3640, # مخلوط‌کن رترو ۶۰۰ وات وستینگهاوس مدل WKBEB221
            3655, # مخلوط‌کن رترو ۱.۵ لیتری ۶۰۰ وات زامروتی مدل 10038
            {"name": "آسیاب کاستلو ۲۷۰", "brand": "کاستلو", "type": "simple", "site_id": None},
        ],
        "همزن برقی": [
            3622, # همزن دستی ۴۰۰ وات توربو دونالکس مدل DN-355
            3645, # همزن دستی ۳۵۰ وات رترو وستینگهاوس
            {"name": "همزن اوریکس کاسه چرخدار", "brand": "اوریکس", "type": "simple", "site_id": None},
            {"name": "همزن کنوود ۴۳۰", "brand": "کنوود", "type": "simple", "site_id": None},
        ]
    },

    "سرمایش و گرمایش": {
        "کولر آبی": [
            2538, # کولر آبی سلولزی 16000 ریتون پرتابل VENTO 16000
            2559, # کولر آبی سلولزی 7000 ریتون مدل VENTO 7000
            {"name": "کولر آبی اوناکس 150L", "brand": "اوناکس", "type": "simple", "site_id": None},
            {"name": "کولر آبی اوناکس B35", "brand": "اوناکس", "type": "simple", "site_id": None},
            {"name": "کولر آبی ریتون", "brand": "ریتون", "type": "simple", "site_id": None},
            {"name": "کولر آبی مدل ۴۵۰۰", "brand": "متفرقه", "type": "simple", "site_id": None},
        ],
        "کولر گازی": [
            3266, # کولر گازی اسپلیت دیواری 18000 دور ثابت پاکشوما مدل TPA-18CH
            {"name": "کولر پنجره‌ای اوجنرال ۱۸ هزار", "brand": "اوجنرال", "type": "simple", "site_id": None},
            {"name": "کولر وستینگهاوس ۲۰ کوپلند", "brand": "وستینگهاوس", "type": "simple", "site_id": None},
        ],
        "پنکه": [
            3540, # پنکه ایستاده ریموت‌دار سانی مدل DWS-2600
            {"name": "پنکه پایه‌بلند 1455", "brand": "متفرقه", "type": "simple", "site_id": None},
            {"name": "پنکه پارس خزر پایه‌بلند", "brand": "پارس خزر", "type": "simple", "site_id": None},
            {"name": "پنکه پاناسونیک ۲ حالته", "brand": "پاناسونیک", "type": "simple", "site_id": None},
            {"name": "پنکه سانی ۷۶۰۰", "brand": "سانی", "type": "simple", "site_id": None},
            {"name": "پنکه سانی مدل ۲۰۱۳ ساده", "brand": "سانی", "type": "simple", "site_id": None},
        ],
        "بخاری و گرمایشی": [
            {"name": "بخاری گلدن لوکس", "brand": "گلدن لوکس", "type": "simple", "site_id": None},
            {"name": "بخاری پارس خزر فندار FH-2000P", "brand": "پارس خزر", "type": "simple", "site_id": None},
            {"name": "بخاری پلار 32-067 شیشه‌ای", "brand": "پلار", "type": "simple", "site_id": None},
        ],
    },

    "تصفیه کننده آب": {
        "دستگاه‌های تصفیه آب خانگی": [
            2766, # دستگاه تصفیه کننده آب سافت واتر مدل IR-06
            3305, # دستگاه تصفیه آب خانگی سی سی کا مدل RO-13
            3504, # دستگاه تصفیه آب خانگی ۶ مرحله‌ای هومگلد مدل RO
            {"name": "تصفیه آب وست 5515", "brand": "وست", "type": "simple", "site_id": None},
        ],
        "آبسردکن و آبگرمکن": [
            3301, # آبسردکن افترون مدل AFWD-5700
            3312, # آبسردکن ایستاده نیکایی مدل NWD_1400R یخچال دار
            {"name": "آبسردکن هانو", "brand": "هانو", "type": "simple", "site_id": None},
            {"name": "آبگرمکن الکترواستیل مخزندار دیواری", "brand": "الکترواستیل", "type": "simple", "site_id": None},
        ],
    },

    "صوتی و تصویری": {
        "تلویزیون و ال‌ای‌دی": [
            3534, # تلویزیون ال ای دی ۸۵ اینچ هوشمند 4K اسمارت Averson مدل Ultra HD
            3531, # تلویزیون ال ای دی ۷۵ اینچ هوشمند 4K هاورسون مدل Cinema HDR
            3523, # تلویزیون ال ای دی ۶۵ اینچ هوشمند 4K هاورسون مدل Frameless IPS
            3520, # تلویزیون ال ای دی ۵۵ اینچ هوشمند 4K هاورسون مدل Smart Android
            3516, # تلویزیون ال ای دی ۳۲ اینچ Averson مدل HD
        ],
    },

    "زیبایی و سلامت فردی": {
        "اصلاح موی سر و صورت": [
            3065, # ماشین اصلاح موی سر و صورت پرو امگا مدل T7
            3056, # ماشین اصلاح موی سر و صورت پرو امگا مدل T5
            {"name": "ماشین اصلاح پروامگا تک", "brand": "پروامگا", "type": "simple", "site_id": None},
            {"name": "ماشین اصلاح پروامگا ۴ کاره", "brand": "پروامگا", "type": "simple", "site_id": None},
            {"name": "ماشین اصلاح پروامگا شارژی و برقی", "brand": "پروامگا", "type": "simple", "site_id": None},
            {"name": "ریشتراش پرومارون ۷۰۶", "brand": "پرومارون", "type": "simple", "site_id": None},
            {"name": "دستگاه پیرایش سیمی صورت ۷۲۱", "brand": "متفرقه", "type": "simple", "site_id": None},
        ],
        "سشوار": [
            3049, # سشوار حرفه ای پرو امگا مدل 8806
            3285, # سشوار پرو امگا مدل 8805
            {"name": "سشوار امگا ۲۰۰۰ وات", "brand": "امگا", "type": "simple", "site_id": None},
            {"name": "سشوار پروامگا ۲۲۰۰ وات", "brand": "پروامگا", "type": "simple", "site_id": None},
        ],
        "حالت‌دهنده و اتو مو": [
            3500, # برس حرارتی صاف‌کننده مو پرومارون مدل 1113 تورمالین
            3488, # اتومو باریک سرامیکی پرومارون مدل 1116
            3484, # اتومو کراتینه سرامیک تیتانیوم پرومارون مدل 1115
            {"name": "فرکننده مو پرومارون ۴+", "brand": "پرومارون", "type": "simple", "site_id": None},
            {"name": "اتو مو Baby3383A", "brand": "متفرقه", "type": "simple", "site_id": None},
            {"name": "اتو مو پاناسونیک HV11", "brand": "پاناسونیک", "type": "simple", "site_id": None},
        ],
        "اپیلاتور": [
            3494, # اپیلاتور شارژی ۵ کاره پرومارون مدل 614 ضدآب
        ],
    },
}

def format_attr_string(attrs_dict):
    if not attrs_dict:
        return ""
    parts = []
    for k, v in attrs_dict.items():
        if k in ['رنگ', 'color']:
            parts.append(f"رنگ: {v}")
        elif k in ['سایز', 'size', 'ابعاد']:
            parts.append(f"سایز: {v}")
        elif k in ['طول', 'ظرفیت']:
            parts.append(f"{k}: {v}")
        else:
            parts.append(f"{k}: {v}")
    return " | ".join(parts)

def build_catalog_workbook():
    print("=" * 60)
    print("شروع ساخت کاتالوگ یکپارچه اکسل (۸ دسته‌بندی اصلی سایت)...")
    print("=" * 60)

    wb = openpyxl.Workbook()
    wb.remove(wb.active) # حذف شیت اولیه پیش‌فرض

    # تعریف اعتبارسنجی منوی کشویی موجودی
    dv_stock = DataValidation(type="list", formula1='"✓ موجود,✗ ناموجود"', allow_blank=True)
    dv_stock.error = 'لطفاً یکی از مقادیر مجاز «✓ موجود» یا «✗ ناموجود» را انتخاب کنید.'
    dv_stock.errorTitle = 'مقدار نامعتبر'

    # آمار کلی برای داشبورد
    stats = {
        "total_parent_rows": 0,
        "total_variation_rows": 0,
        "total_site_products": 0,
        "total_offline_products": 0,
        "in_stock_count": 0,
        "out_of_stock_count": 0,
        "by_category": {}
    }

    border_thin = get_border()

    # حلقه ایجاد شیت‌های ۸ دسته‌بندی
    for sheet_title, subcat_dict in CATALOG_STRUCTURE.items():
        print(f"در حال ایجاد شیت: '{sheet_title}' ...")
        ws = wb.create_sheet(title=sheet_title[:31])
        ws.sheet_view.rightToLeft = True
        ws.add_data_validation(dv_stock)

        # ۱. تنظیم هدر جدول
        ws.row_dimensions[1].height = 32
        for col_idx, (key, header_text, width, align_str, is_price, is_formula) in enumerate(COLUMNS, 1):
            cell = ws.cell(row=1, column=col_idx, value=header_text)
            cell.font = Font(name="Calibri", size=11, bold=True, color=COLOR_HEADER_TEXT)
            cell.fill = PatternFill(fill_type="solid", fgColor=COLOR_HEADER_BG)
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = border_thin
            ws.column_dimensions[get_column_letter(col_idx)].width = width

        current_row = 2
        cat_stats = {
            "total_items": 0,
            "in_stock": 0,
            "out_of_stock": 0,
            "variations": 0,
        }

        # ۲. ایجاد سطرها بر اساس بخش‌ها
        for subcat_name, items_list in subcat_dict.items():
            # سطر بنر دسته‌بندی / بخش
            ws.row_dimensions[current_row].height = 24
            ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=len(COLUMNS))
            banner_cell = ws.cell(row=current_row, column=1, value=f"  📂 {sheet_title}  ◀  {subcat_name}")
            banner_cell.font = Font(name="Calibri", size=11, bold=True, color=COLOR_BANNER_TEXT)
            banner_cell.fill = PatternFill(fill_type="solid", fgColor=COLOR_BANNER_BG)
            banner_cell.alignment = Alignment(horizontal="right", vertical="center")
            for c in range(1, len(COLUMNS) + 1):
                ws.cell(row=current_row, column=c).border = border_thin
            current_row += 1

            for it in items_list:
                # اگر آیتم شناسه سایت باشد
                if isinstance(it, int):
                    prod = live_by_id.get(it)
                    if not prod:
                        print(f"  [هشدار] محصول با شناسه {it} در دیتای لایو یافت نشد!")
                        continue
                    is_site = True
                    item_name = prod['name']
                    ptype = prod.get('type', 'simple')
                    pid = prod['id']
                    sku = prod.get('sku', '')
                    permalink = prod.get('permalink') or f"https://hosseinykala.ir/?p={pid}"
                    p_instock = prod.get('in_stock', False)
                    reg_price = prod.get('price_regular')
                    sale_price = prod.get('price_sale')
                    brand_name = subcat_name
                    status_note = "ثبت‌شده در سایت"
                    variations_list = prod.get('variations', [])
                else: # آیتم تکمیلی کاربر (آفلاین)
                    is_site = False
                    item_name = it['name']
                    ptype = it.get('type', 'simple')
                    pid = it.get('site_id', '')
                    sku = ""
                    permalink = ""
                    p_instock = False
                    reg_price = None
                    sale_price = None
                    brand_name = it.get('brand', subcat_name)
                    status_note = "در سایت تعریف نشده"
                    variations_list = []

                # ثبت آماری
                stats["total_parent_rows"] += 1
                cat_stats["total_items"] += 1
                if is_site:
                    stats["total_site_products"] += 1
                else:
                    stats["total_offline_products"] += 1

                if p_instock:
                    stats["in_stock_count"] += 1
                    cat_stats["in_stock"] += 1
                else:
                    stats["out_of_stock_count"] += 1
                    cat_stats["out_of_stock"] += 1

                # نوشتن سطر والد محصول
                ws.row_dimensions[current_row].height = 21
                is_var_parent = (ptype == 'variable')

                # رنگ سطر
                if not is_site:
                    row_bg = COLOR_OFFLINE_BG
                elif is_var_parent:
                    row_bg = COLOR_VAR_PARENT_BG
                else:
                    row_bg = "FFFFFF"

                fill_parent = PatternFill(fill_type="solid", fgColor=row_bg)

                # داده‌های سطر والد
                # فرمول قیمت تومان:
                formula_reg_toman = f'=IF(ISBLANK(B{current_row}),"",B{current_row}/10)'
                formula_sale_toman = f'=IF(OR(ISBLANK(D{current_row}),D{current_row}=""),"",D{current_row}/10)'

                stock_label = "✓ موجود" if p_instock else "✗ ناموجود"
                type_label = "متغیر" if is_var_parent else "ساده"

                row_values = [
                    item_name,
                    reg_price if reg_price else "",
                    formula_reg_toman if reg_price else "",
                    sale_price if sale_price else "",
                    formula_sale_toman if sale_price else "",
                    stock_label if is_site else "—",
                    sheet_title,
                    subcat_name,
                    brand_name,
                    type_label,
                    "", # بدون مشخصه برای والد
                    pid if pid else "",
                    "", # بدون variation_id برای والد
                    permalink if permalink else "",
                    sku,
                    status_note
                ]

                for col_idx, val in enumerate(row_values, 1):
                    cell = ws.cell(row=current_row, column=col_idx, value=val)
                    cell.fill = fill_parent
                    cell.border = border_thin
                    cell.font = Font(name="Calibri", size=10, bold=is_var_parent)

                    # چینش
                    if col_idx == 1:
                        cell.alignment = Alignment(horizontal="right", vertical="center")
                    elif col_idx in [2, 3, 4, 5, 12, 13]:
                        cell.alignment = Alignment(horizontal="center", vertical="center")
                    elif col_idx == 14:
                        cell.alignment = Alignment(horizontal="left", vertical="center")
                    else:
                        cell.alignment = Alignment(horizontal="center", vertical="center")

                    # فرمت عدد ۳ رقم ۳ رقم برای قیمت‌ها
                    if col_idx in [2, 3, 4, 5] and val:
                        cell.number_format = '#,##0'

                    # استایل رنگ موجودی
                    if col_idx == 6:
                        dv_stock.add(cell)
                        if "✓" in str(val):
                            cell.font = Font(name="Calibri", size=10, bold=True, color=COLOR_IN_STOCK)
                        elif "✗" in str(val):
                            cell.font = Font(name="Calibri", size=10, bold=True, color=COLOR_OUT_OF_STOCK)

                    # هایپرلینک
                    if col_idx == 14 and permalink:
                        cell.hyperlink = permalink
                        cell.font = Font(name="Calibri", size=10, color="0563C1", underline="single")

                current_row += 1

                # نوشتن سطرهای تنوع / واریاسیون‌ها
                if is_var_parent and variations_list:
                    fill_var = PatternFill(fill_type="solid", fgColor=COLOR_VARIATION_BG)
                    for v in variations_list:
                        stats["total_variation_rows"] += 1
                        cat_stats["variations"] += 1

                        ws.row_dimensions[current_row].height = 20
                        vid = v.get('variation_id', '')
                        v_attrs = v.get('attributes', {})
                        attr_str = format_attr_string(v_attrs)
                        v_name = f"    ↳ {attr_str}"
                        v_stock = v.get('in_stock', False)
                        v_reg = v.get('price_regular') or v.get('price')
                        v_sale = v.get('price_sale')
                        v_sku = v.get('sku', '')
                        v_link = v.get('shortlink') or f"https://hosseinykala.ir/?p={vid}"
                        v_stock_label = "✓ موجود" if v_stock else "✗ ناموجود"

                        v_formula_reg = f'=IF(ISBLANK(B{current_row}),"",B{current_row}/10)'
                        v_formula_sale = f'=IF(OR(ISBLANK(D{current_row}),D{current_row}=""),"",D{current_row}/10)'

                        v_row_values = [
                            v_name,
                            v_reg if v_reg else "",
                            v_formula_reg if v_reg else "",
                            v_sale if v_sale else "",
                            v_formula_sale if v_sale else "",
                            v_stock_label,
                            sheet_title,
                            subcat_name,
                            brand_name,
                            "تنوع",
                            attr_str,
                            pid,
                            vid,
                            v_link,
                            v_sku,
                            "ثبت‌شده در سایت"
                        ]

                        for col_idx, val in enumerate(v_row_values, 1):
                            cell = ws.cell(row=current_row, column=col_idx, value=val)
                            cell.fill = fill_var
                            cell.border = border_thin
                            cell.font = Font(name="Calibri", size=9, italic=True)

                            if col_idx == 1:
                                cell.alignment = Alignment(horizontal="right", vertical="center")
                            elif col_idx in [2, 3, 4, 5, 12, 13]:
                                cell.alignment = Alignment(horizontal="center", vertical="center")
                            elif col_idx == 14:
                                cell.alignment = Alignment(horizontal="left", vertical="center")
                            else:
                                cell.alignment = Alignment(horizontal="center", vertical="center")

                            if col_idx in [2, 3, 4, 5] and val:
                                cell.number_format = '#,##0'

                            if col_idx == 6:
                                dv_stock.add(cell)
                                if "✓" in str(val):
                                    cell.font = Font(name="Calibri", size=9, bold=True, color=COLOR_IN_STOCK)
                                elif "✗" in str(val):
                                    cell.font = Font(name="Calibri", size=9, bold=True, color=COLOR_OUT_OF_STOCK)

                            if col_idx == 14 and v_link:
                                cell.hyperlink = v_link
                                cell.font = Font(name="Calibri", size=9, color="0563C1", underline="single")

                        current_row += 1

        # فریز ردیف هدر و تنظیم فیلتر
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = f"A1:{get_column_letter(len(COLUMNS))}{current_row-1}"
        stats["by_category"][sheet_title] = cat_stats
        print(f"  ✓ شیت '{sheet_title}' کامل شد: {cat_stats['total_items']} محصول والد، {cat_stats['variations']} تنوع.")

    # =========================================================
    # ساخت شیت ۱: داشبورد تحلیلی و خلاصه آمار
    # =========================================================
    print("\nدر حال ایجاد شیت خلاصه و داشبورد...")
    ws_dash = wb.create_sheet(title="📊 خلاصه و داشبورد", index=0)
    ws_dash.sheet_view.rightToLeft = True

    # بنر عنوان اصلی داشبورد
    ws_dash.merge_cells("A1:H2")
    title_cell = ws_dash.cell(row=1, column=1, value="📊 داشبورد کاتالوگ جامع و بروزرسانی محصولات — فروشگاه لوازم خانگی حسینی")
    title_cell.font = Font(name="Calibri", size=15, bold=True, color="FFFFFF")
    title_cell.fill = PatternFill(fill_type="solid", fgColor=COLOR_HEADER_BG)
    title_cell.alignment = Alignment(horizontal="center", vertical="center")

    # کارت‌های شاخص‌های کلیدی عملکرد (KPI Cards)
    kpis = [
        ("کل مدل‌ها و اقلام کاتالوگ", stats["total_parent_rows"], "1F4E79"),
        ("محصولات فعال در سایت", stats["total_site_products"], "2E75B6"),
        ("تنوع‌ها و رنگ‌های متغیر", stats["total_variation_rows"], "5B9BD5"),
        ("مجموع گزینه‌های خرید", stats["total_site_products"] + stats["total_variation_rows"], "1E4E79"),
        ("اقلام موجود در انبار", stats["in_stock_count"], "27AE60"),
        ("اقلام ناموجود یا سفارشی", stats["out_of_stock_count"], "C00000"),
        ("اقلام نیازمند ثبت در سایت", stats["total_offline_products"], "ED7D31"),
    ]

    # ردیف ۴: کارت‌های KPI
    col_kpi = 1
    for label, val, bg_color in kpis[:4]:
        ws_dash.merge_cells(start_row=4, start_column=col_kpi, end_row=4, end_column=col_kpi+1)
        ws_dash.merge_cells(start_row=5, start_column=col_kpi, end_row=5, end_column=col_kpi+1)

        c_lbl = ws_dash.cell(row=4, column=col_kpi, value=label)
        c_lbl.font = Font(name="Calibri", size=10, color="FFFFFF", bold=True)
        c_lbl.fill = PatternFill(fill_type="solid", fgColor=bg_color)
        c_lbl.alignment = Alignment(horizontal="center", vertical="center")

        c_val = ws_dash.cell(row=5, column=col_kpi, value=val)
        c_val.font = Font(name="Calibri", size=16, color="FFFFFF", bold=True)
        c_val.fill = PatternFill(fill_type="solid", fgColor=bg_color)
        c_val.alignment = Alignment(horizontal="center", vertical="center")

        for r in [4, 5]:
            for c in range(col_kpi, col_kpi+2):
                ws_dash.cell(row=r, column=c).border = border_thin

        col_kpi += 2

    # ردیف ۷: کارت‌های وضعیت موجودی
    col_kpi = 1
    for label, val, bg_color in kpis[4:]:
        ws_dash.merge_cells(start_row=7, start_column=col_kpi, end_row=7, end_column=col_kpi+1)
        ws_dash.merge_cells(start_row=8, start_column=col_kpi, end_row=8, end_column=col_kpi+1)

        c_lbl = ws_dash.cell(row=7, column=col_kpi, value=label)
        c_lbl.font = Font(name="Calibri", size=10, color="FFFFFF", bold=True)
        c_lbl.fill = PatternFill(fill_type="solid", fgColor=bg_color)
        c_lbl.alignment = Alignment(horizontal="center", vertical="center")

        c_val = ws_dash.cell(row=8, column=col_kpi, value=val)
        c_val.font = Font(name="Calibri", size=16, color="FFFFFF", bold=True)
        c_val.fill = PatternFill(fill_type="solid", fgColor=bg_color)
        c_val.alignment = Alignment(horizontal="center", vertical="center")

        for r in [7, 8]:
            for c in range(col_kpi, col_kpi+2):
                ws_dash.cell(row=r, column=c).border = border_thin

        col_kpi += 2

    # جدول تفکیک آمار ۸ دسته‌بندی اصلی
    ws_dash.cell(row=10, column=1, value="جدول تفکیک آمار محصولات در ۸ دسته‌بندی اصلی سایت").font = Font(name="Calibri", size=12, bold=True, color=COLOR_HEADER_BG)

    headers_table = ["ردیف", "نام دسته‌بندی اصلی", "تعداد مدل‌های محصول", "تعداد تنوع و رنگ‌ها", "موجود", "ناموجود", "درصد موجودی"]
    col_widths_table = [8, 28, 20, 20, 14, 14, 16]

    for col_idx, (h_text, w) in enumerate(zip(headers_table, col_widths_table), 1):
        cell = ws_dash.cell(row=11, column=col_idx, value=h_text)
        cell.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
        cell.fill = PatternFill(fill_type="solid", fgColor=COLOR_HEADER_BG)
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border_thin
        ws_dash.column_dimensions[get_column_letter(col_idx)].width = w

    t_row = 12
    for idx, (cat_name, cdata) in enumerate(stats["by_category"].items(), 1):
        total_p = cdata["total_items"]
        in_s = cdata["in_stock"]
        out_s = cdata["out_of_stock"]
        pct = f"{(in_s / total_p * 100):.1f}%" if total_p > 0 else "0%"

        row_vals = [idx, cat_name, total_p, cdata["variations"], in_s, out_s, pct]
        for col_idx, val in enumerate(row_vals, 1):
            cell = ws_dash.cell(row=t_row, column=col_idx, value=val)
            cell.font = Font(name="Calibri", size=10)
            cell.border = border_thin
            cell.alignment = Alignment(horizontal="center", vertical="center")
            if col_idx == 2:
                cell.alignment = Alignment(horizontal="right", vertical="center")
            if col_idx == 5:
                cell.font = Font(name="Calibri", size=10, bold=True, color=COLOR_IN_STOCK)
            if col_idx == 6:
                cell.font = Font(name="Calibri", size=10, bold=True, color=COLOR_OUT_OF_STOCK)

        t_row += 1

    # سطر مجموع جدول
    ws_dash.cell(row=t_row, column=1, value="")
    ws_dash.cell(row=t_row, column=2, value="مجموع کل").font = Font(name="Calibri", size=10, bold=True)
    ws_dash.cell(row=t_row, column=3, value=f"=SUM(C12:C{t_row-1})").font = Font(name="Calibri", size=10, bold=True)
    ws_dash.cell(row=t_row, column=4, value=f"=SUM(D12:D{t_row-1})").font = Font(name="Calibri", size=10, bold=True)
    ws_dash.cell(row=t_row, column=5, value=f"=SUM(E12:E{t_row-1})").font = Font(name="Calibri", size=10, bold=True, color=COLOR_IN_STOCK)
    ws_dash.cell(row=t_row, column=6, value=f"=SUM(F12:F{t_row-1})").font = Font(name="Calibri", size=10, bold=True, color=COLOR_OUT_OF_STOCK)
    ws_dash.cell(row=t_row, column=7, value=f"=(E{t_row}/C{t_row})*100").font = Font(name="Calibri", size=10, bold=True)
    ws_dash.cell(row=t_row, column=7).number_format = '0.0"%"'

    for col_idx in range(1, 8):
        cell = ws_dash.cell(row=t_row, column=col_idx)
        cell.fill = PatternFill(fill_type="solid", fgColor="EBF1F5")
        cell.border = border_thin
        cell.alignment = Alignment(horizontal="center", vertical="center")

    # =========================================================
    # ساخت شیت ۱۰: راهنمای کاربری
    # =========================================================
    print("در حال ایجاد شیت راهنمای کاربری...")
    ws_guide = wb.create_sheet(title="📖 راهنمای کاربری")
    ws_guide.sheet_view.rightToLeft = True

    guide_lines = [
        ("راهنمای جامع کار با فایل اکسل کاتالوگ حسینی کالا", "", "HEADER"),
        ("", "", "EMPTY"),
        ("۱. معماری ۸ دسته‌بندی اصلی:", "دسته‌بندی‌های این فایل دقیقاً با منوی اصلی فروشگاه حسینی کالا یکپارچه شده‌اند تا از شلوغی و تعدد تب‌ها جلوگیری شود.", "SECTION"),
        ("• یخچال و فریزر", "شامل یخچال‌های ساید، دوقلو، کمبی و هتلی از برندهای کلور، دیپوینت، هیمالیا، الکترواستیل، ایستکول و بست.", "BULLET"),
        ("• شستشو و نظافت", "شامل ماشین‌های لباسشویی، ظرفشویی، جاروبرقی‌های کیسه‌ای و سطلی، پتوشور و انواع اتو بخار.", "BULLET"),
        ("• لوازم برقی و پخت و پز", "شامل سرخ‌کن، غذاساز، گوشت‌کوب برقی، اجاق گاز، فر توکار، انواع ظروف گرانیتی، قابلمه، تابه و زودپز.", "BULLET"),
        ("• نوشیدنی ساز", "شامل اسپرسوساز، چای‌ساز، سماور برقی، کتری برقی، آبمیوه‌گیری، مخلوط‌کن، آسیاب و همزن.", "BULLET"),
        ("• سرمایش و گرمایش", "شامل کولرهای آبی سلولزی، کولر گازی، انواع پنکه ایستاده و بخاری‌های گازی و برقی.", "BULLET"),
        ("• تصفیه کننده آب", "شامل دستگاه‌های تصفیه آب خانگی اسمز معکوس، آبسردکن‌های اداری و مخزن‌دار.", "BULLET"),
        ("• صوتی و تصویری", "شامل تلویزیون‌های هوشمند 4K و ال‌ای‌دی در سایزهای ۳۲ تا ۸۵ اینچ.", "BULLET"),
        ("• زیبایی و سلامت فردی", "شامل ماشین‌های اصلاح سر و صورت، ریش‌تراش، سشوار، اتو مو و اپیلاتورهای حرفه‌ای.", "BULLET"),
        ("", "", "EMPTY"),
        ("۲. ساختار محصولات متغیر و تنوع‌ها:", "محصولاتی که چند رنگ، سایز یا مدل دارند (مانند یخچال‌های سفید و استیل، قابلمه‌ها با سایزهای مختلف) دارای سطرهای فرعی درختی (↳) هستند. شناسه Variation ID به صورت مجزا ثبت شده تا ویرایش قیمت و موجودی هر رنگ به تفکیک انجام گیرد.", "SECTION"),
        ("", "", "EMPTY"),
        ("۳. نحوه ویرایش قیمت‌ها و فرمول تومان:", "قیمت‌ها در ستون «قیمت عادی (ریال)» به ریال وارد می‌شوند و اکسل به‌صورت خودکار در ستون کناری آن قیمت تومان را با فرمول (=B/10) محاسبه می‌کند. برای ویرایش قیمت در سایت، کافیست ستون ریال را تغییر دهید.", "SECTION"),
        ("", "", "EMPTY"),
        ("۴. وضعیت موجودی و منوی کشویی:", "در ستون وضعیت موجودی، یک منوی کشویی با دو گزینه «✓ موجود» و «✗ ناموجود» تعبیه شده است که به راحتی قابل تغییر است.", "SECTION"),
        ("", "", "EMPTY"),
        ("۵. لینک‌های مستقیم و شناسه عددی:", "تمامی لینک‌های درج‌شده با شناسه عددی یکتا (?p=ID) تنظیم شده‌اند تا با تضمین ۱۰۰٪ و بدون ریدایرکت یا خطای ۴۰۴ در مرورگر باز شوند.", "SECTION"),
    ]

    ws_guide.column_dimensions['A'].width = 35
    ws_guide.column_dimensions['B'].width = 75

    for r_idx, (col1, col2, stype) in enumerate(guide_lines, 1):
        c1 = ws_guide.cell(row=r_idx, column=1, value=col1)
        c2 = ws_guide.cell(row=r_idx, column=2, value=col2)

        if stype == "HEADER":
            ws_guide.merge_cells(start_row=r_idx, start_column=1, end_row=r_idx, end_column=2)
            c1.font = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
            c1.fill = PatternFill(fill_type="solid", fgColor=COLOR_HEADER_BG)
            c1.alignment = Alignment(horizontal="center", vertical="center")
            ws_guide.row_dimensions[r_idx].height = 30
        elif stype == "SECTION":
            c1.font = Font(name="Calibri", size=11, bold=True, color=COLOR_HEADER_BG)
            c2.font = Font(name="Calibri", size=10, bold=True)
            c1.alignment = Alignment(horizontal="right", vertical="center")
            c2.alignment = Alignment(horizontal="right", vertical="center")
            ws_guide.row_dimensions[r_idx].height = 24
        elif stype == "BULLET":
            c1.font = Font(name="Calibri", size=10, bold=True, color="2E75B6")
            c2.font = Font(name="Calibri", size=10)
            c1.alignment = Alignment(horizontal="right", vertical="center")
            c2.alignment = Alignment(horizontal="right", vertical="center")
            ws_guide.row_dimensions[r_idx].height = 20
        else:
            ws_guide.row_dimensions[r_idx].height = 16

    # ذخیره در فایل خروجی اصلی و لایو
    wb.save(EXCEL_OUT_LATEST)
    print(f"  ✓ ذخیره موفق: {EXCEL_OUT_LATEST}")

    try:
        wb.save(EXCEL_OUT_MAIN)
        print(f"  ✓ ذخیره موفق: {EXCEL_OUT_MAIN}")
    except PermissionError:
        print(f"  ⚠️ [توجه] فایل '{os.path.basename(EXCEL_OUT_MAIN)}' در برنامه Excel باز است و قفل شده است.")
        print(f"  ✓ تمامی داده‌ها در '{os.path.basename(EXCEL_OUT_LATEST)}' با موفقیت و کامل ذخیره شدند.")

    print("\n" + "=" * 60)
    print(f"✓ کاتالوگ با موفقیت آماده شد!")
    print(f"  فایل اصلی نهایی: {EXCEL_OUT_LATEST}")
    print(f"  کل سطرهای والد: {stats['total_parent_rows']}")
    print(f"  کل سطرهای تنوع: {stats['total_variation_rows']}")
    print(f"  کل شیت‌ها: {len(wb.sheetnames)} شیت (داشبورد + ۸ دسته اصلی + راهنما)")
    print("=" * 60)

if __name__ == '__main__':
    build_catalog_workbook()

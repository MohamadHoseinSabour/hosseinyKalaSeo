"""
update_full_catalog_excel.py
============================
اسکریپت جامع به‌روزرسانی فایل اکسل کاتالوگ حسینی کالا بر اساس آخرین دیتای استخراج‌شده از سایت:
- عناوین دقیق و بروز
- قیمت‌های عادی و حراج (ریال + محاسبه خودکار تومان با فرمول)
- تشخیص دقیق نوع محصول (ساده vs متغیر)
- درج تک‌تک تنوع‌ها و متغیرها (رنگ، سایز، ابعاد، مدل) با Variation ID و لینک مستقیم
- حفظ اقلام لیست کاربر با دسته‌بندی موضوعی
- طراحی RTL شیک، منوی کشویی موجودی، داشبورد آماری و راهنمای کاربری
"""

import os
import sys
import json
import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.chart import BarChart, DoughnutChart, Reference

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"c:\Users\mmhhs\OneDrive\Documents\GitHub\hosseinyKalaSeo"
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
RAW_FILE = os.path.join(DATA_DIR, 'products_raw.json')
EXCEL_OUT_1 = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.xlsx')
EXCEL_OUT_2 = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog_latest.xlsx')

with open(RAW_FILE, encoding='utf-8') as f:
    live_products = json.load(f)

live_by_id = {p['product_id']: p for p in live_products}

# ستون‌های اکسل
COLUMNS = [
    # (key,              header_text,                 width,  align,   is_price,  is_formula)
    ("name",             "نام محصول",                  42,     "right",   False,     False),
    ("price_regular",    "قیمت عادی (ریال)",          18,     "center",  True,      False),
    ("price_reg_toman",  "قیمت عادی (تومان)",          18,     "center",  True,      True),
    ("price_sale",       "قیمت حراج (ریال)",          18,     "center",  True,      False),
    ("price_sale_toman", "قیمت حراج (تومان)",          18,     "center",  True,      True),
    ("in_stock",         "وضعیت موجودی",               14,     "center",  False,     False),
    ("category_path",    "دسته‌بندی / برند",           26,     "right",   False,     False),
    ("type",             "نوع محصول",                  14,     "center",  False,     False),
    ("variant_attr",     "مشخصه تنوع / متغیر",         22,     "center",  False,     False),
    ("product_id",       "شناسه محصول (ID)",           16,     "center",  False,     False),
    ("variation_id",     "شناسه تنوع",                 15,     "center",  False,     False),
    ("link",             "لینک محصول در سایت",         38,     "left",    False,     False),
    ("sku",              "کد SKU",                     14,     "center",  False,     False),
    ("status_note",      "وضعیت در سایت",              22,     "center",  False,     False),
]

# رنگ‌ها
COLOR_HEADER_BG = "1F4E79"
COLOR_HEADER_TEXT = "FFFFFF"
COLOR_SUBCAT_BG = "E2EFDA"
COLOR_SUBCAT_TEXT = "375623"
COLOR_VAR_PARENT_BG = "D9E1F2"   # آبی ملایم برای سطر والد متغیر
COLOR_VARIATION_BG = "F2F2F2"    # خاکستری روشن برای سطرهای تنوع
COLOR_MISSING_BG = "FFF2CC"      # زرد ملایم برای اقلام ثبت‌نشده در سایت
COLOR_TOMAN_HEADER_BG = "2E75B6"
COLOR_IN_STOCK_TEXT = "27AE60"
COLOR_OUT_OF_STOCK = "C00000"

def make_border():
    s = Side(style='thin', color='D9D9D9')
    return Border(top=s, bottom=s, left=s, right=s)

def clean_attr_val(v):
    if not v:
        return ""
    v = str(v).strip()
    return v

# ساختار دسته‌بندی‌ها و محصولات
# ساختار جامع شامل محصولات موجود در سایت (با تمام تنوع‌ها) + اقلام تکمیلی لیست کاربر
CAT_STRUCTURE = {
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
            3395, # یخچال و فریزر دوقلو 28 فوت هیمالیا مدل آیسپول
            {"name": "یخچال هیمالیا آیسپول استیل 60MW", "type": "simple", "site_id": None},
            {"name": "فریزر هیمالیا آیسپول استیل 60MW", "type": "simple", "site_id": None},
        ],
        "الکترواستیل": [
            3453, # یخچال فریزر دوقلو 21 فوت الکترواستیل مدل فیوچر
            {"name": "یخچال الکترواستیل یخساز تیتانیوم", "type": "simple", "site_id": None},
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
        "متفرقه": [
            {"name": "یخچال فریزر R(re01)", "type": "simple", "site_id": None},
        ],
    },

    "ماشین لباسشویی": {
        "کلور": [
            3573, # ماشین لباسشویی ۱۰ کیلوگرم اینورتر کلور مدل دایرکت درایو کرم
            2505, # ماشین لباسشویی 9 کیلوگرم اتوماتیک کلور مدل BMWT2
            2510, # ماشین لباسشویی 8 کیلوگرم اتوماتیک کلور مدل تاچ سری BMW T3
            {"name": "لباسشویی کلور ۹ کیلویی سفید ویوا", "type": "simple", "site_id": None},
            {"name": "لباسشویی کلور مدل 9771 سفید", "type": "simple", "site_id": None},
        ],
        "دوو": [
            2579, # ماشین لباسشویی هوشمند 9 کیلوگرم اتوماتیک دوو مدل LM-9170
            {"name": "اتوماتیک دوو کینو ۹۰۵ سینیور", "type": "simple", "site_id": None},
        ],
        "پاکشوما": [
            3707, # ماشین لباسشویی دوقلو ۲۱ کیلوگرم نیمه‌اتوماتیک پاکشوما
            3563, # ماشین لباسشویی دوقلو ۱۵ کیلوگرم نیمه‌اتوماتیک پاکشوما
            3557, # ماشین لباسشویی ۱۲ کیلوگرم درب از بالا اتوماتیک پاکشوما
            {"name": "لباسشویی دوقلو پاکشوما هاک", "type": "simple", "site_id": None},
        ],
        "ریتون": [
            3551, # ماشین لباسشویی ۱۷ کیلوگرم دوقلو ریتون مدل دو موتوره
        ],
        "پاکیزان": [
            3709, # پتوشور صنعتی و خانگی ۴۰ کیلوگرم تمام استیل پاکیزان
            {"name": "پتوشور صنعتی و خانگی ۲۰ کیلوگرم پاکیزان", "type": "simple", "site_id": None},
        ],
    },

    "ماشین ظرفشویی": {
        "کلور": [
            2871, # ماشین ظرفشویی 15 نفره کلور CDW-H15V
        ],
        "استیل لمسی / انفره": [
            3546, # ماشین ظرفشویی ۱۶ نفره استیل لمسی ۳ سبد
            {"name": "ظرفشویی انفره استیل", "type": "simple", "site_id": None},
        ],
    },

    "جاروبرقی": {
        "هیتاچی": [
            2519, # جاروبرقی سطلی هیتاچی مدل CV-950F
            {"name": "جاروبرقی هیتاچی سطلی ۱۲۰۰", "type": "simple", "site_id": None},
        ],
        "پاناسونیک": [
            2661, # جاروبرقی پاناسونیک مدل MC-CG715
        ],
        "بست (BOST)": [
            2885, # جاروبرقی بست مدل BVC-PC18B
        ],
        "دونالکس": [
            3510, # جاروبرقی ۲۴۰۰ وات دونالکس مدل DN-750 سوپرسایلنت
            {"name": "جاروبرقی دونالکس ۷۷۰", "type": "simple", "site_id": None},
        ],
        "سایر برندها": [
            {"name": "جاروبرقی کلور سطلی", "type": "simple", "site_id": None},
            {"name": "جاروبرقی آراز ۲۰ لیتر", "type": "simple", "site_id": None},
        ],
    },

    "کولر آبی و گازی": {
        "پاکشوما": [
            3266, # کولر گازی اسپلیت دیواری 18000 دور ثابت پاکشوما مدل TPA-18CH
        ],
        "ریتون": [
            2538, # کولر آبی سلولزی 16000 ریتون پرتابل VENTO 16000
            2559, # کولر آبی سلولزی 7000 ریتون مدل VENTO 7000
        ],
        "اوناکس": [
            {"name": "کولر آبی اوناکس 150L", "type": "simple", "site_id": None},
            {"name": "کولر آبی اوناکس B35", "type": "simple", "site_id": None},
        ],
        "اوجنرال": [
            {"name": "کولر پنجره‌ای اوجنرال ۱۸ هزار", "type": "simple", "site_id": None},
        ],
        "وستینگهاوس": [
            {"name": "کولر وستینگهاوس ۲۰ کوپلند", "type": "simple", "site_id": None},
        ],
        "سایر": [
            {"name": "کولر آبی مدل ۴۵۰۰", "type": "simple", "site_id": None},
        ],
    },

    "تصفیه آب و آبسردکن": {
        "سافت واتر": [
            2766, # دستگاه تصفیه کننده آب سافت واتر مدل IR-06
        ],
        "سی سی کا (C.C.K)": [
            3305, # دستگاه تصفیه آب خانگی سی سی کا مدل RO-13
        ],
        "هومگلد": [
            3504, # دستگاه تصفیه آب خانگی ۶ مرحله‌ای هومگلد مدل RO
        ],
        "افترون": [
            3301, # آبسردکن افترون مدل AFWD-5700
        ],
        "نیکایی": [
            3312, # آبسردکن ایستاده نیکایی مدل NWD_1400R یخچال دار
        ],
        "سایر برندها": [
            {"name": "تصفیه آب وست 5515", "type": "simple", "site_id": None},
            {"name": "آبسردکن هانو", "type": "simple", "site_id": None},
            {"name": "آبگرمکن الکترواستیل مخزندار دیواری", "type": "simple", "site_id": None},
        ],
    },

    "پخت و پز (گاز و فر)": {
        "آلتون": [
            3380, # اجاق گاز 5 شعله آلتون مدل MD5S
            3383, # اجاق گاز صفحه ای آلتون مدل S517N
            {"name": "گاز صفحه‌ای آلتون استیل SG518", "type": "simple", "site_id": None},
            {"name": "فر توکار آلتون ۷۳۰۳", "type": "simple", "site_id": None},
            {"name": "فرگاز آلتون MPS", "type": "simple", "site_id": None},
            {"name": "هود آلتون H312", "type": "simple", "site_id": None},
            {"name": "هود آلتون H315B", "type": "simple", "site_id": None},
        ],
        "الکترواستیل": [
            {"name": "فر الکترواستیل تیتانیوم ۱۱", "type": "simple", "site_id": None},
            {"name": "فر الکترواستیل عرض ۶۰ چرمی ۲۱", "type": "simple", "site_id": None},
        ],
    },

    "ظروف آشپزخانه": {
        "اویز و اویزپلاس": [
            3612, # شیرجوش گرانیتی ۱۴ سانتی‌متر اویزپلاس مشکی
            3610, # سرویس قابلمه ۱۲ پارچه گرانیتی اویزپلاس مدل مشکی رزگلد
            3608, # سرویس قابلمه ۲۴ پارچه گرانیتی اویزپلاس مدل سبز لایف
            3606, # سرویس زودپز دوقلو ۵ و ۷ لیتری کلیپسی اویزپلاس مشکی رزگلد
            3602, # زودپز کلیپسی ۷ لیتری اویزپلاس مشکی رزگلد
            3596, # قابلمه گرانیتی مشکی اویز (سایزهای ۱۶ تا ۲۶ و ۳۰ و ۳۲)
            3592, # سرویس قابلمه ۱۰ پارچه خمره‌ای اویز مدل سلین کرم
            3357, # سرویس پخت و پز 10 پارچه اویز مدل سلین
            3318, # سرویس پخت و پز 11 پارچه اویز پلاس مدل ویولا
        ],
        "سایر برندهای ظروف": [
            3354, # سرویس پخت و پز 10 پارچه مدل دستی لوکس
            {"name": "سرویس قابلمه استیل ۱۰ پارچه", "type": "simple", "site_id": None},
            {"name": "سرویس قابلمه اویزپلاس ۱۰ پارچه اناری", "type": "simple", "site_id": None},
            {"name": "تابه اویز سایز ۳۰", "type": "simple", "site_id": None},
            {"name": "تابه اویز سایز ۲۲ مشکی", "type": "simple", "site_id": None},
            {"name": "تابه اویز سایز ۲۶", "type": "simple", "site_id": None},
            {"name": "قابلمه مرغخوری اویزپلاس مشکی", "type": "simple", "site_id": None},
        ],
    },

    "آماده‌ساز غذا": {
        "دونالکس": [
            3711, # آبمیوه‌گیری تک‌کاره ۸۰۰ وات دونالکس مدل DN-110
            3019, # آبمیوه‌گیری ۴ کاره ۱۰۰۰ وات دونالکس مدل DN-110 (DN-120)
            3026, # سرخ‌کن 8 لیتر دونالکس مدل DN-950
            3626, # گوشت‌کوب و غذاساز چندکاره ۸۰۰ وات دونالکس مدل DN-290
            3032, # گوشت کوب برقی دونالکس مدل DN-275
            3035, # مخلوط کن و آسیاب کن 1.5 لیتری دونالکس مدل DN-205
            3622, # همزن دستی ۴۰۰ وات توربو دونالکس مدل DN-355
            3617, # ساندویچ‌ساز و گریل ۱۴۰۰ وات دونالکس مدل DN-940 سفید
        ],
        "وستینگهاوس": [
            3645, # همزن دستی ۳۵۰ وات رترو وستینگهاوس
            3640, # مخلوط‌کن رترو ۶۰۰ وات وستینگهاوس مدل WKBEB221
            3637, # توستر نان ۲ شیار رترو وستینگهاوس
        ],
        "گرنویک": [
            3647, # سرخ‌کن بدون روغن ۸ لیتری گرنویک مدل ProMar
        ],
        "زامروتی": [
            3655, # مخلوط‌کن رترو ۱.۵ لیتری ۶۰۰ وات زامروتی مدل 10038
        ],
        "فیلیپس": [
            3629, # غذاساز حرفه‌ای ۱۳۰۰ وات فیلیپس مدل HR7778
        ],
        "سایر برندهای آماده‌ساز": [
            3631, # آون توستر ۶۰ لیتری کانوکشن نان دلمونتی مدل DN-580
            {"name": "آسیاب کاستلو ۲۷۰", "type": "simple", "site_id": None},
            {"name": "سبزی خردکن KENRA", "type": "simple", "site_id": None},
            {"name": "سبزی خردکن نیکا ۲ کیلویی", "type": "simple", "site_id": None},
            {"name": "پلوپز پارس خزر ۸ نقره", "type": "simple", "site_id": None},
            {"name": "پلوپز پارس خزر مدل ۳۶۱", "type": "simple", "site_id": None},
            {"name": "همزن اوریکس کاسه چرخدار", "type": "simple", "site_id": None},
            {"name": "همزن کنوود ۴۳۰", "type": "simple", "site_id": None},
        ],
    },

    "نوشیدنی‌ساز و کتری": {
        "گرنویک": [
            3681, # سماور برقی پیرکس ۳.۲ لیتری گرنویک مدل GST-883
            3679, # اسپرسوساز ۲۰ بار گرنویک مدل رترو آنالوگ
        ],
        "کورکماز": [
            3673, # چای‌ساز تمام استیل کورکماز مدل A331 چای‌تما
        ],
        "دونالکس": [
            3013, # اسپرسو ساز ۱۲ میلی لیتر دونالکس مدلDN480
            3016, # اسپرسو ساز ۱۸ میلی لیتر دونالکس مدل DN475
            3457, # چای ساز دونالکس مدل DN-185
        ],
        "وستینگهاوس": [
            3664, # کتری برقی رترو ۲۲۰۰ وات وستینگهاوس مدل WKKE210
        ],
        "زامروتی": [
            3657, # سماور برقی ۳ لیتری دیجیتال پیرکس زامروتی
            3660, # کتری برقی رترو ۱.۷ لیتری زامروتی مدل عقربه‌ای کرم
            {"name": "کتری و قوری زامروتی دسته استیل ۲۰۲۲", "type": "simple", "site_id": None},
            {"name": "کتری و قوری زامروتی دسته چوب ۲۰۲۲", "type": "simple", "site_id": None},
        ],
        "وگاتی": [
            3668, # کتری برقی ۱.۸ لیتری وگاتی مدل توپی
        ],
        "سایر": [
            3653, # کتری برقی استیل ۲۰۰۰ وات اریکسون مدل ۱.۸ لیتری
            3662, # کتری و قوری روگازی هرمی ۵ لیتری استیل طلا مدل 604
            {"name": "کتری برقی سانی ۱.۵ لیتر", "type": "simple", "site_id": None},
            {"name": "کتری برقی پروکس", "type": "simple", "site_id": None},
        ],
    },

    "اصلاح و زیبایی": {
        "پرومارون": [
            3500, # برس حرارتی صاف‌کننده مو پرومارون مدل 1113 تورمالین
            3494, # اپیلاتور شارژی ۵ کاره پرومارون مدل 614 ضدآب
            3488, # اتومو باریک سرامیکی پرومارون مدل 1116
            3484, # اتومو کراتینه سرامیک تیتانیوم پرومارون مدل 1115
            {"name": "فرکننده مو پرومارون ۴+", "type": "simple", "site_id": None},
            {"name": "ریشتراش پرومارون ۷۰۶", "type": "simple", "site_id": None},
        ],
        "پرو امگا": [
            3049, # سشوار حرفه ای پرو امگا مدل 8806
            3285, # سشوار پرو امگا مدل 8805
            3065, # ماشین اصلاح موی سر و صورت پرو امگا مدل T7
            3056, # ماشین اصلاح موی سر و صورت پرو امگا مدل T5
            {"name": "ماشین اصلاح پروامگا شارژی و برقی", "type": "simple", "site_id": None},
        ],
        "سایر برندهای شخصی": [
            {"name": "اتو مو پاناسونیک HV11", "type": "simple", "site_id": None},
            {"name": "اتو مو Baby3383A", "type": "simple", "site_id": None},
            {"name": "دستگاه پیرایش سیمی صورت ۷۲۱", "type": "simple", "site_id": None},
        ],
    },

    "لوازم برقی خانگی (اتو)": {
        "دونالکس": [
            3007, # اتو بخار ۲۵۰۰ وات دونالکس مدل 815
        ],
        "فیلیپس": [
            3271, # اتو بخار فیلیپس مدل DST5040
        ],
    },

    "صوتی و تصویری": {
        "تلویزیون": [
            3534, # تلویزیون ال ای دی ۸۵ اینچ هوشمند 4K اسمارت Averson مدل Ultra HD
            3531, # تلویزیون ال ای دی ۷۵ اینچ هوشمند 4K هاورسون مدل Cinema HDR
            3523, # تلویزیون ال ای دی ۶۵ اینچ هوشمند 4K هاورسون مدل Frameless IPS
            3520, # تلویزیون ال ای دی ۵۵ اینچ هوشمند 4K هاورسون مدل Smart Android
            3516, # تلویزیون ال ای دی ۳۲ اینچ Averson مدل HD
        ],
    },

    "پنکه و سیستم گرمایشی": {
        "پنکه": [
            3540, # پنکه ایستاده ریموت‌دار سانی مدل DWS-2600
            {"name": "پنکه پایه‌بلند 1455", "type": "simple", "site_id": None},
            {"name": "پنکه پارس خزر پایه‌بلند", "type": "simple", "site_id": None},
            {"name": "پنکه پاناسونیک ۲ حالته", "type": "simple", "site_id": None},
            {"name": "پنکه سانی ۷۶۰۰", "type": "simple", "site_id": None},
        ],
        "بخاری و گرمایشی": [
            {"name": "بخاری گلدن لوکس", "type": "simple", "site_id": None},
            {"name": "بخاری پارس خزر فندار FH-2000P", "type": "simple", "site_id": None},
            {"name": "بخاری پلار 32-067 شیشه‌ای", "type": "simple", "site_id": None},
        ],
        "متفرقه": [
            {"name": "کسورات اضافات کالا", "type": "simple", "site_id": None},
        ],
    },
}

def generate_catalog():
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    border_thin = make_border()
    
    total_live_items = 0
    total_missing_items = 0
    total_variations_count = 0
    total_parent_vars_count = 0
    total_simple_count = 0
    all_prices_toman = []
    
    category_metrics = []

    # ساخت شیت‌های دسته‌بندی
    for sheet_name, subcats in CAT_STRUCTURE.items():
        ws = wb.create_sheet(title=sheet_name[:31])
        ws.sheet_view.rightToLeft = True

        # هدر ستون‌ها
        ws.row_dimensions[1].height = 28
        for col_idx, (f_key, h_text, width, align_mode, is_price, is_formula) in enumerate(COLUMNS, start=1):
            cell = ws.cell(row=1, column=col_idx, value=h_text)
            cell.font = Font(bold=True, color=COLOR_HEADER_TEXT, size=10, name="Calibri")
            h_bg = COLOR_TOMAN_HEADER_BG if is_formula else COLOR_HEADER_BG
            cell.fill = PatternFill(fill_type='solid', fgColor=h_bg)
            cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            cell.border = border_thin
            ws.column_dimensions[get_column_letter(col_idx)].width = width

        ws.freeze_panes = 'A2'
        ws.auto_filter.ref = f"A1:{get_column_letter(len(COLUMNS))}1"

        row_idx = 2
        sheet_live_count = 0
        sheet_missing_count = 0
        sheet_prices_toman = []

        for subcat_name, item_list in subcats.items():
            # سطر بنر زیردسته/برند
            ws.row_dimensions[row_idx].height = 22
            ws.merge_cells(start_row=row_idx, start_column=1, end_row=row_idx, end_column=len(COLUMNS))
            sub_cell = ws.cell(row=row_idx, column=1, value=f"  📂 {sheet_name}  ◀  {subcat_name}")
            sub_cell.font = Font(bold=True, color=COLOR_SUBCAT_TEXT, size=10, name="Calibri")
            sub_cell.fill = PatternFill(fill_type='solid', fgColor=COLOR_SUBCAT_BG)
            sub_cell.alignment = Alignment(horizontal='right', vertical='center')
            for c in range(1, len(COLUMNS) + 1):
                ws.cell(row=row_idx, column=c).border = border_thin
            row_idx += 1

            cat_path = f"{sheet_name} / {subcat_name}"

            for item in item_list:
                # اگر item یک عدد باشد یعنی ID محصول در سایت است
                if isinstance(item, int):
                    prod = live_by_id.get(item)
                    if not prod:
                        continue
                    
                    pid = prod['product_id']
                    pname = prod['name']
                    ptype = prod['type']
                    reg_price = prod.get('price_regular') or ""
                    sale_price = prod.get('price_sale') or ""
                    in_stk = "موجود" if prod.get('in_stock', True) else "ناموجود"
                    stk_color = COLOR_IN_STOCK_TEXT if in_stk == "موجود" else COLOR_OUT_OF_STOCK
                    link_val = prod.get('shortlink', f"https://hosseinykala.ir/?p={pid}")
                    sku_val = prod.get('sku', '')

                    if ptype == 'variable':
                        total_parent_vars_count += 1
                        sheet_live_count += 1
                        total_live_items += 1
                        vars_list = prod.get('variations', [])
                        var_summary = f"شامل {len(vars_list)} تنوع (رنگ/مدل)"

                        if reg_price:
                            sheet_prices_toman.append(int(reg_price) // 10)
                            all_prices_toman.append(int(reg_price) // 10)

                        # سطر والد متغیر
                        parent_row_data = {
                            "name": pname,
                            "price_regular": reg_price,
                            "price_reg_toman": f'=IF(OR(B{row_idx}="",B{row_idx}=0),"",B{row_idx}/10)',
                            "price_sale": sale_price,
                            "price_sale_toman": f'=IF(OR(D{row_idx}="",D{row_idx}=0),"",D{row_idx}/10)',
                            "in_stock": in_stk,
                            "category_path": cat_path,
                            "type": "متغیر",
                            "variant_attr": var_summary,
                            "product_id": pid,
                            "variation_id": "",
                            "link": link_val,
                            "sku": sku_val,
                            "status_note": "✓ محصول متغیر در سایت",
                        }

                        ws.row_dimensions[row_idx].height = 21
                        parent_fill = PatternFill(fill_type='solid', fgColor=COLOR_VAR_PARENT_BG)

                        for c_idx, (f_key, _, _, align_mode, is_price, is_formula) in enumerate(COLUMNS, start=1):
                            val = parent_row_data.get(f_key, "")
                            c = ws.cell(row=row_idx, column=c_idx, value=val)
                            c.fill = parent_fill
                            c.alignment = Alignment(horizontal=align_mode, vertical='center')
                            c.border = border_thin
                            c.font = Font(bold=(f_key in ("name", "type")), size=10, name="Calibri")

                            if is_price or is_formula:
                                c.number_format = '#,##0'
                                if isinstance(val, int) or is_formula:
                                    c.font = Font(bold=True, size=10, color="1F4E79" if is_formula else "000000", name="Calibri")
                            if f_key == "in_stock":
                                c.font = Font(bold=True, color=stk_color, size=10, name="Calibri")
                            if f_key == "link" and val:
                                c.hyperlink = val
                                c.style = "Hyperlink"
                                c.fill = parent_fill
                            if f_key == "status_note":
                                c.font = Font(size=9, color="27AE60", bold=True, name="Calibri")

                        row_idx += 1

                        # سطرهای فرزند (تنوع‌ها)
                        for v in vars_list:
                            vid = v['variation_id']
                            v_reg = v.get('price_regular') or ""
                            v_sale = v.get('price_sale') or ""
                            v_stk = "موجود" if v.get('in_stock', True) else "ناموجود"
                            v_stk_color = COLOR_IN_STOCK_TEXT if v_stk == "موجود" else COLOR_OUT_OF_STOCK
                            v_link = v.get('shortlink', f"https://hosseinykala.ir/?p={vid}")
                            
                            # نام و ویژگی تنوع
                            v_attrs = v.get('attributes', {})
                            attr_desc_list = [f"{k}: {val}" for k, val in v_attrs.items()] if v_attrs else ["پیش‌فرض"]
                            attr_str = " | ".join(attr_desc_list)
                            var_row_name = f"    ↳ {attr_str}"

                            total_variations_count += 1

                            if v_reg:
                                sheet_prices_toman.append(int(v_reg) // 10)
                                all_prices_toman.append(int(v_reg) // 10)

                            var_row_data = {
                                "name": var_row_name,
                                "price_regular": v_reg,
                                "price_reg_toman": f'=IF(OR(B{row_idx}="",B{row_idx}=0),"",B{row_idx}/10)',
                                "price_sale": v_sale,
                                "price_sale_toman": f'=IF(OR(D{row_idx}="",D{row_idx}=0),"",D{row_idx}/10)',
                                "in_stock": v_stk,
                                "category_path": cat_path,
                                "type": "تنوع (واریاسیون)",
                                "variant_attr": attr_str,
                                "product_id": pid,
                                "variation_id": vid,
                                "link": v_link,
                                "sku": v.get('sku', ''),
                                "status_note": "✓ تنوع فعال در سایت",
                            }

                            ws.row_dimensions[row_idx].height = 19
                            var_fill = PatternFill(fill_type='solid', fgColor=COLOR_VARIATION_BG)

                            for c_idx, (f_key, _, _, align_mode, is_price, is_formula) in enumerate(COLUMNS, start=1):
                                val = var_row_data.get(f_key, "")
                                c = ws.cell(row=row_idx, column=c_idx, value=val)
                                c.fill = var_fill
                                c.alignment = Alignment(horizontal=align_mode, vertical='center')
                                c.border = border_thin
                                c.font = Font(size=9.5, name="Calibri")

                                if f_key == "name":
                                    c.font = Font(size=9.5, italic=True, color="333333", name="Calibri")
                                if is_price or is_formula:
                                    c.number_format = '#,##0'
                                    c.font = Font(bold=True, size=9.5, color="1F4E79", name="Calibri")
                                if f_key == "in_stock":
                                    c.font = Font(bold=True, color=v_stk_color, size=9.5, name="Calibri")
                                if f_key == "link" and val:
                                    c.hyperlink = val
                                    c.style = "Hyperlink"
                                    c.fill = var_fill
                                if f_key == "status_note":
                                    c.font = Font(size=9, color="555555", name="Calibri")

                            row_idx += 1

                    else:
                        # محصول ساده موجود در سایت
                        total_simple_count += 1
                        sheet_live_count += 1
                        total_live_items += 1

                        if reg_price:
                            sheet_prices_toman.append(int(reg_price) // 10)
                            all_prices_toman.append(int(reg_price) // 10)

                        simple_row_data = {
                            "name": pname,
                            "price_regular": reg_price,
                            "price_reg_toman": f'=IF(OR(B{row_idx}="",B{row_idx}=0),"",B{row_idx}/10)',
                            "price_sale": sale_price,
                            "price_sale_toman": f'=IF(OR(D{row_idx}="",D{row_idx}=0),"",D{row_idx}/10)',
                            "in_stock": in_stk,
                            "category_path": cat_path,
                            "type": "ساده",
                            "variant_attr": "-",
                            "product_id": pid,
                            "variation_id": "",
                            "link": link_val,
                            "sku": sku_val,
                            "status_note": "✓ موجود در سایت",
                        }

                        ws.row_dimensions[row_idx].height = 20
                        row_fill = PatternFill(fill_type='solid', fgColor="FFFFFF")

                        for c_idx, (f_key, _, _, align_mode, is_price, is_formula) in enumerate(COLUMNS, start=1):
                            val = simple_row_data.get(f_key, "")
                            c = ws.cell(row=row_idx, column=c_idx, value=val)
                            c.fill = row_fill
                            c.alignment = Alignment(horizontal=align_mode, vertical='center')
                            c.border = border_thin
                            c.font = Font(size=10, name="Calibri")

                            if is_price or is_formula:
                                c.number_format = '#,##0'
                                if isinstance(val, int) or is_formula:
                                    c.font = Font(bold=True, size=10, color="1F4E79" if is_formula else "000000", name="Calibri")
                            if f_key == "in_stock":
                                c.font = Font(bold=True, color=stk_color, size=10, name="Calibri")
                            if f_key == "link" and val:
                                c.hyperlink = val
                                c.style = "Hyperlink"
                                c.fill = row_fill
                            if f_key == "status_note":
                                c.font = Font(size=9, color="27AE60", bold=True, name="Calibri")

                        row_idx += 1

                elif isinstance(item, dict):
                    # محصول لیست کاربر که هنوز روی سایت ثبت نشده است
                    pname = item.get('name')
                    ptype = item.get('type', 'simple')
                    total_missing_items += 1
                    sheet_missing_count += 1

                    missing_row_data = {
                        "name": pname,
                        "price_regular": "",
                        "price_reg_toman": f'=IF(OR(B{row_idx}="",B{row_idx}=0),"",B{row_idx}/10)',
                        "price_sale": "",
                        "price_sale_toman": f'=IF(OR(D{row_idx}="",D{row_idx}=0),"",D{row_idx}/10)',
                        "in_stock": "ناموجود",
                        "category_path": cat_path,
                        "type": "ساده",
                        "variant_attr": "-",
                        "product_id": "",
                        "variation_id": "",
                        "link": "",
                        "sku": "",
                        "status_note": "نیازمند ثبت در سایت",
                    }

                    ws.row_dimensions[row_idx].height = 20
                    missing_fill = PatternFill(fill_type='solid', fgColor=COLOR_MISSING_BG)

                    for c_idx, (f_key, _, _, align_mode, is_price, is_formula) in enumerate(COLUMNS, start=1):
                        val = missing_row_data.get(f_key, "")
                        c = ws.cell(row=row_idx, column=c_idx, value=val)
                        c.fill = missing_fill
                        c.alignment = Alignment(horizontal=align_mode, vertical='center')
                        c.border = border_thin
                        c.font = Font(size=10, name="Calibri")

                        if is_price or is_formula:
                            c.number_format = '#,##0'
                        if f_key == "in_stock":
                            c.font = Font(size=10, color=COLOR_OUT_OF_STOCK, bold=True, name="Calibri")
                        if f_key == "status_note":
                            c.font = Font(size=9, italic=True, color="806000", name="Calibri")

                    row_idx += 1

        # اضافه کردن منوی کشویی وضعیت موجودی
        dv_stock = DataValidation(
            type="list",
            formula1='"موجود,ناموجود"',
            allow_blank=True,
            showDropDown=False,
            showErrorMessage=True,
            errorTitle="خطای انتخاب",
            error="لطفاً وضعیت موجودی را از بین گزینه‌های «موجود» یا «ناموجود» انتخاب کنید."
        )
        ws.add_data_validation(dv_stock)
        dv_stock.add(f"F2:F{row_idx}")

        avg_price = (sum(sheet_prices_toman) // len(sheet_prices_toman)) if sheet_prices_toman else 0
        category_metrics.append({
            "name": sheet_name,
            "subcats_count": len(subcats),
            "live_count": sheet_live_count,
            "missing_count": sheet_missing_count,
            "total_items": sheet_live_count + sheet_missing_count,
            "avg_price_toman": avg_price
        })

    # ─────────────────────────────────────────────────────────
    # ساخت داشبورد مدیریتی و گزارش در شیت اول
    # ─────────────────────────────────────────────────────────
    ws_dash = wb.create_sheet("📊 خلاصه و داشبورد", index=0)
    ws_dash.sheet_view.rightToLeft = True

    now_str = datetime.datetime.now().strftime("%Y/%m/%d - %H:%M")
    avg_price_global = (sum(all_prices_toman) // len(all_prices_toman)) if all_prices_toman else 0
    max_price_global = max(all_prices_toman) if all_prices_toman else 0
    min_price_global = min(all_prices_toman) if all_prices_toman else 0

    # عنوان داشبورد
    ws_dash.merge_cells("A1:J1")
    t_cell = ws_dash["A1"]
    t_cell.value = "📊 داشبورد کاتالوگ جامع و بروزرسانی محصولات — فروشگاه لوازم خانگی حسینی"
    t_cell.font = Font(bold=True, size=14, color="FFFFFF", name="Calibri")
    t_cell.fill = PatternFill(fill_type='solid', fgColor="1F4E79")
    t_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws_dash.row_dimensions[1].height = 36

    # کارت‌های شاخص (KPI Cards)
    cards = [
        ("کل محصولات فعال سایت", f"{len(live_products)} کالا", f"{total_parent_vars_count} مدل متغیر + {total_simple_count} مدل ساده", "27AE60"),
        ("کل تنوع‌ها و متغیرها", f"{total_variations_count} ردیف", "تفکیک رنگ، سایز و ظرفیت", "2E75B6"),
        ("دسته‌بندی‌های اصلی", f"{len(CAT_STRUCTURE)} دسته", "تفکیک در شیت‌های مجزا", "1F4E79"),
        ("میانگین قیمت اقلام", f"{avg_price_global:,} تومان", "بر اساس قیمت‌های جاری سایت", "2E75B6"),
        ("اقلام آماده ثبت", f"{total_missing_items} مدل", "محصولات لیست جهت درج", "C00000"),
    ]

    ws_dash.row_dimensions[3].height = 20
    ws_dash.row_dimensions[4].height = 26
    ws_dash.row_dimensions[5].height = 18

    col_starts = [1, 3, 5, 7, 9]
    for (title, value, subtext, color), c_start in zip(cards, col_starts):
        c_end = c_start + 1
        ws_dash.merge_cells(start_row=3, start_column=c_start, end_row=3, end_column=c_end)
        ws_dash.merge_cells(start_row=4, start_column=c_start, end_row=4, end_column=c_end)
        ws_dash.merge_cells(start_row=5, start_column=c_start, end_row=5, end_column=c_end)

        c3 = ws_dash.cell(row=3, column=c_start, value=title)
        c3.font = Font(bold=True, size=9.5, color="FFFFFF", name="Calibri")
        c3.fill = PatternFill(fill_type='solid', fgColor=color)
        c3.alignment = Alignment(horizontal="center", vertical="center")

        c4 = ws_dash.cell(row=4, column=c_start, value=value)
        c4.font = Font(bold=True, size=13, color=color, name="Calibri")
        c4.fill = PatternFill(fill_type='solid', fgColor="F2F5F9")
        c4.alignment = Alignment(horizontal="center", vertical="center")

        c5 = ws_dash.cell(row=5, column=c_start, value=subtext)
        c5.font = Font(size=8, italic=True, color="555555", name="Calibri")
        c5.fill = PatternFill(fill_type='solid', fgColor="F2F5F9")
        c5.alignment = Alignment(horizontal="center", vertical="center")

        for r in range(3, 6):
            for col in range(c_start, c_end + 1):
                ws_dash.cell(row=r, column=col).border = border_thin

    # نوار اطلاعات قیمت و زمان
    ws_dash.merge_cells("A7:J7")
    info_bar = ws_dash["A7"]
    info_bar.value = f"⏱ آخرین استخراج مستقیم از سایت: {now_str}  |  💰 بالاترین قیمت: {max_price_global:,} تومان  |  🔻 پایین‌ترین قیمت: {min_price_global:,} تومان"
    info_bar.font = Font(bold=True, size=9.5, color="1F4E79", name="Calibri")
    info_bar.fill = PatternFill(fill_type='solid', fgColor="E2EFDA")
    info_bar.alignment = Alignment(horizontal="center", vertical="center")
    info_bar.border = border_thin
    ws_dash.row_dimensions[7].height = 24

    # جدول تفکیک دسته‌بندی‌ها
    table_headers = [
        ("ردیف", 8),
        ("نام دسته‌بندی اصلی", 25),
        ("تعداد برند / زیردسته", 20),
        ("کالاهای ثبت‌شده در سایت", 22),
        ("اقلام در انتظار ثبت", 18),
        ("میانگین قیمت (تومان)", 20),
        ("وضعیت پوشش", 16),
    ]

    ws_dash.merge_cells("A9:G9")
    t_header = ws_dash["A9"]
    t_header.value = "📋 جدول تفکیک آمار دسته‌بندی‌های فروشگاه حسینی کالا"
    t_header.font = Font(bold=True, size=11, color="1F4E79", name="Calibri")
    t_header.alignment = Alignment(horizontal="right", vertical="center")

    ws_dash.row_dimensions[10].height = 26
    for c_i, (h_text, w) in enumerate(table_headers, start=1):
        cell = ws_dash.cell(row=10, column=c_i, value=h_text)
        cell.font = Font(bold=True, color="FFFFFF", size=9.5, name="Calibri")
        cell.fill = PatternFill(fill_type='solid', fgColor="1F4E79")
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border_thin
        ws_dash.column_dimensions[get_column_letter(c_i)].width = w

    t_row_start = 11
    for idx, stat in enumerate(category_metrics, start=1):
        r_num = t_row_start + idx - 1
        ws_dash.row_dimensions[r_num].height = 20
        total_cat = stat["live_count"] + stat["missing_count"]
        coverage_pct = f"{round((stat['live_count'] / total_cat * 100), 1)}%" if total_cat else "0%"

        row_vals = [
            (idx, "center", False),
            (stat["name"], "right", True),
            (stat["subcats_count"], "center", False),
            (stat["live_count"], "center", True),
            (stat["missing_count"], "center", False),
            (stat["avg_price_toman"], "center", False),
            (coverage_pct, "center", False),
        ]

        r_fill = PatternFill(fill_type='solid', fgColor="FFFFFF" if idx % 2 != 0 else "F9FAFB")
        for col_i, (val, aln_mode, is_bold) in enumerate(row_vals, start=1):
            c = ws_dash.cell(row=r_num, column=col_i, value=val)
            c.fill = r_fill
            c.alignment = Alignment(horizontal=aln_mode, vertical="center")
            c.border = border_thin
            c.font = Font(size=9.5, bold=is_bold, name="Calibri")
            if col_i == 6 and isinstance(val, int) and val > 0:
                c.number_format = '#,##0'
            if col_i == 4 and val > 0:
                c.font = Font(bold=True, color="27AE60", size=9.5, name="Calibri")
            if col_i == 5 and val > 0:
                c.font = Font(color="806000", size=9.5, name="Calibri")

    # سطر مجموع جدول
    tot_row = t_row_start + len(category_metrics)
    ws_dash.row_dimensions[tot_row].height = 22
    tot_vals = [
        "مجموع",
        f"{len(category_metrics)} دسته",
        sum(s['subcats_count'] for s in category_metrics),
        total_live_items,
        total_missing_items,
        avg_price_global,
        f"{round((total_live_items/(total_live_items+total_missing_items))*100, 1)}%",
    ]
    ws_dash.merge_cells(start_row=tot_row, start_column=1, end_row=tot_row, end_column=2)
    for col_i, val in enumerate(tot_vals, start=1):
        if col_i == 2: continue
        target_col = 1 if col_i == 1 else col_i
        c = ws_dash.cell(row=tot_row, column=target_col, value=val)
        c.fill = PatternFill(fill_type='solid', fgColor="D9E1F2")
        c.font = Font(bold=True, size=10, color="1F4E79", name="Calibri")
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.border = border_thin
        if col_i == 6 and isinstance(val, int):
            c.number_format = '#,##0'

    # راهنمای کاربری
    guide_start_row = tot_row + 3
    ws_dash.merge_cells(start_row=guide_start_row, start_column=1, end_row=guide_start_row, end_column=10)
    g_title = ws_dash.cell(row=guide_start_row, column=1, value="📖 راهنمای کاربری، ساختار ستون‌ها و مدیریت قیمت‌ها")
    g_title.font = Font(bold=True, size=12, color="FFFFFF", name="Calibri")
    g_title.fill = PatternFill(fill_type='solid', fgColor="1F4E79")
    g_title.alignment = Alignment(horizontal="right", vertical="center")
    ws_dash.row_dimensions[guide_start_row].height = 28

    guide_entries = [
        ("ستون‌های شیت‌ها (از راست به چپ):", ""),
        ("• نام محصول (ستون A):", "نام کامل و استاندارد کالا (شامل سطر والد یا سطرهای مجزای رنگ/مدل با تورفتگی ↳)."),
        ("• قیمت عادی (ریال) (ستون B):", "قیمت پایه بدون تخفیف به ریال (عدد خالص). به صورت خودکار ۳ رقم ۳ رقم تفکیک می‌شود (#,##0)."),
        ("• قیمت عادی (تومان) (ستون C):", "محاسبه خودکار با فرمول اکسل (=B2/10). با تغییر قیمت ریال، معادل تومان بلافاصله بروز می‌شود."),
        ("• قیمت حراج (ریال و تومان) (ستون D و E):", "قیمت با تخفیف کالا در فروشگاه (در صورت وجود تخفیف فعال در سایت)."),
        ("• وضعیت موجودی (ستون F):", "دارای منوی کشویی انتخابی جهت تغییر سریع موجودی بین گزینه‌های «موجود» و «ناموجود»."),
        ("• دسته‌بندی و نوع محصول (ستون G و H):", "مسیر دسته‌بندی و نوع کالا (ساده: قیمت ثابت | متغیر: کالای چندرنگ | تنوع: رنگ/مدل اختصاصی)."),
        ("• مشخصه تنوع / متغیر (ستون I):", "نمایش مشخصات متغیر شامل رنگ، ابعاد، گنجایش یا مدل هر تنوع."),
        ("• شناسه‌ها و لینک (ستون J تا L):", "شامل Product ID و Variation ID جهت اتصال به وردپرس و لینک مستقیم عددی ?p=ID بدون خطای انکودینگ."),
        ("", ""),
        ("راهنمای رنگ‌بندی سطرها:", ""),
        ("• آبی ملایم:", "سطر والد محصولات متغیر (کالاهایی که دارای چند رنگ یا مشخصه هستند)."),
        ("• خاکستری روشن:", "سطرهای تنوع اختصاصی هر رنگ/مدل با قیمت و شناسه تنوع (Variation ID) مجزا."),
        ("• زرد ملایم:", "کالاهایی که هنوز روی سایت ثبت نشده‌اند (قیمت‌ها خالی و آماده ورود اطلاعات)."),
        ("• سفید:", "کالاهای ساده موجود در سایت با اطلاعات و قیمت کامل."),
    ]

    for g_idx, (g_col1, g_col2) in enumerate(guide_entries, start=guide_start_row + 2):
        ws_dash.cell(row=g_idx, column=1, value=g_col1)
        ws_dash.cell(row=g_idx, column=2, value=g_col2)
        ws_dash.merge_cells(start_row=g_idx, start_column=2, end_row=g_idx, end_column=10)

        c1 = ws_dash.cell(row=g_idx, column=1)
        c2 = ws_dash.cell(row=g_idx, column=2)

        c1.alignment = Alignment(horizontal="right", vertical="center")
        c2.alignment = Alignment(horizontal="right", vertical="center")

        if g_col1.startswith("ستون‌های") or g_col1.startswith("راهنمای"):
            c1.font = Font(bold=True, size=10.5, color="1F4E79", name="Calibri")
            c2.font = Font(bold=True, size=10.5, color="1F4E79", name="Calibri")
        else:
            c1.font = Font(bold=True, size=9.5, color="333333", name="Calibri")
            c2.font = Font(size=9.5, color="555555", name="Calibri")

    # ذخیره در هر دو فایل اصلی و latest
    wb.save(EXCEL_OUT_1)
    wb.save(EXCEL_OUT_2)
    print(f"Successfully generated and saved updated Excel catalogs to:\n  1. {EXCEL_OUT_1}\n  2. {EXCEL_OUT_2}")

if __name__ == '__main__':
    generate_catalog()

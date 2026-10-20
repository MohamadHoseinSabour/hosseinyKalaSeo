"""
fix_catalog_structure.py
========================
اسکریپت ساخت کاتالوگ اکسل بدون هیچ‌گونه تکرار در دسته‌بندی‌ها یا محصولات
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
import os, json
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

PROJECT_DIR = r"c:\Users\mmhhs\OneDrive\Documents\GitHub\hosseinyKalaSeo"
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
RAW_FILE = os.path.join(DATA_DIR, 'products_raw.json')
EXCEL_OUTPUT = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.xlsx')
EXCEL_UPDATED = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog_updated.xlsx')

with open(RAW_FILE, encoding='utf-8') as f:
    site_products = json.load(f)

site_by_id = {p['product_id']: p for p in site_products}

# ساختار دسته‌بندی‌شده و مرتب (بدون تکرار)
# هر شیت شامل زیردسته‌ها، و هر زیردسته شامل لیست محصولات یکتا است.
SHEETS_STRUCTURE = {
    "یخچال و فریزر": {
        "کلور": [
            ("یخچال کلور مینی سبز پاستیلی", 2431, 2443), # Product 2431, Variation 2443 (سبز پاستیلی)
            ("یخچال کلور مینی قرمز", 2431, 2439),        # Product 2431, Variation 2439 (قرمز)
            ("یخچال و فریزر کلور کمبی FRNT101 سفید ساده", 2408, 2418),
            ("یخچال فریزر کلور روسو کمبی هوم‌بار سفید", 2484, None),
            ("یخچال فریزر کلور روسو کمبی هوم‌بار استیل", 2484, None),
            ("یخچال فریزر دوقلو کلور ۴۰ فوت گلوری عرض ۶۰ - سفید", 2471, 2475),
            ("یخچال فریزر دوقلو کلور ۴۰ فوت گلوری عرض ۶۰ - استیل", 2471, 2476),
            ("یخچال فریزر دوقلو کلور ۴۰ فوت روسوپلاس عرض ۶۰ - سفید", 2457, 2461),
            ("یخچال فریزر دوقلو کلور ۴۰ فوت روسوپلاس عرض ۶۰ - استیل", 2457, 2462),
            ("یخچال فریزر دوقلو کلور ۴۰ فوت روسوپلاس عرض ۶۰ - استیل بدون آبریز", 2457, 2463),
            ("یخچال فریزر دوقلو کلور ۴۴ فوت گلوریا پلاس LM70 - سفید", 2464, 2470),
            ("یخچال فریزر دوقلو کلور ۴۴ فوت گلوریا پلاس LM70 - استیل", 2464, 2469),
            ("یخچال فریزر کلور ۲۷ فوت گلوریا پلاس کمبی - سفید", 2497, 2503),
            ("یخچال فریزر کلور ۲۷ فوت گلوریا پلاس کمبی - استیل", 2497, 2504),
            ("یخچال و فریزر دوقلو ۳۶ فوت کلور RNT101-FNT101", 2637, 2646),
        ],
        "دیپوینت": [
            ("یخچال فریزر دیپوینت ۲۸ فوت T7 - سفید", 2585, 2593),
            ("یخچال فریزر دیپوینت ۲۸ فوت T7 - نقره‌ای/استیل", 2585, 2592),
            ("یخچال فریزر دیپوینت ۳۰ فوت Boss Pro - سفید", 2594, 2858),
            ("یخچال فریزر دیپوینت ۳۰ فوت Boss Pro - استیل", 2594, 2859),
            ("یخچال فریزر دوقلو دیپوینت ۳۴ فوت MAX.DU مکس", 2745, 2748),
        ],
        "ایستکول": [
            ("یخچال ۵ فوت ایستکول مدل 2835 - سفید", 2704, 2733),
            ("یخچال ۵ فوت ایستکول مدل 2835 - نوک مدادی / مشکی", 2704, 2734),
            ("یخچال فریزر ۹ فوت ایستکول هتلی مدل 2919 - سفید", 2691, 2701),
            ("یخچال فریزر ۹ فوت ایستکول هتلی مدل 2919 - نوک مدادی", 2691, 2702),
        ],
        "الکترواستیل": [
            ("یخچال فریزر دوقلو ۲۱ فوت الکترواستیل مدل فیوچر ES21 - سفید", 2680, 2688),
            ("یخچال فریزر دوقلو ۲۱ فوت الکترواستیل مدل فیوچر ES21 - تیتانیوم/استیل", 2680, 2689),
            ("یخچال الکترواستیل یخساز تیتانیوم", None, None),
        ],
        "هیمالیا": [
            ("یخچال هیمالیا آیسپول استیل 60MW", None, None),
            ("یخچال هیمالیا آیسپول چرم 60MW", None, None),
            ("فریزر هیمالیا آیسپول استیل 60MW", None, None),
            ("فریزر هیمالیا آیسپول چرم 60MW", None, None),
        ],
        "بست (BOST)": [
            ("یخچال فریزر BOST", None, None),
        ],
        "الکتروسان": [
            ("فریزر صندوقی الکتروسان ۳۴۵", None, None),
        ],
        "متفرقه": [
            ("یخچال فریزر R(re01)", None, None),
        ],
    },

    "ماشین لباسشویی": {
        "کلور": [
            ("لباسشویی ۹ کیلوگرم اتوماتیک کلور مدل BMWT2 - سفید", 2505, 2508),
            ("لباسشویی ۹ کیلوگرم اتوماتیک کلور مدل BMWT2 - نقره‌ای/اینوکس", 2505, 2509),
            ("لباسشویی ۸ کیلوگرم اتوماتیک کلور مدل تاچ سری BMW T3 - سفید", 2510, 2513),
            ("لباسشویی ۸ کیلوگرم اتوماتیک کلور مدل تاچ سری BMW T3 - اینوکس", 2510, 2514),
            ("لباسشویی کلور ۹ کیلویی کرمی", None, None),
            ("لباسشویی کلور ۹ کیلویی سفید ویوا", None, None),
            ("لباسشویی کلور مدل 9771 سفید", None, None),
        ],
        "دوو": [
            ("ماشین لباسشویی هوشمند ۹ کیلوگرم اتوماتیک دوو مدل LM-9170 - سفید", 2579, 2582),
            ("ماشین لباسشویی هوشمند ۹ کیلوگرم اتوماتیک دوو مدل LM-9170 - نقره‌ای/استیل", 2579, 2583),
            ("اتوماتیک دوو کینو ۹۰۵ سینیور", None, None),
        ],
        "پاکشوما": [
            ("لباسشویی دوقلو پاکشوما هاک", None, None),
            ("لباسشویی درب بالا پاکشوما ۱۲", None, None),
            ("لباسشویی دوقلو ۲۱ کیلو پاکشوما", None, None),
        ],
        "ریتون": [
            ("لباسشویی ۱۷ دوقلو ریتون", None, None),
        ],
        "پاکیزان": [
            ("پتوشور پاکیزان ۲۰ کیلو", None, None),
            ("پتوشور پاکیزان ۴۰ کیلو", None, None),
        ],
    },

    "جاروبرقی": {
        "هیتاچی": [
            ("جاروبرقی سطلی هیتاچی مدل CV-950F - شرابی", 2519, 2522),
            ("جاروبرقی سطلی هیتاچی مدل CV-950F - مشکی", 2519, 2523),
            ("جاروبرقی هیتاچی سطلی ۱۲۰۰", None, None),
        ],
        "پاناسونیک": [
            ("جاروبرقی پاناسونیک مدل MC-CG715 2100W", 2661, 2673),
        ],
        "بست (BOST)": [
            ("جاروبرقی بست سطلی مدل BVC-PC18B - قرمز", 2885, 2888),
            ("جاروبرقی بست سطلی مدل BVC-PC18B - آبی", 2885, 2889),
            ("جاروبرقی بست سطلی مدل BVC-PC18B - مشکی", 2885, 2890),
        ],
        "دونالکس": [
            ("جاروبرقی دونالکس ۷۵۰ سورمه‌ای", None, None),
            ("جاروبرقی دونالکس ۷۷۰", None, None),
        ],
        "کلور": [
            ("جاروبرقی کلور سطلی", None, None),
        ],
        "آراز": [
            ("جاروبرقی آراز ۲۰ لیتر", None, None),
        ],
    },

    "کولر آبی و سرمایشی": {
        "ریتون": [
            ("کولر آبی سلولزی ۱۶۰۰۰ ریتون پرتابل VENTO 16000", 2538, None),
            ("کولر آبی سلولزی ۷۰۰۰ ریتون VENTO 7000", 2559, None),
        ],
        "پاکشوما": [
            ("کولر گازی اسپلیت دیواری ۱۸۰۰۰ دور ثابت پاکشوما TPA-18CH", 3266, None),
        ],
        "اوناکس": [
            ("کولر آبی اوناکس 150L", None, None),
            ("کولر آبی اوناکس B35", None, None),
        ],
        "اوجنرال": [
            ("کولر پنجره‌ای اوجنرال ۱۸ هزار", None, None),
        ],
        "وستینگهاوس": [
            ("کولر وستینگهاوس ۲۰ کوپلند", None, None),
        ],
        "سایر": [
            ("کولر آبی مدل ۴۵۰۰", None, None),
        ],
    },

    "ماشین ظرفشویی": {
        "کلور": [
            ("ماشین ظرفشویی ۱۵ نفره کلور مدل CDW-H15V - سفید", 2871, 2874),
            ("ماشین ظرفشویی ۱۵ نفره کلور مدل CDW-H15V - استیل", 2871, 2875),
        ],
        "انفره": [
            ("ظرفشویی انفره استیل", None, None),
            ("ظرفشویی انفره لمسی استیل", None, None),
        ],
    },

    "تصفیه آب و آبسردکن": {
        "سافت واتر": [
            ("دستگاه تصفیه کننده آب سافت واتر ۶ مرحله مدل IR-06", 2766, None),
        ],
        "وست": [
            ("تصفیه آب وست 5515", None, None),
        ],
        "هومگلد": [
            ("تصفیه آب هومگلد", None, None),
        ],
        "C.C.K": [
            ("تصفیه آب C.C.K", None, None),
        ],
        "نیکایی": [
            ("آبسردکن نیکایی مدل ۱۱۲۰۶ ایستاده", None, None),
        ],
        "هانو": [
            ("آبسردکن هانو", None, None),
        ],
        "افترون": [
            ("آب سردکن افترون رومیزی", None, None),
        ],
        "الکترواستیل": [
            ("آبگرمکن الکترواستیل مخزندار دیواری", None, None),
        ],
    },

    "لوازم برقی آشپزخانه": {
        "دونالکس": [
            ("اسپرسوساز ۱۲ میلی‌لیتر دونالکس مدل DN480 (۳۸۰)", 3013, None),
            ("اسپرسوساز ۱۸ میلی‌لیتر دونالکس مدل DN475 (۳۷۵)", 3016, None),
            ("آبمیوه‌گیری ۱۰۰۰ وات ۴ کاره دونالکس مدل DN-120", 3019, None),
            ("آبمیوه‌گیر دونالکس ۴ کاره ۱۱۰", None, None),
            ("سرخ‌کن ۸ لیتر دونالکس مدل DN-950 (۱۹۵۰)", 3026, None),
            ("سرخکن دونالکس", None, None),
            ("گوشت‌کوب برقی دونالکس مدل DN-275", 3032, None),
            ("گوشتکوب و غذاساز دونالکس ۱۹۹۰", None, None),
            ("مخلوط‌کن و آسیاب ۱.۵ لیتری دونالکس مدل DN-205", 3035, None),
            ("چایساز دونالکس ۱۸۵ مشکی", None, None),
            ("ساندویچ‌ساز دونالکس ۴۰۹ سفید", None, None),
            ("ساندویچ‌ساز دونالکس ۴۹۰ مشکی", None, None),
            ("همزن دستی دونالکس ۳۵۵", None, None),
        ],
        "گرنویک": [
            ("اسپرسوساز نارنجی گرنویک", None, None),
            ("چایساز ساورر گرنویک", None, None),
            ("سرخکن ایرفرایر خاکستری گرنویک", None, None),
        ],
        "زامروتی": [
            ("چایساز زامروتی", None, None),
            ("کتری برقی تک زامروتی کرم", None, None),
            ("کتری و قوری زامروتی دسته استیل ۲۰۲۲", None, None),
            ("کتری و قوری زامروتی دسته چوب ۲۰۲۲", None, None),
            ("مخلوطکن زامروتی کرم", None, None),
        ],
        "وستینگهاوس": [
            ("توستر وستینگهاوس ۲۷", None, None),
            ("توستر وستینگهاوس کرم", None, None),
            ("کتری برقی وستینگهاوس آبی", None, None),
            ("کتری برقی وستینگهاوس کرم", None, None),
            ("مخلوطکن وستینگهاوس آبی", None, None),
            ("مخلوطکن وستینگهاوس کرم", None, None),
            ("همزن وستینگهاوس آبی", None, None),
            ("همزن وستینگهاوس کرم", None, None),
        ],
        "پارس خزر": [
            ("پلوپز پارس خزر ۸ نقره", None, None),
            ("پلوپز پارس خزر مدل ۳۶۱", None, None),
        ],
        "فیلیپس": [
            ("غذاساز فیلیپس ۷۷۷۸", None, None),
        ],
        "کنوود": [
            ("همزن کنوود ۴۳۰", None, None),
        ],
        "کرکماز": [
            ("چایساز کُرکماز A331", None, None),
        ],
        "سانی": [
            ("کتری برقی سانی ۱.۵ لیتر", None, None),
        ],
        "سایر برندهای آشپزخانه": [
            ("آبمیوهگیری جنرال ۶۰۷ غذاساز", None, None),
            ("آسیاب کاستلو ۲۷۰", None, None),
            ("سبزی خردکن KENRA", None, None),
            ("سبزی خردکن نیکا ۲ کیلویی", None, None),
            ("کتری برقی اریکسون", None, None),
            ("کتری برقی وگاتی توپی", None, None),
            ("کتری برقی پروکس", None, None),
            ("کتری و قوری مدل هرمی تمام‌طلا ۶۰۴", None, None),
            ("توستر ۶۰ لیتر", None, None),
            ("توستر ناندلمونتی ۵۸", None, None),
            ("همزن اوریکس کاسه چرخدار", None, None),
            ("زودپز اویزپلاس تک‌قلو مشکی رزگلد", None, None),
            ("زودپز اویزپلاس دوقلو مشکی رزگلد", None, None),
        ],
    },

    "ظروف و پخت و پز": {
        "تابه اویز": [
            ("تابه اویز سایز ۳۰", None, None),
            ("تابه اویز سایز ۲۲ مشکی", None, None),
            ("تابه اویز سایز ۲۲ فوم مشکی دربدار", None, None),
            ("تابه اویز سایز ۲۶", None, None),
        ],
        "قابلمه اویز تک": [
            ("قابلمه اویز سایز ۱۶ مشکی", None, None),
            ("قابلمه اویز سایز ۱۸ مشکی", None, None),
            ("قابلمه اویز سایز ۲۰ مشکی", None, None),
            ("قابلمه اویز سایز ۲۲ مشکی", None, None),
            ("قابلمه اویز سایز ۲۴ مشکی", None, None),
            ("قابلمه اویز سایز ۲۶ مشکی", None, None),
            ("قابلمه مرغخوری اویزپلاس مشکی", None, None),
        ],
        "سرویس‌های قابلمه": [
            ("سرویس خمره قابلمه اویز کرم‌سلین", None, None),
            ("سرویس قابلمه استیل ۱۰ پارچه", None, None),
            ("سرویس قابلمه اویز ۱۰ پارچه سرمه‌ای", None, None),
            ("سرویس قابلمه اویزپلاس ۱۰ پارچه اناری", None, None),
            ("سرویس قابلمه اویزپلاس ۱۲ پارچه مشکی", None, None),
            ("سرویس قابلمه اویزپلاس ۱۲ پارچه سبز", None, None),
            ("سرویس قابلمه اویزپلاس ویولا ۱۱ پارچه", None, None),
            ("شیرجوش مشکی اویزپلاس", None, None),
        ],
    },

    "اصلاح و زیبایی": {
        "پرو امگا": [
            ("سشوار حرفه‌ای پرو امگا مدل 8806 (۲۲۰۰ وات)", 3049, None),
            ("سشوار امگا ۲۰۰۰ وات", None, None),
            ("ماشین اصلاح موی سر و صورت پرو امگا مدل T5 (تک)", 3056, None),
            ("ماشین اصلاح موی سر و صورت پرو امگا مدل T7 (۴ کاره)", 3065, None),
            ("ماشین اصلاح پروامگا شارژی و برقی", None, None),
        ],
        "پرومارون": [
            ("فرکننده مو پرومارون ۴+", None, None),
            ("پرومارون برس حرارتی ۱۱۳", None, None),
            ("اتومو پرومارون ۱۱۱۵", None, None),
            ("اتومو پرومارون ۱۱۱۶", None, None),
            ("اپیلاتور پرومارون ۵ کاره ۶۱۴", None, None),
            ("ریشتراش پرومارون ۷۰۶", None, None),
        ],
        "پاناسونیک": [
            ("اتو مو پاناسونیک HV11", None, None),
        ],
        "سایر": [
            ("اتو مو Baby3383A", None, None),
            ("دستگاه پیرایش سیمی صورت ۷۲۱", None, None),
        ],
    },

    "اتو بخار": {
        "دونالکس": [
            ("اتو بخار ۲۵۰۰ وات دونالکس مدل 815", 3007, None),
        ],
        "فیلیپس": [
            ("اتو فیلیپس ۵۰۴۰", None, None),
        ],
    },

    "گاز، فر و هود": {
        "آلتون": [
            ("گاز صفحه‌ای آلتون استیل S517", None, None),
            ("گاز صفحه‌ای آلتون استیل SG518", None, None),
            ("فر توکار آلتون ۷۳۰۳", None, None),
            ("فرگاز آلتون MPS", None, None),
            ("فرگاز آلتون MD5W", None, None),
            ("هود آلتون H312", None, None),
            ("هود آلتون H315B", None, None),
        ],
        "الکترواستیل": [
            ("فر الکترواستیل تیتانیوم ۱۱", None, None),
            ("فر الکترواستیل عرض ۶۰ چرمی ۲۱", None, None),
        ],
    },

    "صوتی، تصویری و گرمایشی": {
        "تلویزیون": [
            ("ال ای دی هاورسون ۷۵ اینچ", None, None),
            ("ال ای دی ۶۵ اینچ هاورسون", None, None),
            ("ال ای دی هاورسون ۵۵ پنرست", None, None),
            ("ال ای دی ۳۲ Averson", None, None),
            ("ال ای دی ۸۵ Averson", None, None),
        ],
        "بخاری": [
            ("بخاری گلدن لوکس", None, None),
            ("بخاری پارس خزر فندار FH-2000P", None, None),
            ("بخاری پلار 32-067 شیشه‌ای", None, None),
        ],
        "پنکه": [
            ("پنکه پایه‌بلند 1455", None, None),
            ("پنکه پارس خزر پایه‌بلند", None, None),
            ("پنکه پاناسونیک ۲ حالته", None, None),
            ("پنکه سانی ۷۶۰۰", None, None),
            ("پنکه سانی مدل ۲۰۱۳ ساده", None, None),
        ],
        "متفرقه": [
            ("کسورات اضافات کالا", None, None),
        ],
    },
}

COLUMNS = [
    # (key,              header_text,                 width,  align,   is_price,  is_formula)
    ("name",             "نام محصول",                  40,     "right",   False,     False),
    ("price_regular",    "قیمت عادی (ریال)",          18,     "center",  True,      False),
    ("price_reg_toman",  "قیمت عادی (تومان)",          18,     "center",  True,      True),
    ("price_sale",       "قیمت حراج (ریال)",          18,     "center",  True,      False),
    ("price_sale_toman", "قیمت حراج (تومان)",          18,     "center",  True,      True),
    ("in_stock",         "وضعیت موجودی",               14,     "center",  False,     False),
    ("category_path",    "دسته‌بندی / برند",           26,     "right",   False,     False),
    ("type",             "نوع محصول",                  13,     "center",  False,     False),
    ("variant_attr",     "تنوع / رنگ",                 18,     "center",  False,     False),
    ("product_id",       "شناسه محصول (ID)",           16,     "center",  False,     False),
    ("variation_id",     "شناسه تنوع",                 15,     "center",  False,     False),
    ("link",             "لینک محصول در سایت",         36,     "left",    False,     False),
    ("sku",              "کد SKU",                     14,     "center",  False,     False),
    ("status_note",      "وضعیت در سایت",              22,     "center",  False,     False),
]

COLOR_HEADER_BG = "1F4E79"
COLOR_HEADER_TEXT = "FFFFFF"
COLOR_SUBCAT_BG = "E2EFDA"
COLOR_SUBCAT_TEXT = "375623"
COLOR_VAR_BG = "EBF1F5"
COLOR_MISSING_BG = "FFF2CC"
COLOR_TOMAN_HEADER_BG = "2E75B6"
COLOR_IN_STOCK_TEXT = "27AE60"
COLOR_OUT_OF_STOCK = "C00000"

def make_border():
    s = Side(style='thin', color='D9D9D9')
    return Border(top=s, bottom=s, left=s, right=s)

def build_catalog():
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    border_thin = make_border()
    total_products_count = 0
    matched_count = 0
    unmatched_count = 0

    # شیت راهنما
    ws_guide = wb.create_sheet("راهنمای استفاده", index=0)
    ws_guide.sheet_view.rightToLeft = True
    guide_lines = [
        ("راهنمای جامع کاتالوگ محصولات فروشگاه حسینی کالا", ""),
        ("", ""),
        ("بخش / ستون", "توضیحات و راهنمای کاربری"),
        ("نام محصول (ستون راست)", "نام دقیق و استاندارد محصول"),
        ("قیمت عادی (ریال)", "قیمت پایه به ریال (عدد خالص). با فرمت سه رقم سه رقم خودکار اکسل (#,##0)."),
        ("قیمت عادی (تومان)", "فرمول محاسبه خودکار قیمت به تومان (=قیمت ریال تقسیم بر ۱۰) با تفکیک ۳ رقم."),
        ("قیمت حراج (ریال)", "قیمت حراج به ریال (در صورت وجود تخفیف)."),
        ("قیمت حراج (تومان)", "فرمول محاسبه خودکار قیمت حراج به تومان (=قیمت حراج ریال تقسیم بر ۱۰)."),
        ("وضعیت موجودی (منوی کشویی)", "دکمه و لیست انتخابی بین «موجود» و «ناموجود» جهت تغییر سریع موجودی انبار."),
        ("دسته‌بندی / برند", "مسیر کامل دسته اصلی و برند یا زیردسته کالا"),
        ("نوع محصول", "ساده (یک قیمت ثابت) | تنوع (رنگ/مدل اختصاصی محصول متغیر)"),
        ("شناسه محصول (ID)", "شناسه یکتای عددی وردپرس جهت همگام‌سازی و آپدیت خودکار قیمت‌ها"),
        ("شناسه تنوع (Variation ID)", "شناسه متغیر رنگ خاص (جهت به‌روزرسانی مجزای قیمت هر رنگ)"),
        ("لینک محصول در سایت", "لینک کوتاه و بدون خطای انکودینگ با فرمت عددی ?p=ID"),
        ("", ""),
        ("راهنمای رنگ‌بندی سطرها:", ""),
        ("زرد ملایم", "کالاهایی که هنوز روی سایت ثبت نشده‌اند (قیمت‌ها خالی و آماده ورود اطلاعات است)."),
        ("سفید / آبی ملایم", "کالاهای فعال و موجود در سایت همراه با قیمت رسمی و لینک مستقیم."),
        ("", ""),
        ("نحوه به‌روزرسانی قیمت‌ها به سایت:", ""),
        ("۱. قیمت‌های جدید را در ستون 'قیمت عادی (ریال)' یا 'قیمت حراج (ریال)' همین فایل وارد کنید (قیمت تومان خودکار محاسبه می‌شود).", ""),
        ("۲. وضعیت موجودی را از منوی کشویی روی موجود یا ناموجود تنظیم کنید.", ""),
        ("۳. اسکریپت python scripts/update_prices.py --apply را اجرا کنید تا قیمت‌ها مستقیماً روی سایت اعمال شوند.", ""),
    ]
    for r_idx, (col1, col2) in enumerate(guide_lines, start=1):
        ws_guide.cell(row=r_idx, column=1, value=col1)
        ws_guide.cell(row=r_idx, column=2, value=col2)
        if r_idx == 1:
            ws_guide.cell(row=r_idx, column=1).font = Font(bold=True, size=13, color="1F4E79")
        elif r_idx in (3, 16, 21):
            ws_guide.cell(row=r_idx, column=1).font = Font(bold=True, size=11, color="1F4E79")
            ws_guide.cell(row=r_idx, column=2).font = Font(bold=True, size=11, color="1F4E79")

    ws_guide.column_dimensions['A'].width = 30
    ws_guide.column_dimensions['B'].width = 85

    for sheet_name, subcats in SHEETS_STRUCTURE.items():
        ws = wb.create_sheet(title=sheet_name[:31])
        ws.sheet_view.rightToLeft = True

        # هدر شیت
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

        for subcat_name, products_list in subcats.items():
            # ایجاد هدر زیردسته فقط یک بار برای هر برند
            ws.row_dimensions[row_idx].height = 22
            ws.merge_cells(start_row=row_idx, start_column=1, end_row=row_idx, end_column=len(COLUMNS))
            sub_cell = ws.cell(row=row_idx, column=1, value=f"  📂 {sheet_name}  ◀  {subcat_name}")
            sub_cell.font = Font(bold=True, color=COLOR_SUBCAT_TEXT, size=10, name="Calibri")
            sub_cell.fill = PatternFill(fill_type='solid', fgColor=COLOR_SUBCAT_BG)
            sub_cell.alignment = Alignment(horizontal='right', vertical='center')
            for c in range(1, len(COLUMNS) + 1):
                ws.cell(row=row_idx, column=c).border = border_thin
            row_idx += 1

            for prod_item in products_list:
                prod_title = prod_item[0]
                site_pid = prod_item[1]
                site_vid = prod_item[2] if len(prod_item) > 2 else None

                cat_path = f"{sheet_name} / {subcat_name}"
                site_prod = site_by_id.get(site_pid) if site_pid else None

                total_products_count += 1

                # ۱. محصول در سایت نیست
                if not site_prod:
                    unmatched_count += 1
                    row_data = {
                        "name": prod_title,
                        "price_regular": "",
                        "price_reg_toman": f'=IF(OR(B{row_idx}="",B{row_idx}=0),"",B{row_idx}/10)',
                        "price_sale": "",
                        "price_sale_toman": f'=IF(OR(D{row_idx}="",D{row_idx}=0),"",D{row_idx}/10)',
                        "in_stock": "ناموجود",
                        "category_path": cat_path,
                        "type": "ساده",
                        "variant_attr": "",
                        "product_id": "",
                        "variation_id": "",
                        "link": "",
                        "sku": "",
                        "status_note": "نیازمند ثبت در سایت",
                    }
                    ws.row_dimensions[row_idx].height = 20
                    row_fill = PatternFill(fill_type='solid', fgColor=COLOR_MISSING_BG)

                    for c_idx, (f_key, _, _, align_mode, is_price, is_formula) in enumerate(COLUMNS, start=1):
                        val = row_data.get(f_key, "")
                        c = ws.cell(row=row_idx, column=c_idx, value=val)
                        c.fill = row_fill
                        c.alignment = Alignment(horizontal=align_mode, vertical='center')
                        c.border = border_thin
                        c.font = Font(size=10, name="Calibri")

                        if is_price or is_formula:
                            c.number_format = '#,##0'
                        if f_key == "in_stock":
                            c.font = Font(size=10, color=COLOR_OUT_OF_STOCK, name="Calibri")
                        if f_key == "status_note":
                            c.font = Font(size=9, italic=True, color="806000", name="Calibri")

                    row_idx += 1

                # ۲. محصول در سایت موجود است
                else:
                    matched_count += 1

                    # اگر یک واریاسیون خاص مدنظر است
                    var_obj = None
                    if site_vid:
                        for v in site_prod.get('variations', []):
                            if v.get('variation_id') == site_vid:
                                var_obj = v
                                break

                    if var_obj:
                        reg_price = var_obj.get('price_regular') or site_prod.get('price_regular', '')
                        sale_price = var_obj.get('price_sale') or ''
                        attrs = var_obj.get('attributes', {})
                        attr_str = " / ".join([f"{v}" for k, v in attrs.items()]) if attrs else "-"
                        in_stk = "موجود" if var_obj.get('in_stock', True) else "ناموجود"
                        stk_color = COLOR_IN_STOCK_TEXT if var_obj.get('in_stock', True) else COLOR_OUT_OF_STOCK
                        prod_type = "تنوع (واریاسیون)"
                        variation_id_val = site_vid
                        link_val = var_obj.get('shortlink') or site_prod.get('shortlink', '')
                    else:
                        reg_price = site_prod.get('price_regular') or ""
                        sale_price = site_prod.get('price_sale') or ""
                        attr_str = "-"
                        in_stk = "موجود" if site_prod.get('in_stock', True) else "ناموجود"
                        stk_color = COLOR_IN_STOCK_TEXT if site_prod.get('in_stock', True) else COLOR_OUT_OF_STOCK
                        prod_type = "ساده"
                        variation_id_val = ""
                        link_val = site_prod.get('shortlink', '')

                    row_data = {
                        "name": prod_title,
                        "price_regular": reg_price,
                        "price_reg_toman": f'=IF(OR(B{row_idx}="",B{row_idx}=0),"",B{row_idx}/10)',
                        "price_sale": sale_price,
                        "price_sale_toman": f'=IF(OR(D{row_idx}="",D{row_idx}=0),"",D{row_idx}/10)',
                        "in_stock": in_stk,
                        "category_path": cat_path,
                        "type": prod_type,
                        "variant_attr": attr_str,
                        "product_id": site_pid,
                        "variation_id": variation_id_val,
                        "link": link_val,
                        "sku": site_prod.get('sku', ''),
                        "status_note": "✓ موجود در سایت",
                    }

                    ws.row_dimensions[row_idx].height = 20
                    row_fill = PatternFill(fill_type='solid', fgColor="FFFFFF" if not site_vid else COLOR_VAR_BG)

                    for c_idx, (f_key, _, _, align_mode, is_price, is_formula) in enumerate(COLUMNS, start=1):
                        val = row_data.get(f_key, "")
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

    try:
        wb.save(EXCEL_OUTPUT)
        final_file = EXCEL_OUTPUT
    except PermissionError:
        wb.save(EXCEL_UPDATED)
        final_file = EXCEL_UPDATED
        print(f"⚠️ فایل اصلی در اکسل باز است. فایل در مسیر زیر ایجاد شد:\n   {EXCEL_UPDATED}")

    print("=" * 60)
    print("✓ ساخت کاتالوگ دقیق، بدون تکرار و ساختاریافته به پایان رسید.")
    print(f"📁 مسیر فایل خروجی: {final_file}")
    print(f"📊 کل سطرهای محصولات: {total_products_count}")
    print(f"✅ محصولات مچ‌شده با اطلاعات سایت: {matched_count}")
    print(f"🟡 محصولات نیازمند ثبت در سایت: {unmatched_count}")
    print("=" * 60)

if __name__ == '__main__':
    build_catalog()

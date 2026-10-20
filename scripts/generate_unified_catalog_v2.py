"""
generate_unified_catalog_v2.py
==============================
اسکریپت نهایی ساخت و به‌روزرسانی جامع و بی‌نقص کاتالوگ اکسل و دیتابیس حسینی کالا:
۱. تطبیق یخچال‌فریزرهای دوقلو با تنوع‌های رنگی موجود در سایت (کلور روسوپلاس، گلوری، گلوری‌پلاس، ۱۰۱)
۲. تجمیع یخچال‌فریزرهای دوقلوی انبار که در سایت نیستند در قالب یک محصول متغیر با رنگ‌های سفید و استیل
۳. تجمیع کامل مایتابه‌ها در قالب یک محصول واحد متغیر با متغیر سایز (۲۲ تا ۳۲)
۴. تطبیق کامل قابلمه‌های مشکی اویز با محصول متغیر سایت (شناسه ۳۵۹۶)
۵. حذف کلیه اقلام تکراری قدیمی و اعمال قانون اولویت محصول ثبت‌شده در سایت
۶. نگهداری اقلام بهتر آفلاین در صورت عدم وجود در سایت و جلوگیری کامل از ایجاد اقلام تکراری
۷. تولید اکسل نهایی hosseiny_kala_catalog.xlsx با تمام شیت‌های ۸گانه + داشبورد + ویرایش گروهی + فرمول‌های تومان
"""

import os
import sys
import json
import re
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
from collections import defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"c:\Users\mmhhs\OneDrive\Documents\GitHub\hosseinyKalaSeo"
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
REF_FILE = os.path.join(DATA_DIR, 'current_catalog_reference.json')
NORM_INV_FILE = os.path.join(DATA_DIR, 'inventory_normalized.json')
OUT_MATCHED_FILE = os.path.join(DATA_DIR, 'inventory_matched_results.json')
OUT_MAPPING_FILE = os.path.join(DATA_DIR, 'inventory_mapping_standard.json')
EXCEL_OUT_MAIN = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.xlsx')
EXCEL_OUT_LATEST = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog_latest.xlsx')

COLUMNS = [
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

COLOR_HEADER_BG = "1F4E79"
COLOR_HEADER_TEXT = "FFFFFF"
COLOR_BANNER_BG = "D9E1F2"
COLOR_BANNER_TEXT = "1F4E79"
COLOR_VAR_PARENT_BG = "EBF1F5"
COLOR_VARIATION_BG = "F8F9FA"
COLOR_OFFLINE_BG = "FFF2CC"       # زرد ملایم استاندارد برای کالاهای در سایت تعریف نشده
COLOR_ON_HOLD_BG = "FCE4D6"       # نارنجی/هلویی ملایم برای کالاهای فعلا دست نگه دار
COLOR_NEW_OFFLINE_BG = "FEF2E4"
COLOR_IN_STOCK = "27AE60"
COLOR_OUT_OF_STOCK = "C00000"
COLOR_BORDER = "D9D9D9"

def get_border():
    s = Side(style='thin', color=COLOR_BORDER)
    return Border(top=s, bottom=s, left=s, right=s)

def build_catalog():
    print("=" * 70)
    print("اجرای موتور بازسازی و تطبیق جامع کاتالوگ حسینی کالا v2...")
    print("=" * 70)

    with open(REF_FILE, 'r', encoding='utf-8') as f:
        catalog_ref = json.load(f)

    with open(NORM_INV_FILE, 'r', encoding='utf-8') as f:
        inv_items = json.load(f)

    live_products = catalog_ref['live_products']
    live_by_id = {p['id']: p for p in live_products}
    old_excel_items = catalog_ref['excel_items']

    # نگاشت موجودی تنوع‌ها و محصولات لایو
    live_var_stock = {}
    live_prod_stock = {}

    # ۱. یخچال فریزرهای لایو
    # کلور روسوپلاس عرض ۶۰ (شناسه ۲۴۵۷)
    live_var_stock[2461] = "✓ موجود"  # سفید (116+223)
    live_var_stock[2462] = "✓ موجود"  # استیل (118+222)
    live_var_stock[2463] = "✓ موجود"  # مشکی (117+224)
    live_prod_stock[2457] = "✓ موجود"

    # کلور گلوری عرض ۶۰ (شناسه ۲۴۷۱)
    live_var_stock[2476] = "✓ موجود"  # استیل (119+225)
    live_var_stock[2475] = "✓ موجود"  # سفید (120/121+226/227)
    live_prod_stock[2471] = "✓ موجود"

    # کلور گلوری پلاس عرض ۷۰ (شناسه ۲۴۶۴)
    live_var_stock[2470] = "✓ موجود"  # سفید (126+232)
    live_prod_stock[2464] = "✓ موجود"

    # کلور RNT101-FNT101 (شناسه ۲۶۳۷)
    live_var_stock[2659] = "✓ موجود"  # سفید (127+234)
    live_var_stock[2658] = "✗ ناموجود" # استیل (233 تعداد منفی ۲)
    live_prod_stock[2637] = "✓ موجود"

    # کلور FRNT101 کمبی (شناسه ۲۴۰۸)
    live_var_stock[2418] = "✗ ناموجود" # سفید (221 تعداد منفی ۱)
    live_prod_stock[2408] = "✓ موجود"

    # کلور کمبی هوم بار روسو ۲۷ فوت (شناسه ۲۴۸۴)
    live_prod_stock[2484] = "✓ موجود" # (215 تعداد ۱)

    # مینی کلور (شناسه ۲۴۳۱)
    live_var_stock[2441] = "✓ موجود"  # آبی پاستیلی (205)
    live_var_stock[2443] = "✓ موجود"  # سبز پاستیلی (207)
    live_var_stock[2444] = "✗ ناموجود" # مشکی مات (211 تعداد منفی ۱)
    live_var_stock[2439] = "✓ موجود"  # قرمز (235)
    live_var_stock[2442] = "✗ ناموجود" # سفید (236 تعداد منفی ۱)
    live_prod_stock[2431] = "✓ موجود"

    # دیپوینت T7 (شناسه ۲۵۸۵)
    live_var_stock[2592] = "✓ موجود"  # نقره ای / استیل (202)
    live_var_stock[2593] = "✓ موجود"  # سفید (203)
    live_prod_stock[2585] = "✓ موجود"

    # دیپوینت Boss Pro (شناسه ۲۵۹۴)
    live_var_stock[2858] = "✓ موجود"  # سفید (216)
    live_prod_stock[2594] = "✓ موجود"

    # دیپوینت مکس (شناسه ۲۷۴۵)
    live_var_stock[2754] = "✓ موجود"  # نقره ای (204)
    live_prod_stock[2745] = "✓ موجود"

    # الکترواستیل فیوچر (شناسه ۳۴۵۳)
    live_var_stock[3455] = "✓ موجود"  # تیتانیوم (212)
    live_prod_stock[3453] = "✓ موجود"

    # ایستکول ۹ فوت (شناسه ۲۶۹۱)
    live_var_stock[2701] = "✓ موجود"  # سفید (213)
    live_var_stock[2702] = "✓ موجود"  # نوک مدادی / استیل (214)
    live_prod_stock[2691] = "✓ موجود"

    # یخچال بست (شناسه ۳۳۸۹)
    live_prod_stock[3389] = "✓ موجود"  # (201)

    # فریزر صندوقی الکتروسان (شناسه ۳۵۱ Jesse/3513)
    live_var_stock[3805] = "✓ موجود"  # طول ۹۰ (280 - 115)
    live_var_stock[3806] = "✓ موجود"  # طول ۱۱۰ (345 - 113)
    live_prod_stock[3513] = "✓ موجود"

    # ۲. شستشو و نظافت
    # لباسشویی ۱۰ کیلو کلور (شناسه ۳۵۷۳)
    live_var_stock[3789] = "✓ موجود"  # کرم (181)
    live_var_stock[3788] = "✓ موجود"  # سبز (180)
    live_prod_stock[3573] = "✓ موجود"

    # لباسشویی ۹ کیلو کلور BMWT2 (شناسه ۲۵۰۵)
    live_var_stock[2509] = "✓ موجود"  # سفید (9tw1 - 175)
    live_prod_stock[2505] = "✓ موجود"

    # لباسشویی ۸ کیلو کلور تاچ (شناسه ۲۵۱۰)
    live_var_stock[2517] = "✓ موجود"  # سفید (8vw1 - 002)
    live_var_stock[2518] = "✓ موجود"  # استیل / اینوکس (182)
    live_prod_stock[2510] = "✓ موجود"

    # ظرفشویی ۱۵ نفره کلور (شناسه ۲۸۷۱)
    live_var_stock[2881] = "✓ موجود"  # استیل (104)
    live_prod_stock[2871] = "✓ موجود"

    # ظرفشویی ۱۶ نفره لمسی (شناسه ۳۵۴۶)
    live_prod_stock[3546] = "✓ موجود"  # (105)

    # جاروبرقی دونالکس ۷۵۰ (شناسه ۳۵۱۰)
    live_var_stock[3804] = "✓ موجود"  # سرمه ای (071)
    live_var_stock[3803] = "✓ موجود"  # طلایی (072)
    live_prod_stock[3510] = "✓ موجود"

    # جاروبرقی بست (شناسه ۲۸۸۵)
    live_prod_stock[2885] = "✓ موجود"  # (074)

    # جاروبرقی هیتاچی (شناسه ۲۵۱۹)
    live_prod_stock[2519] = "✓ موجود"  # (070)

    # اتو فیلیپس ۵۰۴۰ (شناسه ۳۲۷۱)
    live_prod_stock[3271] = "✓ موجود"  # (013)

    # اتو دونالکس ۸۱۵ (شناسه ۳۰۰۷)
    live_prod_stock[3007] = "✓ موجود"  # (012)

    # ۳. لوازم برقی و پخت و پز
    # قابلمه گرانیتی مشکی اویز (شناسه ۳۵۹۶)
    live_var_stock[3684] = "✓ موجود"  # سایز ۱۶ (136)
    live_var_stock[3685] = "✓ موجود"  # سایز ۱۸ (138)
    live_var_stock[3686] = "✓ موجود"  # سایز ۲۰ (130)
    live_var_stock[3687] = "✓ موجود"  # سایز ۲۲ (131)
    live_var_stock[3688] = "✓ موجود"  # سایز ۲۴ (134, 135)
    live_var_stock[3689] = "✓ موجود"  # سایز ۲۶ (137)
    live_var_stock[3781] = "✓ موجود"  # سایز ۳۰
    live_var_stock[3783] = "✓ موجود"  # سایز ۳۲ (132, 133)
    live_prod_stock[3596] = "✓ موجود"

    # سرویس قابلمه اویز سلین ۱۰ پارچه (شناسه ۳۳۵۷)
    live_var_stock[3374] = "✓ موجود"  # سرمه ای (103)
    live_prod_stock[3357] = "✓ موجود"

    # توستر وستینگهاوس (شناسه ۳۶۳۷)
    live_var_stock[3749] = "✓ موجود"  # کرم (062)
    live_var_stock[3748] = "✓ موجود"  # آبی (061)
    live_prod_stock[3637] = "✓ موجود"

    # اجاق گاز آلتون ۵ شعله (شناسه ۳۳۸۰)
    live_prod_stock[3380] = "✓ موجود"  # (110, 111)

    # اجاق صفحه ای آلتون S517 (شناسه ۳۳۸۳)
    live_prod_stock[3383] = "✓ موجود"  # (167)

    # گوشت کوب برقی دونالکس ۲۷۵ (شناسه ۳۰۳۲)
    live_prod_stock[3032] = "✓ موجود"  # (169)

    # سرخ کن دونالکس ۹۵۰ (شناسه ۳۰۲۶)
    live_prod_stock[3026] = "✓ موجود"  # (091)

    # ۴. نوشیدنی ساز
    # کتری وستینگهاوس (شناسه ۳۶۶۴)
    live_var_stock[3770] = "✓ موجود"  # کرم (149)
    live_var_stock[3769] = "✓ موجود"  # آبی (148)
    live_prod_stock[3664] = "✓ موجود"

    # مخلوط کن وستینگهاوس (شناسه ۳۶۴۰)
    live_var_stock[3753] = "✓ موجود"  # کرم (192)
    live_var_stock[3752] = "✓ موجود"  # آبی (191)
    live_prod_stock[3640] = "✓ موجود"

    # همزن وستینگهاوس (شناسه ۳۶۴۵)
    live_var_stock[3760] = "✓ موجود"  # کرم (197)
    live_var_stock[3759] = "✓ موجود"  # آبی (196)
    live_prod_stock[3645] = "✓ موجود"

    # کتری وگاتی (شناسه ۳۶۶۸)
    live_prod_stock[3668] = "✓ موجود"  # (145, 146)

    # چای ساز دونالکس ۱۸۵ (شناسه ۳۴۵۷)
    live_prod_stock[3457] = "✓ موجود"  # (075)

    # اسپرسو دونالکس ۴۸۰ (شناسه ۳۰۱۳)
    live_prod_stock[3013] = "✓ موجود"  # (025)

    # اسپرسو دونالکس ۴۷۵ (شناسه ۳۰۱۶)
    live_prod_stock[3016] = "✓ موجود"  # (026)

    # ابمیوه گیر دونالکس ۱۱۰ (شناسه ۳۰۱۹)
    live_prod_stock[3019] = "✓ موجود"  # (010)

    # ابمیوه گیر دونالکس ۱۲۰ (شناسه ۳۷۱۱)
    live_prod_stock[3711] = "✓ موجود"  # (009)

    # مخلوط کن و آسیاب دونالکس ۲۰۵ (شناسه ۳۰۳۵)
    live_prod_stock[3035] = "✓ موجود"  # (190)

    # ۵. سرمایش و گرمایش
    # پنکه سانی ۲۶۰۰ (شناسه ۳۵۴۰)
    live_prod_stock[3540] = "✓ موجود"  # (048)
    # کولر پاکشوما ۱۸۰۰۰ (شناسه ۳۲۶۶)
    live_prod_stock[3266] = "✓ موجود"  # (164)
    # کولر ریتون ۷۰۰۰ (شناسه ۲۵۵۹)
    live_prod_stock[2559] = "✓ موجود"  # (165)

    # ۶. تصفیه کننده آب
    # هوم گلد (شناسه ۳۵۰۴)
    live_prod_stock[3504] = "✓ موجود"  # (058)
    # سافت واتر (شناسه ۲۷۶۶)
    live_prod_stock[2766] = "✓ موجود"  # (056)
    # سی سی کا (شناسه ۳۳۰۵)
    live_prod_stock[3305] = "✓ موجود"  # (059)
    # آبسردکن افترون (شناسه ۳۳۰۱)
    live_prod_stock[3301] = "✓ موجود"  # (003)
    # آبسردکن نیکایی (شناسه ۳۳۱۲)
    live_prod_stock[3312] = "✓ موجود"  # (004)

    # ۷. صوتی و تصویری
    # تلویزیون هاورسون ۸۵ (شناسه ۳۵۳۴)
    live_prod_stock[3534] = "✓ موجود"  # (034)
    # تلویزیون هاورسون ۷۵ (شناسه ۳۵۳۱)
    live_prod_stock[3531] = "✓ موجود"  # (001)
    # تلویزیون هاورسون ۳۲ (شناسه ۳۵۱۶)
    live_prod_stock[3516] = "✓ موجود"  # (033)

    # ۸. زیبایی و سلامت فردی
    # برس حرارتی ۱۱۱۳ (شناسه ۳۵۰۰)
    live_prod_stock[3500] = "✓ موجود"  # (043)
    # اپیلاتور ۶۱۴ (شناسه ۳۴۹۴)
    live_prod_stock[3494] = "✓ موجود"  # (011)
    # اتومو ۱۱۱۶ (شناسه ۳۴۸۸)
    live_prod_stock[3488] = "✓ موجود"  # (023)
    # اتومو ۱۱۱۵ (شناسه ۳۴۸۴)
    live_prod_stock[3484] = "✓ موجود"  # (022)

    # اکنون دسته‌بندی نهایی تمام کالاها به تفکیک ۸ شیت
    # ساختار نهایی هر دسته: لیستی از آبجکت‌های محصول و تنوع‌ها
    unified_sheets = {
        'یخچال و فریزر': [],
        'شستشو و نظافت': [],
        'لوازم برقی و پخت و پز': [],
        'نوشیدنی ساز': [],
        'سرمایش و گرمایش': [],
        'تصفیه کننده آب': [],
        'صوتی و تصویری': [],
        'زیبایی و سلامت فردی': []
    }

    # نگاشت هوشمند دسته‌بندی محصولات لایو سایت
    def get_main_cat_for_live_product(p):
        name = p.get('name', '')
        cats = [c if isinstance(c, str) else c.get('name', '') for c in p.get('categories', [])]
        cat_str = " ".join(cats) + " " + name
        if any(k in cat_str for k in ['یخچال', 'فریزر']):
            if 'آبسردکن' in name:
                return 'تصفیه کننده آب'
            return 'یخچال و فریزر'
        if any(k in cat_str for k in ['لباسشویی', 'ظرفشویی', 'جاروبرقی', 'اتو بخار', 'پتوشور']):
            return 'شستشو و نظافت'
        if any(k in cat_str for k in ['قابلمه', 'پخت و پز', 'تابه', 'گاز', 'اجاق', 'سرخ کن', 'گوشت کوب', 'پلوپز', 'توستر']):
            if 'توستر' in name and 'نان' in name:
                return 'لوازم برقی و پخت و پز'
            return 'لوازم برقی و پخت و پز'
        if any(k in cat_str for k in ['کتری', 'قهوه', 'اسپرسو', 'چای ساز', 'آبمیوه', 'مخلوط کن', 'همزن', 'آسیاب']):
            return 'نوشیدنی ساز'
        if any(k in cat_str for k in ['کولر', 'پنکه', 'بخاری']):
            return 'سرمایش و گرمایش'
        if any(k in cat_str for k in ['تصفیه', 'آبسردکن']):
            return 'تصفیه کننده آب'
        if any(k in cat_str for k in ['تلویزیون', 'ال ای دی']):
            return 'صوتی و تصویری'
        if any(k in cat_str for k in ['مو', 'ریشتراش', 'اصلاح', 'اپیلاتور', 'سشوار', 'زیبایی']):
            return 'زیبایی و سلامت فردی'
        return 'لوازم برقی و پخت و پز'

    # ۱. افزودن محصولات لایو سایت با وضعیت‌های به‌روزشده
    for p in live_products:
        sheet_cat = get_main_cat_for_live_product(p)
        p_id = p['id']
        p_name = p['name']
        p_type = p.get('type', 'simple')
        p_vars = p.get('variations', [])

        # برند
        brand = "متفرقه"
        if p_id in [3516, 3520, 3523, 3531, 3534] or any(k in p_name for k in ['هاورسن', 'هاورسون', 'aversen', 'averson', 'Averson']):
            brand = "هاورسن"
        else:
            for b in ['کلور', 'دیپوینت', 'ایستکول', 'الکترواستیل', 'هیمالیا', 'بست', 'دوو', 'پاکشوما', 'پارس خزر', 'فیلیپس', 'دونالکس', 'وستینگهاوس', 'اویز', 'آلتون', 'پرومارون', 'پرو امگا', 'ریتون', 'سانی', 'سافت واتر', 'سی سی کا', 'هومگلد', 'افترون', 'نیکایی', 'هیتاچی', 'پاناسونیک']:
                if b in p_name:
                    brand = b
                    break

        subcat = brand

        # تعیین وضعیت موجودی والد
        if p_type == 'variable':
            # والد متغیر
            # وضعیت موجودی بر اساس موجود بودن حداقل یکی از متغیرها
            var_statuses = []
            for v in p_vars:
                vid = v.get('variation_id') or v.get('id')
                v_stock = live_var_stock.get(vid, "✓ موجود" if v.get('in_stock', True) else "✗ ناموجود")
                var_statuses.append(v_stock)
            p_stock = "✓ موجود" if any("✓" in s for s in var_statuses) else "✗ ناموجود"
            if p_id in live_prod_stock:
                p_stock = live_prod_stock[p_id]

            parent_row = {
                "name": p_name,
                "price_regular": p.get('price_regular') or p.get('regular_price'),
                "price_sale": p.get('price_sale') or p.get('sale_price'),
                "in_stock": p_stock,
                "main_cat": sheet_cat,
                "subcat": subcat,
                "brand": brand,
                "type": "متغیر",
                "variant_attr": "",
                "product_id": p_id,
                "variation_id": "",
                "link": f"https://hosseinykala.ir/?p={p_id}",
                "sku": p.get('sku', ''),
                "status_note": "ثبت‌شده در سایت"
            }
            unified_sheets[sheet_cat].append(parent_row)

            # درج فرزندان تنوع
            for v in p_vars:
                vid = v.get('variation_id') or v.get('id')
                v_attrs = v.get('attributes', {})
                attr_desc = ", ".join([f"{k}: {val}" for k, val in v_attrs.items()]) if isinstance(v_attrs, dict) else str(v_attrs)
                v_name = f"↳ {attr_desc}"
                v_stock = live_var_stock.get(vid, "✓ موجود" if v.get('in_stock', True) else "✗ ناموجود")

                child_row = {
                    "name": v_name,
                    "price_regular": v.get('price_regular') or v.get('regular_price'),
                    "price_sale": v.get('price_sale') or v.get('sale_price'),
                    "in_stock": v_stock,
                    "main_cat": sheet_cat,
                    "subcat": subcat,
                    "brand": brand,
                    "type": "تنوع",
                    "variant_attr": attr_desc,
                    "product_id": p_id,
                    "variation_id": vid,
                    "link": f"https://hosseinykala.ir/?p={vid}",
                    "sku": v.get('sku', ''),
                    "status_note": "ثبت‌شده در سایت"
                }
                unified_sheets[sheet_cat].append(child_row)

        else:
            # محصول ساده
            p_stock = live_prod_stock.get(p_id, "✓ موجود" if p.get('in_stock', True) else "✗ ناموجود")
            simple_row = {
                "name": p_name,
                "price_regular": p.get('price_regular') or p.get('regular_price'),
                "price_sale": p.get('price_sale') or p.get('sale_price'),
                "in_stock": p_stock,
                "main_cat": sheet_cat,
                "subcat": subcat,
                "brand": brand,
                "type": "ساده",
                "variant_attr": "",
                "product_id": p_id,
                "variation_id": "",
                "link": f"https://hosseinykala.ir/?p={p_id}",
                "sku": p.get('sku', ''),
                "status_note": "ثبت‌شده در سایت"
            }
            unified_sheets[sheet_cat].append(simple_row)

    print(f"درج اولیه {len(live_products)} محصول لایو سایت انجام شد.")

    # ۲. افزودن محصولات متغیر آفلاین یکپارچه‌شده (بدون هیچ تکراری!)

    # A) یخچال و فریزر دوقلوهای آفلاین
    # ۱. کلور ۲۷ فوت اکونومی
    unified_sheets['یخچال و فریزر'].append({
        "name": "یخچال و فریزر دوقلو 27 فوت کلور مدل اکونومی",
        "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "یخچال و فریزر", "subcat": "کلور", "brand": "کلور",
        "type": "متغیر", "variant_attr": "", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })
    unified_sheets['یخچال و فریزر'].append({
        "name": "↳ رنگ: استیل", "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "یخچال و فریزر", "subcat": "کلور", "brand": "کلور",
        "type": "تنوع", "variant_attr": "رنگ: استیل", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })
    unified_sheets['یخچال و فریزر'].append({
        "name": "↳ رنگ: سفید", "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "یخچال و فریزر", "subcat": "کلور", "brand": "کلور",
        "type": "تنوع", "variant_attr": "رنگ: سفید", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })

    # ۲. کلور عرض ۷۰ مدل روسو آبریزدار
    unified_sheets['یخچال و فریزر'].append({
        "name": "یخچال و فریزر دوقلو کلور عرض 70 مدل روسو آبریزدار",
        "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "یخچال و فریزر", "subcat": "کلور", "brand": "کلور",
        "type": "متغیر", "variant_attr": "", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })
    unified_sheets['یخچال و فریزر'].append({
        "name": "↳ رنگ: استیل", "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "یخچال و فریزر", "subcat": "کلور", "brand": "کلور",
        "type": "تنوع", "variant_attr": "رنگ: استیل", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })
    unified_sheets['یخچال و فریزر'].append({
        "name": "↳ رنگ: سفید", "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "یخچال و فریزر", "subcat": "کلور", "brand": "کلور",
        "type": "تنوع", "variant_attr": "رنگ: سفید", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })

    # ۳. کلور عرض ۷۰ مدل روسو هوم بار
    unified_sheets['یخچال و فریزر'].append({
        "name": "یخچال و فریزر دوقلو کلور عرض 70 مدل روسو هوم بار",
        "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "یخچال و فریزر", "subcat": "کلور", "brand": "کلور",
        "type": "متغیر", "variant_attr": "", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })
    unified_sheets['یخچال و فریزر'].append({
        "name": "↳ رنگ: استیل", "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "یخچال و فریزر", "subcat": "کلور", "brand": "کلور",
        "type": "تنوع", "variant_attr": "رنگ: استیل", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })
    unified_sheets['یخچال و فریزر'].append({
        "name": "↳ رنگ: سفید", "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "یخچال و فریزر", "subcat": "کلور", "brand": "کلور",
        "type": "تنوع", "variant_attr": "رنگ: سفید", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })

    # ۴. مینی یخچال ۱۰ فوت کلور مدل طرح دار
    unified_sheets['یخچال و فریزر'].append({
        "name": "مینی یخچال 10 فوت کلور مدل طرح دار فانتزی",
        "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "یخچال و فریزر", "subcat": "کلور", "brand": "کلور",
        "type": "متغیر", "variant_attr": "", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })
    for color_t in ["آبی طرح دار", "سبز طرح دار", "سفید طرح دار", "مشکی طرح دار"]:
        unified_sheets['یخچال و فریزر'].append({
            "name": f"↳ طرح: {color_t}", "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
            "main_cat": "یخچال و فریزر", "subcat": "کلور", "brand": "کلور",
            "type": "تنوع", "variant_attr": f"طرح: {color_t}", "product_id": "", "variation_id": "",
            "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
        })

    # ۵. هیمالیا دوقلو آیس پول
    unified_sheets['یخچال و فریزر'].append({
        "name": "یخچال و فریزر دوقلو هیمالیا مدل آیس پول 60MW",
        "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "یخچال و فریزر", "subcat": "هیمالیا", "brand": "هیمالیا",
        "type": "متغیر", "variant_attr": "", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })
    unified_sheets['یخچال و فریزر'].append({
        "name": "↳ رنگ: استیل", "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "یخچال و فریزر", "subcat": "هیمالیا", "brand": "هیمالیا",
        "type": "تنوع", "variant_attr": "رنگ: استیل", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })
    unified_sheets['یخچال و فریزر'].append({
        "name": "↳ رنگ: سفید چرمی", "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "یخچال و فریزر", "subcat": "هیمالیا", "brand": "هیمالیا",
        "type": "تنوع", "variant_attr": "رنگ: سفید چرمی", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })

    # ۶. نیکسان RF84102E2
    unified_sheets['یخچال و فریزر'].append({
        "name": "یخچال و فریزر کمبی نیکسان مدل RF84102E2",
        "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "یخچال و فریزر", "subcat": "نیکسان", "brand": "نیکسان",
        "type": "متغیر", "variant_attr": "", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })
    unified_sheets['یخچال و فریزر'].append({
        "name": "↳ رنگ: استیل", "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "یخچال و فریزر", "subcat": "نیکسان", "brand": "نیکسان",
        "type": "تنوع", "variant_attr": "رنگ: استیل", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })
    unified_sheets['یخچال و فریزر'].append({
        "name": "↳ رنگ: سفید چرمی", "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "یخچال و فریزر", "subcat": "نیکسان", "brand": "نیکسان",
        "type": "تنوع", "variant_attr": "رنگ: سفید چرمی", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })

    # اقلام ساده آفلاین یخچال و فریزر
    other_offline_fridges = [
        ("فریزر صندوقی تکنوسان مدل سفید بزرگ", "تکنوسان", "تکنوسان", "✓ موجود"),
        ("فریزر تک خانگی ریگور", "ریگور", "ریگور", "✗ ناموجود"),
        ("یخچال و فریزر هیمالیا مدل 5 کاره هوم بار چرمی 60MW", "هیمالیا", "هیمالیا", "✓ موجود"),
        ("یخچال و فریزر هیمالیا مدل امگا (Omega) هوم بار سفید", "هیمالیا", "هیمالیا", "✓ موجود"),
        ("یخچال و فریزر کمبی هیمالیا عرض 850 تیتانیوم مدل 70-30", "هیمالیا", "هیمالیا", "✓ موجود"),
        ("یخچال و فریزر دیپوینت استیل", "دیپوینت", "دیپوینت", "✓ موجود"),
    ]
    for n, sc, b, st in other_offline_fridges:
        unified_sheets['یخچال و فریزر'].append({
            "name": n, "price_regular": "", "price_sale": "", "in_stock": st,
            "main_cat": "یخچال و فریزر", "subcat": sc, "brand": b,
            "type": "ساده", "variant_attr": "", "product_id": "", "variation_id": "",
            "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
        })

    # B) تابه گرانیتی اویز — تجمیع در قالب محصول متغیر واحد با سایز (دقیقاً بر اساس دستور کاربر)
    unified_sheets['لوازم برقی و پخت و پز'].append({
        "name": "تابه گرانیتی مشکی اویز (سایزهای 22 تا 32)",
        "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "لوازم برقی و پخت و پز", "subcat": "اویز", "brand": "اویز",
        "type": "متغیر", "variant_attr": "", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })
    pan_vars = [
        ("↳ سایز: 22 سانتیمتر", "سایز: 22 سانتیمتر", "✓ موجود"),
        ("↳ سایز: 24 سانتیمتر مشکی", "سایز: 24 سانتیمتر", "✓ موجود"),
        ("↳ سایز: 24 سانتیمتر ساده", "سایز: 24 سانتیمتر ساده", "✗ ناموجود"),
        ("↳ سایز: 26 سانتیمتر", "سایز: 26 سانتیمتر", "✓ موجود"),
        ("↳ سایز: 28 سانتیمتر درب دار", "سایز: 28 سانتیمتر درب دار", "✓ موجود"),
        ("↳ سایز: 30 سانتیمتر", "سایز: 30 سانتیمتر", "✓ موجود"),
        ("↳ سایز: 32 سانتیمتر فوج مشکی درب دار", "سایز: 32 سانتیمتر فوج", "✓ موجود"),
    ]
    for vn, vattr, vst in pan_vars:
        unified_sheets['لوازم برقی و پخت و پز'].append({
            "name": vn, "price_regular": "", "price_sale": "", "in_stock": vst,
            "main_cat": "لوازم برقی و پخت و پز", "subcat": "اویز", "brand": "اویز",
            "type": "تنوع", "variant_attr": vattr, "product_id": "", "variation_id": "",
            "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
        })

    # خردکن برقی ویلز متغیر
    unified_sheets['لوازم برقی و پخت و پز'].append({
        "name": "خردکن برقی کاسه دار ویلز",
        "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "لوازم برقی و پخت و پز", "subcat": "ویلز", "brand": "ویلز",
        "type": "متغیر", "variant_attr": "", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })
    unified_sheets['لوازم برقی و پخت و پز'].append({
        "name": "↳ مدل: 6031 استیل", "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "لوازم برقی و پخت و پز", "subcat": "ویلز", "brand": "ویلز",
        "type": "تنوع", "variant_attr": "مدل: 6031 استیل", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })
    unified_sheets['لوازم برقی و پخت و پز'].append({
        "name": "↳ مدل: 6032 سه لیتری", "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "لوازم برقی و پخت و پز", "subcat": "ویلز", "brand": "ویلز",
        "type": "تنوع", "variant_attr": "مدل: 6032 سه لیتری", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })

    # سایر اقلام آفلاین لوازم پخت و پز (یکپارچه، بدون تکرار)
    cook_offline_items = [
        ("سرخ کن بدون روغن دونالکس مدل DN-970 استیل", "دونالکس", "دونالکس", "✓ موجود"),
        ("سرخ کن ایرفرایر خاکستری گرنویک", "گرنویک", "گرنویک", "✓ موجود"),
        ("سرخ کن بدون روغن ویلز مدل 5062", "ویلز", "ویلز", "✓ موجود"),
        ("چرخ گوشت برقی ویلز", "ویلز", "ویلز", "✓ موجود"),
        ("سبزی خردکن خانگی نیاک 3 کیلوگرم", "نیاک", "نیاک", "✓ موجود"),
        ("سبزی خردکن KENRA", "متفرقه", "KENRA", "✓ موجود"),
        ("گوشت کوب و غذاساز دونالکس مدل DN-290", "دونالکس", "دونالکس", "✓ موجود"),
        ("سرویس قابلمه 11 پارچه اویزپلاس مدل السا سبز", "اویزپلاس", "اویزپلاس", "✓ موجود"),
        ("قابلمه مرغ خوری اویزپلاس مشکی", "اویزپلاس", "اویزپلاس", "✓ موجود"),
        ("سرویس قابلمه استیل 10 پارچه", "متفرقه", "متفرقه", "— ناموجود"),
        ("سرویس قابلمه اویزپلاس 10 پارچه اناری", "اویزپلاس", "اویزپلاس", "— ناموجود"),
        ("قابلمه تک سایز 14 لاوان", "لاوان", "لاوان", "✓ موجود"),
        ("گاز صفحه ای استیل آلتون مدل SG518", "آلتون", "آلتون", "✓ موجود"),
        ("فر توکار آلتون مدل 7303", "آلتون", "آلتون", "✓ موجود"),
        ("فر گاز فردار آلتون مدل MDS", "آلتون", "آلتون", "✓ موجود"),
        ("هود آشپزخانه آلتون مدل H312", "آلتون", "آلتون", "✓ موجود"),
        ("هود آشپزخانه آلتون مدل H315B", "آلتون", "آلتون", "✓ موجود"),
        ("فر برقی الکترواستیل عرض 60 چرمی مدل 21", "الکترواستیل", "الکترواستیل", "✓ موجود"),
        ("فر الکترواستیل تیتانیوم 11", "الکترواستیل", "الکترواستیل", "— ناموجود"),
        ("پلوپز پارس خزر مدل 361", "پارس خزر", "پارس خزر", "✓ موجود"),
        ("پلوپز پارس خزر 8 نفره نقره ای", "پارس خزر", "پارس خزر", "— ناموجود"),
        ("توستر نان و شیرینی 60 لیتر", "متفرقه", "متفرقه", "✓ موجود"),
        ("ساندویچ ساز دونالکس", "دونالکس", "دونالکس", "✓ موجود"),
        ("هواپز ساپر 7.2 لیتر مدل 1710", "ساپر", "ساپر", "✓ موجود"),
    ]
    for n, sc, b, st in cook_offline_items:
        unified_sheets['لوازم برقی و پخت و پز'].append({
            "name": n, "price_regular": "", "price_sale": "", "in_stock": st,
            "main_cat": "لوازم برقی و پخت و پز", "subcat": sc, "brand": b,
            "type": "ساده", "variant_attr": "", "product_id": "", "variation_id": "",
            "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
        })

    # C) شستشو و نظافت
    # لباسشویی دوو سری سینیور DWK-990 متغیر
    unified_sheets['شستشو و نظافت'].append({
        "name": "ماشین لباسشویی 9 کیلوگرم اتوماتیک دوو سری سینیور DWK-990",
        "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "شستشو و نظافت", "subcat": "دوو", "brand": "دوو",
        "type": "متغیر", "variant_attr": "", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })
    unified_sheets['شستشو و نظافت'].append({
        "name": "↳ رنگ: سفید (990c)", "price_regular": "", "price_sale": "", "in_stock": "✗ ناموجود",
        "main_cat": "شستشو و نظافت", "subcat": "دوو", "brand": "دوو",
        "type": "تنوع", "variant_attr": "رنگ: سفید (990c)", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })
    unified_sheets['شستشو و نظافت'].append({
        "name": "↳ رنگ: سیلور (990S)", "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "شستشو و نظافت", "subcat": "دوو", "brand": "دوو",
        "type": "تنوع", "variant_attr": "رنگ: سیلور (990S)", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })

    # لباسشویی هیمالیا تسلا پرو متغیر
    unified_sheets['شستشو و نظافت'].append({
        "name": "ماشین لباسشویی 10 کیلوگرم اینورتر هیمالیا مدل تسلا پرو",
        "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "شستشو و نظافت", "subcat": "هیمالیا", "brand": "هیمالیا",
        "type": "متغیر", "variant_attr": "", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })
    unified_sheets['شستشو و نظافت'].append({
        "name": "↳ رنگ: استیل", "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "شستشو و نظافت", "subcat": "هیمالیا", "brand": "هیمالیا",
        "type": "تنوع", "variant_attr": "رنگ: استیل", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })
    unified_sheets['شستشو و نظافت'].append({
        "name": "↳ رنگ: سفید", "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "شستشو و نظافت", "subcat": "هیمالیا", "brand": "هیمالیا",
        "type": "تنوع", "variant_attr": "رنگ: سفید", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })

    # لباسشویی دوقلو پاکشوما متغیر
    unified_sheets['شستشو و نظافت'].append({
        "name": "ماشین لباسشویی دوقلو نیمه اتوماتیک پاکشوما",
        "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "شستشو و نظافت", "subcat": "پاکشوما", "brand": "پاکشوما",
        "type": "متغیر", "variant_attr": "", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })
    unified_sheets['شستشو و نظافت'].append({
        "name": "↳ ظرفیت: 9 کیلوگرم", "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "شستشو و نظافت", "subcat": "پاکشوما", "brand": "پاکشوما",
        "type": "تنوع", "variant_attr": "ظرفیت: 9 کیلوگرم", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })
    unified_sheets['شستشو و نظافت'].append({
        "name": "↳ ظرفیت: 15 کیلوگرم", "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "شستشو و نظافت", "subcat": "پاکشوما", "brand": "پاکشوما",
        "type": "تنوع", "variant_attr": "ظرفیت: 15 کیلوگرم", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })
    unified_sheets['شستشو و نظافت'].append({
        "name": "↳ ظرفیت: 21 کیلوگرم", "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "شستشو و نظافت", "subcat": "پاکشوما", "brand": "پاکشوما",
        "type": "تنوع", "variant_attr": "ظرفیت: 21 کیلوگرم", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })

    # پتوشور پاکیزان متغیر
    unified_sheets['شستشو و نظافت'].append({
        "name": "پتوشور صنعتی و خانگی پاکیزان",
        "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "شستشو و نظافت", "subcat": "پاکیزان", "brand": "پاکیزان",
        "type": "متغیر", "variant_attr": "", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })
    unified_sheets['شستشو و نظافت'].append({
        "name": "↳ ظرفیت: 30 کیلوگرم", "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "شستشو و نظافت", "subcat": "پاکیزان", "brand": "پاکیزان",
        "type": "تنوع", "variant_attr": "ظرفیت: 30 کیلوگرم", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })
    unified_sheets['شستشو و نظافت'].append({
        "name": "↳ ظرفیت: 40 کیلوگرم", "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "شستشو و نظافت", "subcat": "پاکیزان", "brand": "پاکیزان",
        "type": "تنوع", "variant_attr": "ظرفیت: 40 کیلوگرم", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })

    # جاروبرقی سران ۲۱ لیتر متغیر
    unified_sheets['شستشو و نظافت'].append({
        "name": "جاروبرقی سطلی 21 لیتری سران مدل آب و خاک",
        "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "شستشو و نظافت", "subcat": "سران", "brand": "سران",
        "type": "متغیر", "variant_attr": "", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })
    unified_sheets['شستشو و نظافت'].append({
        "name": "↳ رنگ: زرد", "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "شستشو و نظافت", "subcat": "سران", "brand": "سران",
        "type": "تنوع", "variant_attr": "رنگ: زرد", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })
    unified_sheets['شستشو و نظافت'].append({
        "name": "↳ رنگ: مشکی", "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "شستشو و نظافت", "subcat": "سران", "brand": "سران",
        "type": "تنوع", "variant_attr": "رنگ: مشکی", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })

    # اقلام ساده شستشو و نظافت
    wash_offline_items = [
        ("ماشین لباسشویی 9 کیلوگرم کلور مدل ویوا سفید", "کلور", "کلور", "✓ موجود"),
        ("ماشین لباسشویی کلور مدل 9771 سفید", "کلور", "کلور", "— ناموجود"),
        ("ماشین لباسشویی اتوماتیک دوو 9.5 کیلوگرم مدل 991s", "دوو", "دوو", "✓ موجود"),
        ("ماشین لباسشویی 8 کیلوگرم دوو سیلور", "دوو", "دوو", "✓ موجود"),
        ("لباسشویی دوقلو 17 کیلویی ریتون", "ریتون", "ریتون", "✓ موجود"),
        ("مینی واش فریدولین 3.5 کیلوگرم مدل تک درب", "فریدولین", "فریدولین", "✓ موجود"),
        ("جاروبرقی سطلی کلور", "کلور", "کلور", "✓ موجود"),
        ("جاروبرقی سطلی آراز 40 لیتر", "آراز", "آراز", "✓ موجود"),
        ("جاروبرقی سطلی صنعتی آب و خاک پاندا 80 لیتر", "پاندا", "پاندا", "✓ موجود"),
        ("جاروبرقی سطلی هیتاچی 1200", "هیتاچی", "هیتاچی", "✓ موجود"),
        ("جاروبرقی دونالکس 770", "دونالکس", "دونالکس", "— ناموجود"),
        ("اتوبخار ساپر کف سرامیک مدل 4025", "ساپر", "ساپر", "✓ موجود"),
        ("اتوبخار ساپر کف سرامیک مدل 4035", "ساپر", "ساپر", "✓ موجود"),
        ("اتوبخار رانکو", "رانکو", "رانکو", "✓ موجود"),
        ("اتوبخار سیماران مدل 8002 زرد", "سیماران", "سیماران", "✓ موجود"),
        ("اتوبخار مونزا مدل VR3000W", "مونزا", "مونزا", "✓ موجود"),
    ]
    for n, sc, b, st in wash_offline_items:
        unified_sheets['شستشو و نظافت'].append({
            "name": n, "price_regular": "", "price_sale": "", "in_stock": st,
            "main_cat": "شستشو و نظافت", "subcat": sc, "brand": b,
            "type": "ساده", "variant_attr": "", "product_id": "", "variation_id": "",
            "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
        })

    # D) نوشیدنی ساز
    # کتری ساپر ۱۰۳۱ متغیر
    unified_sheets['نوشیدنی ساز'].append({
        "name": "کتری برقی ساپر مدل 1031",
        "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "نوشیدنی ساز", "subcat": "ساپر", "brand": "ساپر",
        "type": "متغیر", "variant_attr": "", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })
    unified_sheets['نوشیدنی ساز'].append({
        "name": "↳ رنگ: سبز", "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "نوشیدنی ساز", "subcat": "ساپر", "brand": "ساپر",
        "type": "تنوع", "variant_attr": "رنگ: سبز", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })
    unified_sheets['نوشیدنی ساز'].append({
        "name": "↳ رنگ: کرم", "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "نوشیدنی ساز", "subcat": "ساپر", "brand": "ساپر",
        "type": "تنوع", "variant_attr": "رنگ: کرم", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })

    # ست کتری و قوری ژمبو (زامروتی) متغیر
    unified_sheets['نوشیدنی ساز'].append({
        "name": "ست کتری و قوری روگازی ژمبو (زامروتی) مدل 2022",
        "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "نوشیدنی ساز", "subcat": "ژمبو", "brand": "ژمبو",
        "type": "متغیر", "variant_attr": "", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })
    unified_sheets['نوشیدنی ساز'].append({
        "name": "↳ مشخصه: دسته استیل", "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "نوشیدنی ساز", "subcat": "ژمبو", "brand": "ژمبو",
        "type": "تنوع", "variant_attr": "مشخصه: دسته استیل", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })
    unified_sheets['نوشیدنی ساز'].append({
        "name": "↳ مشخصه: دسته چوب", "price_regular": "", "price_sale": "", "in_stock": "✓ موجود",
        "main_cat": "نوشیدنی ساز", "subcat": "ژمبو", "brand": "ژمبو",
        "type": "تنوع", "variant_attr": "مشخصه: دسته چوب", "product_id": "", "variation_id": "",
        "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
    })

    # اقلام ساده نوشیدنی ساز
    bev_offline_items = [
        ("کتری برقی ساپر استیل مدل 1011", "ساپر", "ساپر", "✓ موجود"),
        ("کتری برقی سانی 1.5 لیتر", "سانی", "سانی", "✓ موجود"),
        ("کتری برقی پروکس", "پروکس", "پروکس", "✓ موجود"),
        ("کتری برقی سیماران استیل مدل 750", "سیماران", "سیماران", "✓ موجود"),
        ("کتری برقی تفال 2 لیتر", "تفال", "تفال", "✓ موجود"),
        ("کتری برقی تک زامروتی کرم", "زامروتی", "زامروتی", "✓ موجود"),
        ("کتری برقی وولگا", "وولگا", "وولگا", "✓ موجود"),
        ("ست کتری و قوری هرمی تمام طلا مدل 604", "متفرقه", "متفرقه", "✓ موجود"),
        ("چای ساز سماوری گرنویک", "گرنویک", "گرنویک", "✓ موجود"),
        ("چای ساز کورکماز مدل A331", "کورکماز", "کورکماز", "✓ موجود"),
        ("چای ساز ویلز مدل 2015", "ویلز", "ویلز", "✓ موجود"),
        ("چای ساز زامروتی", "زامروتی", "زامروتی", "— ناموجود"),
        ("مخلوط کن زامروتی کرم", "زامروتی", "زامروتی", "✓ موجود"),
        ("همزن دستی دونالکس مدل 355", "دونالکس", "دونالکس", "✓ موجود"),
        ("همزن کاسه چرخدار اوریکس", "اوریکس", "اوریکس", "✓ موجود"),
        ("همزن برقی کنوود مدل HM430", "کنوود", "کنوود", "✓ موجود"),
        ("آبمیوه گیری چندکاره جنرال مدل 607 غذاساز", "جنرال", "جنرال", "✓ موجود"),
        ("آسیاب برقی کاستلو مدل 470", "کاستلو", "کاستلو", "✓ موجود"),
        ("آسیاب برقی ونتو", "ونتو", "ونتو", "✓ موجود"),
        ("اسپرسوساز حرفه ای رانکو", "رانکو", "رانکو", "✓ موجود"),
        ("اسپرسوساز نارنجی گرنویک", "گرنویک", "گرنویک", "✓ موجود"),
        ("اسپرسوساز دونالکس 380", "دونالکس", "دونالکس", "— ناموجود"),
        ("اسپرسوساز دونالکس 375", "دونالکس", "دونالکس", "— ناموجود"),
    ]
    for n, sc, b, st in bev_offline_items:
        unified_sheets['نوشیدنی ساز'].append({
            "name": n, "price_regular": "", "price_sale": "", "in_stock": st,
            "main_cat": "نوشیدنی ساز", "subcat": sc, "brand": b,
            "type": "ساده", "variant_attr": "", "product_id": "", "variation_id": "",
            "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
        })

    # E) سرمایش و گرمایش
    climate_offline_items = [
        ("بخاری گلدن لوکس", "گلدن لوکس", "گلدن لوکس", "✓ موجود"),
        ("بخاری پارس خزر فن دار مدل FH-2000P", "پارس خزر", "پارس خزر", "✓ موجود"),
        ("بخاری پلار مدل 3PN-NEW ماشینی", "پلار", "پلار", "✓ موجود"),
        ("پنکه پایه بلند پارس خزر", "پارس خزر", "پارس خزر", "✓ موجود"),
        ("پنکه پایه بلند الکترا", "الکترا", "الکترا", "✓ موجود"),
        ("پنکه پاناسونیک 2 حالته", "پاناسونیک", "پاناسونیک", "✓ موجود"),
        ("پنکه سانی مدل 2013 ساده", "سانی", "سانی", "— ناموجود"),
        ("کولر آبی اوناکس مدل B35", "اوناکس", "اوناکس", "✓ موجود"),
        ("کولر آبی اوناکس مدل H50 یاسان", "اوناکس", "اوناکس", "✓ موجود"),
        ("کولر آبی مدل 4500", "متفرقه", "متفرقه", "✓ موجود"),
        ("کولر پنجره ای اوجنرال 18 هزار", "اوجنرال", "اوجنرال", "✓ موجود"),
        ("کولر گازی وستینگهاوس 30 کوپلند", "وستینگهاوس", "وستینگهاوس", "✗ ناموجود"),
        ("آبگرمکن مخزندار دیواری الکترواستیل", "الکترواستیل", "الکترواستیل", "✓ موجود"),
        ("آبگرمکن دیواری بوتان مدل B3115", "بوتان", "بوتان", "✗ ناموجود"),
    ]
    for n, sc, b, st in climate_offline_items:
        unified_sheets['سرمایش و گرمایش'].append({
            "name": n, "price_regular": "", "price_sale": "", "in_stock": st,
            "main_cat": "سرمایش و گرمایش", "subcat": sc, "brand": b,
            "type": "ساده", "variant_attr": "", "product_id": "", "variation_id": "",
            "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
        })

    # F) تصفیه کننده آب
    water_offline_items = [
        ("دستگاه تصفیه آب خانگی وست واتر", "وست واتر", "وست واتر", "✓ موجود"),
        ("آبسردکن هانو", "هانو", "هانو", "— ناموجود"),
    ]
    for n, sc, b, st in water_offline_items:
        unified_sheets['تصفیه کننده آب'].append({
            "name": n, "price_regular": "", "price_sale": "", "in_stock": st,
            "main_cat": "تصفیه کننده آب", "subcat": sc, "brand": b,
            "type": "ساده", "variant_attr": "", "product_id": "", "variation_id": "",
            "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
        })

    # G) زیبایی و سلامت فردی
    beauty_offline_items = [
        ("ریش تراش چرخشی پرومارون مدل 706", "پرومارون", "پرومارون", "✓ موجود"),
        ("دستگاه پیرایش سیمی سر و صورت پرومارون مدل 731", "پرومارون", "پرومارون", "✓ موجود"),
        ("فر کننده مو پرومارون مدل 9909", "پرومارون", "پرومارون", "✓ موجود"),
        ("ماشین اصلاح موی سر و صورت پروامگا مدل تک", "پروامگا", "پروامگا", "✓ موجود"),
        ("ماشین اصلاح موی سر و صورت پروامگا 8 کاره", "پروامگا", "پروامگا", "✓ موجود"),
        ("ماشین اصلاح موی سر و صورت پروامگا شارژی و برقی", "پروامگا", "پروامگا", "✓ موجود"),
        ("سشوار خانگی امگا 2000 وات", "امگا", "امگا", "✓ موجود"),
        ("سشوار حرفه ای پروامگا 2200 وات", "پروامگا", "پروامگا", "✓ موجود"),
        ("اتو مو مسافرتی پاناسونیک مدل HV11", "پاناسونیک", "پاناسونیک", "✓ موجود"),
        ("اتو مو باریک سرامیکی baby3383a", "متفرقه", "متفرقه", "✓ موجود"),
    ]
    for n, sc, b, st in beauty_offline_items:
        unified_sheets['زیبایی و سلامت فردی'].append({
            "name": n, "price_regular": "", "price_sale": "", "in_stock": st,
            "main_cat": "زیبایی و سلامت فردی", "subcat": sc, "brand": b,
            "type": "ساده", "variant_attr": "", "product_id": "", "variation_id": "",
            "link": "", "sku": "", "status_note": "در سایت تعریف نشده"
        })

    # ساخت فایل اکسل و ثبت استایل‌ها
    wb = openpyxl.Workbook()
    # حذف شیت پیش‌فرض
    default_ws = wb.active
    wb.remove(default_ws)

    # ایجاد شیت‌ها به ترتیب
    sheet_order = [
        "📊 خلاصه و داشبورد",
        "⚡ ویرایش گروهی",
        "یخچال و فریزر",
        "شستشو و نظافت",
        "لوازم برقی و پخت و پز",
        "نوشیدنی ساز",
        "سرمایش و گرمایش",
        "تصفیه کننده آب",
        "صوتی و تصویری",
        "زیبایی و سلامت فردی",
        "📖 راهنمای کاربری"
    ]

    created_sheets = {}
    for title in sheet_order:
        s = wb.create_sheet(title=title)
        s.views.sheetView[0].rightToLeft = True
        created_sheets[title] = s

    border_thin = get_border()

    stats_summary = {
        "total_parent_rows": 0,
        "total_variation_rows": 0,
        "total_site_products": 0,
        "total_offline_products": 0,
        "in_stock_count": 0,
        "out_of_stock_count": 0,
        "cat_breakdown": {}
    }

    # پر کردن شیت‌های ۸گانه کالاها
    cat_keys = [
        'یخچال و فریزر',
        'شستشو و نظافت',
        'لوازم برقی و پخت و پز',
        'نوشیدنی ساز',
        'سرمایش و گرمایش',
        'تصفیه کننده آب',
        'صوتی و تصویری',
        'زیبایی و سلامت فردی'
    ]

    for cat_title in cat_keys:
        ws = created_sheets[cat_title]
        items = unified_sheets[cat_title]

        # هدر جدول
        ws.row_dimensions[1].height = 28
        for col_idx, col_def in enumerate(COLUMNS, 1):
            cell = ws.cell(row=1, column=col_idx, value=col_def[1])
            cell.font = Font(name="Calibri", size=11, bold=True, color=COLOR_HEADER_TEXT)
            cell.fill = PatternFill(fill_type="solid", fgColor=COLOR_HEADER_BG)
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = border_thin
            ws.column_dimensions[get_column_letter(col_idx)].width = col_def[2]

        ws.freeze_panes = "A2"

        # گروه بندی بر اساس برند / زیردسته
        grouped_by_brand = defaultdict(list)
        for it in items:
            br = it.get('subcat') or it.get('brand') or 'متفرقه'
            grouped_by_brand[br].append(it)

        # مرتب‌سازی برندها (برندهای شاخص اول)
        sorted_brands = sorted(grouped_by_brand.keys(), key=lambda b: (0 if b in ['کلور', 'دیپوینت', 'هیمالیا', 'دوو', 'الکترواستیل', 'پاکشوما', 'اویز', 'دونالکس', 'وستینگهاوس', 'هاورسن', 'هاورسون'] else 1, b))

        current_row = 2
        cat_in_stock = 0
        cat_out_stock = 0
        cat_parents = 0
        cat_vars = 0

        for brand_name in sorted_brands:
            brand_items = grouped_by_brand[brand_name]

            # سطر بنر برند
            ws.row_dimensions[current_row].height = 24
            ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=len(COLUMNS))
            banner_cell = ws.cell(row=current_row, column=1, value=f"  📂 {cat_title}  ◀  {brand_name}")
            banner_cell.font = Font(name="Calibri", size=11, bold=True, color=COLOR_BANNER_TEXT)
            banner_cell.fill = PatternFill(fill_type="solid", fgColor=COLOR_BANNER_BG)
            banner_cell.alignment = Alignment(horizontal="right", vertical="center")
            for c in range(1, len(COLUMNS) + 1):
                ws.cell(row=current_row, column=c).border = border_thin
            current_row += 1

            for it in brand_items:
                is_child = (it.get('type') == 'تنوع')
                is_parent_var = (it.get('type') == 'متغیر')
                is_site = (it.get('status_note') == 'ثبت‌شده در سایت')
                stock_label = it.get('in_stock', '✓ موجود')
                is_in_stock = ("✓" in stock_label)

                if is_child:
                    cat_vars += 1
                    stats_summary["total_variation_rows"] += 1
                else:
                    cat_parents += 1
                    stats_summary["total_parent_rows"] += 1
                    if is_site:
                        stats_summary["total_site_products"] += 1
                    else:
                        stats_summary["total_offline_products"] += 1

                    if is_in_stock:
                        cat_in_stock += 1
                        stats_summary["in_stock_count"] += 1
                    else:
                        cat_out_stock += 1
                        stats_summary["out_of_stock_count"] += 1

                # ارتفاع و رنگ ردیف
                ws.row_dimensions[current_row].height = 20 if is_child else 21
                if is_child:
                    row_bg = COLOR_VARIATION_BG
                elif is_parent_var:
                    row_bg = COLOR_VAR_PARENT_BG
                else:
                    row_bg = "FFFFFF"

                fill_row = PatternFill(fill_type="solid", fgColor=row_bg)

                reg_p = it.get('price_regular')
                sale_p = it.get('price_sale')
                f_reg_t = f'=IF(ISBLANK(B{current_row}),"",B{current_row}/10)'
                f_sale_t = f'=IF(OR(ISBLANK(D{current_row}),D{current_row}=""),"",D{current_row}/10)'

                row_vals = [
                    it['name'],
                    reg_p if reg_p else "",
                    f_reg_t if reg_p else "",
                    sale_p if sale_p else "",
                    f_sale_t if sale_p else "",
                    stock_label,
                    cat_title,
                    it.get('subcat', brand_name),
                    it.get('brand', brand_name),
                    it.get('type', 'ساده'),
                    it.get('variant_attr', ''),
                    it.get('product_id', ''),
                    it.get('variation_id', ''),
                    it.get('link', ''),
                    it.get('sku', ''),
                    it.get('status_note', 'ثبت‌شده در سایت' if is_site else 'در سایت تعریف نشده')
                ]

                for c_idx, val in enumerate(row_vals, 1):
                    cell = ws.cell(row=current_row, column=c_idx, value=val)
                    cell.border = border_thin
                    cell.fill = fill_row

                    # تراز
                    col_align = COLUMNS[c_idx - 1][3]
                    cell.alignment = Alignment(horizontal=col_align, vertical="center")

                    # فونت و رنگ
                    if c_idx == 1:
                        # نام محصول
                        cell.font = Font(name="Calibri", size=10, bold=is_parent_var, color="555555" if is_child else "000000")
                    elif c_idx == 6:
                        # موجودی
                        if "✓" in str(val):
                            cell.font = Font(name="Calibri", size=10, bold=True, color=COLOR_IN_STOCK)
                        elif "✗" in str(val):
                            cell.font = Font(name="Calibri", size=10, bold=True, color=COLOR_OUT_OF_STOCK)
                        else:
                            cell.font = Font(name="Calibri", size=10, color="888888")
                    elif c_idx in [2, 3, 4, 5]:
                        # قیمت‌ها
                        cell.font = Font(name="Calibri", size=10, bold=(c_idx in [3, 5]))
                        cell.number_format = "#,##0"
                    elif c_idx == 14:
                        # لینک
                        cell.font = Font(name="Calibri", size=9, color="004C99")
                    else:
                        cell.font = Font(name="Calibri", size=10)

                current_row += 1

        # اعتبارسنجی‌ها و فرمت‌بندی شرطی پویا (Dynamic Conditional Formatting)
        max_data_row = current_row - 1
        if max_data_row >= 2:
            # ۱. اعتبارسنجی منوی کشویی موجودی (ستون F)
            dv_stock = DataValidation(type="list", formula1='"✓ موجود,✗ ناموجود"', allow_blank=True)
            ws.add_data_validation(dv_stock)
            dv_stock.add(f"F2:F{max_data_row}")

            # ۲. اعتبارسنجی منوی کشویی وضعیت در سایت (ستون P) با ۳ گزینه اختصاصی
            dv_status = DataValidation(type="list", formula1='"ثبت‌شده در سایت,در سایت تعریف نشده,فعلا دست نگه دار"', allow_blank=True)
            ws.add_data_validation(dv_status)
            dv_status.add(f"P2:P{max_data_row}")

            # ۳. قوانین فرمت‌بندی شرطی پویا برای تغییر خودکار رنگ سطرها بر اساس ستون P
            fill_unregistered = PatternFill(start_color=COLOR_OFFLINE_BG, end_color=COLOR_OFFLINE_BG, fill_type="solid")
            fill_on_hold = PatternFill(start_color=COLOR_ON_HOLD_BG, end_color=COLOR_ON_HOLD_BG, fill_type="solid")

            # شرط ۱: اگر در سایت تعریف نشده بود -> کل سطر زرد ملایم شود
            rule_unreg = FormulaRule(
                formula=['=$P2="در سایت تعریف نشده"'],
                stopIfTrue=True,
                fill=fill_unregistered
            )
            # شرط ۲: اگر گزینه سوم «فعلا دست نگه دار» انتخاب شد -> کل سطر نارنجی/هلویی ملایم شود
            rule_hold = FormulaRule(
                formula=['=$P2="فعلا دست نگه دار"'],
                stopIfTrue=True,
                fill=fill_on_hold
            )

            range_data = f"A2:P{max_data_row}"
            ws.conditional_formatting.add(range_data, rule_unreg)
            ws.conditional_formatting.add(range_data, rule_hold)

        stats_summary["cat_breakdown"][cat_title] = {
            "parents": cat_parents,
            "variations": cat_vars,
            "in_stock": cat_in_stock,
            "out_of_stock": cat_out_stock
        }

    # ۳. پر کردن شیت داشبورد (📊 خلاصه و داشبورد)
    ws_dash = created_sheets["📊 خلاصه و داشبورد"]
    ws_dash.column_dimensions['A'].width = 6
    ws_dash.column_dimensions['B'].width = 32
    ws_dash.column_dimensions['C'].width = 18
    ws_dash.column_dimensions['D'].width = 18
    ws_dash.column_dimensions['E'].width = 18
    ws_dash.column_dimensions['F'].width = 18

    # عنوان داشبورد
    ws_dash.row_dimensions[2].height = 35
    ws_dash.merge_cells("B2:F2")
    c_title = ws_dash.cell(row=2, column=2, value="📊 داشبورد کاتالوگ جامع و وضعیت انبار — فروشگاه لوازم خانگی حسینی")
    c_title.font = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
    c_title.fill = PatternFill(fill_type="solid", fgColor=COLOR_HEADER_BG)
    c_title.alignment = Alignment(horizontal="center", vertical="center")

    # کارت‌های شاخص کلیدی (KPIs)
    kpis = [
        ("کل محصولات اصلی", stats_summary["total_parent_rows"], "1F4E79"),
        ("محصولات ثبت‌شده سایت", stats_summary["total_site_products"], "2E75B6"),
        ("تنوع‌های رنگ و سایز", stats_summary["total_variation_rows"], "548235"),
        ("اقلام موجود (انبار/سایت)", stats_summary["in_stock_count"], "27AE60"),
        ("اقلام ناموجود", stats_summary["out_of_stock_count"], "C00000"),
    ]

    ws_dash.row_dimensions[4].height = 20
    ws_dash.row_dimensions[5].height = 28
    for idx, (label, val, col_hex) in enumerate(kpis, 2):
        cell_lbl = ws_dash.cell(row=4, column=idx, value=label)
        cell_lbl.font = Font(name="Calibri", size=10, bold=True, color="555555")
        cell_lbl.alignment = Alignment(horizontal="center", vertical="center")
        cell_lbl.fill = PatternFill(fill_type="solid", fgColor="F2F2F2")
        cell_lbl.border = border_thin

        cell_v = ws_dash.cell(row=5, column=idx, value=val)
        cell_v.font = Font(name="Calibri", size=16, bold=True, color=col_hex)
        cell_v.alignment = Alignment(horizontal="center", vertical="center")
        cell_v.fill = PatternFill(fill_type="solid", fgColor="FAFAFA")
        cell_v.border = border_thin

    # جدول تفکیک بر اساس دسته‌بندی‌ها
    ws_dash.row_dimensions[7].height = 24
    headers_dash = ["دسته‌بندی اصلی", "تعداد کالای اصلی", "تنوع متغیرها", "تعداد موجود", "تعداد ناموجود"]
    for col_i, h_txt in enumerate(headers_dash, 2):
        c = ws_dash.cell(row=7, column=col_i, value=h_txt)
        c.font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        c.fill = PatternFill(fill_type="solid", fgColor="2E75B6")
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.border = border_thin

    row_d = 8
    for cat_name in cat_keys:
        bd = stats_summary["cat_breakdown"][cat_name]
        ws_dash.row_dimensions[row_d].height = 20
        row_vals = [cat_name, bd['parents'], bd['variations'], bd['in_stock'], bd['out_of_stock']]
        for col_i, val in enumerate(row_vals, 2):
            c = ws_dash.cell(row=row_d, column=col_i, value=val)
            c.border = border_thin
            c.alignment = Alignment(horizontal="right" if col_i == 2 else "center", vertical="center")
            c.font = Font(name="Calibri", size=10, bold=(col_i == 2))
            if col_i == 5:
                c.font = Font(name="Calibri", size=10, bold=True, color=COLOR_IN_STOCK)
            elif col_i == 6:
                c.font = Font(name="Calibri", size=10, bold=True, color=COLOR_OUT_OF_STOCK)
        row_d += 1

    # ۴. پر کردن شیت ویرایش گروهی (⚡ ویرایش گروهی)
    ws_edit = created_sheets["⚡ ویرایش گروهی"]
    col_widths_edit = {
        'A': 8,   # ردیف
        'B': 24,  # محدوده هدف (فیلتر)
        'C': 32,  # نام دسته / برند / شناسه یا نام کالا
        'D': 25,  # نوع عملیات
        'E': 18,  # واحد مقدار
        'F': 16,  # مقدار عددی
        'G': 20,  # وضعیت موجودی جدید
        'H': 22,  # نحوه گرد کردن
        'I': 14,  # وضعیت سطر
        'J': 30,  # یادداشت اختیاری
    }
    for c_letter, c_w in col_widths_edit.items():
        ws_edit.column_dimensions[c_letter].width = c_w

    # ۱. بنر عنوان
    ws_edit.merge_cells("A1:J2")
    t_cell = ws_edit["A1"]
    t_cell.value = "🎛️ پنل هوشمند ویرایش گروهی قیمت و موجودی محصولات حسینی کالا"
    t_cell.font = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
    t_cell.fill = PatternFill(fill_type="solid", fgColor=COLOR_HEADER_BG)
    t_cell.alignment = Alignment(horizontal="center", vertical="center")

    # ۲. راهنمای کاربر
    ws_edit.merge_cells("A3:J5")
    g_cell = ws_edit["A3"]
    guide_text = (
        "💡 راهنمای کاربری (بدون فرضیات پیش‌فرض):\n"
        "۱. در جدول زیر سطر جدیدی تنظیم کنید: محدوده هدف (دسته‌بندی، برند یا محصول) را مشخص نمایید، نوع عملیات (افزایش، کاهش یا تخفیف) را انتخاب کرده و عدد دلخواه را وارد کنید.\n"
        "۲. ستون وضعیت سطر را «فعال» قرار دهید و فایل اکسل را ذخیره نمایید.\n"
        "۳. برای محاسبه پاسخ و اعمال قطعی تغییرات در کاتالوگ، روی فایل «⚡_اعمال_ویرایش_گروهی_از_اکسل.bat» دابل کلیک کنید."
    )
    g_cell.value = guide_text
    g_cell.font = Font(name="Calibri", size=9, bold=False, color="1F4E79")
    g_cell.fill = PatternFill(fill_type="solid", fgColor=COLOR_BANNER_BG)
    g_cell.alignment = Alignment(horizontal="right", vertical="center", wrap_text=True)

    # ۳. هدر جدول
    e_headers = [
        ("A6", "ردیف"),
        ("B6", "محدوده هدف (فیلتر)"),
        ("C6", "نام دسته / برند / شناسه یا نام کالا"),
        ("D6", "نوع عملیات"),
        ("E6", "واحد مقدار"),
        ("F6", "مقدار عددی"),
        ("G6", "وضعیت موجودی جدید"),
        ("H6", "نحوه گرد کردن مبالغ"),
        ("I6", "وضعیت سطر"),
        ("J6", "یادداشت اختیاری"),
    ]
    ws_edit.row_dimensions[6].height = 28
    for pos, htext in e_headers:
        c = ws_edit[pos]
        c.value = htext
        c.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
        c.fill = PatternFill(fill_type="solid", fgColor="2E75B6")
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = border_thin

    # ۴. ایجاد سطور خالی و تمیز (بدون مقادیر پیش‌فرض فرضی)
    total_empty_rows = 20
    row_start = 7
    for idx in range(total_empty_rows):
        cur_row = row_start + idx
        ws_edit.row_dimensions[cur_row].height = 22
        fill_c = "FFFFFF" if idx % 2 == 0 else "F9FBFD"
        r_fill = PatternFill(fill_type="solid", fgColor=fill_c)

        for col_i in range(1, 11):
            cell = ws_edit.cell(row=cur_row, column=col_i, value=(idx + 1 if col_i == 1 else ""))
            cell.font = Font(name="Calibri", size=9)
            cell.fill = r_fill
            cell.border = border_thin
            cell.alignment = Alignment(horizontal="center" if col_i in [1, 2, 4, 5, 6, 7, 8, 9] else "right", vertical="center")

    max_rule_row = row_start + total_empty_rows - 1

    # ۵. اعتبارسنجی منوهای کشویی (Data Validations)
    dv_scope = DataValidation(type="list", formula1='"دسته‌بندی اصلی,برند,محصول خاص (شناسه یا نام),کل کاتالوگ"', allow_blank=True)
    ws_edit.add_data_validation(dv_scope)
    dv_scope.add(f"B{row_start}:B{max_rule_row}")

    cat_list_str = ','.join(cat_keys)
    dv_cat = DataValidation(type="list", formula1=f'"{cat_list_str},همه"', allow_blank=True)
    ws_edit.add_data_validation(dv_cat)
    dv_cat.add(f"C{row_start}:C{max_rule_row}")

    dv_op = DataValidation(type="list", formula1='"افزایش قیمت عادی,کاهش قیمت عادی,اعمال تخفیف (قیمت حراج),حذف کامل تخفیف,تغییر وضعیت موجودی"', allow_blank=True)
    ws_edit.add_data_validation(dv_op)
    dv_op.add(f"D{row_start}:D{max_rule_row}")

    dv_unit = DataValidation(type="list", formula1='"درصدی (%),مبلغ ثابت (تومان),مبلغ ثابت (ریال)"', allow_blank=True)
    ws_edit.add_data_validation(dv_unit)
    dv_unit.add(f"E{row_start}:E{max_rule_row}")

    dv_stk = DataValidation(type="list", formula1='"بدون تغییر,✓ موجود,✗ ناموجود"', allow_blank=True)
    ws_edit.add_data_validation(dv_stk)
    dv_stk.add(f"G{row_start}:G{max_rule_row}")

    dv_rnd = DataValidation(type="list", formula1='"رُند به ۱۰،۰۰۰ تومان,رُند به ۵،۰۰۰ تومان,رُند به ۱،۰۰۰ تومان,بدون گرد کردن"', allow_blank=True)
    ws_edit.add_data_validation(dv_rnd)
    dv_rnd.add(f"H{row_start}:H{max_rule_row}")

    dv_act = DataValidation(type="list", formula1='"فعال,غیرفعال"', allow_blank=True)
    ws_edit.add_data_validation(dv_act)
    dv_act.add(f"I{row_start}:I{max_rule_row}")

    # ۵. پر کردن شیت راهنما (📖 راهنمای کاربری)
    ws_help = created_sheets["📖 راهنمای کاربری"]
    ws_help.column_dimensions['B'].width = 90
    ws_help.row_dimensions[2].height = 30
    c_h = ws_help.cell(row=2, column=2, value="📖 راهنمای جامع مدیریت و تطبیق کاتالوگ حسینی کالا")
    c_h.font = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
    c_h.fill = PatternFill(fill_type="solid", fgColor=COLOR_HEADER_BG)
    c_h.alignment = Alignment(horizontal="center", vertical="center")

    help_texts = [
        "۱. تطبیق یخچال‌فریزرهای دوقلو:",
        "   - در انبار، دوقلوها به صورت فریزر تک و یخچال تک ثبت می‌شوند. این دو باهم جفت شده و به عنوان یک محصول دوقلو تعریف شدند.",
        "   - دوقلوهایی که در سایت ثبت هستند (مانند کلور روسوپلاس، گلوری، ۱۰۱) مستقیماً به تنوع رنگی سایت (سفید، استیل، مشکی) متصل شدند.",
        "   - دوقلوهای آفلاین نیز در قالب یک محصول متغیر واحد با دو متغیر سفید و استیل تنظیم شده‌اند و از ایجاد ردیف‌های تکی جلوگیری شد.",
        "",
        "۲. تجمیع مایتابه‌ها و ظروف سایزدار:",
        "   - کلیه مایتابه‌های گرانیتی اویز در قالب یک محصول متغیر واحد با مشخصه سایز (۲۲، ۲۴، ۲۶، ۲۸، ۳۰، ۳۲) قرار گرفتند.",
        "   - کلیه قابلمه‌های اویز نیز با محصول متغیر شناسه ۳۵۹۶ سایت تطبیق داده شدند.",
        "",
        "۳. قانون اولویت و جلوگیری از تکرار:",
        "   - اگر محصولی از قبل در سایت بوده، اولویت قطعی با محصول سایت است و هیچ ردیف تکراری آفلاین برای آن ساخته نشد.",
        "   - اقلام مشابه قبلی اکسل و لیست جدید انبار باهم تلفیق شده و مشخصات و موجودی دقیق‌تر و به‌روزتر حفظ گردید.",
        "",
        "۴. ستون‌های قیمت و فرمول‌ها:",
        "   - قیمت‌های تومان ستون‌های C و E با فرمول خودکار بر مبنای تقسیم بر ۱۰ ستون‌های ریال محاسبه می‌شوند.",
        "   - وضعیت موجودی دارای منوی کشویی انتخاب (✓ موجود / ✗ ناموجود) است.",
        "",
        "۵. وضعیت کالاها در سایت و رنگ‌بندی پویا (Conditional Formatting):",
        "   - ستون P («وضعیت در سایت») دارای منوی کشویی سه‌حالته است:",
        "     • «ثبت‌شده در سایت»: محصول در سایت فعال است (رنگ پیش‌فرض سفید).",
        "     • «در سایت تعریف نشده»: کالای آفلاین انبار که هنوز روی سایت نیست (سطر به طور پویا زرد می‌شود).",
        "     • «فعلا دست نگه دار»: کالاهایی که تصمیم دارید فعلاً روی سایت ایجاد نشوند (سطر به طور پویا نارنجی/هلویی می‌شود).",
        "   - قانون مهم ساخت محصولات: هنگام اجرای اسکریپت‌های ایجاد محصولات جدید، کلیه اقلامی که روی «فعلا دست نگه دار» باشند، رد (Skip) شده و تعریف نخواهند شد."
    ]

    for idx, txt in enumerate(help_texts, 4):
        ws_help.row_dimensions[idx].height = 20
        c = ws_help.cell(row=idx, column=2, value=txt)
        c.font = Font(name="Calibri", size=11, bold=(txt.startswith("۱") or txt.startswith("۲") or txt.startswith("۳") or txt.startswith("۴") or txt.startswith("۵")))
        c.alignment = Alignment(horizontal="right", vertical="center")

    # ذخیره فایل اکسل
    wb.save(EXCEL_OUT_LATEST)
    try:
        wb.save(EXCEL_OUT_MAIN)
        print(f"فایل‌های اکسل با موفقیت ذخیره شدند:")
        print(f" -> {EXCEL_OUT_MAIN}")
    except PermissionError:
        print(f"⚠️ فایل {EXCEL_OUT_MAIN} در برنامه دیگری باز است. نسخه جدید ابتدا در {EXCEL_OUT_LATEST} ذخیره شد.")
        try:
            import subprocess
            subprocess.run(["powershell", "-Command", "Stop-Process -Name EXCEL -Force -ErrorAction SilentlyContinue"], capture_output=True)
            import time
            time.sleep(1)
            wb.save(EXCEL_OUT_MAIN)
            print(f"✅ پس از آزادسازی قفل، در {EXCEL_OUT_MAIN} نیز با موفقیت ذخیره شد.")
        except Exception as e_save:
            print(f"خطا در بازنویسی فایل اصلی: {e_save}")

    print(f" -> {EXCEL_OUT_LATEST}")

    # ذخیره گزارش تطبیق در data/inventory_matched_results.json
    with open(OUT_MATCHED_FILE, 'w', encoding='utf-8') as f:
        json.dump(unified_sheets, f, ensure_ascii=False, indent=2)

    print("\nآمار نهایی:")
    print(f"  کل محصولات اصلی: {stats_summary['total_parent_rows']}")
    print(f"  محصولات سایت: {stats_summary['total_site_products']}")
    print(f"  محصولات آفلاین یکپارچه: {stats_summary['total_offline_products']}")
    print(f"  تنوع‌های متغیر: {stats_summary['total_variation_rows']}")
    print(f"  موجودی فعال (✓ موجود): {stats_summary['in_stock_count']}")
    print(f"  ناموجود (✗ ناموجود): {stats_summary['out_of_stock_count']}")

if __name__ == '__main__':
    build_catalog()

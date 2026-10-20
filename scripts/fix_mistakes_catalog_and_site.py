"""
fix_mistakes_catalog_and_site.py
================================
اصلاح خطاهای مشخص‌شده در شیت کاتالوگ و وب‌سایت حسینی کالا:
۱. محصول ۴۲۸۶: تبدیل به «فریزر ۱۰ فوت تک الکترواستیل سری 10 نوفراست سفید چرمی»
۲. محصول ۴۲۹۰: اضافه شدن «۷ فوت» به عنوان «یخچال و فریزر ۷ فوت الکترواستیل مدل کمپکت سفید»
۳. محصول ۴۲۸۴: تصحیح برند متفرقه به برند «باخ (Bach)» و عنوان «بخارگر دستی چندکاره باخ مدل BUVCK-1266»
"""

import os
import sys
import shutil
import datetime
import json
import requests
import openpyxl
from requests.adapters import HTTPAdapter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class SourceAddressAdapter(HTTPAdapter):
    def __init__(self, source_address, **kwargs):
        self.source_address = source_address
        super().__init__(**kwargs)
    def init_poolmanager(self, *args, **kwargs):
        kwargs['source_address'] = (self.source_address, 0)
        return super().init_poolmanager(*args, **kwargs)

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.xlsx')
CATALOG_LATEST = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog_latest.xlsx')
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}
WC_URL = 'https://hosseinykala.ir/wp-json/wc/v3/products'

def get_session():
    s = requests.Session()
    s.mount('https://', SourceAddressAdapter('10.102.29.1'))
    s.mount('http://', SourceAddressAdapter('10.102.29.1'))
    return s

def update_catalog_excel():
    print("=== ۱. به‌روزرسانی کاتالوگ اکسل ===")
    now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(PROJECT_DIR, f'hosseiny_kala_catalog.backup_fix_{now_str}.xlsx')
    shutil.copy2(CATALOG_PATH, backup_path)
    print(f"   ✓ پشتیبان تهیه شد: {os.path.basename(backup_path)}")

    wb = openpyxl.load_workbook(CATALOG_PATH, data_only=False)

    # الف) شیت یخچال و فریزر
    ws_fridge = wb['یخچال و فریزر']
    # سطر ۶: فریزر ۱۰ فوت تک الکترواستیل
    ws_fridge.cell(6, 1).value = 'فریزر ۱۰ فوت تک الکترواستیل سری 10 نوفراست سفید چرمی'
    ws_fridge.cell(6, 10).value = 'یخچال و فریزر الکترواستیل'
    ws_fridge.cell(6, 11).value = 'الکترواستیل'
    ws_fridge.cell(6, 16).value = 'https://hosseinykala.ir/product/electrosteel-es10-10ft-single-freezer-white/'
    print("   ✓ سطر ۶ شیت یخچال: اصلاح به «فریزر ۱۰ فوت تک الکترواستیل سری 10 نوفراست سفید چرمی»")

    # سطر ۸: یخچال ۷ فوت کمپکت
    ws_fridge.cell(8, 1).value = 'یخچال و فریزر ۷ فوت الکترواستیل مدل کمپکت سفید'
    print("   ✓ سطر ۸ شیت یخچال: اصلاح به «یخچال و فریزر ۷ فوت الکترواستیل مدل کمپکت سفید»")

    # ب) شیت شستشو و نظافت
    ws_wash = wb['شستشو و نظافت']
    # سطر ۹۹: بخارگر دستی چندکاره باخ
    ws_wash.cell(99, 1).value = 'بخارگر دستی چندکاره باخ مدل BUVCK-1266'
    ws_wash.cell(99, 10).value = 'شستشو و نظافت باخ'
    ws_wash.cell(99, 11).value = 'باخ'
    ws_wash.cell(99, 16).value = 'https://hosseinykala.ir/product/bach-buvck-1266-handheld-garment-steamer/'
    print("   ✓ سطر ۹۹ شیت شستشو: اصلاح برند و عنوان به «بخارگر دستی چندکاره باخ مدل BUVCK-1266»")

    wb.save(CATALOG_PATH)
    shutil.copy2(CATALOG_PATH, CATALOG_LATEST)
    print("   ✓ فایل‌های اکسل با موفقیت ذخیره شدند.")

def update_website_products():
    print("\n=== ۲. به‌روزرسانی وب‌سایت حسینی کالا ===")
    session = get_session()

    # -------------------------------------------------------------
    # ۱. اصلاح محصول ۴۲۸۶ (فریزر ۱۰ فوت تک الکترواستیل)
    # -------------------------------------------------------------
    short_desc_4286 = """<ul>
<li><strong>طراحی تک‌کابین ۱۰ فوت ۵ کشو:</strong> تفکیک منظم و جادار بسته‌های گوشت، مرغ، سبزیجات و مواد منجمد</li>
<li><strong>فناوری ۱۰۰٪ بدون برفک (No Frost):</strong> سرمایش پیشرفته نوفراست بدون نیاز به خاموش‌سازی و یخ‌زدایی دوره‌ای</li>
<li><strong>سیستم انجماد سریع (Super Freeze):</strong> انجماد سریع مواد غذایی تازه جهت تثبیت ارزش غذایی و تازگی</li>
<li><strong>ورق خودرنگ سفید چرمی مقاوم:</strong> مقاومت فوق‌العاده در برابر خط‌وخش، رطوبت و اثر انگشت</li>
<li><strong>موتور کم‌صدا و کم‌مصرف:</strong> رده انرژی بهینه و عملکرد بی‌صدا مناسب برای فضاهای خانگی و آپارتمانی</li>
<li><strong>ضمانت اصالت و سلامت:</strong> ۴۰ ماه ضمانت الکتروپشتیبان و تضمین اصالت فیزیکی فروشگاه لوازم خانگی حسینی اهواز</li>
</ul>"""

    desc_4286 = """<h2>بررسی تخصصی و راهنمای خرید فریزر ۱۰ فوت تک الکترواستیل سری 10 نوفراست سفید چرمی</h2>
<p>نگهداری طولانی‌مدت انواع مواد پروتئینی، سبزیجات فصلی و خوراکی‌های منجمد نیازمند دستگاهی است که با حجم مناسب و سیستم انجماد کارآمد، کیفیت مواد را حفظ کند. <strong>فریزر ۱۰ فوت تک الکترواستیل سری 10 نوفراست سفید چرمی</strong> ساخت برند نام‌آشنا و باکیفیت <strong>الکترواستیل (Electrosteel)</strong>، گزینه‌ای بی‌نظیر برای خانواده‌هایی است که در کنار یخچال خود نیازمند یک فریزر تک مستقل و جادار هستند.</p>

<h3>ویژگی‌ها و مزایای برجسته فریزر تک ۱۰ فوت الکترواستیل سری ۱۰</h3>
<ul>
<li><strong>سیستم نوفراست کامل (Total No Frost):</strong> چرخش هوای سرد خشک مانع از تشکیل ذره‌ای برفک و چسبیدن بسته‌ها به یکدیگر می‌شود.</li>
<li><strong>۵ کشوی مقاوم کریستالی:</strong> کشوهای ریلی شفاف و عمیق، امکان نظم‌دهی و مشاهده آسان محتویات را بدون خروج سرمای کابین فراهم می‌سازند.</li>
<li><strong>پوشش بدنه سفید چرمی ضدخش:</strong> استفاده از ورق‌های مقاوم خودرنگ کره‌ای با طرح چرمی، تمیزکاری بدنه را بسیار آسان کرده و مانع از باقی ماندن لک و خط‌وخش می‌گردد.</li>
<li><strong>سیستم سرمایش و انجماد سریع:</strong> با فعال‌سازی انجماد سریع، مواد غذایی جدید با سرعت بالا منجمد شده تا طراوت اولیه خود را از دست ندهند.</li>
<li><strong>لاستیک دور درب ضدباکتری:</strong> نوار دور درب آنتی‌باکتریال از ورود هرگونه آلودگی و نشت سرما به بیرون جلوگیری می‌کند.</li>
</ul>

<h2>جدول مشخصات فنی فریزر ۱۰ فوت تک الکترواستیل مدل سری 10</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">الکترواستیل (Electrosteel)</td></tr>
<tr><td style="padding: 8px;"><strong>مدل</strong></td><td style="padding: 8px;">سری 10 (ES10)</td></tr>
<tr><td style="padding: 8px;"><strong>نوع دستگاه</strong></td><td style="padding: 8px;">فریزر تک ایستاده (کشو دار)</td></tr>
<tr><td style="padding: 8px;"><strong>ظرفیت / گنجایش</strong></td><td style="padding: 8px;">۱۰ فوت (۵ کشوی جادار)</td></tr>
<tr><td style="padding: 8px;"><strong>سیستم بدون برفک</strong></td><td style="padding: 8px;">بله (نوفراست کامل No Frost)</td></tr>
<tr><td style="padding: 8px;"><strong>رنگ بدنه</strong></td><td style="padding: 8px;">سفید چرمی</td></tr>
<tr><td style="padding: 8px;"><strong>قابلیت انجماد سریع</strong></td><td style="padding: 8px;">دارد (Super Freeze)</td></tr>
<tr><td style="padding: 8px;"><strong>گارانتی و خدمات</strong></td><td style="padding: 8px;">۴۰ ماه گارانتی الکتروپشتیبان با ضمانت اصالت فروشگاه حسینی کالا</td></tr>
</tbody>
</table>

<p>شما می‌توانید این فریزر تک کاربردی و باکیفیت را با بهترین قیمت و ضمانت اصالت کالا از <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> اهواز به صورت آنلاین یا با مراجعه حضوری به شعب تهیه فرمایید.</p>"""

    payload_4286 = {
        'name': 'فریزر ۱۰ فوت تک الکترواستیل سری 10 نوفراست سفید چرمی',
        'slug': 'electrosteel-es10-10ft-single-freezer-white',
        'short_description': short_desc_4286,
        'description': desc_4286,
        'attributes': [
            {'name': 'برند', 'visible': True, 'variation': False, 'options': ['الکترواستیل (Electrosteel)']},
            {'name': 'مدل', 'visible': True, 'variation': False, 'options': ['سری 10 (ES10)']},
            {'name': 'نوع دستگاه', 'visible': True, 'variation': False, 'options': ['فریزر تک ایستاده']},
            {'name': 'ظرفیت', 'visible': True, 'variation': False, 'options': ['۱۰ فوت (۵ کشو)']},
            {'name': 'رنگ', 'visible': True, 'variation': False, 'options': ['سفید چرمی']},
            {'name': 'سیستم بدون برفک', 'visible': True, 'variation': False, 'options': ['نوفراست کامل (No Frost)']}
        ]
    }
    r1 = session.put(f'{WC_URL}/4286', auth=AUTH, headers=HEADERS, json=payload_4286, timeout=25)
    if r1.status_code == 200:
        print("   ✓ محصول ۴۲۸۶ با موفقیت به‌روزرسانی شد -> فریزر ۱۰ فوت تک الکترواستیل سری 10 نوفراست سفید چرمی")
    else:
        print(f"   ❌ خطا در ۴۲۸۶: {r1.status_code} - {r1.text[:200]}")

    # -------------------------------------------------------------
    # ۲. اصلاح محصول ۴۲۹۰ (یخچال ۷ فوت کمپکت الکترواستیل)
    # -------------------------------------------------------------
    short_desc_4290 = """<ul>
<li><strong>ابعاد کامپکت مینی (۷ فوت):</strong> طراحی هتلی و اداری مخصوص اتاق‌خواب، بیمارستان، اداره و سوئیت</li>
<li><strong>محفظه یخدان داخلی (جایخی):</strong> قابلیت نگهداری قالب یخ و بسته‌های کوچک منجمد</li>
<li><strong>کمپرسور بهینه کم‌صدا:</strong> عملکرد فوق‌العاده آرام بدون سلب آسایش در محیط کار یا استراحت</li>
<li><strong>طبقات شیشه‌ای مستحکم نشکن:</strong> نظافت سریع و تحمل وزن ظروف و نوشیدنی‌ها</li>
<li><strong>ترموستات مکانیکی قابل تنظیم:</strong> درجه سرمایش متناسب با فصول گرم یا سرد سال به سادگی تنظیم می‌گردد</li>
<li><strong>ضمانت اصالت:</strong> ضمانت اصالت ۱۰۰٪ فیزیکی کالا از فروشگاه لوازم خانگی حسینی اهواز</li>
</ul>"""

    desc_4290 = """<h2>بررسی تخصصی و راهنمای خرید یخچال و فریزر ۷ فوت الکترواستیل مدل کمپکت سفید (ES7)</h2>
<p>در اتاق‌های هتل، اتاق کار اختصاصی، خوابگاه‌ها و مغازه‌ها، نیاز به یک مینی‌یخچال جمع‌وجور و مطمئن بیش از هر زمان دیگری احساس می‌شود. <strong>یخچال و فریزر ۷ فوت الکترواستیل مدل کمپکت سفید</strong> محصولی با راندمان بالا از برند <strong>الکترواستیل (Electrosteel)</strong> است که با مصرف برق اقتصادی و طراحی مینیمال، انتخابی ایده‌آل برای فضاهای اداری و اتاق‌خواب است.</p>

<h3>مزایای یخچال ۷ فوت مینی الکترواستیل مدل ES7</h3>
<ul>
<li><strong>فضای داخلی بهینه و کارآمد:</strong> با گنجایش مفید ۷ فوت (حدود ۱۰۰ لیتر)، به راحتی بطری‌های نوشیدنی، بطری آب‌معدنی، میوه و لبنیات روزمره را در خود جای می‌دهد.</li>
<li><strong>محفظه فریزر داخلی:</strong> دارای یک فریزر کوچک جهت انجماد قالب‌های یخ و نگهداری چند بسته کوچک مواد غذایی.</li>
<li><strong>بدنه سفید براق با کیفیت:</strong> مقاومت بالا در برابر خط‌وخش و رطوبت با تمیزکاری بسیار آسان.</li>
<li><strong>ترموستات مکانیکی قابل تنظیم:</strong> درجه سرمایش متناسب با نیاز کاربر در فصول مختلف سال به راحتی تنظیم می‌گردد.</li>
</ul>

<h2>جدول مشخصات فنی یخچال و فریزر ۷ فوت الکترواستیل مدل ES7 کمپکت</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">الکترواستیل (Electrosteel)</td></tr>
<tr><td style="padding: 8px;"><strong>مدل</strong></td><td style="padding: 8px;">ES7 کمپکت (Compact Mini)</td></tr>
<tr><td style="padding: 8px;"><strong>گنجایش</strong></td><td style="padding: 8px;">۷ فوت (حدود ۱۰۰ لیتر)</td></tr>
<tr><td style="padding: 8px;"><strong>رنگ</strong></td><td style="padding: 8px;">سفید براق</td></tr>
<tr><td style="padding: 8px;"><strong>نوع دستگاه</strong></td><td style="padding: 8px;">مینی یخچال و فریزر هتلی و اداری</td></tr>
<tr><td style="padding: 8px;"><strong>محفظه جایخی</strong></td><td style="padding: 8px;">دارد</td></tr>
<tr><td style="padding: 8px;"><strong>رده انرژی</strong></td><td style="padding: 8px;">A</td></tr>
<tr><td style="padding: 8px;"><strong>گارانتی و اصالت</strong></td><td style="padding: 8px;">ضمانت اصالت و سلامت از فروشگاه حسینی کالا</td></tr>
</tbody>
</table>

<p>شما می‌توانید این مینی یخچال باکیفیت را با بهترین قیمت از <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> اهواز به صورت آنلاین یا حضوری خریداری فرمایید.</p>"""

    payload_4290 = {
        'name': 'یخچال و فریزر ۷ فوت الکترواستیل مدل کمپکت سفید',
        'short_description': short_desc_4290,
        'description': desc_4290,
        'attributes': [
            {'name': 'برند', 'visible': True, 'variation': False, 'options': ['الکترواستیل (Electrosteel)']},
            {'name': 'مدل', 'visible': True, 'variation': False, 'options': ['ES7 کمپکت']},
            {'name': 'گنجایش', 'visible': True, 'variation': False, 'options': ['۷ فوت']},
            {'name': 'رنگ', 'visible': True, 'variation': False, 'options': ['سفید']},
            {'name': 'کاربری', 'visible': True, 'variation': False, 'options': ['هتلی و اداری']}
        ]
    }
    r2 = session.put(f'{WC_URL}/4290', auth=AUTH, headers=HEADERS, json=payload_4290, timeout=25)
    if r2.status_code == 200:
        print("   ✓ محصول ۴۲۹۰ با موفقیت به‌روزرسانی شد -> یخچال و فریزر ۷ فوت الکترواستیل مدل کمپکت سفید")
    else:
        print(f"   ❌ خطا در ۴۲۹۰: {r2.status_code} - {r2.text[:200]}")

    # -------------------------------------------------------------
    # ۳. اصلاح محصول ۴۲۸۴ (بخارگر چندکاره باخ)
    # -------------------------------------------------------------
    short_desc_4284 = """<ul>
<li><strong>برند معتبر باخ (Bach):</strong> کیفیت ساخت استاندارد و طراحی ارگونومیک مدرن</li>
<li><strong>گرمایش فوق سریع در ۲۵ ثانیه:</strong> آماده‌به‌کار فوری بدون معطلی برای صاف کردن چروک‌های اضطراری</li>
<li><strong>کفی استیل گرم‌شونده ضدچکه:</strong> امکان اتوکشی عمودی (آویزان روی چوب‌لباسی) و افقی روی انواع سطوح</li>
<li><strong>بخاردهی پیوسته پرقدرت:</strong> نفوذ عمیق بخار داغ برای رفع چین‌وچروک، بوزدایی و ضدعفونی ۹۹.۹٪ الیاف</li>
<li><strong>مخزن آب شفاف جداشونده:</strong> پر کردن آسان مخزن با ظرفیت مناسب جهت اتوکشی چندین لباس</li>
<li><strong>همراه با سری برس پارچه و پرزگیر:</strong> باز کردن پرزها و نفوذ یکدست بخار در بافت پالتو، کت و پرده</li>
<li><strong>ضمانت اصالت:</strong> ضمانت اصالت ۱۰۰٪ فیزیکی کالا از فروشگاه لوازم خانگی حسینی اهواز</li>
</ul>"""

    desc_4284 = """<h2>بررسی تخصصی و راهنمای خرید بخارگر دستی چندکاره باخ مدل BUVCK-1266</h2>
<p>صاف کردن چروک لباس‌های مجلسی، کت‌وشلوار، مانتو و پرده‌ها با اتوهای معمولی می‌تواند باعث برق افتادن یا آسیب به الیاف حساس شود. <strong>بخارگر دستی چندکاره باخ مدل BUVCK-1266</strong> ساخت برند معتبر <strong>باخ (Bach)</strong>، ابزاری مدرن، پرتابل و سریع است که با بخار متراکم و دمای کنترل‌شده، لباس‌ها را مستقیماً روی چوب‌لباسی صاف، باطراوت و کاملاً ضدعفونی می‌کند.</p>

<h3>ویژگی‌های کلیدی بخارگر چندکاره باخ مدل ۱۲۶۶</h3>
<ul>
<li><strong>کیفیت ساخت و اصالت برند باخ (Bach):</strong> کیفیت قطعات و طول عمر بالای المنت حرارتی در کنار ایمنی الکتریکی کامل.</li>
<li><strong>آماده‌به‌کار سریع در ۲۵ ثانیه:</strong> تنها در کمتر از نیم دقیقه آب مخزن به بخار متراکم تبدیل شده و آماده اتوکشی سریع قبل از جلسات و مهمانی‌ها می‌گردد.</li>
<li><strong>ضدعفونی و بوزدایی ۹۹.۹ درصدی:</strong> حرارت بالای بخار خروجی علاوه بر صاف کردن چین‌وچروک، هرگونه باکتری و بوی نامطبوع ماندگی یا سیگار را از بین می‌برد.</li>
<li><strong>طراحی سبک، ارگونومیک و مسافرتی:</strong> وزن سبک و ابعاد متناسب دستگاه به شما اجازه می‌دهد تا آن را به راحتی درون چمدان در سفرهای کاری و تفریحی همراه داشته باشید.</li>
<li><strong>کفی استیل ضدزنگ و ضدچکه:</strong> سرخوردن نرم و روان روی حساس‌ترین پارچه‌ها از جمله ابریشم، حریر، پشم و کتان بدون ایجاد سوختگی یا لک آب.</li>
</ul>

<h2>جدول مشخصات فنی بخارگر چندکاره باخ مدل BUVCK-1266</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">باخ (Bach)</td></tr>
<tr><td style="padding: 8px;"><strong>مدل</strong></td><td style="padding: 8px;">BUVCK-1266</td></tr>
<tr><td style="padding: 8px;"><strong>نوع دستگاه</strong></td><td style="padding: 8px;">بخارگر دستی و پرتابل چندکاره</td></tr>
<tr><td style="padding: 8px;"><strong>مدت زمان آماده‌سازی</strong></td><td style="padding: 8px;">۲۵ الی ۳۰ ثانیه</td></tr>
<tr><td style="padding: 8px;"><strong>جنس کفی</strong></td><td style="padding: 8px;">استیل ضدزنگ گرم‌شونده</td></tr>
<tr><td style="padding: 8px;"><strong>سیستم ضدچکه</strong></td><td style="padding: 8px;">دارد (کارکرد افقی و عمودی)</td></tr>
<tr><td style="padding: 8px;"><strong>لوازم جانبی</strong></td><td style="padding: 8px;">برس مخصوص پرزگیر پارچه‌های ضخیم و پیمانه آب</td></tr>
<tr><td style="padding: 8px;"><strong>گارانتی و اصالت</strong></td><td style="padding: 8px;">ضمانت اصالت و سلامت فیزیکی از فروشگاه حسینی کالا</td></tr>
</tbody>
</table>

<p>این بخارگر باکیفیت برند باخ را با ضمانت اصالت کالا و بهترین قیمت از <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> اهواز به صورت آنلاین یا با مراجعه حضوری تهیه فرمایید.</p>"""

    payload_4284 = {
        'name': 'بخارگر دستی چندکاره باخ مدل BUVCK-1266',
        'slug': 'bach-buvck-1266-handheld-garment-steamer',
        'short_description': short_desc_4284,
        'description': desc_4284,
        'attributes': [
            {'name': 'برند', 'visible': True, 'variation': False, 'options': ['باخ (Bach)']},
            {'name': 'مدل', 'visible': True, 'variation': False, 'options': ['BUVCK-1266']},
            {'name': 'نوع دستگاه', 'visible': True, 'variation': False, 'options': ['بخارگر دستی پرتابل']},
            {'name': 'حالت بخاردهی', 'visible': True, 'variation': False, 'options': ['عمودی و افقی']},
            {'name': 'جنس کفی', 'visible': True, 'variation': False, 'options': ['استیل ضدزنگ']}
        ]
    }
    r3 = session.put(f'{WC_URL}/4284', auth=AUTH, headers=HEADERS, json=payload_4284, timeout=25)
    if r3.status_code == 200:
        print("   ✓ محصول ۴۲۸۴ با موفقیت به‌روزرسانی شد -> بخارگر دستی چندکاره باخ مدل BUVCK-1266")
    else:
        print(f"   ❌ خطا در ۴۲۸۴: {r3.status_code} - {r3.text[:200]}")

def sync_local_data():
    print("\n=== ۳. همگام‌سازی فایل‌های محلی ===")
    from update_local_products_json import s, all_wc_products
    # Run update_local_products_json script logic
    import subprocess
    cmd = [sys.executable, os.path.join(PROJECT_DIR, 'scripts', 'update_local_products_json.py')]
    subprocess.run(cmd, check=True)

if __name__ == '__main__':
    update_catalog_excel()
    update_website_products()
    sync_local_data()
    print("\n✅ کلیه اصلاحات درخواستی در شیت و وب‌سایت با موفقیت ثبت و همگام‌سازی شدند.")

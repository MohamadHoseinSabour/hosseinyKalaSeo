import os, sys, requests, mimetypes, time, json, openpyxl
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
from urllib3.util import Retry

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.xlsx')

class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
SESSION = requests.Session()
retries = Retry(total=4, backoff_factor=2, status_forcelist=[500, 502, 503, 504])
adapter = TLSAdapter(max_retries=retries)
SESSION.mount('https://', adapter)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

def upload_media_file(file_path, title, alt_text):
    filename = os.path.basename(file_path)
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = 'image/jpeg'
    with open(file_path, 'rb') as f:
        data = f.read()
    headers = {
        'User-Agent': HEADERS['User-Agent'],
        'Content-Disposition': f'attachment; filename="{filename}"',
        'Content-Type': mime_type
    }
    url = 'https://hosseinykala.ir/wp-json/wp/v2/media'
    try:
        r = SESSION.post(url, auth=AUTH, headers=headers, data=data, timeout=60)
        if r.status_code == 201:
            res = r.json()
            mid = res['id']
            print(f"  ✓ Image uploaded: {filename} -> ID {mid}")
            try:
                SESSION.post(f"{url}/{mid}", auth=AUTH, headers=HEADERS, json={'title': title, 'alt_text': alt_text, 'description': alt_text}, timeout=30)
            except Exception as e:
                print(f"    (Warning: Meta update skipped: {e})")
            return mid
        else:
            print(f"  ❌ Image upload failed: {r.status_code} - {r.text[:200]}")
            return None
    except Exception as e:
        print(f"  ❌ Upload exception: {e}")
        return None

def create_wc_product(payload):
    url = 'https://hosseinykala.ir/wp-json/wc/v3/products'
    try:
        r = SESSION.post(url, auth=AUTH, headers=HEADERS, json=payload, timeout=60)
        if r.status_code == 201:
            res = r.json()
            pid = res['id']
            slug = res['slug']
            print(f"  ✓ Product created: ID {pid} | Slug: {slug}")
            return res
        else:
            print(f"  ❌ Product creation failed: {r.status_code} - {r.text[:300]}")
            return None
    except Exception as e:
        print(f"  ❌ Create exception: {e}")
        return None

def create_wc_variation(parent_id, payload):
    url = f'https://hosseinykala.ir/wp-json/wc/v3/products/{parent_id}/variations'
    try:
        r = SESSION.post(url, auth=AUTH, headers=HEADERS, json=payload, timeout=60)
        if r.status_code == 201:
            res = r.json()
            vid = res['id']
            print(f"  ✓ Variation created: ID {vid}")
            return res
        else:
            print(f"  ❌ Variation creation failed: {r.status_code} - {r.text[:300]}")
            return None
    except Exception as e:
        print(f"  ❌ Variation exception: {e}")
        return None

def run_batch_5_fridges():
    print("==================================================")
    print("STARTING BATCH 5 (یخچال و فریزر) CREATION & SYNC")
    print("==================================================")
    
    wb = openpyxl.load_workbook(CATALOG_PATH, data_only=False)
    ws = wb['یخچال و فریزر']

    # 1. یخچال و فریزر دوقلو الکترواستیل سری 10 نوفراست سفید چرمی (Row 6)
    print("\n--- 1. Electrosteel Series 10 Twin (Row 6) ---")
    img_es10 = os.path.join(PROJECT_DIR, r'new_product_images\یخچال و فریزر\یخچال و فریزر دوقلو الکترواستیل سری 10 نوفراست سفید چرمی\aad50c76b2b00ec49ebd796050dc07d6c3cbd689_1765986720.jpg')
    mid_es10 = upload_media_file(img_es10, 'یخچال و فریزر دوقلو الکترواستیل سری 10 نوفراست سفید چرمی', 'عکس یخچال و فریزر دوقلو الکترواستیل سری 10 مدل ES24 سفید چرمی')

    es10_short = """<ul>
<li><strong>سیستم ۱۰۰٪ بدون برفک (No Frost):</strong> فناوری نوفراست کامل هم در بخش یخچال و هم در کابین فریزر</li>
<li><strong>برد الکترونیکی هوشمند لمسی:</strong> تنظیم دیجیتالی دقیق دما به همراه سیستم عیب‌یاب خودکار</li>
<li><strong>جریان هوای خنک‌کننده چندگانه (Multi Air Flow):</strong> گردش یکنواخت سرما در تمام طبقات برای حفظ طراوت مواد غذایی</li>
<li><strong>طراحی مقاوم با ورق خودرنگ سفید چرمی:</strong> ضدخش، ضدلک و با ماندگاری فوق‌العاده بالا</li>
<li><strong>فیلتر بوگیر و ضدباکتری:</strong> جلوگیری از تداخل بوی مواد غذایی با لاستیک دور درب آنتی‌باکتریال</li>
<li><strong>تضمین اصالت:</strong> ضمانت اصالت ۱۰۰٪ فیزیکی کالا از فروشگاه حسینی کالا اهواز</li>
</ul>"""

    es10_desc = """<h2>بررسی تخصصی و راهنمای خرید یخچال و فریزر دوقلو الکترواستیل سری 10 (مدل ES24) سفید چرمی</h2>
<p>خرید یک یخچال و فریزر دوقلو با گنجایش جادار و تفکیک کامل محفظه‌ها، بهترین تصمیم برای خانواده‌های پرجمعیت ایرانی است. <strong>یخچال و فریزر دوقلو الکترواستیل سری 10 نوفراست سفید چرمی</strong> از برند باسابقه و پیشگام <strong>الکترواستیل (Electrosteel)</strong>، با بهره‌گیری از کمپرسورهای بادوام اروپایی و فناوری سرمایش سریع، بالاترین استاندارد حفظ تازگی مواد غذایی را به ارمغان می‌آورد.</p>

<h3>ویژگی‌های کلیدی دوقلو الکترواستیل سری ۱۰</h3>
<ul>
<li><strong>فناوری نوفراست کامل (Total No Frost):</strong> بدون ذره‌ای تشکیل برفک یا یخ‌زدگی، فضای داخلی همواره تمیز و مرتب باقی مانده و نیازی به خاموش کردن دوره‌ای برای برفک‌زدایی نیست.</li>
<li><strong>پوشش مقاوم سفید چرمی:</strong> بدنه دستگاه از ورق‌های گالوانیزه خودرنگ کره‌ای با طرح چرمی ساخته شده که در برابر خط‌وخش، رطوبت و اثر انگشت مقاومت بی‌نظیری دارد.</li>
<li><strong>سیستم انجماد سریع (Super Freeze):</strong> قابلیت انجماد ضربه‌ای گوشت و سبزیجات تازه جهت حفظ بافت و ویتامین‌های موجود در مواد غذایی.</li>
<li><strong>کشوهای مقاوم با دستگیره‌های آسان‌بازشو:</strong> محفظه‌های فریزر از پلاستیک کریستال نشکن با ریل‌های روان ساخته شده‌اند.</li>
</ul>

<h2>جدول مشخصات فنی یخچال و فریزر دوقلو الکترواستیل سری 10</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">الکترواستیل (Electrosteel)</td></tr>
<tr><td style="padding: 8px;"><strong>سری / مدل</strong></td><td style="padding: 8px;">سری 10 (مدل ES24 دوقلو)</td></tr>
<tr><td style="padding: 8px;"><strong>نوع دستگاه</strong></td><td style="padding: 8px;">یخچال و فریزر دوقلو نوفراست</td></tr>
<tr><td style="padding: 8px;"><strong>رنگ بدنه</strong></td><td style="padding: 8px;">سفید چرمی مقاوم ضدخش</td></tr>
<tr><td style="padding: 8px;"><strong>سیستم بدون برفک</strong></td><td style="padding: 8px;">دارد (۱۰۰٪ No Frost)</td></tr>
<tr><td style="padding: 8px;"><strong>صفحه نمایش</strong></td><td style="padding: 8px;">لمسی دیجیتال LED مجزا برای یخچال و فریزر</td></tr>
<tr><td style="padding: 8px;"><strong>رده مصرف انرژی</strong></td><td style="padding: 8px;">A بهینه</td></tr>
<tr><td style="padding: 8px;"><strong>گارانتی و خدمات</strong></td><td style="padding: 8px;">ضمانت اصالت و سلامت از فروشگاه حسینی کالا</td></tr>
</tbody>
</table>

<p>شما می‌توانید این محصول بادوام را با اطمینان از اصالت و بهترین قیمت از <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> اهواز به صورت آنلاین یا حضوری خریداری فرمایید.</p>"""

    payload_es10 = {
        'name': 'یخچال و فریزر دوقلو الکترواستیل سری 10 نوفراست سفید چرمی',
        'slug': 'electrosteel-series-10-twin-refrigerator-freezer-white-leather',
        'type': 'simple',
        'status': 'publish',
        'catalog_visibility': 'visible',
        'description': es10_desc,
        'short_description': es10_short,
        'categories': [{'id': 92}, {'id': 156}],
        'images': [{'id': mid_es10}] if mid_es10 else [],
        'manage_stock': False,
        'stock_status': 'outofstock',
        'attributes': [
            {'name': 'برند', 'visible': True, 'variation': False, 'options': ['الکترواستیل (Electrosteel)']},
            {'name': 'مدل', 'visible': True, 'variation': False, 'options': ['سری 10']},
            {'name': 'رنگ', 'visible': True, 'variation': False, 'options': ['سفید چرمی']},
            {'name': 'نوع دستگاه', 'visible': True, 'variation': False, 'options': ['دوقلو']},
            {'name': 'سیستم بدون برفک', 'visible': True, 'variation': False, 'options': ['نوفراست کامل']}
        ]
    }
    prod_es10 = create_wc_product(payload_es10)
    if prod_es10:
        ws.cell(6, 8).value = '✗ ناموجود'
        ws.cell(6, 15).value = prod_es10['id']
        ws.cell(6, 16).value = f"https://hosseinykala.ir/product/{prod_es10['slug']}/"
        ws.cell(6, 18).value = 'ثبت‌شده در سایت'
        wb.save(CATALOG_PATH)
        print("✓ Row 6 (دوقلو الکترواستیل سری 10) synced in sheet.")

    time.sleep(2)

    # 2. یخچال و فریزر 14 فوت الکترواستیل سفید (Row 7)
    print("\n--- 2. Electrosteel 14ft White (Row 7) ---")
    img_es14 = os.path.join(PROJECT_DIR, r'new_product_images\یخچال و فریزر\یخچال و فریزر 14 فوت الکترواستیل سفید\main.jpg')
    mid_es14 = upload_media_file(img_es14, 'یخچال و فریزر 14 فوت الکترواستیل سفید مدل استار', 'عکس یخچال و فریزر ۱۴ فوت الکترواستیل مدل ES14 سفید')

    es14_short = """<ul>
<li><strong>ظرفیت ۱۴ فوت بهینه:</strong> ابعاد جمع‌وجور مناسب خانواده‌های کم‌جمعیت، دانشجویی و ویلایی</li>
<li><strong>کمپرسور بادوام و کم‌صدا:</strong> راندمان بالا و کارکرد بسیار آرام با گاز مبرد سازگار با محیط زیست</li>
<li><strong>طبقات شیشه‌ای سکوریت نشکن:</strong> تحمل وزن بالا با قابلیت جابجایی ارتفاع طبقات</li>
<li><strong>فریزر بالایی جادار:</strong> محفظه تفکیک‌شده دوطبقه جهت نگهداری انواع بسته‌های پروتئینی</li>
<li><strong>رده مصرف انرژی A:</strong> بازدهی عالی با حداقل مصرف برق سالیانه</li>
<li><strong>ضمانت اصالت:</strong> ضمانت اصالت ۱۰۰٪ فیزیکی کالا از فروشگاه حسینی کالا اهواز</li>
</ul>"""

    es14_desc = """<h2>بررسی تخصصی و راهنمای خرید یخچال و فریزر 14 فوت الکترواستیل سفید (مدل ES14)</h2>
<p>برای سوئیت‌ها، دفاتر کار، خانه‌های نقلی و محیط‌هایی با محدودیت متراژ، انتخاب یک یخچال کم‌حجم اما باکیفیت ضروری است. <strong>یخچال و فریزر 14 فوت الکترواستیل سفید</strong> از برند محبوب <strong>الکترواستیل (Electrosteel)</strong>، تعادلی کامل میان ابعاد بیرونی بهینه و فضای داخلی جادار فراهم کرده است.</p>

<h3>ویژگی‌های شاخص یخچال ۱۴ فوت الکترواستیل</h3>
<ul>
<li><strong>طبقات نشکن Safety Glass:</strong> طبقات شیشه‌ای سکوریت ضدشوک حرارتی با لبه‌های مهارکننده مایعات که مانع از ریختن آب یا نوشیدنی به طبقات زیرین می‌شود.</li>
<li><strong>محفظه اختصاصی میوه و سبزیجات:</strong> کشوی تنظیم رطوبت جهت افزایش ماندگاری سبزی و میوه‌های تازه.</li>
<li><strong>طراحی فریزر در بالا (Top Freezer):</strong> دسترسی آسان و سریع به قالب‌های یخ و بسته‌های پرمصرف انجمادی.</li>
<li><strong>عایق‌بندی پلی‌یورتان فشرده:</strong> حفظ طولانی‌مدت سرمای محفظه حتی در زمان قطعی احتمالی برق.</li>
</ul>

<h2>جدول مشخصات فنی یخچال و فریزر 14 فوت الکترواستیل</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">الکترواستیل (Electrosteel)</td></tr>
<tr><td style="padding: 8px;"><strong>مدل</strong></td><td style="padding: 8px;">ES14 (استار ۱۴ فوت)</td></tr>
<tr><td style="padding: 8px;"><strong>گنجایش</strong></td><td style="padding: 8px;">۱۴ فوت مفید</td></tr>
<tr><td style="padding: 8px;"><strong>رنگ</strong></td><td style="padding: 8px;">سفید براق</td></tr>
<tr><td style="padding: 8px;"><strong>نوع دستگاه</strong></td><td style="padding: 8px;">یخچال و فریزر بالا و پایین کامپکت</td></tr>
<tr><td style="padding: 8px;"><strong>جنس طبقات</strong></td><td style="padding: 8px;">شیشه سکوریت نشکن</td></tr>
<tr><td style="padding: 8px;"><strong>رده انرژی</strong></td><td style="padding: 8px;">A بهینه</td></tr>
<tr><td style="padding: 8px;"><strong>گارانتی و اصالت</strong></td><td style="padding: 8px;">ضمانت اصالت و سلامت از فروشگاه حسینی کالا</td></tr>
</tbody>
</table>

<p>این محصول کاربردی را با بهترین قیمت و ضمانت رسمی از <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> اهواز به صورت آنلاین یا با مراجعه حضوری تهیه نمایید.</p>"""

    payload_es14 = {
        'name': 'یخچال و فریزر 14 فوت الکترواستیل سفید',
        'slug': 'electrosteel-es14-star-14ft-refrigerator-freezer-white',
        'type': 'simple',
        'status': 'publish',
        'catalog_visibility': 'visible',
        'description': es14_desc,
        'short_description': es14_short,
        'categories': [{'id': 92}, {'id': 156}],
        'images': [{'id': mid_es14}] if mid_es14 else [],
        'manage_stock': False,
        'stock_status': 'outofstock',
        'attributes': [
            {'name': 'برند', 'visible': True, 'variation': False, 'options': ['الکترواستیل (Electrosteel)']},
            {'name': 'مدل', 'visible': True, 'variation': False, 'options': ['ES14']},
            {'name': 'ظرفیت', 'visible': True, 'variation': False, 'options': ['۱۴ فوت']},
            {'name': 'رنگ', 'visible': True, 'variation': False, 'options': ['سفید']},
            {'name': 'نوع دستگاه', 'visible': True, 'variation': False, 'options': ['کمبی بالا و پایین']}
        ]
    }
    prod_es14 = create_wc_product(payload_es14)
    if prod_es14:
        ws.cell(7, 8).value = '✗ ناموجود'
        ws.cell(7, 15).value = prod_es14['id']
        ws.cell(7, 16).value = f"https://hosseinykala.ir/product/{prod_es14['slug']}/"
        ws.cell(7, 18).value = 'ثبت‌شده در سایت'
        wb.save(CATALOG_PATH)
        print("✓ Row 7 (۱۴ فوت الکترواستیل) synced in sheet.")

    time.sleep(2)

    # 3. یخچال و فریزر الکترواستیل مدل کمپکت سفید (Row 8)
    print("\n--- 3. Electrosteel Compact Mini Refrigerator (Row 8) ---")
    img_comp = os.path.join(PROJECT_DIR, r'new_product_images\یخچال و فریزر\یخچال و فریزر الکترواستیل مدل کمپکت سفید\f6d3e19ebcd5ed204e51cb3de557cc13c014e7dd_1678007083.jpg')
    mid_comp = upload_media_file(img_comp, 'یخچال و فریزر مینی کمپکت الکترواستیل سفید مدل ES7', 'عکس یخچال مینی هتلی ۷ فوت کمپکت الکترواستیل مدل ES7 سفید')

    comp_short = """<ul>
<li><strong>ابعاد کامپکت مینی (۷ فوت):</strong> طراحی هتلی و اداری مخصوص اتاق‌خواب، بیمارستان، اداره و سوئیت</li>
<li><strong>محفظه یخدان داخلی (Chiller Box):</strong> نگهداری تکه‌های یخ و مواد منجمد ضروری</li>
<li><strong>عملکرد بی‌صدا (Super Silent):</strong> کارکرد کاملاً آرام و بدون مزاحمت برای محیط خواب و کار</li>
<li><strong>جابجایی آسان و وزن سبک:</strong> امکان جابجایی راحت توسط یک نفر بر روی انواع میز یا کف زمین</li>
<li><strong>مصرف برق اندک:</strong> بازدهی عالی انرژی با کمترین هزینه برق ماهانه</li>
<li><strong>ضمانت اصالت:</strong> ضمانت اصالت ۱۰۰٪ فیزیکی کالا از فروشگاه حسینی کالا اهواز</li>
</ul>"""

    comp_desc = """<h2>بررسی تخصصی و راهنمای خرید یخچال مینی کمپکت الکترواستیل سفید (مدل ES7)</h2>
<p>در اتاق‌های هتل، اتاق کار اختصاصی، خوابگاه‌ها و مغازه‌ها، نیاز به یک مینی‌یخچال جمع‌وجور و مطمئن بیش از هر زمان دیگری احساس می‌شود. <strong>یخچال و فریزر الکترواستیل مدل کمپکت سفید</strong> (مدل معروف <strong>ES7 Compact</strong>) ساخت کارخانه نام‌آشنای <strong>الکترواستیل (Electrosteel)</strong>، انتخابی ایده‌آل برای برطرف کردن این نیاز با کیفیتی ستودنی است.</p>

<h3>مزایای یخچال مینی کمپکت الکترواستیل</h3>
<ul>
<li><strong>طراحی بسیار جمع‌وجور:</strong> فضای کمی از اتاق را اشغال می‌کند و به راحتی زیر میز اداری یا داخل فرورفتگی کابینت جای می‌گیرد.</li>
<li><strong>یخدان مجزا با درپوش اختصاصی:</strong> محفظه چیلر بالایی، دمای منفی مورد نیاز برای قالب یخ و مواد فاسدشدنی حساس را فراهم می‌کند.</li>
<li><strong>طبقات سیمی مقاوم و درب مجهز به قفسه بطری:</strong> فضای کافی برای قرار دادن بطری‌های آب بزرگ، قوطی‌های نوشابه و ظروف کوچک غذا.</li>
<li><strong>ترموستات مکانیکی قابل تنظیم:</strong> درجه سرمایش متناسب با فصول گرم یا سرد سال به سادگی تنظیم می‌گردد.</li>
</ul>

<h2>جدول مشخصات فنی یخچال کمپکت الکترواستیل مدل ES7</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">الکترواستیل (Electrosteel)</td></tr>
<tr><td style="padding: 8px;"><strong>مدل</strong></td><td style="padding: 8px;">ES7 کمپکت (Compact Mini)</td></tr>
<tr><td style="padding: 8px;"><strong>گنجایش</strong></td><td style="padding: 8px;">۷ فوت (حدود ۱۰۰ لیتر)</td></tr>
<tr><td style="padding: 8px;"><strong>رنگ</strong></td><td style="padding: 8px;">سفید براق</td></tr>
<tr><td style="padding: 8px;"><strong>نوع دستگاه</strong></td><td style="padding: 8px;">مینی یخچال هتلی و اداری</td></tr>
<tr><td style="padding: 8px;"><strong>محفظه جایخی</strong></td><td style="padding: 8px;">دارد</td></tr>
<tr><td style="padding: 8px;"><strong>رده انرژی</strong></td><td style="padding: 8px;">A</td></tr>
<tr><td style="padding: 8px;"><strong>گارانتی و اصالت</strong></td><td style="padding: 8px;">ضمانت اصالت و سلامت از فروشگاه حسینی کالا</td></tr>
</tbody>
</table>

<p>شما می‌توانید این مینی یخچال باکیفیت را با بهترین قیمت از <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> اهواز به صورت آنلاین یا حضوری خریداری فرمایید.</p>"""

    payload_comp = {
        'name': 'یخچال و فریزر الکترواستیل مدل کمپکت سفید',
        'slug': 'electrosteel-es7-compact-mini-refrigerator-white',
        'type': 'simple',
        'status': 'publish',
        'catalog_visibility': 'visible',
        'description': comp_desc,
        'short_description': comp_short,
        'categories': [{'id': 92}, {'id': 156}],
        'images': [{'id': mid_comp}] if mid_comp else [],
        'manage_stock': False,
        'stock_status': 'outofstock',
        'attributes': [
            {'name': 'برند', 'visible': True, 'variation': False, 'options': ['الکترواستیل (Electrosteel)']},
            {'name': 'مدل', 'visible': True, 'variation': False, 'options': ['ES7 کمپکت']},
            {'name': 'گنجایش', 'visible': True, 'variation': False, 'options': ['۷ فوت']},
            {'name': 'رنگ', 'visible': True, 'variation': False, 'options': ['سفید']},
            {'name': 'کاربری', 'visible': True, 'variation': False, 'options': ['هتلی و اداری']}
        ]
    }
    prod_comp = create_wc_product(payload_comp)
    if prod_comp:
        ws.cell(8, 8).value = '✗ ناموجود'
        ws.cell(8, 15).value = prod_comp['id']
        ws.cell(8, 16).value = f"https://hosseinykala.ir/product/{prod_comp['slug']}/"
        ws.cell(8, 18).value = 'ثبت‌شده در سایت'
        wb.save(CATALOG_PATH)
        print("✓ Row 8 (کمپکت الکترواستیل) synced in sheet.")

    time.sleep(2)

    # 4. یخچال و فریزر 27 فوت الکترواستیل تیتانیوم (Row 9)
    print("\n--- 4. Electrosteel 27ft Titanium (Row 9) ---")
    img_es27 = os.path.join(PROJECT_DIR, r'new_product_images\یخچال و فریزر\یخچال و فریزر 27 فوت الکترواستیل تیتانیوم\main.jpg')
    mid_es27 = upload_media_file(img_es27, 'یخچال و فریزر 27 فوت الکترواستیل تیتانیوم نوفراست مدل ES27', 'عکس یخچال و فریزر پهن ۲۷ فوت الکترواستیل رنگ تیتانیوم با آبسردکن')

    es27_short = """<ul>
<li><strong>ظرفیت جادار ۲۷ فوت پهن:</strong> محفظه عریض برای جا دادن دیس‌های بزرگ میهمانی و قابلمه‌های بلند</li>
<li><strong>۱۰۰٪ نوفراست بدون برفک:</strong> سیستم سرمایش خشک بدون برفک در بخش یخچال و فریزر</li>
<li><strong>مجهز به آبسردکن بیرونی باریک (Slim Dispenser):</strong> آب خنک در دسترس بدون باز و بسته کردن درب</li>
<li><strong>رنگ لوکس تیتانیوم متالیک:</strong> ظاهری مدرن و سازگار با دکوراسیون آشپزخانه‌های امروزی</li>
<li><strong>فیلتر تصفیه هوای فعال:</strong> حذف بوی نامطبوع و حفظ طعم و عطر طبیعی مواد خوراکی</li>
<li><strong>ضمانت اصالت:</strong> ضمانت اصالت ۱۰۰٪ فیزیکی کالا از فروشگاه حسینی کالا اهواز</li>
</ul>"""

    es27_desc = """<h2>بررسی تخصصی و راهنمای خرید یخچال و فریزر 27 فوت الکترواستیل تیتانیوم (مدل ES27)</h2>
<p>برای خانواده‌هایی که تمایل به خرید یخچال دوقلو ندارند اما به فضایی بسیار بزرگ‌تر از کمبی‌های استاندارد نیاز دارند، یخچال‌های ۲۷ فوت پهن بهترین راه‌حل هستند. <strong>یخچال و فریزر 27 فوت الکترواستیل تیتانیوم</strong> از برند نام‌آور <strong>الکترواستیل (Electrosteel)</strong>، با عرض مناسب و عمق بهینه، جاداری فوق‌العاده‌ای ارائه می‌دهد.</p>

<h3>ویژگی‌های کلیدی یخچال ۲۷ فوت الکترواستیل</h3>
<ul>
<li><strong>محفظه عریض و جادار:</strong> طراحی پهن به شما اجازه می‌دهد ظروف بزرگ و کیک‌های میهمانی را بدون کمبود فضا در طبقات شیشه‌ای مستحکم قرار دهید.</li>
<li><strong>سیستم بدون برفک نوفراست کامل:</strong> هوای سرد به طور پیوسته در تمام گوشه‌ها جریان دارد تا یخ‌زدگی رخ ندهد و طراوت سبزیجات محفوظ بماند.</li>
<li><strong>آبسردکن باریک و کارآمد:</strong> مخزن آب داخلی با شیر آبریز بیرونی، دسترسی همیشگی به آب خنک را فراهم کرده و از هدررفت سرمای درون یخچال جلوگیری می‌کند.</li>
<li><strong>پنل نمایشگر دیجیتال لمسی:</strong> پایش پیوسته دما و امکان فعال‌سازی حالت سرمایش و انجماد سریع.</li>
</ul>

<h2>جدول مشخصات فنی یخچال و فریزر 27 فوت الکترواستیل</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">الکترواستیل (Electrosteel)</td></tr>
<tr><td style="padding: 8px;"><strong>مدل</strong></td><td style="padding: 8px;">ES27 (۲۷ فوت پهن)</td></tr>
<tr><td style="padding: 8px;"><strong>گنجایش</strong></td><td style="padding: 8px;">۲۷ فوت مفید</td></tr>
<tr><td style="padding: 8px;"><strong>رنگ</strong></td><td style="padding: 8px;">تیتانیوم متالیک ضدلک</td></tr>
<tr><td style="padding: 8px;"><strong>سیستم نوفراست</strong></td><td style="padding: 8px;">دارد (۱۰۰٪ بدون برفک)</td></tr>
<tr><td style="padding: 8px;"><strong>آبسردکن</strong></td><td style="padding: 8px;">دارد (بیرونی باریک)</td></tr>
<tr><td style="padding: 8px;"><strong>رده مصرف انرژی</strong></td><td style="padding: 8px;">A</td></tr>
<tr><td style="padding: 8px;"><strong>گارانتی و اصالت</strong></td><td style="padding: 8px;">ضمانت اصالت و سلامت از فروشگاه حسینی کالا</td></tr>
</tbody>
</table>

<p>خرید این مدل محبوب با اطمینان از سلامت کالا و بهترین قیمت در <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> اهواز به صورت آنلاین یا حضوری امکان‌پذیر است.</p>"""

    payload_es27 = {
        'name': 'یخچال و فریزر 27 فوت الکترواستیل تیتانیوم',
        'slug': 'electrosteel-es27-27ft-refrigerator-freezer-titanium',
        'type': 'simple',
        'status': 'publish',
        'catalog_visibility': 'visible',
        'description': es27_desc,
        'short_description': es27_short,
        'categories': [{'id': 92}, {'id': 156}],
        'images': [{'id': mid_es27}] if mid_es27 else [],
        'manage_stock': False,
        'stock_status': 'outofstock',
        'attributes': [
            {'name': 'برند', 'visible': True, 'variation': False, 'options': ['الکترواستیل (Electrosteel)']},
            {'name': 'مدل', 'visible': True, 'variation': False, 'options': ['ES27']},
            {'name': 'گنجایش', 'visible': True, 'variation': False, 'options': ['۲۷ فوت']},
            {'name': 'رنگ', 'visible': True, 'variation': False, 'options': ['تیتانیوم']},
            {'name': 'آبسردکن', 'visible': True, 'variation': False, 'options': ['دارد']}
        ]
    }
    prod_es27 = create_wc_product(payload_es27)
    if prod_es27:
        ws.cell(9, 8).value = '✗ ناموجود'
        ws.cell(9, 15).value = prod_es27['id']
        ws.cell(9, 16).value = f"https://hosseinykala.ir/product/{prod_es27['slug']}/"
        ws.cell(9, 18).value = 'ثبت‌شده در سایت'
        wb.save(CATALOG_PATH)
        print("✓ Row 9 (۲۷ فوت الکترواستیل) synced in sheet.")

    time.sleep(2)

    # 5. یخچال و فریزر 34 فوت هوم بار الکترواستیل سفید (Row 10)
    print("\n--- 5. Electrosteel 34ft Home Bar White (Row 10) ---")
    img_es34 = os.path.join(PROJECT_DIR, r'new_product_images\یخچال و فریزر\یخچال و فریزر 34 فوت هوم بار الکترواستیل سفید\main.jpg')
    mid_es34 = upload_media_file(img_es34, 'یخچال و فریزر 34 فوت هوم بار الکترواستیل سفید مدل التیما', 'عکس یخچال و فریزر ۳۴ فوت هوم بار الکترواستیل مدل ES34 سفید')

    es34_short = """<ul>
<li><strong>گنجایش فوق‌العاده ۳۴ فوت:</strong> ماکزیمم فضای ذخیره‌سازی در کلاس کمبی‌های لوکس ایرانی</li>
<li><strong>درب دسترسی سریع هوم‌بار (Home Bar):</strong> دسترسی آسان به بطری‌ها و نوشیدنی‌ها بدون باز کردن درب اصلی</li>
<li><strong>یخ‌ساز و آبسردکن اتوماتیک:</strong> اتصال مستقیم به آب شهری همراه با فیلتر تصفیه آبداخلی</li>
<li><strong>کمپرسور اینورتر دیجیتال هوشمند:</strong> کاهش مصرف برق، صدای حداقلی و دوام فوق‌العاده بالا</li>
<li><strong>سیستم جریان هوای چندگانه ۳۶۰ درجه:</strong> توزیع یکنواخت سرمایش برای طراوت طولانی‌مدت مواد پروتئینی</li>
<li><strong>ضمانت اصالت:</strong> ضمانت اصالت ۱۰۰٪ فیزیکی کالا از فروشگاه حسینی کالا اهواز</li>
</ul>"""

    es34_desc = """<h2>بررسی تخصصی و راهنمای خرید یخچال و فریزر 34 فوت هوم‌بار الکترواستیل سفید (مدل ES34)</h2>
<p>پرچمدار یخچال‌های کمبی شرکت <strong>الکترواستیل (Electrosteel)</strong>، مدل <strong>۳۴ فوت مجهز به هوم‌بار</strong> است که با ابعاد باشکوه و امکاناتی در سطح سایدبای‌سایدهای خارجی، لوکس‌ترین تجربه استفاده را به ارمغان می‌آورد. این مدل با درب اختصاصی بار خانگی، مانع از اتلاف انرژی و سرمای محفظه اصلی می‌شود.</p>

<h3>ویژگی‌های متمایز یخچال ۳۴ فوت هوم‌بار الکترواستیل</h3>
<ul>
<li><strong>درب بار خانگی (Home Bar):</strong> با فشردن ملایم بخش هوم‌بار، محفظه نوشیدنی‌ها باز شده و شما بدون نیاز به باز کردن کامل درب اصلی و هدر رفتن هوای سرد، به نوشیدنی‌ها دسترسی خواهید داشت.</li>
<li><strong>یخساز اتوماتیک و آبسردکن متصل به آب شهری:</strong> فیلتر تصفیه آب پیشرفته تعبیه‌شده، آبی زلال و یخ‌های حبه‌ای کریستالی را به صورت پیوسته آماده می‌سازد.</li>
<li><strong>کمپرسور نسل جدید اینورتر:</strong> تنظیم هوشمند دور موتور متناسب با دمای محیط و تعداد دفعات باز شدن درب، مصرف انرژی را تا ۳۰٪ کاهش می‌دهد.</li>
<li><strong>طراحی فریزر کشویی جادار در پایین:</strong> کشوهای ریلی مستحکم و عمیق، سازمان‌دهی مواد غذایی منجمد را بسیار ساده می‌سازد.</li>
</ul>

<h2>جدول مشخصات فنی یخچال ۳۴ فوت هوم‌بار الکترواستیل</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">الکترواستیل (Electrosteel)</td></tr>
<tr><td style="padding: 8px;"><strong>مدل</strong></td><td style="padding: 8px;">ES34 (۳۴ فوت هوم‌بار التیما)</td></tr>
<tr><td style="padding: 8px;"><strong>گنجایش</strong></td><td style="padding: 8px;">۳۴ فوت مفید فوق‌العاده بزرگ</td></tr>
<tr><td style="padding: 8px;"><strong>درب هوم‌بار</strong></td><td style="padding: 8px;">دارد (دسترسی سریع به نوشیدنی‌ها)</td></tr>
<tr><td style="padding: 8px;"><strong>رنگ</strong></td><td style="padding: 8px;">سفید براق چرمی</td></tr>
<tr><td style="padding: 8px;"><strong>سیستم بدون برفک</strong></td><td style="padding: 8px;">نوفراست کامل ۱۰۰٪</td></tr>
<tr><td style="padding: 8px;"><strong>رده انرژی</strong></td><td style="padding: 8px;">+A اینورتر فوق کم‌مصرف</td></tr>
<tr><td style="padding: 8px;"><strong>گارانتی و اصالت</strong></td><td style="padding: 8px;">ضمانت اصالت و سلامت از فروشگاه حسینی کالا</td></tr>
</tbody>
</table>

<p>شما می‌توانید این محصول لوکس را با بهترین قیمت و ضمانت رسمی از <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> اهواز به صورت آنلاین یا حضوری خریداری فرمایید.</p>"""

    payload_es34 = {
        'name': 'یخچال و فریزر 34 فوت هوم بار الکترواستیل سفید',
        'slug': 'electrosteel-es34-home-bar-34ft-refrigerator-freezer-white',
        'type': 'simple',
        'status': 'publish',
        'catalog_visibility': 'visible',
        'description': es34_desc,
        'short_description': es34_short,
        'categories': [{'id': 92}, {'id': 156}],
        'images': [{'id': mid_es34}] if mid_es34 else [],
        'manage_stock': False,
        'stock_status': 'outofstock',
        'attributes': [
            {'name': 'برند', 'visible': True, 'variation': False, 'options': ['الکترواستیل (Electrosteel)']},
            {'name': 'مدل', 'visible': True, 'variation': False, 'options': ['ES34']},
            {'name': 'گنجایش', 'visible': True, 'variation': False, 'options': ['۳۴ فوت']},
            {'name': 'هوم بار', 'visible': True, 'variation': False, 'options': ['دارد']},
            {'name': 'رنگ', 'visible': True, 'variation': False, 'options': ['سفید']}
        ]
    }
    prod_es34 = create_wc_product(payload_es34)
    if prod_es34:
        ws.cell(10, 8).value = '✗ ناموجود'
        ws.cell(10, 15).value = prod_es34['id']
        ws.cell(10, 16).value = f"https://hosseinykala.ir/product/{prod_es34['slug']}/"
        ws.cell(10, 18).value = 'ثبت‌شده در سایت'
        wb.save(CATALOG_PATH)
        print("✓ Row 10 (۳۴ فوت هوم بار الکترواستیل) synced in sheet.")

    time.sleep(2)

    # 6. یخچال و فریزر دوقلو دیپوینت مدل اکسپلور (Explore) - Variable (Rows 22-24)
    print("\n--- 6. Depoint Explore Twin Refrigerator Freezer (Variable) ---")
    img_exp_wh = os.path.join(PROJECT_DIR, r'new_product_images\یخچال و فریزر\یخچال و فریزر دوقلو دیپوینت مدل اکسپلور (Explore) - سفید\main.jpg')
    img_exp_si = os.path.join(PROJECT_DIR, r'new_product_images\یخچال و فریزر\یخچال و فریزر دوقلو دیپوینت مدل اکسپلور (Explore) - سیلور\main.jpg')
    mid_exp_wh = upload_media_file(img_exp_wh, 'یخچال و فریزر دوقلو دیپوینت مدل اکسپلور سفید', 'عکس دوقلو دیپوینت مدل Explore رنگ سفید')
    mid_exp_si = upload_media_file(img_exp_si, 'یخچال و فریزر دوقلو دیپوینت مدل اکسپلور سیلور', 'عکس دوقلو دیپوینت مدل Explore رنگ سیلور نقره ای')

    exp_short = """<ul>
<li><strong>طراحی مدرن درب شیشه‌ای با پنل هوشمند:</strong> تکنولوژی پیشرفته کنترل سرمایش و نمای بسیار لوکس</li>
<li><strong>ظرفیت دوقلو فوق‌العاده جادار (۴۰ فوت):</strong> تفکیک کامل کابین یخچال و فریزر برای حداکثر گنجایش</li>
<li><strong>آبسردکن و یخ‌ساز اتوماتیک بیرونی:</strong> اتصال به آب شهری به همراه فیلتر تصفیه آب قدرتمند</li>
<li><strong>سیستم ۱۰۰٪ نوفراست با گردش هوای سه‌بعدی:</strong> ماندگاری طولانی‌مدت سبزیجات، میوه‌ها و مواد گوشتی</li>
<li><strong>کمپرسور اینورتر هوشمند کم‌مصرف:</strong> عملکرد سایلنت و صرفه‌جویی چشمگیر در مصرف برق</li>
<li><strong>ضمانت اصالت فیزیکی:</strong> تضمین ۱۰۰٪ اصالت کالا در فروشگاه حسینی کالا اهواز</li>
</ul>"""

    exp_desc = """<h2>بررسی تخصصی و راهنمای خرید یخچال و فریزر دوقلو دیپوینت مدل اکسپلور (Explore)</h2>
<p>مدل <strong>اکسپلور (Explore)</strong> گل سرسبد تولیدات برند نامدار <strong>دیپوینت (Depoint)</strong> در رده یخچال‌های دوقلو است. این دستگاه با ترکیب درب‌های مدرن، آبسردکن و یخساز اتوماتیک متصل به آب شهری و گنجایش عظیم ۴۰ فوت، استانداردهای روز دنیا را به آشپزخانه شما هدیه می‌دهد.</p>

<h3>ویژگی‌های متمایز دوقلو دیپوینت مدل اکسپلور</h3>
<ul>
<li><strong>یخ‌ساز و آب‌سردکن اتوماتیک متصل به آب شهری:</strong> آبریز و یخساز باریک با پنل کنترل لمسی، یخ حبه‌ای و خردشده و آب گوارا را در هر لحظه آماده می‌سازد.</li>
<li><strong>فناوری سرمایش بدون برفک No Frost:</strong> سیستم تهویه مطبوع هوای داخلی مانع از تجمع رطوبت و بوی نامطبوع در کابین‌ها می‌شود.</li>
<li><strong>کمپرسور اینورتر کم‌صدا:</strong> کاهش استهلاک، ثبات دمایی و مصرف انرژی رده A با کارکرد بی‌صدا.</li>
<li><strong>کشوهای فریزر با ریل‌های تلسکوپی:</strong> تحمل وزن سنگین اقلام منجمد با حرکت روان و دسترسی بسیار آسان.</li>
</ul>

<h2>جدول مشخصات فنی یخچال و فریزر دوقلو دیپوینت مدل اکسپلور</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">دیپوینت (Depoint)</td></tr>
<tr><td style="padding: 8px;"><strong>مدل</strong></td><td style="padding: 8px;">اکسپلور (Explore)</td></tr>
<tr><td style="padding: 8px;"><strong>نوع دستگاه</strong></td><td style="padding: 8px;">یخچال و فریزر دوقلو اتوماتیک</td></tr>
<tr><td style="padding: 8px;"><strong>گنجایش کلی</strong></td><td style="padding: 8px;">۴۰ فوت (حدود ۷۹۰ لیتر)</td></tr>
<tr><td style="padding: 8px;"><strong>یخساز و آبسردکن</strong></td><td style="padding: 8px;">اتوماتیک متصل به آب شهری با فیلتر تصفیه</td></tr>
<tr><td style="padding: 8px;"><strong>رنگ‌بندی</strong></td><td style="padding: 8px;">سفید و سیلور (نقره‌ای)</td></tr>
<tr><td style="padding: 8px;"><strong>کمپرسور</strong></td><td style="padding: 8px;">اینورتر دیجیتال کم‌مصرف</td></tr>
<tr><td style="padding: 8px;"><strong>گارانتی و اصالت</strong></td><td style="padding: 8px;">ضمانت اصالت و سلامت از فروشگاه حسینی کالا</td></tr>
</tbody>
</table>

<p>شما می‌توانید این محصول لوکس را با بهترین قیمت و ضمانت رسمی از <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> اهواز به صورت آنلاین یا با مراجعه حضوری خریداری فرمایید.</p>"""

    payload_exp_parent = {
        'name': 'یخچال و فریزر دوقلو دیپوینت مدل اکسپلور (Explore)',
        'slug': 'depoint-explore-twin-refrigerator-freezer',
        'type': 'variable',
        'status': 'publish',
        'catalog_visibility': 'visible',
        'description': exp_desc,
        'short_description': exp_short,
        'categories': [{'id': 92}, {'id': 154}],
        'images': [{'id': mid_exp_wh}] if mid_exp_wh else [],
        'attributes': [
            {'name': 'برند', 'visible': True, 'variation': False, 'options': ['دیپوینت (Depoint)']},
            {'name': 'مدل', 'visible': True, 'variation': False, 'options': ['اکسپلور (Explore)']},
            {'name': 'رنگ', 'visible': True, 'variation': True, 'options': ['سفید', 'سیلور (نقره ای)']},
            {'name': 'نوع دستگاه', 'visible': True, 'variation': False, 'options': ['دوقلو اتوماتیک']}
        ]
    }
    prod_exp = create_wc_product(payload_exp_parent)
    if prod_exp:
        exp_id = prod_exp['id']
        exp_slug = prod_exp['slug']
        ws.cell(22, 14).value = exp_id
        ws.cell(22, 16).value = f"https://hosseinykala.ir/product/{exp_slug}/"
        ws.cell(22, 18).value = 'ثبت‌شده در سایت'
        
        # Variation White (Row 23)
        var_wh_payload = {
            'manage_stock': False,
            'stock_status': 'outofstock',
            'image': {'id': mid_exp_wh} if mid_exp_wh else None,
            'attributes': [{'name': 'رنگ', 'option': 'سفید'}]
        }
        var_wh = create_wc_variation(exp_id, var_wh_payload)
        if var_wh:
            ws.cell(23, 8).value = '✗ ناموجود'
            ws.cell(23, 14).value = exp_id
            ws.cell(23, 15).value = var_wh['id']
            ws.cell(23, 16).value = f"https://hosseinykala.ir/product/{exp_slug}/"
            ws.cell(23, 18).value = 'ثبت‌شده در سایت'

        # Variation Silver (Row 24)
        var_si_payload = {
            'manage_stock': False,
            'stock_status': 'outofstock',
            'image': {'id': mid_exp_si} if mid_exp_si else None,
            'attributes': [{'name': 'رنگ', 'option': 'سیلور (نقره ای)'}]
        }
        var_si = create_wc_variation(exp_id, var_si_payload)
        if var_si:
            ws.cell(24, 8).value = '✗ ناموجود'
            ws.cell(24, 14).value = exp_id
            ws.cell(24, 15).value = var_si['id']
            ws.cell(24, 16).value = f"https://hosseinykala.ir/product/{exp_slug}/"
            ws.cell(24, 18).value = 'ثبت‌شده در سایت'

        wb.save(CATALOG_PATH)
        print("✓ Rows 22-24 (دوقلو دیپوینت اکسپلور و تنوع‌ها) synced in sheet.")

    time.sleep(2)

    # 7. یخچال و فریزر کمبی دیپوینت مدل دیسنت (Decent) - Variable (Rows 25-27)
    print("\n--- 7. Depoint Decent Combi Refrigerator Freezer (Variable) ---")
    img_dec_wh = os.path.join(PROJECT_DIR, r'new_product_images\یخچال و فریزر\یخچال و فریزر کمبی دیپوینت مدل دیسنت (Decent) - سفید\0c3e3417c2095a9eae8cb5c3260bc297a69c8904_1754244051.jpg')
    img_dec_st = os.path.join(PROJECT_DIR, r'new_product_images\یخچال و فریزر\یخچال و فریزر کمبی دیپوینت مدل دیسنت (Decent) - استیل\images.jpg')
    mid_dec_wh = upload_media_file(img_dec_wh, 'یخچال و فریزر کمبی دیپوینت مدل دیسنت سفید', 'عکس یخچال کمبی دیپوینت مدل Decent رنگ سفید با آبسردکن')
    mid_dec_st = upload_media_file(img_dec_st, 'یخچال و فریزر کمبی دیپوینت مدل دیسنت استیل', 'عکس یخچال کمبی دیپوینت مدل Decent رنگ استیل ضدلک')

    dec_short = """<ul>
<li><strong>ظرفیت بهینه کمبی (فریزر در پایین):</strong> دسترسی آسان و ارگونومیک به محفظه پرکاربرد یخچال</li>
<li><strong>آبسردکن باریک بیرونی (Slim Water Dispenser):</strong> آب خنک همیشگی بدون باز و بسته کردن مداوم درب</li>
<li><strong>۱۰۰٪ نوفراست بدون برفک:</strong> سیستم خنک‌کنندگی پیشرفته بدون تشکیل یخ و برفک</li>
<li><strong>سیستم کنترل پنل لمسی دیجیتال:</strong> نمایش وضعیت دما با قابلیت انجماد سریع</li>
<li><strong>کشوهای فریزر شفاف و عمیق:</strong> چیدمان تفکیک‌شده و منظم انواع مواد پروتئینی و سبزیجات منجمد</li>
<li><strong>ضمانت اصالت:</strong> ضمانت اصالت ۱۰۰٪ فیزیکی کالا از فروشگاه حسینی کالا اهواز</li>
</ul>"""

    dec_desc = """<h2>بررسی تخصصی و راهنمای خرید یخچال و فریزر کمبی دیپوینت مدل دیسنت (Decent)</h2>
<p>طراحی ارگونومیک یخچال‌های کمبی با فریزر در پایین (Bottom Freezer)، باعث شده تا بیشترین دسترسی به اقلام روزمره یخچال در ارتفاع قد انسان قرار گیرد و دیگر نیازی به خم شدن مداوم نباشد. <strong>یخچال و فریزر کمبی دیپوینت مدل دیسنت (Decent)</strong> از برند پیشرو <strong>دیپوینت (Depoint)</strong>، ترکیبی بی‌نظیر از زیبایی مدرن، کارایی بالا و قیمت مقرون‌به‌صرفه را ارائه می‌دهد.</p>

<h3>ویژگی‌های برجسته کمبی دیپوینت دیسنت</h3>
<ul>
<li><strong>طراحی فریزر در پایین با ۴ کشوی جادار:</strong> نگهداری مقادیر زیادی از مواد منجمد با تفکیک کامل و کشوهای شیشه‌ای نشکن.</li>
<li><strong>آبسردکن باریک با مخزن داخلی:</strong> دسترسی سریع به آب خنک بدون نیاز به لوله‌کشی و اشغال حداقل فضا از طبقات درب یخچال.</li>
<li><strong>سیستم گردش هوای چندگانه (Multi Air Flow):</strong> سرمایش یکدست در تمامی طبقات برای حفظ حداکثر طراوت میوه و لبنیات.</li>
<li><strong>حالت مسافرت (Holiday Mode):</strong> کاهش مصرف برق در زمان عدم حضور طولانی‌مدت در منزل.</li>
</ul>

<h2>جدول مشخصات فنی یخچال و فریزر دیپوینت مدل دیسنت</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">دیپوینت (Depoint)</td></tr>
<tr><td style="padding: 8px;"><strong>مدل</strong></td><td style="padding: 8px;">دیسنت (Decent)</td></tr>
<tr><td style="padding: 8px;"><strong>نوع دستگاه</strong></td><td style="padding: 8px;">یخچال و فریزر کمبی (فریزر پایین)</td></tr>
<tr><td style="padding: 8px;"><strong>سیستم نوفراست</strong></td><td style="padding: 8px;">دارد (۱۰۰٪ بدون برفک)</td></tr>
<tr><td style="padding: 8px;"><strong>آبسردکن</strong></td><td style="padding: 8px;">دارد (مخزنی باریک)</td></tr>
<tr><td style="padding: 8px;"><strong>رنگ‌بندی</strong></td><td style="padding: 8px;">سفید و استیل</td></tr>
<tr><td style="padding: 8px;"><strong>تعداد کشوهای فریزر</strong></td><td style="padding: 8px;">۴ کشوی عمیق کریستالی</td></tr>
<tr><td style="padding: 8px;"><strong>گارانتی و اصالت</strong></td><td style="padding: 8px;">ضمانت اصالت و سلامت از فروشگاه حسینی کالا</td></tr>
</tbody>
</table>

<p>شما می‌توانید این محصول کارآمد را با ضمانت اصالت کالا و مناسب‌ترین قیمت از <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> اهواز به صورت آنلاین یا حضوری تهیه فرمایید.</p>"""

    payload_dec_parent = {
        'name': 'یخچال و فریزر کمبی دیپوینت مدل دیسنت (Decent)',
        'slug': 'depoint-decent-combi-refrigerator-freezer',
        'type': 'variable',
        'status': 'publish',
        'catalog_visibility': 'visible',
        'description': dec_desc,
        'short_description': dec_short,
        'categories': [{'id': 92}, {'id': 154}],
        'images': [{'id': mid_dec_wh}] if mid_dec_wh else [],
        'attributes': [
            {'name': 'برند', 'visible': True, 'variation': False, 'options': ['دیپوینت (Depoint)']},
            {'name': 'مدل', 'visible': True, 'variation': False, 'options': ['دیسنت (Decent)']},
            {'name': 'رنگ', 'visible': True, 'variation': True, 'options': ['سفید', 'استیل']},
            {'name': 'نوع دستگاه', 'visible': True, 'variation': False, 'options': ['کمبی فریزر پایین']}
        ]
    }
    prod_dec = create_wc_product(payload_dec_parent)
    if prod_dec:
        dec_id = prod_dec['id']
        dec_slug = prod_dec['slug']
        ws.cell(25, 14).value = dec_id
        ws.cell(25, 16).value = f"https://hosseinykala.ir/product/{dec_slug}/"
        ws.cell(25, 18).value = 'ثبت‌شده در سایت'
        
        # Variation White (Row 26)
        var_dec_wh_payload = {
            'manage_stock': False,
            'stock_status': 'outofstock',
            'image': {'id': mid_dec_wh} if mid_dec_wh else None,
            'attributes': [{'name': 'رنگ', 'option': 'سفید'}]
        }
        var_dec_wh = create_wc_variation(dec_id, var_dec_wh_payload)
        if var_dec_wh:
            ws.cell(26, 8).value = '✗ ناموجود'
            ws.cell(26, 14).value = dec_id
            ws.cell(26, 15).value = var_dec_wh['id']
            ws.cell(26, 16).value = f"https://hosseinykala.ir/product/{dec_slug}/"
            ws.cell(26, 18).value = 'ثبت‌شده در سایت'

        # Variation Steel (Row 27)
        var_dec_st_payload = {
            'manage_stock': False,
            'stock_status': 'outofstock',
            'image': {'id': mid_dec_st} if mid_dec_st else None,
            'attributes': [{'name': 'رنگ', 'option': 'استیل'}]
        }
        var_dec_st = create_wc_variation(dec_id, var_dec_st_payload)
        if var_dec_st:
            ws.cell(27, 8).value = '✗ ناموجود'
            ws.cell(27, 14).value = dec_id
            ws.cell(27, 15).value = var_dec_st['id']
            ws.cell(27, 16).value = f"https://hosseinykala.ir/product/{dec_slug}/"
            ws.cell(27, 18).value = 'ثبت‌شده در سایت'

        wb.save(CATALOG_PATH)
        print("✓ Rows 25-27 (کمبی دیپوینت دیسنت و تنوع‌ها) synced in sheet.")

    print("\n✓ Batch 5 (یخچال و فریزر) completed and catalog saved!")

if __name__ == '__main__':
    run_batch_5_fridges()

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

def run_batch_2_continue():
    print("==================================================")
    print("CONTINUING BATCH 2 (نوشیدنی ساز) CREATION & SYNC")
    print("==================================================")
    
    wb = openpyxl.load_workbook(CATALOG_PATH, data_only=False)
    ws = wb['نوشیدنی ساز']

    # 3. آب مرکبات گیری برقی کنوود (Row 68)
    print("\n--- 3. Kenwood JE290 Citrus Juicer ---")
    img_kenwood = os.path.join(PROJECT_DIR, r'new_product_images\نوشیدنی ساز\آب مرکبات گیری برقی کنوود\15.jpg')
    mid_kenwood = upload_media_file(img_kenwood, 'آب مرکبات گیری برقی کنوود مدل JE290', 'عکس آب مرکبات گیری برقی ۱ لیتری کنوود مدل JE290')
    
    kenwood_short = """<ul>
<li><strong>مخزن جادار ۱ لیتری:</strong> پارچ شفاف مدرج با ظرفیت ۱۰۰۰ میلی‌لیتر و دستگیره ارگونومیک</li>
<li><strong>چرخش دوطرفه هوشمند:</strong> سیستم چرخش معکوس سری مخروطی برای استخراج حداکثری آب‌میوه</li>
<li><strong>صافی استیل ضدزنگ:</strong> شبکه فیلتر تمام استیل با دوام بالا برای جداسازی کامل هسته و پالپ</li>
<li><strong>مکانیزم فشاری خودکار:</strong> شروع به کار آسان تنها با فشردن میوه روی سری مخروطی</li>
<li><strong>شستشوی آسان:</strong> قطعات جداشونده با قابلیت شستشو در ماشین ظرفشویی</li>
<li><strong>تضمین اصالت:</strong> ضمانت اصالت ۱۰۰٪ کالا از فروشگاه حسینی کالا اهواز</li>
</ul>"""

    kenwood_desc = """<h2>بررسی تخصصی و راهنمای خرید آب مرکبات‌گیری برقی کنوود مدل JE290</h2>
<p>نوشیدن یک لیوان آب پرتقال یا لیمو شیرین طبیعی و خنک، بهترین شیوه برای جذب ویتامین C و حفظ شادابی روزانه است. <strong>آب مرکبات گیری برقی کنوود مدل JE290</strong> از برند صاحب‌نام <strong>کنوود (Kenwood)</strong>، دستگاهی سبک، کارآمد و بادوام برای آبگیری سریع انواع مرکبات ریز و درشت در خانه است.</p>

<h3>ویژگی‌های کلیدی آب مرکبات‌گیری کنوود ۲۹۰</h3>
<ul>
<li><strong>موتور با چرخش دوطرفه:</strong> سری مخروطی دستگاه با هر بار فشردن میوه، جهت چرخش خود را تغییر می‌دهد. این چرخش دوطرفه (Two-way rotation) باعث می‌شود تا آخرین قطره آب‌میوه از بافت پرتقال، گریپ‌فروت یا لیمو ترش جدا شود.</li>
<li><strong>پارچ مدرج ۱۰۰۰ میلی‌لیتری:</strong> مخزن شفاف مدرج دستگاه به شما امکان می‌دهد حجم آبمیوه طبیعی تهیه شده را مشاهده کرده و به کمک لبه آبریز مخصوص، مستقیماً داخل لیوان سرو نمایید.</li>
<li><strong>فیلتر تمام استیل ضد زنگ:</strong> برخلاف مدل‌های ارزان‌قیمت پلاستیکی، صافی این دستگاه از استیل SUS ساخته شده که در برابر اسید میوه مقاوم بوده و طعم نوشیدنی را تغییر نمی‌دهد.</li>
<li><strong>سیستم ضد لغزش و جمع‌آوری کابل:</strong> پایه‌های مکنده لاستیکی از لغزش دستگاه جلوگیری کرده و سیم برق در پایه زیرین جمع‌آوری می‌شود.</li>
</ul>

<h2>جدول مشخصات فنی آب مرکبات‌گیری کنوود مدل JE290</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">کنوود (Kenwood)</td></tr>
<tr><td style="padding: 8px;"><strong>مدل</strong></td><td style="padding: 8px;">JE290</td></tr>
<tr><td style="padding: 8px;"><strong>نوع دستگاه</strong></td><td style="padding: 8px;">آب مرکبات‌گیری برقی فشاری</td></tr>
<tr><td style="padding: 8px;"><strong>توان مصرفی</strong></td><td style="padding: 8px;">۶۰ وات بهینه</td></tr>
<tr><td style="padding: 8px;"><strong>ظرفیت مخزن</strong></td><td style="padding: 8px;">۱ لیتر (۱۰۰۰ میلی‌لیتر) مدرج</td></tr>
<tr><td style="padding: 8px;"><strong>جنس فیلتر</strong></td><td style="padding: 8px;">استیل ضدزنگ</td></tr>
<tr><td style="padding: 8px;"><strong>سیستم چرخش</strong></td><td style="padding: 8px;">دو جهته خودکار (راست‌گرد و چپ‌گرد)</td></tr>
<tr><td style="padding: 8px;"><strong>درپوش ضد گردوغبار</strong></td><td style="padding: 8px;">دارد</td></tr>
<tr><td style="padding: 8px;"><strong>گارانتی و اصالت</strong></td><td style="padding: 8px;">ضمانت اصالت و سلامت فیزیکی از حسینی کالا</td></tr>
</tbody>
</table>

<p>این محصول کاربردی را با بهترین قیمت و ضمانت اصالت فیزیکی از <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> اهواز به صورت آنلاین یا حضوری خریداری فرمایید.</p>"""

    payload_kenwood = {
        'name': 'آب مرکبات گیری برقی کنوود مدل JE290',
        'slug': 'kenwood-je290-electric-citrus-juicer',
        'type': 'simple',
        'status': 'publish',
        'catalog_visibility': 'visible',
        'description': kenwood_desc,
        'short_description': kenwood_short,
        'categories': [{'id': 240}, {'id': 120}],
        'images': [{'id': mid_kenwood}] if mid_kenwood else [],
        'manage_stock': False,
        'stock_status': 'outofstock',
        'attributes': [
            {'name': 'برند', 'visible': True, 'variation': False, 'options': ['کنوود (Kenwood)']},
            {'name': 'مدل', 'visible': True, 'variation': False, 'options': ['JE290']},
            {'name': 'توان مصرفی', 'visible': True, 'variation': False, 'options': ['۶۰ وات']},
            {'name': 'ظرفیت مخزن', 'visible': True, 'variation': False, 'options': ['۱ لیتر']},
            {'name': 'جنس صافی', 'visible': True, 'variation': False, 'options': ['استیل ضدزنگ']},
            {'name': 'عملکرد چرخش', 'visible': True, 'variation': False, 'options': ['چرخش دوطرفه خودکار']}
        ]
    }
    prod_kenwood = create_wc_product(payload_kenwood)
    if prod_kenwood:
        ws.cell(68, 8).value = '✗ ناموجود'
        ws.cell(68, 15).value = prod_kenwood['id']
        ws.cell(68, 16).value = f"https://hosseinykala.ir/product/{prod_kenwood['slug']}/"
        ws.cell(68, 18).value = 'ثبت‌شده در سایت'
        wb.save(CATALOG_PATH)
        print("✓ Row 68 (آب مرکبات‌گیری کنوود) synced in sheet.")

    time.sleep(2)

    # 4. آسیاب قهوه مایر (Row 79)
    print("\n--- 4. Maier MR-4155 Coffee Grinder ---")
    img_maier = os.path.join(PROJECT_DIR, r'new_product_images\نوشیدنی ساز\آسیاب قهوه مایر\main.jpg')
    mid_maier = upload_media_file(img_maier, 'آسیاب قهوه مایر مدل MR-4155 مخروطی لمسی', 'عکس آسیاب قهوه دیجیتال ۳۰ حالته مایر مدل MR-4155')
    
    maier_short = """<ul>
<li><strong>موتور تمام مس ۳۰۰ وات:</strong> موتور قدرتمند فول کوپر با راندمان بالا و سرعت کنترل‌شده</li>
<li><strong>تنظیم ۳۰ درجه آسیاب:</strong> پوشش کامل درجه‌بندی از اسپرسو بسیار نرم تا فرنچ‌پرس درشت</li>
<li><strong>تیغه‌های دندانه‌ای مخروطی:</strong> خردایش یکنواخت بدون سوزاندن عطر و طعم دانه‌های قهوه</li>
<li><strong>پنل لمسی دیجیتال:</strong> نمایشگر دیجیتالی جهت تنظیم دقیق زمان و تعداد شات قهوه</li>
<li><strong>مخزن دانه ۳۵۰ گرمی:</strong> مخزن هاپر ضد اشعه UV با قفل ایمنی و هولدر اختصاصی پرتافیلتر</li>
<li><strong>ضمانت اصالت کالا:</strong> تضمین اصالت و سلامت از فروشگاه لوازم خانگی حسینی اهواز</li>
</ul>"""

    maier_desc = """<h2>بررسی تخصصی و راهنمای خرید آسیاب قهوه مایر مدل MR-4155</h2>
<p>عصاره‌گیری یک شات اسپرسوی استاندارد بیش از هر چیز به درجه و یکنواختی آسیاب دانه قهوه وابسته است. <strong>آسیاب قهوه مایر مدل MR-4155</strong> ساخت برند معتبر <strong>مایر (Maier)</strong>، دستگاهی حرفه‌ای و مجهز به تیغه‌های مخروطی Conical Burr است که طراوت و روغن‌های معطر دانه قهوه را به بهترین شکل حفظ می‌نماید.</p>

<h3>ویژگی‌های متمایز آسیاب قهوه دیجیتال مایر ۴۱۵۵</h3>
<ul>
<li><strong>تیغه مخروطی فولادی ضدسایش:</strong> مکانیزم آسیاب مخروطی با چرخش ملایم، دانه‌ها را بدون ایجاد گرمای مخرب پودر می‌کند تا عطر و طعم اصیل قهوه کاملاً محفوظ بماند.</li>
<li><strong>۳۰ درجه تنظیم نرمی و درشتی:</strong> امکان انتخاب دقیق سایز سابش متناسب با روش‌های مختلف دم‌آوری: قهوه ترک، اسپرسو، موکاپات، V60، ایروپرس، کمکس و فرنچ‌پرس.</li>
<li><strong>اتصال مستقیم پرتافیلتر:</strong> دستگاه دارای پایه نگه‌دارنده پرتافیلتر صنعتی و خانگی است تا پودر قهوه مستقیماً داخل بسکت هدایت شود. همچنین دارای مخزن مجزای پودر قهوه است.</li>
<li><strong>صفحه لمسی هوشمند:</strong> پنل مدرن دیجیتال برای تعیین زمان بر حسب ثانیه یا انتخاب تعداد فنجان با خاموشی خودکار.</li>
</ul>

<h2>جدول مشخصات فنی آسیاب قهوه مایر مدل MR-4155</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">مایر (Maier)</td></tr>
<tr><td style="padding: 8px;"><strong>مدل</strong></td><td style="padding: 8px;">MR-4155</td></tr>
<tr><td style="padding: 8px;"><strong>توان مصرفی</strong></td><td style="padding: 8px;">۳۰۰ وات (موتور مس خالص)</td></tr>
<tr><td style="padding: 8px;"><strong>نوع تیغه</strong></td><td style="padding: 8px;">مخروطی فولادی ضدزنگ (Conical Burr)</td></tr>
<tr><td style="padding: 8px;"><strong>تعداد حالات آسیاب</strong></td><td style="padding: 8px;">۳۰ حالت قابل تنظیم</td></tr>
<tr><td style="padding: 8px;"><strong>ظرفیت مخزن دانه</strong></td><td style="padding: 8px;">۳۵۰ گرم</td></tr>
<tr><td style="padding: 8px;"><strong>صفحه نمایش</strong></td><td style="padding: 8px;">تمام لمسی دیجیتال LED</td></tr>
<tr><td style="padding: 8px;"><strong>لوازم همراه</strong></td><td style="padding: 8px;">استند پرتافیلتر، مخزن پودر قهوه، فرچه نظافت</td></tr>
<tr><td style="padding: 8px;"><strong>گارانتی و اصالت</strong></td><td style="padding: 8px;">ضمانت اصالت و سلامت کالا از حسینی کالا</td></tr>
</tbody>
</table>

<p>شما می‌توانید این آسیاب قهوه را با اطمینان کامل از اصالت و بهترین قیمت از <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> اهواز به صورت آنلاین یا حضوری خریداری نمایید.</p>"""

    payload_maier = {
        'name': 'آسیاب قهوه مایر مدل MR-4155',
        'slug': 'maier-mr4155-digital-conical-burr-coffee-grinder',
        'type': 'simple',
        'status': 'publish',
        'catalog_visibility': 'visible',
        'description': maier_desc,
        'short_description': maier_short,
        'categories': [{'id': 240}],
        'images': [{'id': mid_maier}] if mid_maier else [],
        'manage_stock': False,
        'stock_status': 'outofstock',
        'attributes': [
            {'name': 'برند', 'visible': True, 'variation': False, 'options': ['مایر (Maier)']},
            {'name': 'مدل', 'visible': True, 'variation': False, 'options': ['MR-4155']},
            {'name': 'توان مصرفی', 'visible': True, 'variation': False, 'options': ['۳۰۰ وات']},
            {'name': 'درجات تنظیم', 'visible': True, 'variation': False, 'options': ['۳۰ درجه قابل تنظیم']},
            {'name': 'نوع تیغه', 'visible': True, 'variation': False, 'options': ['مخروطی فولادی (Burr)']},
            {'name': 'پنل کنترل', 'visible': True, 'variation': False, 'options': ['تمام لمسی دیجیتال']}
        ]
    }
    prod_maier = create_wc_product(payload_maier)
    if prod_maier:
        ws.cell(79, 8).value = '✗ ناموجود'
        ws.cell(79, 15).value = prod_maier['id']
        ws.cell(79, 16).value = f"https://hosseinykala.ir/product/{prod_maier['slug']}/"
        ws.cell(79, 18).value = 'ثبت‌شده در سایت'
        wb.save(CATALOG_PATH)
        print("✓ Row 79 (آسیاب قهوه مایر 4155) synced in sheet.")

    time.sleep(2)

    # 5. آسیاب قهوه زیکو مدل 6501 (Row 81)
    print("\n--- 5. Zico ZC-6501 Coffee Grinder ---")
    img_ziko6501 = os.path.join(PROJECT_DIR, r'new_product_images\نوشیدنی ساز\آسیاب قهوه زیکو مدل 6501\0x176.jpg')
    mid_ziko6501 = upload_media_file(img_ziko6501, 'آسیاب قهوه دیجیتال زیکو مدل ZC-6501', 'عکس آسیاب قهوه بدنه استیل زیکو مدل 6501')
    
    ziko6501_short = """<ul>
<li><strong>موتور دور آرام ۴۵۰ دور:</strong> موتور ۲۲۰ وات با گشتاور بالا جهت خردایش سرد بدون گرم شدن قهوه</li>
<li><strong>بدنه تمام استیل ضدزنگ:</strong> ساخته شده از ورق استیل ۱۸/۱۰ مستحکم با طراحی نیمه‌صنعتی</li>
<li><strong>چرخ‌دنده‌های تمام فلز:</strong> دوام فوق‌العاده چرخ‌دنده‌ها با تیغه مخروطی نانوتایتانیوم</li>
<li><strong>نمایشگر LED دیجیتال:</strong> تنظیم هوشمند زمان آسیاب و تعداد کاپ خروجی</li>
<li><strong>هولدر پرتافیلتر:</strong> امکان آسیاب مستقیم درون پرتافیلتر یا مخزن ذخیره پودر</li>
<li><strong>ضمانت اصالت کالا:</strong> تضمین اصالت و سلامت در فروشگاه لوازم خانگی حسینی اهواز</li>
</ul>"""

    ziko6501_desc = """<h2>بررسی تخصصی آسیاب قهوه دیجیتال زیکو مدل ZC-6501</h2>
<p>دقت در اندازه ذرات پودر قهوه، کلید طلایی تهیه اسپرسویی با کیفیت کافه‌ای در منزل است. <strong>آسیاب قهوه زیکو مدل ZC-6501</strong> از برند مدرن و پرطرفدار <strong>زیکو (ZICO)</strong>، با بهره‌گیری از موتور ۲۲۰ واتی دور پایین و بدنه مقاوم استیل، برای کافی‌شاپ‌های کوچک و باریستاهای خانگی گزینه‌ای کم‌نظیر است.</p>

<h3>مزایای منحصربه‌فرد آسیاب زیکو ۶۵۰۱</h3>
<ul>
<li><strong>موتور دور آرام (Low RPM):</strong> چرخش با سرعت بهینه ۴۵۰ دور در دقیقه مانع از ایجاد بار الکترواستاتیک و گرم شدن تیغه‌ها می‌شود؛ در نتیجه دانه‌ها بدون از دست دادن رایحه اصیل خود پودر می‌شوند.</li>
<li><strong>تیغه‌های تیتانیومی بادوام:</strong> طراحی مخروطی از آلیاژ سخت، دقت بالایی در یکنواختی سابش برای اسپرسو، موکاپات و فرنچ‌پرس فراهم می‌سازد.</li>
<li><strong>صفحه کنترل هوشمند دیجیتال:</strong> نمایشگر LED به شما اجازه می‌دهد زمان خردایش را به دقت ثانیه تنظیم نمایید.</li>
<li><strong>بدنه استیل مات ۱۸/۱۰:</strong> ضد خط‌وخش، ضد لک و کاملاً هماهنگ با دستگاه‌های اسپرسوساز استیل.</li>
</ul>

<h2>جدول مشخصات فنی آسیاب قهوه زیکو مدل ZC-6501</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">زیکو (ZICO)</td></tr>
<tr><td style="padding: 8px;"><strong>مدل</strong></td><td style="padding: 8px;">ZC-6501</td></tr>
<tr><td style="padding: 8px;"><strong>توان مصرفی</strong></td><td style="padding: 8px;">۲۲۰ وات</td></tr>
<tr><td style="padding: 8px;"><strong>سرعت چرخش موتور</strong></td><td style="padding: 8px;">۴۵۰ دور در دقیقه (دور آرام ضد حرارت)</td></tr>
<tr><td style="padding: 8px;"><strong>جنس بدنه</strong></td><td style="padding: 8px;">تمام استیل ضدزنگ ۱۸/۱۰</td></tr>
<tr><td style="padding: 8px;"><strong>جنس چرخ‌دنده‌ها</strong></td><td style="padding: 8px;">تمام فلز بادوام</td></tr>
<tr><td style="padding: 8px;"><strong>نمایشگر</strong></td><td style="padding: 8px;">دیجیتال LED با تنظیم تایم و کاپ</td></tr>
<tr><td style="padding: 8px;"><strong>گارانتی و اصالت</strong></td><td style="padding: 8px;">ضمانت اصالت و سلامت از فروشگاه حسینی کالا</td></tr>
</tbody>
</table>

<p>شما می‌توانید این آسیاب را از <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> اهواز به صورت آنلاین یا حضوری با تضمین بهترین قیمت تهیه فرمایید.</p>"""

    payload_ziko6501 = {
        'name': 'آسیاب قهوه زیکو مدل 6501',
        'slug': 'ziko-zc6501-digital-coffee-grinder',
        'type': 'simple',
        'status': 'publish',
        'catalog_visibility': 'visible',
        'description': ziko6501_desc,
        'short_description': ziko6501_short,
        'categories': [{'id': 240}],
        'images': [{'id': mid_ziko6501}] if mid_ziko6501 else [],
        'manage_stock': False,
        'stock_status': 'outofstock',
        'attributes': [
            {'name': 'برند', 'visible': True, 'variation': False, 'options': ['زیکو (ZICO)']},
            {'name': 'مدل', 'visible': True, 'variation': False, 'options': ['ZC-6501']},
            {'name': 'توان مصرفی', 'visible': True, 'variation': False, 'options': ['۲۲۰ وات']},
            {'name': 'جنس بدنه', 'visible': True, 'variation': False, 'options': ['تمام استیل ۱۸/۱۰']},
            {'name': 'سرعت موتور', 'visible': True, 'variation': False, 'options': ['۴۵۰ دور در دقیقه']}
        ]
    }
    prod_ziko6501 = create_wc_product(payload_ziko6501)
    if prod_ziko6501:
        ws.cell(81, 8).value = '✗ ناموجود'
        ws.cell(81, 15).value = prod_ziko6501['id']
        ws.cell(81, 16).value = f"https://hosseinykala.ir/product/{prod_ziko6501['slug']}/"
        ws.cell(81, 18).value = 'ثبت‌شده در سایت'
        wb.save(CATALOG_PATH)
        print("✓ Row 81 (آسیاب قهوه زیکو 6501) synced in sheet.")

    time.sleep(2)

    # 6. آسیاب قهوه زیکو مدل 6502 (Row 82)
    print("\n--- 6. Zico ZC-6502 Coffee Grinder ---")
    img_ziko6502 = os.path.join(PROJECT_DIR, r'new_product_images\نوشیدنی ساز\آسیاب قهوه زیکو مدل 6502\images.jpg')
    mid_ziko6502 = upload_media_file(img_ziko6502, 'آسیاب قهوه حرفه‌ای زیکو مدل ZC-6502', 'عکس آسیاب قهوه دیجیتال نیمه صنعتی زیکو مدل 6502')
    
    ziko6502_short = """<ul>
<li><strong>موتور ارتقایافته ۲۲۰ وات:</strong> سیستم حرکتی سایلنت ۴۵۰ دور در دقیقه با گشتاور پیوسته</li>
<li><strong>طراحی پیشرفته استیل ۱۸/۱۰:</strong> بدنه مستحکم متالیک با پوشش ضداثرانگشت</li>
<li><strong>تیغه‌های مخروطی نانوتایتانیوم:</strong> بالاترین مقاومت در برابر سایش با سابش فوق‌العاده یکدست</li>
<li><strong>پنل نمایشگر دیجیتال:</strong> برنامه‌ریزی دقیق زمان بر حسب دهم ثانیه برای دقت باریستا</li>
<li><strong>اتصال مستقیم پرتافیلتر:</strong> مجهز به گیره استقرار پرتافیلتر برای خروجی تمیز بدون هدررفت پودر</li>
<li><strong>ضمانت اصالت:</strong> ضمانت اصالت ۱۰۰٪ فیزیکی از فروشگاه حسینی کالا اهواز</li>
</ul>"""

    ziko6502_desc = """<h2>بررسی تخصصی و راهنمای خرید آسیاب قهوه زیکو مدل ZC-6502</h2>
<p>برای باریستاهایی که به دنبال بالاترین دقت در ریزتنظیم درجه آسیاب اسپرسو هستند، <strong>آسیاب قهوه زیکو مدل ZC-6502</strong> نسل ارتقایافته آسیاب‌های نیمه‌صنعتی برند <strong>زیکو (ZICO)</strong> است. این دستگاه با چرخ‌دنده‌های کاملاً فلزی و تیغه مخروطی مقاوم، عملکردی بی‌نقص و بادوام ارائه می‌دهد.</p>

<h3>ویژگی‌های متمایز مدل زیکو ZC-6502</h3>
<ul>
<li><strong>تنظیم دقیق گام‌های سابش:</strong> امکان تنظیم بدون لغزش از پودر میکرونی برای اسپرسوهای تک‌خاستگاه تا ذرات درشت برای کلدبرو و فرنچ‌پرس.</li>
<li><strong>موتور با انتقال قدرت مستقیم:</strong> طراحی مکانیکی بهینه‌شده مانع از افت گشتاور زیر بار سنگین آسیاب دانه‌های سخت رست روشن (Light Roast) می‌شود.</li>
<li><strong>صفحه دیجیتال کنترل دوز:</strong> تعیین مقدار پودر بر اساس زمان‌بندی دقیق جهت ثبات طعم در تمامی شات‌های قهوه روزانه.</li>
</ul>

<h2>جدول مشخصات فنی آسیاب قهوه زیکو مدل ZC-6502</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">زیکو (ZICO)</td></tr>
<tr><td style="padding: 8px;"><strong>مدل</strong></td><td style="padding: 8px;">ZC-6502</td></tr>
<tr><td style="padding: 8px;"><strong>توان مصرفی</strong></td><td style="padding: 8px;">۲۲۰ وات</td></tr>
<tr><td style="padding: 8px;"><strong>سرعت چرخش</strong></td><td style="padding: 8px;">۴۵۰ دور در دقیقه (سایلنت و خنک)</td></tr>
<tr><td style="padding: 8px;"><strong>جنس بدنه</strong></td><td style="padding: 8px;">استیل ضدزنگ ۱۸/۱۰ مقاوم</td></tr>
<tr><td style="padding: 8px;"><strong>مکانیزم تیغه</strong></td><td style="padding: 8px;">مخروطی با روکش تیتانیوم ضدسایش</td></tr>
<tr><td style="padding: 8px;"><strong>نمایشگر</strong></td><td style="padding: 8px;">LED لمسی با زمان‌سنج دیجیتال</td></tr>
<tr><td style="padding: 8px;"><strong>گارانتی و اصالت</strong></td><td style="padding: 8px;">ضمانت اصالت و سلامت از فروشگاه حسینی کالا</td></tr>
</tbody>
</table>

<p>سفارش آنلاین یا خرید حضوری این محصول در شعب <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> مستقر در <strong>اهواز</strong> با بهترین شرایط قیمتی در دسترس شماست.</p>"""

    payload_ziko6502 = {
        'name': 'آسیاب قهوه زیکو مدل 6502',
        'slug': 'ziko-zc6502-digital-coffee-grinder',
        'type': 'simple',
        'status': 'publish',
        'catalog_visibility': 'visible',
        'description': ziko6502_desc,
        'short_description': ziko6502_short,
        'categories': [{'id': 240}],
        'images': [{'id': mid_ziko6502}] if mid_ziko6502 else [],
        'manage_stock': False,
        'stock_status': 'outofstock',
        'attributes': [
            {'name': 'برند', 'visible': True, 'variation': False, 'options': ['زیکو (ZICO)']},
            {'name': 'مدل', 'visible': True, 'variation': False, 'options': ['ZC-6502']},
            {'name': 'توان مصرفی', 'visible': True, 'variation': False, 'options': ['۲۲۰ وات']},
            {'name': 'جنس بدنه', 'visible': True, 'variation': False, 'options': ['استیل ضدزنگ ۱۸/۱۰']},
            {'name': 'سرعت موتور', 'visible': True, 'variation': False, 'options': ['۴۵۰ دور در دقیقه']}
        ]
    }
    prod_ziko6502 = create_wc_product(payload_ziko6502)
    if prod_ziko6502:
        ws.cell(82, 8).value = '✗ ناموجود'
        ws.cell(82, 15).value = prod_ziko6502['id']
        ws.cell(82, 16).value = f"https://hosseinykala.ir/product/{prod_ziko6502['slug']}/"
        ws.cell(82, 18).value = 'ثبت‌شده در سایت'
        wb.save(CATALOG_PATH)
        print("✓ Row 82 (آسیاب قهوه زیکو 6502) synced in sheet.")

    time.sleep(2)

    # 7. آبمیوه گیری زیکو مدل 4038 (Row 83)
    print("\n--- 7. Zico ZC-4038 Electric Juicer ---")
    img_ziko4038 = os.path.join(PROJECT_DIR, r'new_product_images\نوشیدنی ساز\آبمیوه گیری زیکو مدل 4038\4ivPHO9Dq8Rb2Snl.jpg')
    mid_ziko4038 = upload_media_file(img_ziko4038, 'آبمیوه گیری تک کاره زیکو مدل ZC-4038 دیجیتال', 'عکس آبمیوه گیری تک کاره پرقدرت استیل زیکو مدل 4038')
    
    ziko4038_short = """<ul>
<li><strong>موتور سنگین پرقدرت ۱۳۵۰ وات:</strong> موتور AC قدرتمند با توان آبگیری سخت‌ترین میوه‌ها مانند سیب و هویج</li>
<li><strong>بدنه تمام استیل ضدزنگ ۱۸/۱۰:</strong> بدنه و ورودی/خروجی مقاوم استیل با طول عمر مادام‌العمر</li>
<li><strong>نمایشگر دیجیتال با ولوم نورانی:</strong> نمایش وضعیت سرعت و دمای موتور به همراه پنل کنترل دایره‌ای</li>
<li><strong>دهانه ورودی بزرگ میوه کامل:</strong> امکان قرار دادن سیب و گلابی درسته بدون نیاز به قطعه‌قطعه کردن</li>
<li><strong>مخزن تفاله‌گیر بزرگ و پارچ مدرج:</strong> پارچ آبمیوه ۱۰۰۰ میلی‌لیتری با درپوش اختصاصی جداکننده کف</li>
<li><strong>ضمانت و اصالت:</strong> ضمانت اصالت ۱۰۰٪ کالا از فروشگاه لوازم خانگی حسینی اهواز</li>
</ul>"""

    ziko4038_desc = """<h2>بررسی تخصصی و راهنمای خرید آبمیوه‌گیری تک‌کاره زیکو مدل ZC-4038</h2>
<p>آبگیری سریع و راحت مقادیر زیادی از میوه‌ها بدون افت دور موتور یا داغ شدن دستگاه، نشان‌دهنده کیفیت ساخت یک آبمیوه‌گیری حرفه‌ای است. <strong>آبمیوه گیری زیکو مدل 4038</strong> (کد فنی <strong>ZC-4038</strong>) از برند معتبر <strong>زیکو (ZICO)</strong>، با موتور استثنایی ۱۳۵۰ واتی و بدنه مقاوم از جنس استیل ۱۸/۱۰، پاسخگوی کامل نیاز خانواده‌های پرجمعیت و دوستداران آبمیوه طبیعی است.</p>

<h3>ویژگی‌های برجسته آبمیوه‌گیری زیکو ۴۰۳۸</h3>
<ul>
<li><strong>توان بی‌رقیب ۱۳۵۰ وات با موتور سنگین AC:</strong> موتور صنعتی دستگاه سخت‌ترین میوه‌ها و سبزیجات ریشه‌ای (مانند هویج، کرفس و چغندر) را در چند ثانیه آبگیری می‌کند.</li>
<li><strong>دهانه ورودی سایز بزرگ (Big Mouth):</strong> نیازی به خرد کردن وقت‌گیر میوه‌ها نیست؛ سیب متوسط، هلو یا گلابی به صورت درسته وارد مجرا شده و خرد می‌شوند.</li>
<li><strong>تیغه و توری میکرومش استیل:</strong> توری میکروسکوپی تفاله‌ها را کاملاً خشک کرده و حداکثر حجم آب زلال و بدون لرد را استخراج می‌کند.</li>
<li><strong>طراحی لوکس با پنل دیجیتال:</strong> نمایشگر دیجیتالی وضعیت کارکرد و ولوم تنظیم سرعت با نور پس‌زمینه آبی، جلوه‌ای مدرن به آشپزخانه می‌بخشد.</li>
<li><strong>اهرم قفل امنیتی فلزی:</strong> میکروسوئیچ‌های ایمنی تا زمانی که اهرم استیل کاملاً قفل نشود، اجازه روشن شدن به موتور را نمی‌دهند.</li>
</ul>

<h2>جدول مشخصات فنی آبمیوه‌گیری زیکو مدل ZC-4038</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">زیکو (ZICO)</td></tr>
<tr><td style="padding: 8px;"><strong>مدل</strong></td><td style="padding: 8px;">ZC-4038</td></tr>
<tr><td style="padding: 8px;"><strong>نوع دستگاه</strong></td><td style="padding: 8px;">آبمیوه‌گیری تک‌کاره حرفه‌ای</td></tr>
<tr><td style="padding: 8px;"><strong>توان مصرفی</strong></td><td style="padding: 8px;">۱۳۵۰ وات پرقدرت (موتور AC سنگین)</td></tr>
<tr><td style="padding: 8px;"><strong>جنس بدنه</strong></td><td style="padding: 8px;">تمام استیل ضدزنگ ۱۸/۱۰</td></tr>
<tr><td style="padding: 8px;"><strong>جنس تیغه و فیلتر</strong></td><td style="padding: 8px;">استیل ضدزنگ SUS فودگرید</td></tr>
<tr><td style="padding: 8px;"><strong>قطر دهانه ورودی</strong></td><td style="padding: 8px;">سایز بزرگ برای ورود میوه درسته</td></tr>
<tr><td style="padding: 8px;"><strong>صفحه نمایش</strong></td><td style="padding: 8px;">دیجیتال LED به همراه ولوم دایره‌ای</td></tr>
<tr><td style="padding: 8px;"><strong>گنجایش پارچ آبمیوه</strong></td><td style="padding: 8px;">۱۰۰۰ میلی‌لیتر (۱ لیتر) مدرج</td></tr>
<tr><td style="padding: 8px;"><strong>گارانتی و اصالت</strong></td><td style="padding: 8px;">ضمانت اصالت و سلامت فیزیکی از حسینی کالا</td></tr>
</tbody>
</table>

<p>خرید این دستگاه پرتوان با اطمینان خاطر و بهترین قیمت از <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> با امکان سفارش آنلاین و تحویل در شعب حضوری <strong>اهواز</strong> فراهم است.</p>"""

    payload_ziko4038 = {
        'name': 'آبمیوه گیری زیکو مدل 4038',
        'slug': 'ziko-zc4038-digital-electric-juicer',
        'type': 'simple',
        'status': 'publish',
        'catalog_visibility': 'visible',
        'description': ziko4038_desc,
        'short_description': ziko4038_short,
        'categories': [{'id': 240}, {'id': 120}],
        'images': [{'id': mid_ziko4038}] if mid_ziko4038 else [],
        'manage_stock': False,
        'stock_status': 'outofstock',
        'attributes': [
            {'name': 'برند', 'visible': True, 'variation': False, 'options': ['زیکو (ZICO)']},
            {'name': 'مدل', 'visible': True, 'variation': False, 'options': ['ZC-4038']},
            {'name': 'توان مصرفی', 'visible': True, 'variation': False, 'options': ['۱۳۵۰ وات']},
            {'name': 'جنس بدنه', 'visible': True, 'variation': False, 'options': ['تمام استیل ۱۸/۱۰']},
            {'name': 'نوع دستگاه', 'visible': True, 'variation': False, 'options': ['آبمیوه‌گیری تک‌کاره حرفه‌ای']},
            {'name': 'ورودی میوه', 'visible': True, 'variation': False, 'options': ['دهانه بزرگ برای میوه کامل']}
        ]
    }
    prod_ziko4038 = create_wc_product(payload_ziko4038)
    if prod_ziko4038:
        ws.cell(83, 8).value = '✗ ناموجود'
        ws.cell(83, 15).value = prod_ziko4038['id']
        ws.cell(83, 16).value = f"https://hosseinykala.ir/product/{prod_ziko4038['slug']}/"
        ws.cell(83, 18).value = 'ثبت‌شده در سایت'
        wb.save(CATALOG_PATH)
        print("✓ Row 83 (آبمیوه‌گیری زیکو 4038) synced in sheet.")

    time.sleep(2)

    # 8. اسپرسوساز مباشی (Row 85)
    print("\n--- 8. Mebashi Semi-Industrial Espresso Maker ---")
    img_mebashi = os.path.join(PROJECT_DIR, r'new_product_images\نوشیدنی ساز\اسپرسوساز مباشی\main.jpg')
    mid_mebashi = upload_media_file(img_mebashi, 'اسپرسوساز نیمه صنعتی مباشی با نمایشگر دیجیتال دما', 'عکس اسپرسوساز نیمه صنعتی مباشی مجهز به کنترل دما و عقربه فشارسنج')
    
    mebashi_short = """<ul>
<li><strong>سیستم کنترل دیجیتال دما (PID):</strong> نمایشگر دیجیتالی دمای بویلر (۹۲ درجه) برای عصاره‌گیری یکدست و بدون سوختگی قهوه</li>
<li><strong>فشار پمپ پرقدرت ۲۰ بار ایتالیایی:</strong> ایجاد کرمای متراکم و استخراج استاندارد عطر و کافئین دانه‌های قهوه</li>
<li><strong>گیج سنجش فشار عصاره‌گیری:</strong> عقربه آنالوگ دقیق جهت پایش فشار بار هنگام تماس آب با کیک قهوه</li>
<li><strong>نازل بخار حرفه‌ای استیل:</strong> بخاردهی پرفشار و خشک جهت تهیه فوم شیر ابریشمی و انواع نوشیدنی‌های بار گرم</li>
<li><strong>صفحه گرم‌کن فنجان با لوگوی اختصاصی:</strong> سینی گرم‌کننده فنجان با ظرفیت چند فنجان به صورت همزمان</li>
<li><strong>ضمانت اصالت فیزیکی:</strong> تضمین ۱۰۰٪ اصالت کالا در فروشگاه لوازم خانگی حسینی اهواز</li>
</ul>"""

    mebashi_desc = """<h2>بررسی تخصصی و راهنمای خرید اسپرسوساز نیمه‌صنعتی مباشی با نمایشگر دیجیتال دما</h2>
<p>ثبات دما و فشار، دو رکن اساسی برای دستیابی به طعم متعادل و بدون ترشی یا تلخی زننده در اسپرسو است. <strong>اسپرسوساز نیمه‌صنعتی مباشی</strong> از برند محبوب ژاپنی <strong>مباشی (Mebashi)</strong>، با بهره‌گیری از فناوری پیشرفته کنترل حرارت و نمایشگر دیجیتالی دما، استانداردهای یک کافی‌شاپ حرفه‌ای را به خانه یا محیط کار شما می‌آورد.</p>

<h3>ویژگی‌های برجسته اسپرسوساز مباشی</h3>
<ul>
<li><strong>نمایشگر دیجیتال دما (PID Temperature Control):</strong> این سیستم دمای دقیق آب درون بویلر را پایش کرده و بر روی صفحه LED نمایش می‌دهد تا عصاره‌گیری همواره در نقطه طلایی ۹۰ تا ۹۳ درجه سانتی‌گراد انجام شود.</li>
<li><strong>پمپ پرفشار ۲۰ بار ULKA ایتالیا:</strong> پمپ قدرتمند این دستگاه با ایجاد فشار پایدار در محفظه بسکت، کریما (کف خامه) ضخیم و ماندگاری را روی فنجان اسپرسو تشکیل می‌دهد.</li>
<li><strong>نشانگر آنالوگ فشارسنج:</strong> ترکیب عقربه کلاسیک فشارسنج و نمایشگر دیجیتالی دما، تسلط کامل باریستا بر متغیرهای عصاره‌گیری را تضمین می‌کند.</li>
<li><strong>نازل بخار استیل ارگونومیک:</strong> نازل با زاویه چرخش مناسب و توان بخاردهی خشک، به شما امکان می‌دهد در چند ثانیه شیر سرد را به میکروفوم لطیف برای آرت قهوه تبدیل نمایید.</li>
<li><strong>پرتافیلتر سنگین با بسکت دبل و تک:</strong> انتقال حرارت عالی و جلوگیری از افت دمای آب حین عبور از پودر قهوه فشرده‌شده.</li>
</ul>

<h2>جدول مشخصات فنی اسپرسوساز نیمه‌صنعتی مباشی</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">مباشی (Mebashi)</td></tr>
<tr><td style="padding: 8px;"><strong>نوع دستگاه</strong></td><td style="padding: 8px;">اسپرسوساز نیمه‌صنعتی و خانگی حرفه‌ای</td></tr>
<tr><td style="padding: 8px;"><strong>فشار بخار پمپ</strong></td><td style="padding: 8px;">۲۰ بار (پمپ ایتالیایی)</td></tr>
<tr><td style="padding: 8px;"><strong>توان مصرفی</strong></td><td style="padding: 8px;">۱۳۵۰ وات</td></tr>
<tr><td style="padding: 8px;"><strong>نمایشگر دما</strong></td><td style="padding: 8px;">دیجیتال LED (سیستم هوشمند دمایی)</td></tr>
<tr><td style="padding: 8px;"><strong>فشارسنج عقربه‌ای</strong></td><td style="padding: 8px;">دارد (Bar Gauge)</td></tr>
<tr><td style="padding: 8px;"><strong>قابلیت‌های آماده‌سازی</strong></td><td style="padding: 8px;">اسپرسو، کاپوچینو، لاته، ماکیاتو، آمریکانو، فوم شیر</td></tr>
<tr><td style="padding: 8px;"><strong>سینی چکه‌گیر و گرم‌کن فنجان</strong></td><td style="padding: 8px;">دارد (استیل ضدزنگ جداشونده)</td></tr>
<tr><td style="padding: 8px;"><strong>گارانتی و خدمات</strong></td><td style="padding: 8px;">ضمانت اصالت و سلامت کالا از حسینی کالا</td></tr>
</tbody>
</table>

<p>شما می‌توانید این اسپرسوساز پیشرفته را با بهترین قیمت و ضمانت معتبر از <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> اهواز به صورت آنلاین یا با مراجعه حضوری تهیه فرمایید.</p>"""

    payload_mebashi = {
        'name': 'اسپرسوساز نیمه صنعتی مباشی با نمایشگر دیجیتال دما',
        'slug': 'mebashi-semi-industrial-digital-espresso-maker',
        'type': 'simple',
        'status': 'publish',
        'catalog_visibility': 'visible',
        'description': mebashi_desc,
        'short_description': mebashi_short,
        'categories': [{'id': 240}, {'id': 119}],
        'images': [{'id': mid_mebashi}] if mid_mebashi else [],
        'manage_stock': False,
        'stock_status': 'outofstock',
        'attributes': [
            {'name': 'برند', 'visible': True, 'variation': False, 'options': ['مباشی (Mebashi)']},
            {'name': 'نوع دستگاه', 'visible': True, 'variation': False, 'options': ['اسپرسوساز نیمه‌صنعتی']},
            {'name': 'فشار پمپ', 'visible': True, 'variation': False, 'options': ['۲۰ بار']},
            {'name': 'نمایشگر دما', 'visible': True, 'variation': False, 'options': ['دیجیتال LED']},
            {'name': 'فشارسنج عقربه‌ای', 'visible': True, 'variation': False, 'options': ['دارد']}
        ]
    }
    prod_mebashi = create_wc_product(payload_mebashi)
    if prod_mebashi:
        ws.cell(85, 8).value = '✗ ناموجود'
        ws.cell(85, 15).value = prod_mebashi['id']
        ws.cell(85, 16).value = f"https://hosseinykala.ir/product/{prod_mebashi['slug']}/"
        ws.cell(85, 18).value = 'ثبت‌شده در سایت'
        wb.save(CATALOG_PATH)
        print("✓ Row 85 (اسپرسوساز مباشی) synced in sheet.")

    print("\n✓ Batch 2 (نوشیدنی ساز) completed and saved!")

if __name__ == '__main__':
    run_batch_2_continue()

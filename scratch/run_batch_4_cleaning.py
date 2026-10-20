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

def run_batch_4_cleaning():
    print("==================================================")
    print("STARTING BATCH 4 (شستشو و نظافت) CREATION & SYNC")
    print("==================================================")
    
    wb = openpyxl.load_workbook(CATALOG_PATH, data_only=False)
    ws = wb['شستشو و نظافت']

    # 1. اتو بخار پاناسونیک مدل 650 (Row 82)
    print("\n--- 1. Panasonic NI-W650T Steam Iron (Row 82) ---")
    img_pan = os.path.join(PROJECT_DIR, r'new_product_images\شستشو و نظافت\اتو بخار پاناسونیک مدل 650\main.jpg')
    mid_pan = upload_media_file(img_pan, 'اتو بخار پاناسونیک مدل NI-W650T کفی ۳۶۰ درجه', 'عکس اتو بخار پاناسونیک مدل 650 با کفی دوطرفه تیتانیوم')

    pan_short = """<ul>
<li><strong>کفی دوطرفه ۳۶۰ درجه (Multi-Directional):</strong> طراحی بیضی ارگونومیک جهت حرکت روان در تمام جهات بدون چروک شدن پارچه</li>
<li><strong>توان پرقدرت ۲۲۰۰ وات:</strong> داغ شدن سریع و حفظ دمای پایدار در حین اتوکشی مداوم</li>
<li><strong>پوشش تیتانیومی ضدخش و نچسب:</strong> سر خوردن فوق‌العاده روی انواع الیاف طبیعی و مصنوعی</li>
<li><strong>سیستم ضد رسوب پیشرفته (Calc Cut):</strong> تخلیه آسان املاح آب و جلوگیری از گرفتگی منافذ بخار</li>
<li><strong>سیستم ضد چکه هوشمند (Anti-Drip):</strong> ممانعت از لکه‌دار شدن البسه تیره در دماهای پایین</li>
<li><strong>ضمانت اصالت فیزیکی:</strong> تضمین ۱۰۰٪ اصالت کالا در فروشگاه حسینی کالا اهواز</li>
</ul>"""

    pan_desc = """<h2>بررسی تخصصی و راهنمای خرید اتو بخار پاناسونیک مدل NI-W650T (مدل 650)</h2>
<p>حرکت دادن سنتی اتو فقط به سمت جلو، بخش عمده‌ای از زمان اتوکشی را هدر می‌دهد و باعث چروک مجدد بخش‌های اتوشده در حرکت رو به عقب می‌شود. <strong>اتو بخار پاناسونیک مدل NI-W650T</strong> (معروف به مدل ۶۵۰) از برند اصیل ژاپنی <strong>پاناسونیک (Panasonic)</strong>، با کفی خلاقانه دو سر مخروطی ۳۶۰ درجه این چالش را به کلی حل کرده است.</p>

<h3>ویژگی‌های متمایز اتو بخار پاناسونیک ۶۵۰</h3>
<ul>
<li><strong>کفی ۳۶۰ درجه بیضی شکل:</strong> دو نوک تیز در جلو و عقب به شما اجازه می‌دهد اتو را بدون نیاز به بلند کردن یا چرخاندن دست، به راحتی به سمت عقب، چپ و راست حرکت دهید و سرعت اتوکشی را تا ۲۵٪ افزایش دهید.</li>
<li><strong>کفی تیتانیوم مقاوم:</strong> کفی با روکش تیتانیومی نچسب و ضد سایش، اصطکاک را به حداقل رسانده و از برق افتادن روی پارچه‌های حساس جلوگیری می‌کند.</li>
<li><strong>بخاردهی قدرتمند عمودی:</strong> امکان بخاردهی در حالت آویزان برای صاف کردن چروک کت، لباس مجلسی و پرده بدون نیاز به میز اتو.</li>
<li><strong>سیستم ضد رسوب داخلی:</strong> فیلتر تعبیه‌شده در مخزن از رسوب املاح آب در محفظه بخار جلوگیری کرده و طول عمر دستگاه را تضمین می‌نماید.</li>
</ul>

<h2>جدول مشخصات فنی اتو بخار پاناسونیک مدل NI-W650T</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">پاناسونیک (Panasonic)</td></tr>
<tr><td style="padding: 8px;"><strong>مدل</strong></td><td style="padding: 8px;">NI-W650T (مدل 650)</td></tr>
<tr><td style="padding: 8px;"><strong>توان مصرفی</strong></td><td style="padding: 8px;">۲۲۰۰ وات پرقدرت</td></tr>
<tr><td style="padding: 8px;"><strong>جنس کفی</strong></td><td style="padding: 8px;">تیتانیوم نچسب و ضدخش ۳۶۰ درجه</td></tr>
<tr><td style="padding: 8px;"><strong>سیستم ضد چکه</strong></td><td style="padding: 8px;">دارد (Anti-Drip)</td></tr>
<tr><td style="padding: 8px;"><strong>سیستم ضد رسوب</strong></td><td style="padding: 8px;">دارد (Calc Cut)</td></tr>
<tr><td style="padding: 8px;"><strong>بخاردهی عمودی</strong></td><td style="padding: 8px;">دارد (Vertical Steam)</td></tr>
<tr><td style="padding: 8px;"><strong>گارانتی و اصالت</strong></td><td style="padding: 8px;">ضمانت اصالت و سلامت فیزیکی از حسینی کالا</td></tr>
</tbody>
</table>

<p>شما می‌توانید این اتو بخار بادوام را با ضمانت اصالت و بهترین قیمت از <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> اهواز به صورت آنلاین یا حضوری خریداری نمایید.</p>"""

    payload_pan = {
        'name': 'اتو بخار پاناسونیک مدل 650',
        'slug': 'panasonic-ni-w650t-steam-iron',
        'type': 'simple',
        'status': 'publish',
        'catalog_visibility': 'visible',
        'description': pan_desc,
        'short_description': pan_short,
        'categories': [{'id': 239}, {'id': 118}],
        'images': [{'id': mid_pan}] if mid_pan else [],
        'manage_stock': False,
        'stock_status': 'outofstock',
        'attributes': [
            {'name': 'برند', 'visible': True, 'variation': False, 'options': ['پاناسونیک (Panasonic)']},
            {'name': 'مدل', 'visible': True, 'variation': False, 'options': ['NI-W650T (650)']},
            {'name': 'توان مصرفی', 'visible': True, 'variation': False, 'options': ['۲۲۰۰ وات']},
            {'name': 'جنس کفی', 'visible': True, 'variation': False, 'options': ['تیتانیوم ۳۶۰ درجه']},
            {'name': 'سیستم ضد چکه', 'visible': True, 'variation': False, 'options': ['دارد']},
            {'name': 'سیستم ضد رسوب', 'visible': True, 'variation': False, 'options': ['دارد']}
        ]
    }
    prod_pan = create_wc_product(payload_pan)
    if prod_pan:
        ws.cell(82, 8).value = '✗ ناموجود'
        ws.cell(82, 15).value = prod_pan['id']
        ws.cell(82, 16).value = f"https://hosseinykala.ir/product/{prod_pan['slug']}/"
        ws.cell(82, 18).value = 'ثبت‌شده در سایت'
        wb.save(CATALOG_PATH)
        print("✓ Row 82 (اتو بخار پاناسونیک) synced in sheet.")

    time.sleep(2)

    # 2. جاروبرقی سطلی جنرال فیت مدل اسکای پلاس 4500 (Row 91)
    print("\n--- 2. General Fit Sky Plus 4500 (Row 91) ---")
    img_sky = os.path.join(PROJECT_DIR, r'new_product_images\شستشو و نظافت\جاروبرقی سطلی جنرال فیت مدل اسکای پلاس 4500\main.jpg')
    mid_sky = upload_media_file(img_sky, 'جاروبرقی سطلی جنرال فیت مدل اسکای پلاس 4500', 'عکس جاروبرقی سطلی پرقدرت جنرال فیت مدل اسکای پلاس 4500')

    sky_short = """<ul>
<li><strong>موتور پرقدرت و کم‌صدا:</strong> موتور دو سرعته با مکش فوق‌العاده جهت نظافت انواع سطوح فرش و موکت</li>
<li><strong>مخزن سطلی جادار:</strong> ظرفیت مخزن بزرگ با بدنه فلزی مقاوم در برابر ضربه و خوردگی</li>
<li><strong>فیلتر استاندارد بهداشتی:</strong> جلوگیری از خروج گردوغبار ریز به فضای تنفسی محیط</li>
<li><strong>کیسه قابل شستشو:</strong> مجهز به کیسه دائمی بادوام با تخلیه آسان بدون نیاز به خرید پاکت مصرفی</li>
<li><strong>چرخ‌های روان ۳۶۰ درجه:</strong> جابجایی راحت و آسان بر روی سطوح مختلف بدون واژگونی</li>
<li><strong>ضمانت اصالت:</strong> ضمانت اصالت ۱۰۰٪ فیزیکی کالا از فروشگاه حسینی کالا اهواز</li>
</ul>"""

    sky_desc = """<h2>بررسی تخصصی و راهنمای خرید جاروبرقی سطلی جنرال فیت مدل اسکای پلاس 4500</h2>
<p>جاروبرقی‌های سطلی به دلیل مکش پایدار، دوام مکانیکی بالا و مخزن بزرگ، از محبوب‌ترین گزینه‌ها برای منازل بزرگ، مساجد، حسینیه‌ها و دفاتر کار هستند. <strong>جاروبرقی سطلی جنرال فیت مدل اسکای پلاس 4500</strong> از برند معتبر ایرانی <strong>جنرال فیت (General Fit)</strong>، ترکیبی از قدرت مکش بالا، بدنه مستحکم و طول عمر طولانی را به ارمغان می‌آورد.</p>

<h3>ویژگی‌های شاخص جاروبرقی جنرال فیت اسکای پلاس</h3>
<ul>
<li><strong>موتور دو سرعته استاندارد:</strong> کلید دو حالته برای تنظیم دور موتور متناسب با نظافت روزانه پارکت و سرامیک یا جاروکشی عمیق پرز فرش‌های متراکم.</li>
<li><strong>مخزن سطلی با رنگ پودری الکترواستاتیک:</strong> بدنه فلزی ضدزنگ و ضدخش با آبکاری صنعتی که در برابر ضربه‌های محیطی کاملاً مقاوم است.</li>
<li><strong>کیسه پارچه‌ای نانوفیلتر قابل شستشو:</strong> تخلیه سریع زیپی با امکان شستشوی دوره‌ای جهت حفظ بهداشت و مکش حداکثری.</li>
<li><strong>لوازم جانبی کامل:</strong> شامل گوشه‌گیر، برس مبل و پارویی استاندارد برای تمیزکاری تمامی زوایا.</li>
</ul>

<h2>جدول مشخصات فنی جاروبرقی جنرال فیت مدل اسکای پلاس 4500</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">جنرال فیت (General Fit)</td></tr>
<tr><td style="padding: 8px;"><strong>مدل</strong></td><td style="padding: 8px;">اسکای پلاس 4500 (Sky Plus)</td></tr>
<tr><td style="padding: 8px;"><strong>نوع دستگاه</strong></td><td style="padding: 8px;">جاروبرقی سطلی خانگی و اداری</td></tr>
<tr><td style="padding: 8px;"><strong>تعداد حالات سرعت</strong></td><td style="padding: 8px;">۲ سرعته (دور کم و دور زیاد)</td></tr>
<tr><td style="padding: 8px;"><strong>جنس بدنه</strong></td><td style="padding: 8px;">فلزی با رنگ پودری الکترواستاتیک</td></tr>
<tr><td style="padding: 8px;"><strong>نوع فیلتر</strong></td><td style="padding: 8px;">میکروفیلتر نمدی + کیسه پارچه‌ای دائمی</td></tr>
<tr><td style="padding: 8px;"><strong>چرخ‌های هدایت</strong></td><td style="padding: 8px;">۴ چرخ گردان ۳۶۰ درجه روان</td></tr>
<tr><td style="padding: 8px;"><strong>گارانتی و اصالت</strong></td><td style="padding: 8px;">ضمانت اصالت و سلامت از فروشگاه حسینی کالا</td></tr>
</tbody>
</table>

<p>برای خرید این جاروبرقی سطلی با بهترین قیمت و ضمانت رسمی به <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> اهواز به صورت آنلاین یا حضوری مراجعه فرمایید.</p>"""

    payload_sky = {
        'name': 'جاروبرقی سطلی جنرال فیت مدل اسکای پلاس 4500',
        'slug': 'generalfit-sky-plus-4500-canister-vacuum-cleaner',
        'type': 'simple',
        'status': 'publish',
        'catalog_visibility': 'visible',
        'description': sky_desc,
        'short_description': sky_short,
        'categories': [{'id': 239}, {'id': 21}],
        'images': [{'id': mid_sky}] if mid_sky else [],
        'manage_stock': False,
        'stock_status': 'outofstock',
        'attributes': [
            {'name': 'برند', 'visible': True, 'variation': False, 'options': ['جنرال فیت (General Fit)']},
            {'name': 'مدل', 'visible': True, 'variation': False, 'options': ['اسکای پلاس 4500']},
            {'name': 'نوع جاروبرقی', 'visible': True, 'variation': False, 'options': ['سطلی']},
            {'name': 'تنظیم سرعت', 'visible': True, 'variation': False, 'options': ['۲ سرعته']},
            {'name': 'نوع کیسه', 'visible': True, 'variation': False, 'options': ['پارچه‌ای دائمی قابل شستشو']}
        ]
    }
    prod_sky = create_wc_product(payload_sky)
    if prod_sky:
        ws.cell(91, 8).value = '✗ ناموجود'
        ws.cell(91, 15).value = prod_sky['id']
        ws.cell(91, 16).value = f"https://hosseinykala.ir/product/{prod_sky['slug']}/"
        ws.cell(91, 18).value = 'ثبت‌شده در سایت'
        wb.save(CATALOG_PATH)
        print("✓ Row 91 (جنرال فیت اسکای پلاس) synced in sheet.")

    time.sleep(2)

    # 3. جاروبرقی سطلی جنرال فیت مدل پرستو 5300 (Row 92)
    print("\n--- 3. General Fit Parastoo 5300 (Row 92) ---")
    img_parastoo = os.path.join(PROJECT_DIR, r'new_product_images\شستشو و نظافت\جاروبرقی سطلی جنرال فیت مدل پرستو 5300\main.jpg')
    mid_parastoo = upload_media_file(img_parastoo, 'جاروبرقی سطلی جنرال فیت مدل پرستو 5300', 'عکس جاروبرقی سطلی جنرال فیت مدل پرستو 5300 دو سرعته')

    parastoo_short = """<ul>
<li><strong>موتور بهینه‌شده نسل جدید:</strong> مکش قدرتمند و راندمان بالا برای جمع‌آوری ریزترین ذرات غبار</li>
<li><strong>مخزن مقاوم سطلی:</strong> ظرفیت ایده‌آل با مقاومت در برابر زنگ‌زدگی و خط‌وخش</li>
<li><strong>لوله تلسکوپی فلزی:</strong> امکان تنظیم ارگونومیک ارتفاع متناسب با قد کاربر</li>
<li><strong>شعاع عملکرد وسیع:</strong> کابل برق بلند به همراه شلنگ انعطاف‌پذیر با زاویه چرخش ۳۶۰ درجه</li>
<li><strong>فیلتراسیون چندلایه:</strong> مجهز به فیلتر هپا داخلی جهت پاکیزگی هوای خروجی</li>
<li><strong>ضمانت اصالت:</strong> ضمانت اصالت ۱۰۰٪ فیزیکی کالا از فروشگاه حسینی کالا اهواز</li>
</ul>"""

    parastoo_desc = """<h2>بررسی تخصصی و راهنمای خرید جاروبرقی سطلی جنرال فیت مدل پرستو 5300</h2>
<p>مدل <strong>پرستو 5300</strong> یکی از پرفروش‌ترین اعضای خانواده جاروبرقی‌های سطلی <strong>جنرال فیت (General Fit)</strong> است. این جاروبرقی با ترکیب قدرت مکش بالا، بدنه مهندسی‌شده و قطعات مرغوب، نیازهای نظافتی روزمره خانوارها را با کمترین زحمت برطرف می‌سازد.</p>

<h3>ویژگی‌های کلیدی جاروبرقی جنرال فیت پرستو ۵۳۰۰</h3>
<ul>
<li><strong>راندمان مکش فوق‌العاده:</strong> موتور پرقدرت طراحی‌شده برای کارکرد مداوم بدون داغ شدن بیش از حد، مکشی یکنواخت از ابتدا تا پر شدن مخزن ارائه می‌دهد.</li>
<li><strong>کیسه قابل شستشوی دائمی:</strong> حذف هزینه‌های خرید مداوم پاکت کاغذی با قابلیت شستشوی آسان و سریع.</li>
<li><strong>اتصال خرطومی چرخشی:</strong> زانویی و خرطومی با قابلیت چرخش آزاد، مانع از پیچ‌خوردگی شلنگ حین حرکت در راهروها و اتاق‌ها می‌شود.</li>
<li><strong>پایه‌های ضربه‌گیر و چرخ‌های روان:</strong> حرکت بدون صدا بر روی انواع سرامیک، پارکت و موکت.</li>
</ul>

<h2>جدول مشخصات فنی جاروبرقی جنرال فیت مدل پرستو 5300</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">جنرال فیت (General Fit)</td></tr>
<tr><td style="padding: 8px;"><strong>مدل</strong></td><td style="padding: 8px;">پرستو 5300 (Parastoo)</td></tr>
<tr><td style="padding: 8px;"><strong>نوع دستگاه</strong></td><td style="padding: 8px;">جاروبرقی سطلی خانگی</td></tr>
<tr><td style="padding: 8px;"><strong>تنظیم سرعت</strong></td><td style="padding: 8px;">۲ سرعته با کلید روی بدنه</td></tr>
<tr><td style="padding: 8px;"><strong>جنس مخزن</strong></td><td style="padding: 8px;">فلزی با رنگ کوره‌ای مقاوم</td></tr>
<tr><td style="padding: 8px;"><strong>نوع لوله</strong></td><td style="padding: 8px;">تلسکوپی فلزی مقاوم</td></tr>
<tr><td style="padding: 8px;"><strong>گارانتی و اصالت</strong></td><td style="padding: 8px;">ضمانت اصالت و سلامت از فروشگاه حسینی کالا</td></tr>
</tbody>
</table>

<p>این محصول کاربردی را می‌توانید با اطمینان از اصالت فیزیکی و بهترین قیمت از <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> اهواز به صورت آنلاین یا حضوری تهیه نمایید.</p>"""

    payload_parastoo = {
        'name': 'جاروبرقی سطلی جنرال فیت مدل پرستو 5300',
        'slug': 'generalfit-parastoo-5300-canister-vacuum-cleaner',
        'type': 'simple',
        'status': 'publish',
        'catalog_visibility': 'visible',
        'description': parastoo_desc,
        'short_description': parastoo_short,
        'categories': [{'id': 239}, {'id': 21}],
        'images': [{'id': mid_parastoo}] if mid_parastoo else [],
        'manage_stock': False,
        'stock_status': 'outofstock',
        'attributes': [
            {'name': 'برند', 'visible': True, 'variation': False, 'options': ['جنرال فیت (General Fit)']},
            {'name': 'مدل', 'visible': True, 'variation': False, 'options': ['پرستو 5300']},
            {'name': 'نوع جاروبرقی', 'visible': True, 'variation': False, 'options': ['سطلی']},
            {'name': 'تنظیم سرعت', 'visible': True, 'variation': False, 'options': ['۲ سرعته']},
            {'name': 'نوع کیسه', 'visible': True, 'variation': False, 'options': ['دائمی قابل شستشو']}
        ]
    }
    prod_parastoo = create_wc_product(payload_parastoo)
    if prod_parastoo:
        ws.cell(92, 8).value = '✗ ناموجود'
        ws.cell(92, 15).value = prod_parastoo['id']
        ws.cell(92, 16).value = f"https://hosseinykala.ir/product/{prod_parastoo['slug']}/"
        ws.cell(92, 18).value = 'ثبت‌شده در سایت'
        wb.save(CATALOG_PATH)
        print("✓ Row 92 (جنرال فیت پرستو 5300) synced in sheet.")

    time.sleep(2)

    # 4. جاروبرقی سطلی جنرال فیت مدل پروانه 5500 (Row 93)
    print("\n--- 4. General Fit Parvaneh 5500 (Row 93) ---")
    img_parvaneh = os.path.join(PROJECT_DIR, r'new_product_images\شستشو و نظافت\جاروبرقی سطلی جنرال فیت مدل پروانه 5500\main.jpg')
    mid_parvaneh = upload_media_file(img_parvaneh, 'جاروبرقی سطلی جنرال فیت مدل پروانه 5500 توربو', 'عکس جاروبرقی سطلی پرقدرت ۲۲۰۰ وات جنرال فیت مدل پروانه 5500')

    parvaneh_short = """<ul>
<li><strong>موتور توربو فوق قدرتمند ۲۲۰۰ وات:</strong> بالاترین رده مکش در بین جاروبرقی‌های سطلی ایرانی</li>
<li><strong>فیلتر دوار هپا اختصاصی:</strong> تصفیه کامل هوای خروجی و تفکیک زباله‌های درشت در فیلتر اولیه</li>
<li><strong>بدنه تمام فلزی آنودایز استاتیک:</strong> مقاومت فوق‌العاده در برابر ضربات و فرسایش محیطی</li>
<li><strong>کلید دو سرعته فشاری:</strong> انتخاب آسان بین مکش اکونومی و توان ماکزیمم توربو</li>
<li><strong>مجموعه کامل سری‌ها و نازل‌ها:</strong> سری پارویی دوکاره، گوشه‌گیر باریک و برس پرزگیر مبلمان</li>
<li><strong>ضمانت اصالت:</strong> ضمانت اصالت ۱۰۰٪ فیزیکی کالا از فروشگاه حسینی کالا اهواز</li>
</ul>"""

    parvaneh_desc = """<h2>بررسی تخصصی و راهنمای خرید جاروبرقی سطلی جنرال فیت مدل پروانه 5500</h2>
<p>اگر به دنبال نهایت قدرت مکش برای تمیز کردن موی حیوانات، پرزهای عمیق فرش و نظافت مساحت‌های بزرگ هستید، <strong>جاروبرقی سطلی جنرال فیت مدل پروانه 5500</strong> پرچمدار بی‌رقیب برند <strong>جنرال فیت (General Fit)</strong> است. این جاروبرقی با موتور سنگین توربو، قدرت مکشی فراتر از استانداردهای معمول خانگی ارائه می‌دهد.</p>

<h3>مزایای منحصربه‌فرد جاروبرقی جنرال فیت پروانه ۵۵۰۰</h3>
<ul>
<li><strong>موتور پرتوان ۲۲۰۰ وات تقویت‌شده:</strong> ایجاد خلاء هوایی قدرتمند برای بیرون کشیدن عمیق‌ترین گردوغبار از تاروپود فرش و موکت.</li>
<li><strong>فیلتر دوار تفکیک‌کننده:</strong> فیلتر سیلیکونی دوار مانع از ورود اشیای تیز یا زباله‌های سنگین به محفظه اصلی کیسه شده و تخلیه را آسان‌تر می‌سازد.</li>
<li><strong>عایق‌بندی صوتی دوگانه:</strong> با وجود توان بالای موتور، محفظه آکوستیک دوجداره میزان صدای مزاحم را به حداقل کاهش داده است.</li>
<li><strong>چرخ‌های بزرگ و مقاوم:</strong> پایداری بالا در هنگام کشیدن روی لبه‌های فرش و عبور از موانع.</li>
</ul>

<h2>جدول مشخصات فنی جاروبرقی جنرال فیت مدل پروانه 5500</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">جنرال فیت (General Fit)</td></tr>
<tr><td style="padding: 8px;"><strong>مدل</strong></td><td style="padding: 8px;">پروانه 5500 (Parvaneh)</td></tr>
<tr><td style="padding: 8px;"><strong>توان موتور</strong></td><td style="padding: 8px;">۲۲۰۰ وات توربو پرقدرت</td></tr>
<tr><td style="padding: 8px;"><strong>نوع دستگاه</strong></td><td style="padding: 8px;">جاروبرقی سطلی نیمه‌صنعتی و خانگی</td></tr>
<tr><td style="padding: 8px;"><strong>سیستم فیلتراسیون</strong></td><td style="padding: 8px;">فیلتر دوار + فیلتر هپا بهداشتی</td></tr>
<tr><td style="padding: 8px;"><strong>جنس بدنه</strong></td><td style="padding: 8px;">فلزی ضخیم با رنگ کوره‌ای الکترواستاتیک</td></tr>
<tr><td style="padding: 8px;"><strong>گارانتی و اصالت</strong></td><td style="padding: 8px;">ضمانت اصالت و سلامت از فروشگاه حسینی کالا</td></tr>
</tbody>
</table>

<p>شما می‌توانید این جاروبرقی پرقدرت را با قیمت استثنایی از <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> اهواز به صورت آنلاین یا حضوری خریداری فرمایید.</p>"""

    payload_parvaneh = {
        'name': 'جاروبرقی سطلی جنرال فیت مدل پروانه 5500',
        'slug': 'generalfit-parvaneh-5500-canister-vacuum-cleaner',
        'type': 'simple',
        'status': 'publish',
        'catalog_visibility': 'visible',
        'description': parvaneh_desc,
        'short_description': parvaneh_short,
        'categories': [{'id': 239}, {'id': 21}],
        'images': [{'id': mid_parvaneh}] if mid_parvaneh else [],
        'manage_stock': False,
        'stock_status': 'outofstock',
        'attributes': [
            {'name': 'برند', 'visible': True, 'variation': False, 'options': ['جنرال فیت (General Fit)']},
            {'name': 'مدل', 'visible': True, 'variation': False, 'options': ['پروانه 5500']},
            {'name': 'توان مصرفی', 'visible': True, 'variation': False, 'options': ['۲۲۰۰ وات توربو']},
            {'name': 'نوع جاروبرقی', 'visible': True, 'variation': False, 'options': ['سطلی']},
            {'name': 'فیلتر هپا', 'visible': True, 'variation': False, 'options': ['دارد']}
        ]
    }
    prod_parvaneh = create_wc_product(payload_parvaneh)
    if prod_parvaneh:
        ws.cell(93, 8).value = '✗ ناموجود'
        ws.cell(93, 15).value = prod_parvaneh['id']
        ws.cell(93, 16).value = f"https://hosseinykala.ir/product/{prod_parvaneh['slug']}/"
        ws.cell(93, 18).value = 'ثبت‌شده در سایت'
        wb.save(CATALOG_PATH)
        print("✓ Row 93 (جنرال فیت پروانه 5500) synced in sheet.")

    time.sleep(2)

    # 5. جاروبرقی سطلی جنرال فیت مدل تاچ استار 4800 (Row 94)
    print("\n--- 5. General Fit Touch Star 4800 (Row 94) ---")
    img_touch = os.path.join(PROJECT_DIR, r'new_product_images\شستشو و نظافت\جاروبرقی سطلی جنرال فیت مدل تاچ استار 4800\main.jpg')
    mid_touch = upload_media_file(img_touch, 'جاروبرقی سطلی جنرال فیت مدل تاچ استار 4800 پنل لمسی', 'عکس جاروبرقی سطلی دیجیتال جنرال فیت مدل تاچ استار 4800')

    touch_short = """<ul>
<li><strong>پنل کنترل لمسی مدرن (Touch Control):</strong> تنظیم دیجیتالی و نرم دور موتور با کلیدهای لمسی هوشمند</li>
<li><strong>موتور بهینه‌سازی‌شده کم‌مصرف:</strong> راندمان مکش بالا همراه با صدای آرام و کنترل‌شده</li>
<li><strong>مخزن سطلی جادار با روکش ضدلک:</strong> بدنه بادوام با رنگ‌آمیزی صنعتی ماندگار</li>
<li><strong>فیلتراسیون ضد حساسیت:</strong> فیلتر بهداشتی جلوگیری از بازگشت آلرژن‌ها به محیط خانه</li>
<li><strong>کیسه دائمی قابل شستشو:</strong> ظرفیت مخزن بزرگ بدون نیاز به تعویض مداوم پاکت</li>
<li><strong>ضمانت اصالت:</strong> ضمانت اصالت ۱۰۰٪ فیزیکی کالا از فروشگاه حسینی کالا اهواز</li>
</ul>"""

    touch_desc = """<h2>بررسی تخصصی و راهنمای خرید جاروبرقی سطلی جنرال فیت مدل تاچ استار 4800</h2>
<p>ترکیب ساختار مستحکم جاروبرقی‌های سطلی با فناوری‌های مدرن دیجیتال، در <strong>جاروبرقی سطلی جنرال فیت مدل تاچ استار 4800</strong> به بهترین شکل محقق شده است. برند <strong>جنرال فیت (General Fit)</strong> با افزودن پنل کنترل لمسی هوشمند، کاربری این دستگاه را بسیار مدرن‌تر و لذت‌بخش‌تر ساخته است.</p>

<h3>ویژگی‌های شاخص جاروبرقی جنرال فیت تاچ استار ۴۸۰۰</h3>
<ul>
<li><strong>کلیدهای کنترل لمسی (Touch Panel):</strong> بر خلاف کلیدهای فشاری سنتی، تغییر دور موتور در این مدل تنها با یک لمس ملایم انجام می‌شود و جلوه‌ای مدرن به ظاهر جاروبرقی می‌بخشد.</li>
<li><strong>سیستم مکش هوشمند چندسطحی:</strong> امکان تنظیم دقیق توان موتور برای پرده‌ها، مبلمان، فرش‌های ابریشمی و موکت‌های ضخیم.</li>
<li><strong>طراحی ارگونومیک و جابجایی سبک:</strong> با وجود مخزن فلزی مقاوم، توزیع وزن دستگاه به گونه‌ای است که کشیدن آن بر روی سطوح مختلف فشاری به دست وارد نمی‌کند.</li>
<li><strong>فیلترهای قابل شستشو:</strong> نظافت آسان تمام اجزای فیلتر و کیسه بدون تحمیل هزینه‌های جانبی.</li>
</ul>

<h2>جدول مشخصات فنی جاروبرقی جنرال فیت مدل تاچ استار 4800</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">جنرال فیت (General Fit)</td></tr>
<tr><td style="padding: 8px;"><strong>مدل</strong></td><td style="padding: 8px;">تاچ استار 4800 (Touch Star)</td></tr>
<tr><td style="padding: 8px;"><strong>نوع پنل</strong></td><td style="padding: 8px;">کنترل لمسی هوشمند (Touch)</td></tr>
<tr><td style="padding: 8px;"><strong>نوع دستگاه</strong></td><td style="padding: 8px;">جاروبرقی سطلی مدرن</td></tr>
<tr><td style="padding: 8px;"><strong>جنس مخزن</strong></td><td style="padding: 8px;">فلزی با رنگ کوره مقاوم ضدخش</td></tr>
<tr><td style="padding: 8px;"><strong>نوع کیسه</strong></td><td style="padding: 8px;">پارچه‌ای دائمی قابل شستشو</td></tr>
<tr><td style="padding: 8px;"><strong>گارانتی و اصالت</strong></td><td style="padding: 8px;">ضمانت اصالت و سلامت از فروشگاه حسینی کالا</td></tr>
</tbody>
</table>

<p>خرید این جاروبرقی لمسی پیشرفته با اطمینان از اصالت کالا و بهترین قیمت در <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> اهواز به صورت آنلاین یا حضوری امکان‌پذیر است.</p>"""

    payload_touch = {
        'name': 'جاروبرقی سطلی جنرال فیت مدل تاچ استار 4800',
        'slug': 'generalfit-touch-star-4800-canister-vacuum-cleaner',
        'type': 'simple',
        'status': 'publish',
        'catalog_visibility': 'visible',
        'description': touch_desc,
        'short_description': touch_short,
        'categories': [{'id': 239}, {'id': 21}],
        'images': [{'id': mid_touch}] if mid_touch else [],
        'manage_stock': False,
        'stock_status': 'outofstock',
        'attributes': [
            {'name': 'برند', 'visible': True, 'variation': False, 'options': ['جنرال فیت (General Fit)']},
            {'name': 'مدل', 'visible': True, 'variation': False, 'options': ['تاچ استار 4800']},
            {'name': 'نوع پنل', 'visible': True, 'variation': False, 'options': ['لمسی دیجیتال']},
            {'name': 'نوع جاروبرقی', 'visible': True, 'variation': False, 'options': ['سطلی']},
            {'name': 'نوع کیسه', 'visible': True, 'variation': False, 'options': ['پارچه‌ای دائمی']}
        ]
    }
    prod_touch = create_wc_product(payload_touch)
    if prod_touch:
        ws.cell(94, 8).value = '✗ ناموجود'
        ws.cell(94, 15).value = prod_touch['id']
        ws.cell(94, 16).value = f"https://hosseinykala.ir/product/{prod_touch['slug']}/"
        ws.cell(94, 18).value = 'ثبت‌شده در سایت'
        wb.save(CATALOG_PATH)
        print("✓ Row 94 (جنرال فیت تاچ استار 4800) synced in sheet.")

    time.sleep(2)

    # 6. جاروبرقی سطلی جنرال فیت مدل کیوتی 4300 (Row 95)
    print("\n--- 6. General Fit Cutie 4300 (Row 95) ---")
    img_cutie = os.path.join(PROJECT_DIR, r'new_product_images\شستشو و نظافت\جاروبرقی سطلی جنرال فیت مدل کیوتی 4300\main.jpg')
    mid_cutie = upload_media_file(img_cutie, 'جاروبرقی سطلی جنرال فیت مدل کیوتی 4300 جمع و جور', 'عکس جاروبرقی سطلی جمع و جور جنرال فیت مدل کیوتی 4300')

    cutie_short = """<ul>
<li><strong>طراحی کامپکت و جمع‌وجور:</strong> اشغال فضای اندک و ایده‌آل برای آپارتمان‌ها و محیط‌های کوچک</li>
<li><strong>موتور قدرتمند و بهینه:</strong> مکش بالا با مصرف برق کنترل‌شده و استهلاک بسیار پایین</li>
<li><strong>وزن سبک با مانور عالی:</strong> جابجایی فوق‌العاده راحت در راه‌پله‌ها و فضاهای فشرده</li>
<li><strong>مخزن سطلی مقاوم:</strong> بدنه فلزی بادوام با رنگ باکیفیت و درب پلیمری مهندسی</li>
<li><strong>کیسه دائمی زیپ‌دار:</strong> نظافت و تخلیه آسان بدون نیاز به هزینه خرید پاکت یکبار مصرف</li>
<li><strong>ضمانت اصالت:</strong> ضمانت اصالت ۱۰۰٪ فیزیکی کالا از فروشگاه حسینی کالا اهواز</li>
</ul>"""

    cutie_desc = """<h2>بررسی تخصصی و راهنمای خرید جاروبرقی سطلی جنرال فیت مدل کیوتی 4300</h2>
<p>بسیاری از خریداران به دنبال قدرت و دوام جاروبرقی‌های سطلی هستند اما نگران ابعاد بزرگ و وزن سنگین آن‌ها در فضاهای آپارتمانی می‌باشند. <strong>جاروبرقی سطلی جنرال فیت مدل کیوتی 4300</strong> (Cutie) از برند <strong>جنرال فیت (General Fit)</strong>، دقیقاً برای حل این مسئله با ابعادی کامپکت، وزنی سبک و مکشی عالی طراحی شده است.</p>

<h3>ویژگی‌های متمایز جاروبرقی جنرال فیت کیوتی ۴۳۰۰</h3>
<ul>
<li><strong>ابعاد کوچک با ظرفیت بهینه:</strong> این مدل فضای بسیار کمی از کمد را اشغال کرده و به راحتی با یک دست قابل حمل است.</li>
<li><strong>موتور با عملکرد بی‌نقص:</strong> توان مکش بالای موتور تمامی کرک‌ها، پرزها و ذرات ریز گردوغبار را از روی سطوح مختلف جمع‌آوری می‌کند.</li>
<li><strong>چرخ‌های هدایت چندجهته:</strong> چرخ‌های باکیفیت زیرین دستگاه مانع از واژگونی جاروبرقی حین چرخش‌های تند در گوشه‌های خانه می‌شوند.</li>
<li><strong>صرفه‌جویی اقتصادی:</strong> مجهز به کیسه دائمی قابل شستشو که نیاز به تعویض و خرید پاکت‌های کاغذی را به طور کامل برطرف می‌سازد.</li>
</ul>

<h2>جدول مشخصات فنی جاروبرقی جنرال فیت مدل کیوتی 4300</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">جنرال فیت (General Fit)</td></tr>
<tr><td style="padding: 8px;"><strong>مدل</strong></td><td style="padding: 8px;">کیوتی 4300 (Cutie)</td></tr>
<tr><td style="padding: 8px;"><strong>نوع دستگاه</strong></td><td style="padding: 8px;">جاروبرقی سطلی کامپکت خانگی</td></tr>
<tr><td style="padding: 8px;"><strong>تنظیمات سرعت</strong></td><td style="padding: 8px;">۲ سرعته</td></tr>
<tr><td style="padding: 8px;"><strong>جنس مخزن</strong></td><td style="padding: 8px;">فلزی با رنگ پودری الکترواستاتیک</td></tr>
<tr><td style="padding: 8px;"><strong>نوع کیسه</strong></td><td style="padding: 8px;">پارچه‌ای دائمی با تخلیه زیپی</td></tr>
<tr><td style="padding: 8px;"><strong>گارانتی و اصالت</strong></td><td style="padding: 8px;">ضمانت اصالت و سلامت از فروشگاه حسینی کالا</td></tr>
</tbody>
</table>

<p>شما می‌توانید این جاروبرقی سطلی سبک و کارآمد را با ضمانت اصالت از <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> اهواز به صورت آنلاین یا با مراجعه حضوری تهیه فرمایید.</p>"""

    payload_cutie = {
        'name': 'جاروبرقی سطلی جنرال فیت مدل کیوتی 4300',
        'slug': 'generalfit-cutie-4300-canister-vacuum-cleaner',
        'type': 'simple',
        'status': 'publish',
        'catalog_visibility': 'visible',
        'description': cutie_desc,
        'short_description': cutie_short,
        'categories': [{'id': 239}, {'id': 21}],
        'images': [{'id': mid_cutie}] if mid_cutie else [],
        'manage_stock': False,
        'stock_status': 'outofstock',
        'attributes': [
            {'name': 'برند', 'visible': True, 'variation': False, 'options': ['جنرال فیت (General Fit)']},
            {'name': 'مدل', 'visible': True, 'variation': False, 'options': ['کیوتی 4300']},
            {'name': 'نوع جاروبرقی', 'visible': True, 'variation': False, 'options': ['سطلی کامپکت']},
            {'name': 'تنظیم سرعت', 'visible': True, 'variation': False, 'options': ['۲ سرعته']},
            {'name': 'نوع کیسه', 'visible': True, 'variation': False, 'options': ['پارچه‌ای دائمی']}
        ]
    }
    prod_cutie = create_wc_product(payload_cutie)
    if prod_cutie:
        ws.cell(95, 8).value = '✗ ناموجود'
        ws.cell(95, 15).value = prod_cutie['id']
        ws.cell(95, 16).value = f"https://hosseinykala.ir/product/{prod_cutie['slug']}/"
        ws.cell(95, 18).value = 'ثبت‌شده در سایت'
        wb.save(CATALOG_PATH)
        print("✓ Row 95 (جنرال فیت کیوتی 4300) synced in sheet.")

    time.sleep(2)

    # 7. جارو شارژی باخ مدل 1454 (Row 97)
    print("\n--- 7. Bach 1454 Cordless Stick Vacuum (Row 97) ---")
    img_bach = os.path.join(PROJECT_DIR, r'new_product_images\شستشو و نظافت\جارو شارژی باخ مدل 1454\5394980a5e9e5ddc852162c24ed2ed8741fc49e1_1779361104.jpg')
    mid_bach = upload_media_file(img_bach, 'جارو شارژی عصایی و دستی باخ مدل 1454 تاشو', 'عکس جارو شارژی تاشو باخ مدل 1454 با فیلتر هپا و چراغ LED')

    bach_short = """<ul>
<li><strong>کاربری دوگانه عصایی و دستی (2-in-1):</strong> تبدیل سریع از جاروی ایستاده بلند به جاروی دستی سبک</li>
<li><strong>دسته تاشو ارگونومیک (Foldable):</strong> تا شدن ۹۰ درجه دسته برای نظافت بدون خم شدن زیر مبل و تخت</li>
<li><strong>باتری قدرتمند لیتیوم یون:</strong> بازدهی شارژدهی طولانی با شارژ سریع و نگهداری پایدار شارژ</li>
<li><strong>چراغ‌های روشنایی LED سر پارویی:</strong> نورپردازی تاریک‌ترین نقاط زیر کابینت و مبلمان</li>
<li><strong>فیلتر تصفیه بهداشتی هپا (HEPA):</strong> جذب ذرات معلق، گردوغبار میکرونی و عوامل حساسیت‌زا</li>
<li><strong>ضمانت اصالت:</strong> ضمانت اصالت ۱۰۰٪ فیزیکی کالا از فروشگاه حسینی کالا اهواز</li>
</ul>"""

    bach_desc = """<h2>بررسی تخصصی و راهنمای خرید جارو شارژی باخ مدل 1454 (تاشو ۲ در ۱)</h2>
<p>جارو کردن سریع خرده‌نان‌ها، موها و خاک‌های روزمره بدون نیاز به سیم‌کشی و پریز برق، نظافت منزل را به تجربه‌ای سریع و بی‌دردسر تبدیل می‌کند. <strong>جارو شارژی باخ مدل 1454</strong> از برند نوین <strong>باخ (Bach)</strong>، با طراحی تاشو و قابلیت تبدیل به جاروی دستی، همراهی ایده‌آل برای نظافت خانه و اتومبیل است.</p>

<h3>ویژگی‌های متمایز جارو شارژی باخ مدل ۱۴۵۴</h3>
<ul>
<li><strong>دسته تاشو از وسط (Foldable Handle):</strong> مکانیزم لولایی دسته به شما امکان می‌دهد بدون نیاز به خم کردن کمر، سر پارویی را به عمق زیر مبل، تختخواب و میزهای کوتاه هدایت کنید. همچنین نگهداری آن در کمد فضای بسیار کمی می‌گیرد.</li>
<li><strong>استفاده به عنوان جاروی دستی پرتابل:</strong> با فشردن یک کلید، موتور و مخزن از بدنه عصایی جدا شده و به یک جاروی دستی سبک برای نظافت صندلی خودرو، گوشه مبل و پرده‌ها تبدیل می‌شود.</li>
<li><strong>روشنایی LED بر روی سری پارویی:</strong> چراغ‌های پرنور جلوی پارویی باعث می‌شوند حتی ریزترین ذرات غبار و مو در فضاهای کم‌نور و تاریک به وضوح دیده شوند.</li>
<li><strong>فیلتراسیون پیشرفته HEPA:</strong> فیلتر قابل شستشوی هپا از بازگشت ذرات آلرژی‌زا به هوای خانه جلوگیری کرده و هوایی تمیز در محیط آزاد می‌سازد.</li>
</ul>

<h2>جدول مشخصات فنی جارو شارژی باخ مدل 1454</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">باخ (Bach)</td></tr>
<tr><td style="padding: 8px;"><strong>مدل</strong></td><td style="padding: 8px;">1454</td></tr>
<tr><td style="padding: 8px;"><strong>نوع دستگاه</strong></td><td style="padding: 8px;">جارو شارژی عصایی و دستی ۲ در ۱ تاشو</td></tr>
<tr><td style="padding: 8px;"><strong>نوع باتری</strong></td><td style="padding: 8px;">لیتیوم یون پرقدرت (Li-ion)</td></tr>
<tr><td style="padding: 8px;"><strong>ویژگی دسته</strong></td><td style="padding: 8px;">تاشو ارگونومیک جهت دسترسی به زیر مبلمان</td></tr>
<tr><td style="padding: 8px;"><strong>چراغ روشنایی پارویی</strong></td><td style="padding: 8px;">دارد (LED پرنور)</td></tr>
<tr><td style="padding: 8px;"><strong>نوع فیلتر</strong></td><td style="padding: 8px;">فیلتر بهداشتی HEPA قابل شستشو</td></tr>
<tr><td style="padding: 8px;"><strong>گارانتی و اصالت</strong></td><td style="padding: 8px;">ضمانت اصالت و سلامت از فروشگاه حسینی کالا</td></tr>
</tbody>
</table>

<p>شما می‌توانید این جارو شارژی مدرن را با بهترین شرایط قیمتی از <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> اهواز به صورت آنلاین یا حضوری خریداری فرمایید.</p>"""

    payload_bach = {
        'name': 'جارو شارژی باخ مدل 1454',
        'slug': 'bach-1454-foldable-cordless-stick-vacuum-cleaner',
        'type': 'simple',
        'status': 'publish',
        'catalog_visibility': 'visible',
        'description': bach_desc,
        'short_description': bach_short,
        'categories': [{'id': 239}, {'id': 21}],
        'images': [{'id': mid_bach}] if mid_bach else [],
        'manage_stock': False,
        'stock_status': 'outofstock',
        'attributes': [
            {'name': 'برند', 'visible': True, 'variation': False, 'options': ['باخ (Bach)']},
            {'name': 'مدل', 'visible': True, 'variation': False, 'options': ['1454']},
            {'name': 'نوع دستگاه', 'visible': True, 'variation': False, 'options': ['جارو شارژی عصایی و دستی']},
            {'name': 'طراحی دسته', 'visible': True, 'variation': False, 'options': ['تاشو ارگونومیک']},
            {'name': 'چراغ LED', 'visible': True, 'variation': False, 'options': ['دارد']}
        ]
    }
    prod_bach = create_wc_product(payload_bach)
    if prod_bach:
        ws.cell(97, 8).value = '✗ ناموجود'
        ws.cell(97, 15).value = prod_bach['id']
        ws.cell(97, 16).value = f"https://hosseinykala.ir/product/{prod_bach['slug']}/"
        ws.cell(97, 18).value = 'ثبت‌شده در سایت'
        wb.save(CATALOG_PATH)
        print("✓ Row 97 (جارو شارژی باخ 1454) synced in sheet.")

    time.sleep(2)

    # 8. بخارگر دستی چندکاره مدل BUVCK-1266 (Row 99)
    print("\n--- 8. BUVCK-1266 Garment Steamer (Row 99) ---")
    img_buvck = os.path.join(PROJECT_DIR, r'new_product_images\شستشو و نظافت\بخارگر دستی چندکاره مدل BUVCK-1266\images.jpg')
    mid_buvck = upload_media_file(img_buvck, 'بخارگر دستی چندکاره مدل BUVCK-1266 پرتابل', 'عکس بخارگر دستی مسافرتی چندکاره BUVCK مدل 1266')

    buvck_short = """<ul>
<li><strong>گرمایش فوق سریع در ۲۵ ثانیه:</strong> آماده‌به‌کار فوری بدون معطلی برای صاف کردن چروک‌های اضطراری</li>
<li><strong>کفی استیل گرم‌شونده ضدچکه:</strong> امکان اتوکشی عمودی (آویزان) و افقی بر روی هر نوع سطح صاف</li>
<li><strong>بخاردهی پیوسته پرقدرت:</strong> نفوذ عمیق بخار داغ برای رفع چین‌وچروک، بوزدایی و ضدعفونی الیاف</li>
<li><strong>مخزن آب شفاف جداشونده:</strong> پر کردن آسان مخزن با گنجایش مناسب برای چندین دست لباس</li>
<li><strong>همراه با برس مخصوص پارچه و پرزگیر:</strong> باز کردن پرزها و نفوذ بخار در بافت پالتو، کت و پرده</li>
<li><strong>ضمانت اصالت:</strong> ضمانت اصالت ۱۰۰٪ فیزیکی کالا از فروشگاه حسینی کالا اهواز</li>
</ul>"""

    buvck_desc = """<h2>بررسی تخصصی و راهنمای خرید بخارگر دستی چندکاره مدل BUVCK-1266</h2>
<p>صاف کردن چروک لباس‌های مجلسی، کت‌وشلوار، مانتو و پرده‌ها با اتوهای معمولی می‌تواند باعث برق افتادن یا آسیب به الیاف حساس شود. <strong>بخارگر دستی چندکاره مدل BUVCK-1266</strong> دستگاهی سبک، مدرن و پرتابل است که با بخار متراکم و دمای کنترل‌شده، لباس‌ها را مستقیماً روی چوب‌لباسی صاف، باطراوت و ضدعفونی می‌کند.</p>

<h3>ویژگی‌های کلیدی بخارگر دستی BUVCK-1266</h3>
<ul>
<li><strong>آماده‌به‌کار سریع کمتر از نیم دقیقه:</strong> با المنت حرارتی بهینه، تنها در ۲۵ ثانیه آب به بخار داغ تبدیل شده و آماده استفاده می‌گردد؛ گزینه‌ای ایده‌آل برای زمانی که عجله دارید.</li>
<li><strong>ضدعفونی و بوزدایی ۹۹.۹ درصدی:</strong> بخار حرارت‌بالا علاوه بر صاف کردن الیاف، باکتری‌ها، ذرات گردوغبار و بوی نامطبوع ماندگی یا سیگار را از تاروپود لباس پاک می‌کند.</li>
<li><strong>طراحی سبک و مسافرتی:</strong> ابعاد جمع‌وجور دستگاه اجازه می‌دهد تا آن را به راحتی درون چمدان در سفرهای کاری و تفریحی همراه داشته باشید.</li>
<li><strong>کفی استیل نچسب:</strong> سر خوردن ایمن روی انواع پارچه‌های حریر، نخ، پشم، پلی‌استر و کتان بدون سوختگی.</li>
</ul>

<h2>جدول مشخصات فنی بخارگر دستی مدل BUVCK-1266</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">BUVCK</td></tr>
<tr><td style="padding: 8px;"><strong>مدل</strong></td><td style="padding: 8px;">BUVCK-1266</td></tr>
<tr><td style="padding: 8px;"><strong>نوع دستگاه</strong></td><td style="padding: 8px;">بخارگر دستی و پرتابل چندکاره</td></tr>
<tr><td style="padding: 8px;"><strong>مدت زمان آماده‌سازی</strong></td><td style="padding: 8px;">حدود ۲۵ الی ۳۰ ثانیه</td></tr>
<tr><td style="padding: 8px;"><strong>کفی بخاردهی</strong></td><td style="padding: 8px;">استیل ضدزنگ گرم‌شونده</td></tr>
<tr><td style="padding: 8px;"><strong>حالت کاربری</strong></td><td style="padding: 8px;">عمودی (آویزان) و افقی بدون چکه</td></tr>
<tr><td style="padding: 8px;"><strong>لوازم جانبی</strong></td><td style="padding: 8px;">برس مخصوص پارچه‌های ضخیم و پیمانه آب</td></tr>
<tr><td style="padding: 8px;"><strong>گارانتی و اصالت</strong></td><td style="padding: 8px;">ضمانت اصالت و سلامت از فروشگاه حسینی کالا</td></tr>
</tbody>
</table>

<p>این بخارگر کاربردی را با بهترین قیمت و ضمانت سلامت فیزیکی از <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> اهواز به صورت آنلاین یا حضوری تهیه فرمایید.</p>"""

    payload_buvck = {
        'name': 'بخارگر دستی چندکاره مدل BUVCK-1266',
        'slug': 'buvck-1266-handheld-garment-steamer',
        'type': 'simple',
        'status': 'publish',
        'catalog_visibility': 'visible',
        'description': buvck_desc,
        'short_description': buvck_short,
        'categories': [{'id': 239}, {'id': 118}],
        'images': [{'id': mid_buvck}] if mid_buvck else [],
        'manage_stock': False,
        'stock_status': 'outofstock',
        'attributes': [
            {'name': 'برند', 'visible': True, 'variation': False, 'options': ['BUVCK']},
            {'name': 'مدل', 'visible': True, 'variation': False, 'options': ['BUVCK-1266']},
            {'name': 'نوع دستگاه', 'visible': True, 'variation': False, 'options': ['بخارگر دستی پرتابل']},
            {'name': 'حالت بخاردهی', 'visible': True, 'variation': False, 'options': ['عمودی و افقی']},
            {'name': 'جنس کفی', 'visible': True, 'variation': False, 'options': ['استیل ضدزنگ']}
        ]
    }
    prod_buvck = create_wc_product(payload_buvck)
    if prod_buvck:
        ws.cell(99, 8).value = '✗ ناموجود'
        ws.cell(99, 15).value = prod_buvck['id']
        ws.cell(99, 16).value = f"https://hosseinykala.ir/product/{prod_buvck['slug']}/"
        ws.cell(99, 18).value = 'ثبت‌شده در سایت'
        wb.save(CATALOG_PATH)
        print("✓ Row 99 (بخارگر دستی BUVCK-1266) synced in sheet.")

    print("\n✓ Batch 4 (شستشو و نظافت) completed and catalog saved!")

if __name__ == '__main__':
    run_batch_4_cleaning()

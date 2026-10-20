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
retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
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
    r = SESSION.post(url, auth=AUTH, headers=headers, data=data, timeout=40)
    if r.status_code == 201:
        res = r.json()
        mid = res['id']
        src = res['source_url']
        SESSION.post(f"{url}/{mid}", auth=AUTH, headers=HEADERS, json={'title': title, 'alt_text': alt_text, 'description': alt_text}, timeout=20)
        print(f"  ✓ Image uploaded: {filename} -> ID {mid}")
        return mid, src
    else:
        print(f"  ❌ Image upload failed: {r.status_code} - {r.text[:200]}")
        return None, None

def create_wc_product(payload):
    url = 'https://hosseinykala.ir/wp-json/wc/v3/products'
    r = SESSION.post(url, auth=AUTH, headers=HEADERS, json=payload, timeout=40)
    if r.status_code == 201:
        res = r.json()
        pid = res['id']
        slug = res['slug']
        perm = res['permalink']
        print(f"  ✓ Product created: ID {pid} | Slug: {slug} | Perm: {perm}")
        return res
    else:
        print(f"  ❌ Product creation failed: {r.status_code} - {r.text[:300]}")
        return None

def run_batch_1():
    print("==================================================")
    print("STARTING BATCH 1 CREATION & SYNC")
    print("==================================================")
    
    wb = openpyxl.load_workbook(CATALOG_PATH, data_only=False)
    
    # ----------------------------------------------------
    # 0. Sync Ziko 5020 (Already created ID 4235) in Excel
    # ----------------------------------------------------
    ws_beauty = wb['زیبایی و سلامت فردی']
    ws_beauty.cell(26, 8).value = '✗ ناموجود'
    ws_beauty.cell(26, 15).value = 4235
    ws_beauty.cell(26, 16).value = 'https://hosseinykala.ir/product/ziko-zc5020-professional-hair-dryer/'
    ws_beauty.cell(26, 18).value = 'ثبت‌شده در سایت'
    print("✓ Row 26 (زیبایی و سلامت فردی - سشوار زیکو 5020) synced in sheet.")

    # ----------------------------------------------------
    # 1. تلویزیون ال ای دی ۵۵ اینچ هوشمند دوو مدل 7000
    # ----------------------------------------------------
    print("\n--- 1. Daewoo 55 Inch TV 7000 ---")
    img_daewoo = os.path.join(PROJECT_DIR, r'new_product_images\صوتی و تصویری\تلویزیون ال ای دی ۵۵ اینچ هوشمند دوو مدل 7000\images.jpg')
    mid_daewoo, _ = upload_media_file(img_daewoo, 'تلویزیون ۵۵ اینچ هوشمند دوو مدل DSL-55S7000EUM', 'عکس تلویزیون ۵۵ اینچ 4K هوشمند دوو سری ۷۰۰۰')
    
    daewoo_short = """<ul>
<li><strong>کیفیت تصویر:</strong> وضوح فوق‌العاده 4K Ultra HD با رزولوشن ۳۸۴۰×۲۱۶۰ و پشتیبانی از HDR</li>
<li><strong>نوع پنل:</strong> پنل ضد ضربه و مقاوم IPS با درجه کیفی +A و زاویه دید گسترده ۱۷۸ درجه</li>
<li><strong>سیستم هوشمند:</strong> سیستم‌عامل اندروید با قابلیت اتصال به Wi-Fi و نصب انواع اپلیکیشن و بازی</li>
<li><strong>سیستم صوتی:</strong> صدای فراگیر ۳۰ وات مجهز به فناوری پردازش دالبی دیجیتال (Dolby Digital)</li>
<li><strong>درگاه‌های ارتباطی:</strong> مجهز به ۳ پورت HDMI، ۲ پورت USB، گیرنده دیجیتال داخلی DVB-T2 و بلوتوث</li>
<li><strong>گارانتی و اصالت:</strong> ضمانت اصالت فیزیکی کالا و امکان خرید اقساطی از فروشگاه حسینی کالا</li>
</ul>"""

    daewoo_desc = """<h2>بررسی تخصصی تلویزیون ال ای دی ۵۵ اینچ هوشمند دوو مدل DSL-55S7000EUM</h2>
<p>تماشای فیلم‌ها، مسابقات ورزشی و بازی‌ها زمانی لذت‌بخش و هیجان‌انگیز است که تصویری شفاف با وضوح خیره‌کننده و صدایی رسا در اختیار داشته باشید. <strong>تلویزیون ال ای دی ۵۵ اینچ هوشمند دوو مدل 7000</strong> (کد فنی <strong>DSL-55S7000EUM</strong>)، با بهره‌مندی از پنل باکیفیت 4K و قابلیت‌های هوشمند پیشرفته، انتخابی ایده‌آل برای سالن‌های پذیرایی و محیط‌های خانگی مدرن به شمار می‌رود.</p>

<h3>کیفیت تصویر 4K و پنل مقاوم IPS</h3>
<p>این تلویزیون با رزولوشن <strong>3840×2160 پیکسل</strong>، تصاویری ۴ برابر شفاف‌تر از نمایشگرهای Full HD ارائه می‌دهد. استفاده از <strong>پنل IPS رده +A</strong> نه تنها وضوح و دقت رنگ‌ها را در تمامی زوایا حفظ می‌کند، بلکه مقاومت بالایی در برابر ضربه‌های ناخواسته دارد. همچنین پشتیبانی از فناوری <strong>HDR</strong> باعث تفکیک عمیق‌تر سایه‌ها، روشنایی درخشان‌تر و نمایش طبیعی‌تر طیف رنگ‌ها می‌شود.</p>

<h3>امکانات هوشمند و سیستم‌عامل اندروید</h3>
<ul>
<li><strong>سیستم‌عامل اندروید:</strong> دسترسی سریع و آسان به دنیای سرگرمی، وبگردی، تماشای آنلاین فیلم در فیلیمو و نماوا، و نصب برنامه‌های کاربردی.</li>
<li><strong>اتصال بی‌سیم و اشتراک‌گذاری صفحه (Screen Mirroring):</strong> امکان انتقال تصویر گوشی موبایل یا تبلت روی صفحه بزرگ تلویزیون بدون نیاز به کابل.</li>
<li><strong>گیرنده دیجیتال نسل جدید:</strong> مجهز به تیونر داخلی DVB-T2 جهت دریافت تمامی شبکه‌های دیجیتال و HD صدا و سیما با بالاترین کیفیت.</li>
<li><strong>صدای پرقدرت دالبی:</strong> مجهز به دو بلندگوی ۱۵ وات (مجموعاً ۳۰ وات) با فناوری صوتی دالبی دیجیتال برای ایجاد صدای شفاف و سینمایی.</li>
</ul>

<h2>جدول مشخصات فنی تلویزیون ۵۵ اینچ دوو سری 7000</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">دوو (Daewoo)</td></tr>
<tr><td style="padding: 8px;"><strong>سایز صفحه نمایش</strong></td><td style="padding: 8px;">۵۵ اینچ</td></tr>
<tr><td style="padding: 8px;"><strong>کیفیت تصویر</strong></td><td style="padding: 8px;">4K Ultra HD (رزولوشن ۳۸۴۰×۲۱۶۰)</td></tr>
<tr><td style="padding: 8px;"><strong>نوع پنل</strong></td><td style="padding: 8px;">IPS ضد ضربه با کیفیت +A</td></tr>
<tr><td style="padding: 8px;"><strong>سیستم‌عامل</strong></td><td style="padding: 8px;">اندروید (Android)</td></tr>
<tr><td style="padding: 8px;"><strong>توان خروجی صدا</strong></td><td style="padding: 8px;">۳۰ وات با استاندارد Dolby Digital</td></tr>
<tr><td style="padding: 8px;"><strong>درگاه‌های ورودی</strong></td><td style="padding: 8px;">۳ درگاه HDMI / ۲ درگاه USB / خروجی اپتیکال / LAN</td></tr>
<tr><td style="padding: 8px;"><strong>اتصالات بی‌سیم</strong></td><td style="padding: 8px;">Wi-Fi و بلوتوث (Bluetooth)</td></tr>
<tr><td style="padding: 8px;"><strong>گیرنده دیجیتال</strong></td><td style="padding: 8px;">دارد (DVB-T2 با پشتیبانی از HEVC)</td></tr>
<tr><td style="padding: 8px;"><strong>گارانتی و خدمات</strong></td><td style="padding: 8px;">ضمانت اصالت و سلامت کالا از فروشگاه حسینی کالا</td></tr>
</tbody>
</table>

<p>شما می‌توانید برای بررسی و خرید این محصول به <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> مراجعه نمایید. امکان خرید اقساطی آسان و تحویل فوری در شعب حضوری ما در <strong>اهواز</strong> فراهم است.</p>"""

    payload_daewoo = {
        'name': 'تلویزیون ال ای دی ۵۵ اینچ هوشمند دوو مدل 7000',
        'slug': 'daewoo-dsl55-s7000eum-55inch-smart-4k-tv',
        'type': 'simple',
        'status': 'publish',
        'catalog_visibility': 'visible',
        'description': daewoo_desc,
        'short_description': daewoo_short,
        'categories': [{'id': 242}, {'id': 243}],
        'images': [{'id': mid_daewoo}] if mid_daewoo else [],
        'manage_stock': False,
        'stock_status': 'outofstock',
        'attributes': [
            {'name': 'برند', 'visible': True, 'variation': False, 'options': ['دوو (Daewoo)']},
            {'name': 'سایز صفحه نمایش', 'visible': True, 'variation': False, 'options': ['۵۵ اینچ']},
            {'name': 'کیفیت تصویر', 'visible': True, 'variation': False, 'options': ['4K Ultra HD']},
            {'name': 'نوع پنل', 'visible': True, 'variation': False, 'options': ['IPS مقاوم']},
            {'name': 'سیستم هوشمند', 'visible': True, 'variation': False, 'options': ['اندروید (Android)']},
            {'name': 'توان صدا', 'visible': True, 'variation': False, 'options': ['۳۰ وات Dolby Digital']}
        ]
    }
    prod_daewoo = create_wc_product(payload_daewoo)
    if prod_daewoo:
        ws_audio = wb['صوتی و تصویری']
        ws_audio.cell(9, 8).value = '✗ ناموجود'
        ws_audio.cell(9, 15).value = prod_daewoo['id']
        ws_audio.cell(9, 16).value = f"https://hosseinykala.ir/product/{prod_daewoo['slug']}/"
        ws_audio.cell(9, 18).value = 'ثبت‌شده در سایت'
        print(f"✓ Row 9 (صوتی و تصویری - تلویزیون دوو 7000) synced in sheet.")

    # ----------------------------------------------------
    # 2. آبگرمکن دیواری شمعک دار ایران شرق مدل 3020
    # ----------------------------------------------------
    print("\n--- 2. Iran Shargh 3020 Water Heater ---")
    img_is = os.path.join(PROJECT_DIR, r'new_product_images\سرمایش و گرمایش\آبگرمکن دیواری شمعک دار ایران شرق مدل 3020\main.jpg')
    mid_is, _ = upload_media_file(img_is, 'آبگرمکن دیواری شمعک دار ایران شرق مدل 3020', 'عکس آبگرمکن گازی دیواری ایران شرق مدل 3020 کیانا')
    
    is_short = """<ul>
<li><strong>ظرفیت حرارتی:</strong> توان حرارتی پرقدرت ۱۸,۰۰۰ کیلوکالری بر ساعت با سیستم زودجوش</li>
<li><strong>آبدهی لحظه‌ای:</strong> خروجی آب گرم یکنواخت تا ۱۳ لیتر در دقیقه متناسب با مصارف خانگی</li>
<li><strong>کارکرد با کمترین فشار آب:</strong> راه‌اندازی سریع حتی با حداقل فشار ۰.۱۵ بار (ایده‌آل برای طبقات بالا)</li>
<li><strong>نوع احتراق:</strong> مجهز به پیلوت دائم (شمعک‌دار) و سیستم جرقه‌زن پیزوالکتریک بادوام</li>
<li><strong>ایمنی استاندارد:</strong> دارای ترموستات حد، سنسور حرارتی دودکش و کلید ایمنی قطع خودکار گاز</li>
<li><strong>گارانتی معتبر:</strong> گارانتی رسمی شرکت ایران شرق و ضمانت اصالت در فروشگاه حسینی کالا</li>
</ul>"""

    is_desc = """<h2>بررسی مشخصات و راهنمای خرید آبگرمکن دیواری شمعک‌دار ایران شرق مدل 3020 (کیانا)</h2>
<p>دسترسی همیشگی به آب گرم فوری و بدون افت دما، یکی از ضروری‌ترین نیازهای هر خانه است. <strong>آبگرمکن دیواری شمعک دار ایران شرق مدل 3020</strong> (معروف به سری <strong>کیانا</strong>)، با راندمان حرارتی بالا و مصرف بهینه گاز، پاسخی مطمئن برای نیاز آب گرم مصرفی منازل مسکونی و اماکن تجاری است.</p>

<h3>مزایای آبگرمکن دیواری ایران شرق ۳۰۲۰</h3>
<ul>
<li><strong>عملکرد مطمئن با فشار کم آب:</strong> یکی از بزرگ‌ترین دغدغه‌های ساکنان آپارتمان‌ها افت فشار آب شهری است. این مدل با حداقل فشار ورودی ۰.۱۵ بار به راحتی فعال شده و آب گرمی یکنواخت و پایدار در اختیار شما قرار می‌دهد.</li>
<li><strong>مبدل حرارتی مسی با پوشش ضد رسوب:</strong> رادیاتور مسی ضخیم آبگرمکن انتقال حرارت سریع را تضمین کرده و مقاومت فوق‌العاده‌ای در برابر تشکیل رسوبات و گچ دارد.</li>
<li><strong>سیستم ایمنی سه‌گانه:</strong> مجهز به کلید حرارتی کلاهک تعدیل (سنسور دود)، ترموستات قطع گاز در دمای بحرانی، و شیر اطمینان مکانیکی استاندارد.</li>
<li><strong>طراحی کم‌حجم دیواری:</strong> ابعاد مناسب این دستگاه فضای بسیار ناچیزی از دیوار آشپزخانه یا بالکن را اشغال می‌کند و امکان تنظیم دستی دما به وسیله ولوم کنترل روی بدنه فراهم است.</li>
</ul>

<h2>جدول مشخصات فنی آبگرمکن دیواری ایران شرق مدل 3020</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">ایران شرق (Iran Shargh)</td></tr>
<tr><td style="padding: 8px;"><strong>مدل</strong></td><td style="padding: 8px;">3020 (کیانا)</td></tr>
<tr><td style="padding: 8px;"><strong>نوع نصب</strong></td><td style="padding: 8px;">دیواری کم‌حجم</td></tr>
<tr><td style="padding: 8px;"><strong>نوع سوخت</strong></td><td style="padding: 8px;">گاز شهری (قابل تنظیم برای گاز مایع)</td></tr>
<tr><td style="padding: 8px;"><strong>ظرفیت حرارتی</strong></td><td style="padding: 8px;">۱۸,۰۰۰ کیلوکالری در ساعت</td></tr>
<tr><td style="padding: 8px;"><strong>ظرفیت تامین آب گرم</strong></td><td style="padding: 8px;">۱۳ لیتر در دقیقه</td></tr>
<tr><td style="padding: 8px;"><strong>حداقل فشار راه‌اندازی</strong></td><td style="padding: 8px;">۰.۱۵ بار (کارکرد با کمترین فشار آب)</td></tr>
<tr><td style="padding: 8px;"><strong>نوع احتراق</strong></td><td style="padding: 8px;">شمعک دائم (پیلوت‌دار)</td></tr>
<tr><td style="padding: 8px;"><strong>سیستم‌های ایمنی</strong></td><td style="padding: 8px;">سنسور دودکش، ترموستات حد، ترموکوپل ایمنی</td></tr>
<tr><td style="padding: 8px;"><strong>گارانتی و خدمات</strong></td><td style="padding: 8px;">۲۴ ماه ضمانت رسمی شرکت ایران شرق</td></tr>
</tbody>
</table>

<p>شما می‌توانید این محصول بادوام را با تضمین اصالت و بهترین قیمت بازار از <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> تهیه نمایید و در صورت حضور در <strong>اهواز</strong> از خدمات و پشتیبانی شعب حضوری بهره‌مند شوید.</p>"""

    payload_is = {
        'name': 'آبگرمکن دیواری شمعک دار ایران شرق مدل 3020',
        'slug': 'iran-shargh-3020-kiana-gas-water-heater',
        'type': 'simple',
        'status': 'publish',
        'catalog_visibility': 'visible',
        'description': is_desc,
        'short_description': is_short,
        'categories': [{'id': 241}],
        'images': [{'id': mid_is}] if mid_is else [],
        'manage_stock': False,
        'stock_status': 'outofstock',
        'attributes': [
            {'name': 'برند', 'visible': True, 'variation': False, 'options': ['ایران شرق']},
            {'name': 'مدل', 'visible': True, 'variation': False, 'options': ['3020 (کیانا)']},
            {'name': 'نوع آبگرمکن', 'visible': True, 'variation': False, 'options': ['دیواری فوری شمعک‌دار']},
            {'name': 'ظرفیت تامین آب گرم', 'visible': True, 'variation': False, 'options': ['۱۳ لیتر در دقیقه']},
            {'name': 'حداقل فشار آب', 'visible': True, 'variation': False, 'options': ['۰.۱۵ بار (فشار کم)']},
            {'name': 'ظرفیت حرارتی', 'visible': True, 'variation': False, 'options': ['۱۸,۰۰۰ کیلوکالری بر ساعت']}
        ]
    }
    prod_is = create_wc_product(payload_is)
    if prod_is:
        ws_heat = wb['سرمایش و گرمایش']
        ws_heat.cell(37, 8).value = '✗ ناموجود'
        ws_heat.cell(37, 15).value = prod_is['id']
        ws_heat.cell(37, 16).value = f"https://hosseinykala.ir/product/{prod_is['slug']}/"
        ws_heat.cell(37, 18).value = 'ثبت‌شده در سایت'
        print(f"✓ Row 37 (سرمایش و گرمایش - آبگرمکن ایران شرق 3020) synced in sheet.")

    # ----------------------------------------------------
    # 3. بخاری گازی کابینتی آبسال مدل 405
    # ----------------------------------------------------
    print("\n--- 3. Absal 405 Radiant Gas Heater ---")
    img_absal = os.path.join(PROJECT_DIR, r'new_product_images\سرمایش و گرمایش\بخاری گازی کابینتی آبسال مدل 405\main.jpg')
    mid_absal, _ = upload_media_file(img_absal, 'بخاری گازی کابینتی آبسال مدل 405', 'عکس بخاری گازی بدون دودکش تابشی سرامیکی آبسال مدل 405')
    
    absal_short = """<ul>
<li><strong>نوع بخاری:</strong> بدون دودکش تابشی و سرامیکی با رده انرژی بسیار بهینه A</li>
<li><strong>بازده حرارتی بالا:</strong> راندمان گرمایشی بیش از ۹۰.۴ درصد بدون اتلاف انرژی</li>
<li><strong>تنظیم حرارت سه‌حالته:</strong> قابلیت تنظیم توان در ۳ وضعیت کم (۱۵۰۰)، متوسط (۲۷۰۰) و زیاد (۳۹۰۰ کیلوکالری)</li>
<li><strong>سیستم ایمنی پیشرفته ODS:</strong> سنسور حساس به اکسیژن جهت قطع خودکار گاز در صورت افت اکسیژن زیر ۱۸٪</li>
<li><strong>مشعل سرامیکی تابشی:</strong> گرمایش سریع و یکنواخت محیط با پنل‌های سرامیکی بادوام و جرقه زن پیزوالکتریک</li>
<li><strong>گارانتی و اصالت:</strong> ۲ سال گارانتی رسمی شرکت آبسال و تضمین اصالت کالا در حسینی کالا</li>
</ul>"""

    absal_desc = """<h2>بررسی تخصصی و راهنمای خرید بخاری گازی کابینتی آبسال مدل 405</h2>
<p>گرمایش سریع، بدون دردسر لوله‌کشی و دودکش، همراه با بالاترین راندمان حرارتی، مزیت اصلی بخاری‌های تابشی بدون دودکش است. <strong>بخاری گازی کابینتی آبسال مدل 405</strong> تولید شده توسط شرکت باسابقه و معتبر <strong>آبسال (Aabsal)</strong>، گزینه‌ای بی‌نظیر برای فضاهای خانگی، دفاتر اداری و مغازه‌ها با تهویه هوای مناسب است.</p>

<h3>ویژگی‌های متمایز بخاری سرامیکی آبسال ۴۰۵</h3>
<ul>
<li><strong>سیستم ایمنی هوشمند ODS:</strong> ایمنی مهم‌ترین فاکتور در بخاری‌های بدون دودکش است. سنسور ODS میزان اکسیژن محیط را به طور پیوسته ارزیابی کرده و در صورتی که اکسیژن به کمتر از ۱۸ درصد برسد، فوراً جریان گاز را به صورت قطعی مسدود می‌کند.</li>
<li><strong>ترموکوپل ایمنی و گاورنر تثبیت فشار:</strong> ترموکوپل در صورت خاموش شدن ناخواسته پیلوت، گاز را قطع می‌کند. همچنین گاورنر نوسانات شدید فشار گاز ورودی را مهار و یکنواخت می‌سازد.</li>
<li><strong>بازده حرارتی ۹۰.۴ درصدی:</strong> از آنجا که نیازی به اتلاف حرارت از طریق لوله دودکش نیست، نزدیک به تمامی گرمای حاصل از گاز شهری وارد محیط می‌شود که موجب صرفه‌جویی محسوس در مصرف سوخت خواهد شد.</li>
<li><strong>بدنه فلزی بادوام با رنگ کوره‌ای:</strong> پوشش رنگ الکترواستاتیک ضد حرارت و بخش بالایی لعاب‌کاری‌شده مقاومت بدنه را در برابر زنگ‌زدگی و خط‌وخش برای سال‌ها حفظ می‌کند.</li>
</ul>

<h2>جدول مشخصات فنی بخاری گازی آبسال مدل 405</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">آبسال (Aabsal)</td></tr>
<tr><td style="padding: 8px;"><strong>مدل</strong></td><td style="padding: 8px;">405</td></tr>
<tr><td style="padding: 8px;"><strong>نوع دستگاه</strong></td><td style="padding: 8px;">بخاری گازی بدون دودکش تابشی (سرامیکی)</td></tr>
<tr><td style="padding: 8px;"><strong>رده مصرف انرژی</strong></td><td style="padding: 8px;">رده A (فوق‌العاده کم‌مصرف)</td></tr>
<tr><td style="padding: 8px;"><strong>بازده حرارتی</strong></td><td style="padding: 8px;">۹۰.۴ درصد</td></tr>
<tr><td style="padding: 8px;"><strong>ظرفیت گرمادهی</strong></td><td style="padding: 8px;">۱۵۰۰ تا ۳۹۰۰ کیلوکالری در ساعت (۳ وضعیت)</td></tr>
<tr><td style="padding: 8px;"><strong>سیستم ایمنی اکسیژن (ODS)</strong></td><td style="padding: 8px;">دارد (قطع خودکار در افت اکسیژن)</td></tr>
<tr><td style="padding: 8px;"><strong>سیستم جرقه زن</strong></td><td style="padding: 8px;">پیزوالکتریک (روشن شدن آسان بدون کبریت)</td></tr>
<tr><td style="padding: 8px;"><strong>ابعاد (ارتفاع×پهنا×عمق)</strong></td><td style="padding: 8px;">۵۷.۴ × ۴۳.۵ × ۳۱.۲ سانتی‌متر</td></tr>
<tr><td style="padding: 8px;"><strong>وزن</strong></td><td style="padding: 8px;">۷.۵ کیلوگرم (سبک با جابه‌جایی راحت)</td></tr>
<tr><td style="padding: 8px;"><strong>گارانتی</strong></td><td style="padding: 8px;">۲۴ ماه ضمانت رسمی شرکت آبسال</td></tr>
</tbody>
</table>

<p>شما عزیزان می‌توانید این محصول استاندارد و ایمن را با اطمینان خاطر از <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> اهواز به صورت آنلاین یا با مراجعه حضوری به شعب فروشگاه تهیه فرمایید.</p>"""

    payload_absal = {
        'name': 'بخاری گازی کابینتی آبسال مدل 405',
        'slug': 'absal-405-flueless-radiant-gas-heater',
        'type': 'simple',
        'status': 'publish',
        'catalog_visibility': 'visible',
        'description': absal_desc,
        'short_description': absal_short,
        'categories': [{'id': 241}, {'id': 214}],
        'images': [{'id': mid_absal}] if mid_absal else [],
        'manage_stock': False,
        'stock_status': 'outofstock',
        'attributes': [
            {'name': 'برند', 'visible': True, 'variation': False, 'options': ['آبسال (Aabsal)']},
            {'name': 'مدل', 'visible': True, 'variation': False, 'options': ['405']},
            {'name': 'نوع بخاری', 'visible': True, 'variation': False, 'options': ['بدون دودکش تابشی سرامیکی']},
            {'name': 'رده انرژی', 'visible': True, 'variation': False, 'options': ['A']},
            {'name': 'سیستم ایمنی اکسیژن (ODS)', 'visible': True, 'variation': False, 'options': ['دارد']},
            {'name': 'ظرفیت گرمادهی', 'visible': True, 'variation': False, 'options': ['۳۹۰۰ کیلوکالری بر ساعت']}
        ]
    }
    prod_absal = create_wc_product(payload_absal)
    if prod_absal:
        ws_heat = wb['سرمایش و گرمایش']
        ws_heat.cell(39, 8).value = '✗ ناموجود'
        ws_heat.cell(39, 15).value = prod_absal['id']
        ws_heat.cell(39, 16).value = f"https://hosseinykala.ir/product/{prod_absal['slug']}/"
        ws_heat.cell(39, 18).value = 'ثبت‌شده در سایت'
        print(f"✓ Row 39 (سرمایش و گرمایش - بخاری آبسال 405) synced in sheet.")

    wb.save(CATALOG_PATH)
    print("\n✓ Batch 1 successfully synced and saved to hosseiny_kala_catalog.xlsx!")

if __name__ == '__main__':
    run_batch_1()

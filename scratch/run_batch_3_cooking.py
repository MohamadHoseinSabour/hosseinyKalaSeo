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

def run_batch_3_cooking():
    print("==================================================")
    print("STARTING BATCH 3 (لوازم برقی و پخت و پز) CREATION")
    print("==================================================")
    
    wb = openpyxl.load_workbook(CATALOG_PATH, data_only=False)
    ws = wb['لوازم برقی و پخت و پز']

    # 1. تنوع خردکن کاسه دار ویلز مدل 6033 سه لیتری (Row 79, Parent 4106)
    print("\n--- 1. Vills 6033 3-Liter Chopper Variation (Row 79) ---")
    img_vills = os.path.join(PROJECT_DIR, r'new_product_images\لوازم برقی و پخت و پز\خردکن برقی کاسه دار ویلز مدل 6033 سه لیتری\560x560.webp')
    mid_vills = upload_media_file(img_vills, 'خردکن کاسه دار ویلز مدل 6033 سه لیتری', 'عکس خردکن برقی کاسه پیرکس ۳ لیتری ویلز مدل 6033')
    
    # Update parent product 4106 attribute options
    try:
        r_p = SESSION.get('https://hosseinykala.ir/wp-json/wc/v3/products/4106', auth=AUTH, headers=HEADERS, timeout=30)
        if r_p.status_code == 200:
            parent_data = r_p.json()
            attrs = parent_data.get('attributes', [])
            found = False
            for attr in attrs:
                if attr.get('name') == 'مدل':
                    if '6033 سه لیتری' not in attr.get('options', []):
                        attr['options'].append('6033 سه لیتری')
                    found = True
                    break
            if not found:
                attrs.append({'name': 'مدل', 'visible': True, 'variation': True, 'options': ['6031 استیل', '6032 سه لیتری', '6033 سه لیتری']})
            SESSION.put('https://hosseinykala.ir/wp-json/wc/v3/products/4106', auth=AUTH, headers=HEADERS, json={'attributes': attrs}, timeout=30)
            print("  ✓ Parent product 4106 attributes updated with '6033 سه لیتری'")
    except Exception as e:
        print(f"  ❌ Error updating parent attributes: {e}")

    payload_vills_var = {
        'manage_stock': False,
        'stock_status': 'outofstock',
        'image': {'id': mid_vills} if mid_vills else None,
        'attributes': [
            {'name': 'مدل', 'option': '6033 سه لیتری'}
        ]
    }
    var_vills = create_wc_variation(4106, payload_vills_var)
    if var_vills:
        ws.cell(79, 8).value = '✗ ناموجود'
        ws.cell(79, 15).value = var_vills['id']
        ws.cell(79, 16).value = 'https://hosseinykala.ir/product/willez-electric-bowl-chopper/'
        ws.cell(79, 18).value = 'ثبت‌شده در سایت'
        wb.save(CATALOG_PATH)
        print("✓ Row 79 (خردکن ویلز 6033) synced in sheet.")

    time.sleep(2)

    # 2. گوشت کوب برقی رترو وستینگهاوس قرمز (Row 55)
    print("\n--- 2. Westinghouse Retro Hand Blender Red (Row 55) ---")
    img_west = os.path.join(PROJECT_DIR, r'new_product_images\لوازم برقی و پخت و پز\گوشت کوب برقی رترو وستینگهاوس - قرمز\584d2e817d7438b717ea9f9a8c567180911c5a47_1752677357.jpg')
    mid_west = upload_media_file(img_west, 'گوشت کوب برقی رترو وستینگهاوس قرمز مدل WKHB101RD', 'عکس گوشت کوب برقی کلاسیک رترو قرمز وستینگهاوس')

    west_short = """<ul>
<li><strong>طراحی نوستالژیک سری رترو:</strong> بدنه ارگونومیک با رنگ قرمز متالیک کلاسیک و جلوه بصری خاص</li>
<li><strong>تیغه ۴ پره استیل ضدزنگ:</strong> تکنولوژی ضدپاشش (Anti-Splash) جهت میکس یکدست انواع سوپ و پوره</li>
<li><strong>موتور تمام مس قدرتمند:</strong> موتور پرتوان با لرزش و صدای بسیار کم جهت عملکرد مداوم</li>
<li><strong>کنترل سرعت متغیر + توربو:</strong> تنظیم پیوسته دور چرخش به همراه کلید توربو برای مواد سخت‌تر</li>
<li><strong>پایه تمام استیل جداشونده:</strong> شستشوی آسان و امکان قرارگیری در ماشین ظرفشویی</li>
<li><strong>ضمانت اصالت فیزیکی:</strong> تضمین ۱۰۰٪ سلامت و اصالت کالا از فروشگاه حسینی کالا اهواز</li>
</ul>"""

    west_desc = """<h2>بررسی تخصصی و راهنمای خرید گوشت‌کوب برقی رترو وستینگهاوس قرمز</h2>
<p>ترکیب استایل وینتیج دهه ۵۰ میلادی و فناوری مهندسی مدرن، سری رترو برند <strong>وستینگهاوس (Westinghouse)</strong> را به یکی از محبوب‌ترین تجهیزات آشپزخانه‌های مدرن تبدیل کرده است. <strong>گوشت کوب برقی رترو وستینگهاوس قرمز</strong>، ابزاری سبک، کارآمد و چشم‌نواز است که با قدرت بالای خود عملیات پوره کردن، له کردن، میکس و تهیه اسموتی‌ها را در کمترین زمان ممکن می‌سازد.</p>

<h3>ویژگی‌های متمایز گوشت‌کوب رترو وستینگهاوس</h3>
<ul>
<li><strong>طراحی ارگونومیک و ارگونومی دستگیره:</strong> انحنای بدنه متناسب با فرم دست طراحی شده و پوشش نرم Soft-Touch مانع از لیز خوردن دستگاه حتی با دست خیس می‌شود.</li>
<li><strong>سیستم ضدپاشش (Anti-Splash Blade Guard):</strong> کلاهک فلزی محافظ تیغه به گونه‌ای زاویه‌بندی شده است که مواد غذایی داغ حین هم‌زدن به بیرون ظرف نپاشد.</li>
<li><strong>پایه استیل فودگرید:</strong> میله و پایه این دستگاه از استیل مقاوم در برابر زنگ‌زدگی و اسید مواد غذایی ساخته شده و برای پوره کردن سوپ‌های داغ درون قابلمه کاملاً ایمن است.</li>
<li><strong>تنظیم دور ولومی + حالت توربو:</strong> امکان انتخاب دور آرام برای سس و مایونز و دور حداکثری توربو برای آماده‌سازی اسموتی یخ‌زده.</li>
</ul>

<h2>جدول مشخصات فنی گوشت‌کوب برقی رترو وستینگهاوس</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">وستینگهاوس (Westinghouse)</td></tr>
<tr><td style="padding: 8px;"><strong>سری ساخت</strong></td><td style="padding: 8px;">رترو (Retro Series)</td></tr>
<tr><td style="padding: 8px;"><strong>رنگ‌بندی</strong></td><td style="padding: 8px;">قرمز متالیک رترو</td></tr>
<tr><td style="padding: 8px;"><strong>جنس بدنه</strong></td><td style="padding: 8px;">پلیمر مقاوم ABS با دستگیره ارگونومیک</td></tr>
<tr><td style="padding: 8px;"><strong>جنس میله و تیغه</strong></td><td style="padding: 8px;">استیل ضدزنگ SUS فودگرید</td></tr>
<tr><td style="padding: 8px;"><strong>عملکرد توربو</strong></td><td style="padding: 8px;">دارد (Turbo Function)</td></tr>
<tr><td style="padding: 8px;"><strong>تنظیمات سرعت</strong></td><td style="padding: 8px;">ولوم متغیر پیوسته</td></tr>
<tr><td style="padding: 8px;"><strong>گارانتی و اصالت</strong></td><td style="padding: 8px;">ضمانت اصالت و سلامت فیزیکی از حسینی کالا</td></tr>
</tbody>
</table>

<p>شما می‌توانید این محصول زیبا و باکیفیت را با بهترین قیمت از <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> اهواز به صورت آنلاین یا با مراجعه حضوری تهیه نمایید.</p>"""

    payload_west = {
        'name': 'گوشت کوب برقی رترو وستینگهاوس قرمز',
        'slug': 'westinghouse-retro-hand-blender-red',
        'type': 'simple',
        'status': 'publish',
        'catalog_visibility': 'visible',
        'description': west_desc,
        'short_description': west_short,
        'categories': [{'id': 216}, {'id': 122}],
        'images': [{'id': mid_west}] if mid_west else [],
        'manage_stock': False,
        'stock_status': 'outofstock',
        'attributes': [
            {'name': 'برند', 'visible': True, 'variation': False, 'options': ['وستینگهاوس (Westinghouse)']},
            {'name': 'رنگ', 'visible': True, 'variation': False, 'options': ['قرمز']},
            {'name': 'سری', 'visible': True, 'variation': False, 'options': ['رترو (Retro)']},
            {'name': 'جنس تیغه و میله', 'visible': True, 'variation': False, 'options': ['استیل ضدزنگ']},
            {'name': 'کلید توربو', 'visible': True, 'variation': False, 'options': ['دارد']}
        ]
    }
    prod_west = create_wc_product(payload_west)
    if prod_west:
        ws.cell(55, 8).value = '✗ ناموجود'
        ws.cell(55, 15).value = prod_west['id']
        ws.cell(55, 16).value = f"https://hosseinykala.ir/product/{prod_west['slug']}/"
        ws.cell(55, 18).value = 'ثبت‌شده در سایت'
        wb.save(CATALOG_PATH)
        print("✓ Row 55 (گوشت‌کوب رترو وستینگهاوس) synced in sheet.")

    time.sleep(2)

    # 3. خردکن برقی ۲ کاسه زیکو مدل 70028 (Row 97)
    print("\n--- 3. Zico ZC-7028 Double Bowl Chopper (Row 97) ---")
    img_ziko_ch = os.path.join(PROJECT_DIR, r'new_product_images\لوازم برقی و پخت و پز\خردکن برقی ۲ کاسه زیکو مدل 70028\BO1DW7xtHUQZ4xZT.webp')
    mid_ziko_ch = upload_media_file(img_ziko_ch, 'خردکن برقی ۲ کاسه زیکو مدل ZC-7028 با تیغه تیتانیوم', 'عکس خردکن برقی دو کاسه پیرکس و استیل زیکو مدل 70028')

    ziko_ch_short = """<ul>
<li><strong>دو کاسه مجزا پیرکس و استیل:</strong> همراه با یک کاسه شیشه‌ای پیرکس شفاف و یک کاسه تمام استیل نشکن</li>
<li><strong>موتور تمام مس ۸۰۰ وات:</strong> موتور قدرتمند سیم‌پیچ مسی با ۳ دور سرعت مختلف متناسب با نوع مواد غذایی</li>
<li><strong>تیغه‌های تیتانیومی طلایی:</strong> تیغه‌های ۶ پره ضخیم تیتانیومی با برندگی لیزری ماندگار</li>
<li><strong>چرخ‌دنده‌های اتصال فولادی:</strong> کوپلینگ تمام فلز بادوام بدون ساییدگی زیر فشار مواد سخت</li>
<li><strong>لوازم کاربردی همراه:</strong> مجهز به سری سیرپوست‌کن سیلیکونی، همزن سس و تخم‌مرغ و کاردک</li>
<li><strong>تضمین اصالت:</strong> ضمانت اصالت ۱۰۰٪ فیزیکی کالا از فروشگاه حسینی کالا اهواز</li>
</ul>"""

    ziko_ch_desc = """<h2>بررسی تخصصی و راهنمای خرید خردکن برقی ۲ کاسه زیکو مدل ZC-7028</h2>
<p>داشتن دو کاسه مجزا برای یک خردکن برقی آشپزخانه، بزرگترین مزیت بهداشتی و کاربردی است؛ شما می‌توانید بدون معطلی و نیاز به شستشوی سریع کاسه در میانه آشپزی، در یک کاسه گوشت و مرغ را چرخ کنید و در کاسه دیگر سبزیجات، پیاز و سالاد را آماده نمایید. <strong>خردکن برقی ۲ کاسه زیکو مدل 70028</strong> (کد <strong>ZC-7028</strong>) از برند محبوب <strong>زیکو (ZICO)</strong>، مجهز به یک کاسه پیرکس شفاف و یک کاسه استیل نشکن ضدزنگ است.</p>

<h3>ویژگی‌های شاخص خردکن ۲ کاسه زیکو</h3>
<ul>
<li><strong>کاسه شیشه‌ای پیرکس ضخیم + کاسه استیل SUS:</strong> کاسه پیرکس برای مشاهده بافت مواد و خرد کردن سبزیجات و پیاز عالی است و کاسه استیل برای چرخ کردن بدون خط‌وخش گوشت‌های سخت و تکه‌های یخ به کار می‌رود.</li>
<li><strong>تیغه‌های تیتانیومی ۶ پره نانوتک:</strong> روکش تیتانیوم طلایی تیغه‌ها مانع از کند شدن، تغییر رنگ و اکسیداسیون در تماس با پیاز و مواد اسیدی می‌شود.</li>
<li><strong>۳ سرعت چرخش با دکمه‌های مجزا:</strong> سرعت ۱ برای سبزی‌های نرم و گوجه، سرعت ۲ برای میوه‌ها و پیاز، و سرعت ۳ برای گوشت و مغزیجات.</li>
<li><strong>اتصال کوپلینگ فلز به فلز:</strong> چرخ‌دنده‌های موتور و شفت تیغه از آلیاژ فولادی ساخته شده‌اند تا برخلاف مدل‌های پلاستیکی زیر بارهای سنگین دچار هرزگردی نشوند.</li>
</ul>

<h2>جدول مشخصات فنی خردکن برقی ۲ کاسه زیکو مدل ZC-7028</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">زیکو (ZICO)</td></tr>
<tr><td style="padding: 8px;"><strong>مدل</strong></td><td style="padding: 8px;">ZC-7028 (70028)</td></tr>
<tr><td style="padding: 8px;"><strong>توان موتور</strong></td><td style="padding: 8px;">۸۰۰ وات (موتور تمام مس با گشتاور بالا)</td></tr>
<tr><td style="padding: 8px;"><strong>تعداد کاسه‌ها</strong></td><td style="padding: 8px;">۲ عدد (۱ کاسه پیرکس شیشه‌ای + ۱ کاسه استیل نشکن)</td></tr>
<tr><td style="padding: 8px;"><strong>نوع تیغه‌ها</strong></td><td style="padding: 8px;">۶ پره تیتانیوم طلایی دولایه</td></tr>
<tr><td style="padding: 8px;"><strong>تنظیمات سرعت</strong></td><td style="padding: 8px;">۳ سرعته با کلیدهای تفکیک‌شده</td></tr>
<tr><td style="padding: 8px;"><strong>اقلام جانبی</strong></td><td style="padding: 8px;">سری سیرپوست‌کن، پره همزن، کاردک و لاستیک لرزه‌گیر</td></tr>
<tr><td style="padding: 8px;"><strong>گارانتی و اصالت</strong></td><td style="padding: 8px;">ضمانت اصالت و سلامت کالا از حسینی کالا</td></tr>
</tbody>
</table>

<p>این خردکن فوق‌العاده کاربردی را با ضمانت اصالت و بهترین قیمت از <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> اهواز به صورت حضوری یا ثبت سفارش آنلاین خریداری کنید.</p>"""

    payload_ziko_ch = {
        'name': 'خردکن برقی ۲ کاسه زیکو مدل 70028',
        'slug': 'ziko-zc7028-double-bowl-electric-chopper',
        'type': 'simple',
        'status': 'publish',
        'catalog_visibility': 'visible',
        'description': ziko_ch_desc,
        'short_description': ziko_ch_short,
        'categories': [{'id': 216}],
        'images': [{'id': mid_ziko_ch}] if mid_ziko_ch else [],
        'manage_stock': False,
        'stock_status': 'outofstock',
        'attributes': [
            {'name': 'برند', 'visible': True, 'variation': False, 'options': ['زیکو (ZICO)']},
            {'name': 'مدل', 'visible': True, 'variation': False, 'options': ['ZC-7028 (70028)']},
            {'name': 'تعداد کاسه', 'visible': True, 'variation': False, 'options': ['۲ کاسه (پیرکس + استیل)']},
            {'name': 'نوع تیغه', 'visible': True, 'variation': False, 'options': ['۶ پره تیتانیوم طلایی']},
            {'name': 'توان مصرفی', 'visible': True, 'variation': False, 'options': ['۸۰۰ وات']},
            {'name': 'تعداد سرعت', 'visible': True, 'variation': False, 'options': ['۳ سرعته']}
        ]
    }
    prod_ziko_ch = create_wc_product(payload_ziko_ch)
    if prod_ziko_ch:
        ws.cell(97, 8).value = '✗ ناموجود'
        ws.cell(97, 15).value = prod_ziko_ch['id']
        ws.cell(97, 16).value = f"https://hosseinykala.ir/product/{prod_ziko_ch['slug']}/"
        ws.cell(97, 18).value = 'ثبت‌شده در سایت'
        wb.save(CATALOG_PATH)
        print("✓ Row 97 (خردکن ۲ کاسه زیکو) synced in sheet.")

    time.sleep(2)

    # 4. خردکن برقی بوش (Row 99)
    print("\n--- 4. Bosch Glass Bowl Chopper (Row 99) ---")
    img_bosch = os.path.join(PROJECT_DIR, r'new_product_images\لوازم برقی و پخت و پز\خردکن برقی بوش\main.jpg')
    mid_bosch = upload_media_file(img_bosch, 'خردکن برقی کاسه پیرکس بوش', 'عکس خردکن برقی کاسه دار پیرکس بوش با تیغه استیل')

    bosch_short = """<ul>
<li><strong>کاسه پیرکس ضخیم مدرج:</strong> شیشه باکیفیت و بهداشتی ضدبو با مقاومت در برابر حرارت</li>
<li><strong>تیغه دولایه استیل ضدزنگ:</strong> تیغه‌های تیز با فناوری لیزری برای خردایش یکدست مواد غذایی</li>
<li><strong>موتور فشاری آسان (Push-Down):</strong> شروع به کار ساده و مطمئن تنها با فشردن موتور از بالا</li>
<li><strong>پایه لاستیکی ضدلغزش:</strong> پایداری کامل روی صفحه کابینت حین خرد کردن گوشت و سبزی</li>
<li><strong>شستشوی آسان:</strong> قطعات جداشونده و ایمن برای ماشین ظرفشویی</li>
<li><strong>ضمانت اصالت:</strong> تضمین اصالت و سلامت از فروشگاه لوازم خانگی حسینی اهواز</li>
</ul>"""

    bosch_desc = """<h2>بررسی تخصصی و راهنمای خرید خردکن برقی کاسه‌دار بوش</h2>
<p>سرعت و یکدستی در خرد کردن پیاز، سبزیجات، دانه‌ها و قطعات گوشت، آماده‌سازی غذاهای روزمره را چندین برابر سریع‌تر و لذت‌بخش‌تر می‌کند. <strong>خردکن برقی بوش</strong> با کاسه شیشه‌ای پیرکس بهداشتی و تیغه‌های دولایه برنده، یکی از دم‌دستی‌ترین و کارآمدترین ابزارهای آشپزخانه است.</p>

<h3>ویژگی‌های کلیدی خردکن بوش</h3>
<ul>
<li><strong>کاسه شیشه‌ای بهداشتی و مقاوم:</strong> کاسه شیشه‌ای این خردکن مانع از جذب بو و رنگ مواد غذایی مانند سیر یا زردچوبه می‌شود و طعم خالص مواد را حفظ می‌کند.</li>
<li><strong>طراحی مکانیزم فشاری ایمن:</strong> بدون پیچیدگی و دکمه‌های متعدد؛ با فشردن ملایم بخش بالایی موتور، تیغه‌ها با قدرت شروع به چرخش کرده و با برداشتن دست بلافاصله متوقف می‌شوند.</li>
<li><strong>تیغه‌های دولایه برنده:</strong> استقرار ۴ پره تیغه در دو ارتفاع متفاوت باعث می‌شود تا مواد غذایی از کف تا بالای کاسه به طور یکنواخت خرد شده و له نشوند.</li>
<li><strong>نظافت سریع:</strong> تمامی قطعات کاسه، درپوش و تیغه‌ها به راحتی جدا شده و قابلیت شستشو در ماشین ظرفشویی را دارند.</li>
</ul>

<h2>جدول مشخصات فنی خردکن برقی بوش</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">بوش (Bosch)</td></tr>
<tr><td style="padding: 8px;"><strong>نوع دستگاه</strong></td><td style="padding: 8px;">خردکن برقی کاسه‌دار</td></tr>
<tr><td style="padding: 8px;"><strong>جنس کاسه</strong></td><td style="padding: 8px;">پیرکس شیشه‌ای مقاوم و مدرج</td></tr>
<tr><td style="padding: 8px;"><strong>جنس تیغه</strong></td><td style="padding: 8px;">استیل ضدزنگ دولایه (۴ پره)</td></tr>
<tr><td style="padding: 8px;"><strong>نحوه عملکرد</strong></td><td style="padding: 8px;">فشاری ارگونومیک (Push-Down)</td></tr>
<tr><td style="padding: 8px;"><strong>پایه ضدلغزش</strong></td><td style="padding: 8px;">دارد (حلقه لاستیکی لرزه‌گیر)</td></tr>
<tr><td style="padding: 8px;"><strong>گارانتی و اصالت</strong></td><td style="padding: 8px;">ضمانت اصالت و سلامت فیزیکی از حسینی کالا</td></tr>
</tbody>
</table>

<p>خرید این خردکن برقی با اطمینان از اصالت و مناسب‌ترین قیمت در <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> اهواز به صورت آنلاین یا مراجعه حضوری در دسترس شماست.</p>"""

    payload_bosch = {
        'name': 'خردکن برقی کاسه پیرکس بوش',
        'slug': 'bosch-glass-bowl-electric-food-chopper',
        'type': 'simple',
        'status': 'publish',
        'catalog_visibility': 'visible',
        'description': bosch_desc,
        'short_description': bosch_short,
        'categories': [{'id': 216}],
        'images': [{'id': mid_bosch}] if mid_bosch else [],
        'manage_stock': False,
        'stock_status': 'outofstock',
        'attributes': [
            {'name': 'برند', 'visible': True, 'variation': False, 'options': ['بوش (Bosch)']},
            {'name': 'جنس کاسه', 'visible': True, 'variation': False, 'options': ['پیرکس شیشه‌ای']},
            {'name': 'جنس تیغه', 'visible': True, 'variation': False, 'options': ['استیل ضدزنگ دولایه']},
            {'name': 'نحوه عملکرد', 'visible': True, 'variation': False, 'options': ['دکمه فشاری']}
        ]
    }
    prod_bosch = create_wc_product(payload_bosch)
    if prod_bosch:
        ws.cell(99, 8).value = '✗ ناموجود'
        ws.cell(99, 15).value = prod_bosch['id']
        ws.cell(99, 16).value = f"https://hosseinykala.ir/product/{prod_bosch['slug']}/"
        ws.cell(99, 18).value = 'ثبت‌شده در سایت'
        wb.save(CATALOG_PATH)
        print("✓ Row 99 (خردکن برقی بوش) synced in sheet.")

    time.sleep(2)

    # 5. میوه خشک کن مایر مدل 5959 (Row 101)
    print("\n--- 5. Maier MR-5959 Food Dehydrator (Row 101) ---")
    img_maier_fd = os.path.join(PROJECT_DIR, r'new_product_images\لوازم برقی و پخت و پز\میوه خشک کن مایر مدل 5959\b3693b97b92c42ce38e9c52967ab56500695f9f7_1601483993.jpg')
    mid_maier_fd = upload_media_file(img_maier_fd, 'میوه خشک کن دیجیتال مایر مدل MR-5959', 'عکس میوه و سبزی خشک کن ۵ طبقه دیجیتال مایر مدل 5959')

    maier_fd_short = """<ul>
<li><strong>۵ طبقه شفاف با ارتفاع قابل تنظیم:</strong> امکان چیدمان حجم زیاد انواع اسلایس‌های میوه و سبزیجات</li>
<li><strong>کنترل پنل دیجیتال با نمایشگر LED:</strong> تنظیم دقیق درجه حرارت و زمان با کلیدهای لمسی</li>
<li><strong>تنظیم دما بین ۳۵ تا ۷۰ درجه:</strong> دمای سفارشی برای خشک کردن گوشت، سبزی، قارچ، لواشک و انواع میوه</li>
<li><strong>تایمر هوشمند ۲۴ ساعته:</strong> مجهز به زمان‌سنج دیجیتالی با سیستم قطع‌کن و خاموشی خودکار</li>
<li><strong>گردش هوای یکنواخت ۳۶۰ درجه:</strong> توزیع بهینه گرما بدون نیاز به جابجایی مداوم سینی‌ها</li>
<li><strong>ضمانت اصالت:</strong> ضمانت اصالت ۱۰۰٪ کالا از فروشگاه لوازم خانگی حسینی اهواز</li>
</ul>"""

    maier_fd_desc = """<h2>بررسی تخصصی و راهنمای خرید میوه خشک‌کن دیجیتال مایر مدل MR-5959</h2>
<p>تهیه چیپس میوه‌های سالم و خوش‌رنگ، خشک کردن سبزی‌های معطر محلی و تهیه لواشک‌های بهداشتی بدون مواد افزودنی در منزل، با <strong>میوه خشک کن مایر مدل MR-5959</strong> کاری ساده و دلپذیر است. برند معتبر <strong>مایر (Maier)</strong> با عرضه این مدل دیجیتال ۵ طبقه، ابزاری کم‌مصرف و بی‌صدا را برای دوستداران تغذیه سالم فراهم کرده است.</p>

<h3>ویژگی‌های متمایز میوه خشک‌کن مایر ۵۹۵۹</h3>
<ul>
<li><strong>سیستم همرفت هوای گرم ۳۶۰ درجه:</strong> المنت‌های حرارتی و فن تعبیه‌شده در پایه، جریان هوای گرم یکنواختی را در تمامی طبقات به گردش درمی‌آورند تا میوه‌ها بدون سوختن یا از دست دادن رنگ طبیعی خود به آرامی خشک شوند.</li>
<li><strong>تنظیم دمای دیجیتالی دقیق (۳۵ تا ۷۰ درجه سانتی‌گراد):</strong> شما می‌توانید متناسب با حساسیت ماده غذایی (مانند دمای پایین برای سبزی و گیاهان دارویی یا دمای بالاتر برای سیب، موز و پرتقال) دما را تعیین نمایید.</li>
<li><strong>سینی‌های فودگرید بدون BPA:</strong> طبقات دستگاه از پلاستیک مقاوم به حرارت و بدون مواد مضر ساخته شده‌اند و به راحتی با آب و شوینده ملایم تمیز می‌شوند.</li>
<li><strong>تایمر دیجیتال اتوماتیک:</strong> با تنظیم زمان دلخواه تا ۲۴ ساعت، دستگاه پس از اتمام فرآیند به صورت خودکار خاموش شده و از خشک شدن بیش از حد مواد جلوگیری می‌کند.</li>
</ul>

<h2>جدول مشخصات فنی میوه خشک‌کن مایر مدل MR-5959</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">مایر (Maier)</td></tr>
<tr><td style="padding: 8px;"><strong>مدل</strong></td><td style="padding: 8px;">MR-5959</td></tr>
<tr><td style="padding: 8px;"><strong>تعداد طبقات</strong></td><td style="padding: 8px;">۵ طبقه مجزا با ارتفاع قابل تنظیم</td></tr>
<tr><td style="padding: 8px;"><strong>محدوده تنظیم دما</strong></td><td style="padding: 8px;">۳۵ تا ۷۰ درجه سانتی‌گراد</td></tr>
<tr><td style="padding: 8px;"><strong>تایمر دیجیتال</strong></td><td style="padding: 8px;">تا ۲۴ ساعت با خاموشی خودکار</td></tr>
<tr><td style="padding: 8px;"><strong>صفحه نمایش</strong></td><td style="padding: 8px;">دیجیتال LED خوانا</td></tr>
<tr><td style="padding: 8px;"><strong>جنس سینی‌ها</strong></td><td style="padding: 8px;">پلاستیک فودگرید شفاف مقاوم</td></tr>
<tr><td style="padding: 8px;"><strong>گارانتی و اصالت</strong></td><td style="padding: 8px;">ضمانت اصالت و سلامت از حسینی کالا</td></tr>
</tbody>
</table>

<p>شما می‌توانید این میوه خشک‌کن پرطرفدار را با بهترین قیمت و ضمانت معتبر از <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> اهواز به صورت آنلاین یا حضوری تهیه فرمایید.</p>"""

    payload_maier_fd = {
        'name': 'میوه خشک کن مایر مدل 5959',
        'slug': 'maier-mr5959-digital-food-dehydrator',
        'type': 'simple',
        'status': 'publish',
        'catalog_visibility': 'visible',
        'description': maier_fd_desc,
        'short_description': maier_fd_short,
        'categories': [{'id': 216}],
        'images': [{'id': mid_maier_fd}] if mid_maier_fd else [],
        'manage_stock': False,
        'stock_status': 'outofstock',
        'attributes': [
            {'name': 'برند', 'visible': True, 'variation': False, 'options': ['مایر (Maier)']},
            {'name': 'مدل', 'visible': True, 'variation': False, 'options': ['MR-5959']},
            {'name': 'تعداد طبقات', 'visible': True, 'variation': False, 'options': ['۵ طبقه']},
            {'name': 'تنظیم دما', 'visible': True, 'variation': False, 'options': ['۳۵ تا ۷۰ درجه سانتی‌گراد']},
            {'name': 'تایمر', 'visible': True, 'variation': False, 'options': ['دیجیتال ۲۴ ساعته']},
            {'name': 'صفحه نمایش', 'visible': True, 'variation': False, 'options': ['دیجیتال LED']}
        ]
    }
    prod_maier_fd = create_wc_product(payload_maier_fd)
    if prod_maier_fd:
        ws.cell(101, 8).value = '✗ ناموجود'
        ws.cell(101, 15).value = prod_maier_fd['id']
        ws.cell(101, 16).value = f"https://hosseinykala.ir/product/{prod_maier_fd['slug']}/"
        ws.cell(101, 18).value = 'ثبت‌شده در سایت'
        wb.save(CATALOG_PATH)
        print("✓ Row 101 (میوه خشک کن مایر 5959) synced in sheet.")

    print("\n✓ Batch 3 (لوازم برقی و پخت و پز) completed and catalog saved!")

if __name__ == '__main__':
    run_batch_3_cooking()

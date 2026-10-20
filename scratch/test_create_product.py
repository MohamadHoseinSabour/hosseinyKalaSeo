import sys, requests
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
SESSION = requests.Session()
SESSION.mount('https://', TLSAdapter())

short_desc = """<ul>
<li><strong>توان مصرفی:</strong> موتور پرقدرت ۲۶۰۰ وات AC سالنی و حرفه‌ای با پرتاب باد فوق‌العاده</li>
<li><strong>فناوری تولید یون:</strong> سیستم آیونیک جهت مهار الکتریسیته ساکن و جلوگیری از وز شدن موها</li>
<li><strong>تنظیمات دما و سرعت:</strong> ۵ حالت ترکیبی مختلف پرتاب باد و حرارت به همراه دکمه باد سرد لحظه‌ای (Cool Shot)</li>
<li><strong>اقلام همراه:</strong> دارای سری متمرکزکننده باد و سری دیسپانسر حرفه‌ای برای حجم‌دهی به موهای فر</li>
<li><strong>گارانتی و اصالت:</strong> تضمین ۱۰۰٪ اصالت فیزیکی کالا در فروشگاه لوازم خانگی حسینی اهواز</li>
</ul>"""

desc = """<h2>بررسی تخصصی و راهنمای خرید سشوار حرفه‌ای زیکو مدل ZC-5020</h2>
<p>خشک کردن سریع و حالت‌دهی استاندارد به موها بدون آسیب رساندن به بافت و ساقه مو، نیازمند دستگاهی پرتوان با موتور استاندارد است. <strong>سشوار حرفه‌ای زیکو مدل ZC-5020</strong> از برند معتبر <strong>زیکو (Zico)</strong>، یکی از قدرتمندترین و مدرن‌ترین سشوارهای موجود در بازار است که با بهره‌گیری از موتور سنگین AC و توان ۲۶۰۰ وات، هم برای مصارف حرفه‌ای در سالن‌های آرایشی و هم برای استفاده شخصی پیشرفته در منزل گزینه‌ای تمام‌عیار محسوب می‌شود.</p>

<h3>ویژگی‌های برجسته سشوار حرفه‌ای زیکو 5020</h3>
<ul>
<li><strong>موتور سنگین AC با توان ۲۶۰۰ وات:</strong> موتورهای AC جریان متناوب برخلاف مدل‌های خانگی معمولی، طول عمر بسیار بالاتری دارند و می‌توانند بدون داغ شدن بیش از حد، برای مدت طولانی باد پرفشار و گرمای یکنواخت تولید کنند.</li>
<li><strong>فناوری پیشرفته تولید یون (Ionic):</strong> این قابلیت با شکستن مولکول‌های آب، سرعت خشک شدن مو را دو برابر کرده و با خنثی‌سازی بارهای مثبت، از وز شدن موها جلوگیری می‌کند و درخشندگی طبیعی به آن‌ها می‌بخشد.</li>
<li><strong>طراحی ارگونومیک و لوکس:</strong> بدنه مشکی براق با رینگ رزگلد در انتهای موتور، زیبایی چشم‌نوازی به دستگاه داده است. همچنین وزن متعادل و کلیدهای کنترل در محل دستگیره، خستگی دست را در استفاده طولانی به حداقل می‌رساند.</li>
<li><strong>سری دیسپانسر و متمرکزکننده باد:</strong> همراه با دستگاه دو سری اختصاصی ارائه می‌شود؛ سری متمرکزکننده برای صاف کردن و براشینگ دقیق، و سری دیسپانسر (دیفیوزر) برای تثبیت حالت موهای مجعد و فر.</li>
<li><strong>سیستم محافظ حرارتی Overheat:</strong> در صورت استفاده طولانی و افزایش غیرمجاز دما، دستگاه به صورت خودکار ایمنی المنت‌ها را کنترل می‌کند تا از آسیب به موتور جلوگیری شود.</li>
</ul>

<h2>جدول مشخصات فنی سشوار حرفه‌ای زیکو مدل ZC-5020</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">زیکو (Zico)</td></tr>
<tr><td style="padding: 8px;"><strong>مدل</strong></td><td style="padding: 8px;">ZC-5020</td></tr>
<tr><td style="padding: 8px;"><strong>کاربری</strong></td><td style="padding: 8px;">حرفه‌ای و سالنی / خانگی پیشرفته</td></tr>
<tr><td style="padding: 8px;"><strong>توان مصرفی</strong></td><td style="padding: 8px;">۲۶۰۰ وات</td></tr>
<tr><td style="padding: 8px;"><strong>نوع موتور</strong></td><td style="padding: 8px;">AC پرقدرت و بادوام (موتور سنگین)</td></tr>
<tr><td style="padding: 8px;"><strong>فناوری یونیزاسیون</strong></td><td style="padding: 8px;">دارد (ضد وز و درخشان‌کننده)</td></tr>
<tr><td style="padding: 8px;"><strong>دکمه باد سرد (Cool Shot)</strong></td><td style="padding: 8px;">دارد (تثبیت حالت مو)</td></tr>
<tr><td style="padding: 8px;"><strong>حالت‌های تنظیم</strong></td><td style="padding: 8px;">۵ حالت سرعت و حرارت</td></tr>
<tr><td style="padding: 8px;"><strong>اقلام همراه</strong></td><td style="padding: 8px;">سری متمرکزکننده باد + سری دیسپانسر (دیفیوزر)</td></tr>
<tr><td style="padding: 8px;"><strong>طول کابل برق</strong></td><td style="padding: 8px;">کابل حرفه‌ای با حلقه آویز استاندارد</td></tr>
<tr><td style="padding: 8px;"><strong>ضمانت و اصالت</strong></td><td style="padding: 8px;">ضمانت اصالت و سلامت فیزیکی از فروشگاه حسینی کالا</td></tr>
</tbody>
</table>

<p>شما می‌توانید این محصول باکیفیت را با اطمینان کامل از اصالت کالا از <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> تهیه نمایید و در صورت تمایل به خرید حضوری به شعب فروشگاه در <strong>اهواز</strong> مراجعه فرمایید.</p>"""

payload = {
    'name': 'سشوار حرفه ای زیکو مدل ZC-5020',
    'slug': 'ziko-zc5020-professional-hair-dryer',
    'type': 'simple',
    'status': 'publish',
    'catalog_visibility': 'visible',
    'description': desc,
    'short_description': short_desc,
    'categories': [{'id': 212}, {'id': 124}],
    'images': [{'id': 4234}],
    'manage_stock': False,
    'stock_status': 'outofstock',
    'attributes': [
        {'name': 'برند', 'visible': True, 'variation': False, 'options': ['زیکو (Zico)']},
        {'name': 'توان مصرفی', 'visible': True, 'variation': False, 'options': ['۲۶۰۰ وات']},
        {'name': 'نوع موتور', 'visible': True, 'variation': False, 'options': ['AC حرفه‌ای (موتور سنگین)']},
        {'name': 'فناوری تولید یون', 'visible': True, 'variation': False, 'options': ['دارد (Ionic)']},
        {'name': 'باد سرد لحظه‌ای', 'visible': True, 'variation': False, 'options': ['دارد (Cool Shot)']},
        {'name': 'اقلام همراه', 'visible': True, 'variation': False, 'options': ['سری متمرکز کننده باد، سری دیسپانسر (دیفیوزر)']}
    ]
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

url = 'https://hosseinykala.ir/wp-json/wc/v3/products'
r = SESSION.post(url, auth=AUTH, headers=headers, json=payload, timeout=30)
print("Create Product Status:", r.status_code)
if r.status_code == 201:
    res = r.json()
    print(f"Product created successfully! ID: {res['id']} | Name: {res['name']} | Slug: {res['slug']} | Stock: {res['stock_status']}")
else:
    print("Failed:", r.status_code, r.text[:300])
